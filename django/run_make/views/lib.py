from   datetime import datetime # for datetime.datetime.now
import hashlib
import json
import os
import subprocess

from   django.core.files.storage import FileSystemStorage
from   django.http import HttpResponseRedirect
from   django.shortcuts import render
from   django.urls import reverse
from   django.forms import ModelForm

from   run_make.forms import TaxConfigForm


def write_form_to_maybe_new_user_folder (
    users_folder : str, # a path
    form : ModelForm ):
  """ Completely IO; returns nothing. """
  hp = os.path.join (
       users_folder,
       ( hashlib . md5 (
           form . cleaned_data ["user_email"] . encode () )
         . hexdigest () ) )
  if not os.path.exists ( hp ):
      os.mkdir ( hp )
  with open ( os.path.join ( hp, 'shell.json' ),
              'w' ) as f:
    json . dump ( form . cleaned_data,
                  f )
