from django.core.files.storage import FileSystemStorage
import json
import os
import subprocess
from datetime import datetime # for datetime.datetime.now

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TaxConfigForm


def write_time ( request ):
  """Demonstrates how visiting a URL can be made to (create and) write to a file."""
  wd = os . getcwd ()
  now = datetime . now () . timestamp()
  with open( "/home/appuser/" + str ( now ),
             'w' ) as f:
    f . write( "Hello?\n" )
  return render (
    request,
    'run_make/write_time.html',
    { "wd" : wd,
      "now" : now } )

def ingest_spec ( request ):
  """ PITFALL: Strange, slightly-recursive call structure.
  The user first visits this URL with a GET.
  They see a blank form, corresponding to the second ("else") branch below.
  Once they fill out and submit the form, it is sent via POST
  to this same function, and goes through the first ("if") branch.
  """

  if request . method == 'POST':
    form = TaxConfigForm ( request . POST )
    if form . is_valid ():
      os . chdir ( "/mnt/web/run_make/fake_make" )
      with open ( 'input.json', 'w' ) as f:
        json . dump ( form . cleaned_data,
                      f )
      subprocess . run ( [ "make", "output.json" ] )
      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "email" : form . cleaned_data [ "email" ]
                   } ) )

  else:
      form = TaxConfigForm ()
      return render ( request,
                      'run_make/ingest_spec.html',
                      { 'form' :  form } )

def thank_for_spec ( request, email ):
  return render ( request,
                  'run_make/thank_for_spec.html',
                  { 'email' :  email } )

def download ( request ):
  return render ( request,
                  'run_make/download.html' )

def upload ( request ):
    # From this tutorial:
    #   https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
    #   https://github.com/sibtc/simple-file-upload
    #     cloned at aws/upload-tutorial
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(
            request,
            'run_make/upload.html',
            { 'uploaded_file_url' : uploaded_file_url } )
    return render(request, 'run_make/upload.html')
