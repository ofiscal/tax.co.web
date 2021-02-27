import hashlib
import json
import os

from   django.forms import ModelForm


def hash_from_str ( s : str ) -> str:
  return (
      hashlib . md5 (
        s . encode () )
      . hexdigest () )

def write_form_to_maybe_new_user_folder (
    users_folder : str, # a path
    form : ModelForm ):
  """ Completely IO; returns nothing. """
  hp = os.path.join (
       users_folder,
       hash_from_str (
           form . cleaned_data ["user_email"] ) )
  if not os.path.exists ( hp ):
      os.mkdir ( hp )
  with open ( os.path.join ( hp, 'shell.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )
