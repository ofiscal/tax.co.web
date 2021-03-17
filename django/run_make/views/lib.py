from   django.core.files.storage import FileSystemStorage
from   django.forms import ModelForm
import hashlib
import json
import os
import subprocess
from   typing import List


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
  with open ( os.path.join ( user_path, 'config/shell.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )

def write_uploaded_files_to_user_folder (
    table_rel_paths : List [ str ],
      # Relative to the user's config/ folder,
      # or to the project root config/ folder for defaults.
    user_path : str,
    default_tables_path : str, # If the user does not supply a table,
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
    tapu = os . path . join ( # Table absolute path in user folder.
        user_path,
        "config",
        trp_stripped )
    if os . path . exists ( tapu ):
      os . remove ( tapu )
    if trp in request_files:
      fs . save (
        tapu,
        request_files [ trp ] )
    else:
      os . symlink (
        os . path . join ( default_tables_path , trp_stripped ),
        tapu )

def append_request_to_db ( user_hash : str ):
    os . chdir ( "/mnt/tax_co" )
    os . system (
        " " . join ( [
            "PYTHONPATH=\".\"",
            "python3 ",
            "python/requests/main.py", # the program
            os . path . join (
                "users/", user_hash, "config/shell.json" ), # the config file
            "add" ] ) )        # the action to take
