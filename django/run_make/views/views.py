from   datetime import datetime # for datetime.datetime.now
import os
import subprocess

from   django.core.files.storage import FileSystemStorage
from   django.http import HttpResponseRedirect
from   django.shortcuts import render
from   django.urls import reverse

from   run_make.forms import TaxConfigForm
import run_make.views.lib as lib


def ingest_full_spec ( request ):
  """ For comments and simpler illustrations, see the functions
      ingest_json() and upload_multiple() in examples.py.
  """

  # PITFALL: Django treats as root every DocumentRoot folder
  # configured in apache2.conf. Name collisions must be hell.
  tables = { "vat_by_coicop"     : "/vat-by-coicop.csv",
             "vat_by_capitulo_c" : "/vat-by-capitulo-c.csv" }

  if request . method == 'POST':
    form = TaxConfigForm ( request . POST )
    if form . is_valid ():

      lib.write_form_to_maybe_new_user_folder (
          '/mnt/tax/users/',
          form )

      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "user_email" : form . cleaned_data [ "user_email" ]
                   } ) )

  else:
      form = TaxConfigForm ()
      return render ( request,
                      'run_make/ingest_full_spec.html',
                      { 'form' :  form,
                        "tables" : tables
                      } )
