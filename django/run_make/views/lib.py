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

