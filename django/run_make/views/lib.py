from   django.core.files.storage import FileSystemStorage
from   django.forms import ModelForm
import hashlib
import json
import os
from   typing import List


def hash_from_str ( s : str ) -> str:
  return (
      hashlib . md5 (
        s . encode () )
      . hexdigest () )

def write_form_to_user_folder (
    user_path : str,
    form : ModelForm
    ): # No return value; entirely IO.
  with open ( os.path.join ( user_path, 'shell.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )

def write_uploaded_files_to_user_folder (
    table_rel_paths : List [ str ], # Will be relative to the user folder.
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
    if trp in request_files: fs . save (
      os . path . join ( user_path, trp_stripped ),
      request_files [ trp ] )
    else: os . symlink (
      os . path . join ( default_tables_path , trp_stripped ),
      os . path . join ( user_path           , trp_stripped ) )
