if True:
  from   datetime import datetime
  from   django.core.files.storage import FileSystemStorage
  from   django.forms import ModelForm
  import hashlib
  import json
  import os
  import subprocess
  from   typing import List


log_path = "/mnt/tax_co/users/view_log.txt"

def hash_from_str ( s : str ) -> str:
  return (
    "u" + # Because Python library paths must start with letters, not numbers.
    hashlib . md5 (
      s . encode () )
    . hexdigest () )

def write_form_to_user_folder (
    user_path : str,
    form : ModelForm
    ): # No return value; entirely IO.
  with open ( os.path.join ( user_path, 'config/config.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )

def write_uploaded_files_to_user_folder (
    table_rel_paths : List [ str ],
      # Relative to the user's config/ folder,
      # or to the project root config/ folder for defaults.
    user_path : str,
    tax_co_root : str, # If the user does not supply a table,
                               # a default one can be found here.
    request_files # The Django docs are vague about what this is,
                  # calling it only a "dictionary-like object"
                  # from names (probably strings) to `UploadedFile`s.
    ): # No return value; entirely IO.

  fs = FileSystemStorage ()
  for trp in table_rel_paths:
    trp_stripped = trp . strip ("/")
      # Remove leading slashes. Otherwise,
      # path.join discards any args preceding this one.
    tapu = os . path . join ( # Table Absolute Path in User folder.
        user_path,
        trp_stripped )
    if os . path . exists ( tapu ):
      os . remove ( tapu )
    if trp in request_files:
      fs . save (
        tapu,
        request_files [ trp ] )
    else:
      os . symlink (
        os . path . join ( tax_co_root , trp_stripped ),
        tapu )

def append_request_to_db ( user_hash : str ):
    tax_co_root_path = "/mnt/tax_co"
    user_root_path = os.path.join ( tax_co_root_path, "users/", user_hash )
    os . chdir ( tax_co_root_path )

    with open( log_path, "a" ) as f:
        f.write( "trying to append request\n" )

    if True: # Refine the environment.
        my_env = os . environ . copy ()
        env_additions = ":" . join (
            [ tax_co_root_path,
              "/opt/conda/lib/python3.8/site-packages" ] )
              # TODO ? Why must this second folder be specified?
              # It's the default when I run python3 from the shell.
        my_env["PYTHONPATH"] = (
            ":" . join ( [ env_additions,
                           my_env [ "PYTHONPATH" ] ] )
            if "PYTHONPATH" in my_env . keys ()
            else env_additions )
    sp = subprocess . run (
        [ "/opt/conda/bin/python3.8", # TODO : Why do I have to specify kthis?
                                      # It's the default python in the shell.
          "/mnt/tax_co/python/requests/main.py", # run this program
          os . path . join (                     # use this config file
                "users/", user_hash, "config/config.json" ),
          "add-to-temp-queue" ],                 # take this action
        env    = my_env,
        stdout = subprocess . PIPE,
        stderr = subprocess . PIPE )
    for ( path, source ) in [ ("view.stdout.txt", sp.stdout),
                              ("view.stderr.txt", sp.stderr) ]:
      with open ( os.path.join ( user_root_path, path ),
                  "a" ) as f:
        f . write ( str ( datetime.now () ) + "\n" )
        f . write ( source . decode () )
