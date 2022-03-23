if True:
  import csv
  from   datetime import datetime
  from   django.core.files.storage import FileSystemStorage
  from   django.forms import ModelForm
  import hashlib
  import json
  import os
  from   shutil import rmtree
  import subprocess
  from   typing import List
  #
  from   run_make.common import tax_co_root
  from   run_make.forms import TaxConfigForm


# PITFALL: Some of the path arguments below are absolute.
# Those should not be hardcoded here;
# instead, one can use `tax_co_root`.)

global_requests_log = os.path.join ( tax_co_root,
                                     "requests-log.txt" )

def get_client_ip(request):
  """https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django/4581997#4581997"""
  x_forwarded_for = request.META.get ( 'HTTP_X_FORWARDED_FOR' )
  if x_forwarded_for:
      ip = x_forwarded_for.split (',') [0]
  else:
      ip = request.META.get ( 'REMOTE_ADDR' )
  return ip

def get_csv ( filename ):
  with open( filename,
             encoding = 'utf-8'
            ) as csvfile:
    rows = []
    for row in csv.reader ( csvfile,
                            delimiter = ',',
                            quotechar = '"' ):
      rows . append( row )
  return rows

vat_data_path = "config/vat"

def get_VAT_rate_groups () -> List[ float ]:
  return get_csv (
    os.path.join ( tax_co_root,
                   vat_data_path,
                   "rate_groups.csv" )
  ) [1:] # Drop column names.

def get_consumable_groups_by_coicop():
  return get_csv (
    os.path.join ( tax_co_root,
                   vat_data_path,
                   "grouped",
                   "consumable_groups_by_coicop.csv" )
  ) [1:] # Drop column names.

def get_consumable_groups_other():
  return get_csv (
    os.path.join ( tax_co_root,
                   vat_data_path,
                   "grouped",
                   "consumable_groups_other.csv" )
  ) [1:] # Drop column names.

def hash_from_str ( s : str ) -> str:
  return (
    "u" + # Because Python library paths must start with letters, not numbers.
    hashlib . md5 (
      s . encode () )
    . hexdigest () )

def create_user_folder_tree ( user_path : str ):
  rmtree ( user_path, ignore_errors = True )
    # Remove the path.
    # If it already doesn't exist, no problem.
  for p in [
      (                  user_path),
      os . path . join ( user_path, "logs" ),
      os . path . join ( user_path, "config" ),
      os . path . join ( user_path, "config/vat" ),
      os . path . join ( user_path, "config/marginal_rates" ) ]:
     if not os . path . exists ( p ):
         os . mkdir ( p )

def write_form_to_user_folder (
    user_path : str, # Absolute path to user folder.
    form : TaxConfigForm
    ): # No return value; entirely IO.
  with open ( os.path.join ( user_path,
                             'config/config.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )

def write_uploaded_files_to_user_folder (
    table_rel_paths : List [ str ],
      # Relative to the user's config/ folder, or,
      # for defaults, to the project root's config/ folder.
    user_path : str, # Absolute path to user folder.
    request_files # Django docs are vague, calling this only a
                  # "dictionary-like object" from names
                  # (probably strings) to `UploadedFile`s.
    ): # No return value; entirely IO.

  fs = FileSystemStorage ()
  for trp in table_rel_paths:
    trp_stripped = trp . strip ("/")
      # Remove leading slashes. Otherwise,
      # path.join discards any args preceding this one.
    tapu = os . path . join ( # "Table Absolute Paths in User folder"
        user_path,
        trp_stripped )
    if os . path . exists ( tapu ):
      os . remove ( tapu ) # PITFALL: Overwrites user's preexisting data.
    if trp in request_files:
      fs . save (
        tapu,
        request_files [ trp ] )
    else:
      os . symlink (
        os . path . join ( tax_co_root ,
                           trp_stripped ),
        tapu )

def append_request_to_db ( user_hash : str ):
    user_root_path = os.path.join (
      tax_co_root, "users/", user_hash )
    user_logs_path = os.path.join (
      user_root_path, "logs" )
    os . chdir ( tax_co_root )

    with open( global_requests_log, "a" ) as f:
        f.write( "\ndjango: trying to append request\n" )

    if True: # Refine the environment.
        my_env = os . environ . copy ()
        env_additions = ":" . join (
            [ tax_co_root,
              "/opt/conda/lib/python3.9/site-packages" ] )
              # TODO ? Why must this second folder be specified?
              # It's the default when I run python3 from the shell.
        my_env["PYTHONPATH"] = (
            ":" . join ( [ env_additions,
                           my_env [ "PYTHONPATH" ] ] )
            if "PYTHONPATH" in my_env . keys ()
            else env_additions )
    sp = subprocess . run (
        [ "/opt/conda/bin/python3.9", # TODO : Why do I have to specify this?
                                      # It's the default python in the shell.
          "python/requests/main.py", # Run this program.
          os . path . join (         # Use this config file.
                "users/", user_hash, "config/config.json" ),
          "add-to-temp-queue" ],     # Take this action.
        cwd    = tax_co_root,
        env    = my_env,
        stdout = subprocess . PIPE,
        stderr = subprocess . PIPE )
    for ( path, source ) in [ ("django.stdout.txt", sp.stdout),
                              ("django.stderr.txt", sp.stderr) ]:
      with open ( os.path.join ( user_logs_path, path ),
                  "a" ) as f:
        f . write ( str ( datetime.now () ) + "\n" )
        f . write ( source . decode () )

def rate_ceiling_pairs_to_rate_floor_pairs (
    pairs : List[ List[ float ] ]
    ) ->    List[ List[ float ] ]:
  """
  Leaves the rates (first) column unchanged.
  Moves each ceiling down a cell,
  which means the last ceiling (which should be infinity) is lost,
  and sets the first ceiling to 0.
  """
  ceiling = 1 # Just an index, for the second elt of each pair.
  ln = len ( pairs )
  for i in range( 0, ln-1 ):
    pairs  [ ln-i-1 ] [ ceiling ] = (
      pairs[ ln-i-2 ] [ ceiling ]  )
  pairs    [ 0 ]      [ ceiling ]  = 0
  return pairs

def read_rate_floor_table (
    csvFilePath : str
    ) -> List: # Sadly, this list cannot be typed further,
               # as it is not homogenous,
               # because it is pretending to be a tuple,
               # which Javascript does not support.
  #
  # Fetch some portion of each row.
  with open( csvFilePath ) as csvFile:
    reader = csv . DictReader ( csvFile )
    pairs = []
    for row in reader:
      pairs . append ( [ row [ "rate" ],
                         row [ "ceiling" ] ] )
  csvFileName = ( os.path.split ( csvFilePath ) [1]
                   . replace( ".csv", "" ) )
  return [ csvFileName,
           rate_ceiling_pairs_to_rate_floor_pairs ( pairs ) ]

def fetch_marginal_rate_floor_taxes ( paths_to_rate_tables ):
  """
  INPUT: A list of (path, Spanish description) pairs.
  #
  OUTPUT: a list of lists in which:
    the first element is an income tax name,
    the second element is a list of 2-element lists,
      the first element of which is a rate and the second an income floor
      at which the rate begins to apply,
    and the third element is a label in Spanish of the tax.
  #
  PITFALL: This (tax.co.web) uses floors, not ceilings as in tax.co,
  because floors are easier to represent in the UI:
  they don't require the user to understand the concept of infinity,
  let alone floating-point approximations to it.
  """
  rates = []
  for p in paths_to_rate_tables:
    (path, description) = (p[0], p[1])
    rates . append (
      read_rate_floor_table ( path ) + [ description ]
    )
  return rates
