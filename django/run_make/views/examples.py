from   datetime import datetime # for datetime.datetime.now
import hashlib
import json
import os
import subprocess

from   django.core.files.storage import FileSystemStorage
from   django.http import HttpResponseRedirect
from   django.shortcuts import render
from   django.urls import reverse

from   run_make.forms import TaxConfigForm
import run_make.views.lib as lib


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

def ingest_json ( request ):
  """ PITFALL: Strange, slightly-recursive call structure.
  The user first visits this URL with a GET.
  They see a blank form, corresponding to the second ("else") branch below.
  Once they fill out and submit the form, it is sent via POST
  to this same function, and goes through the first ("if") branch.
  """

  if request . method == 'POST':
    form = TaxConfigForm ( request . POST )
    if form . is_valid ():

      lib.write_form_to_maybe_new_user_folder (
          '/mnt/tax/users/',
          form )

      os . chdir ( "/mnt/web/run_make/fake_make" )
      subprocess . run ( [ "make", "output.json" ] )

      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "user_email" : form . cleaned_data [ "user_email" ]
                   } ) )

  else:
      form = TaxConfigForm ()
      return render ( request,
                      'run_make/ingest_json.html',
                      { 'form' :  form } )

def thank_for_spec ( request, user_email ):
  return render ( request,
                  'run_make/thank_for_spec.html',
                  { 'user_email' :  user_email } )

def download ( request ):
  return render ( request,
                  'run_make/download.html' )


#################
#### Uploads ####
#################

# Based on this tutorial:
#   https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
#   https://github.com/sibtc/simple-file-upload
#     cloned at aws/upload-tutorial

def upload_multiple ( request ):
    # Demonstrates that the return value of "filename" is redundant;
    # only the IO performed before its assignment matters.
    if request.method == 'POST':
      fs = FileSystemStorage()
      for fn in ["myfile","myfile2"]:
        if request . FILES [ fn ]:
          myfile = request.FILES[fn]
          filename = fs.save(
              fn, # Use myfile.name to save under the user-provided name.
              myfile )
          uploaded_file_url = fs.url(filename)
      return render(
          request,
          'run_make/upload_multiple.html',
          { 'evidence_of_upload' : True } )
    return render(request, 'run_make/upload_multiple.html')

def upload_and_show_url ( request ):
    # Just for learning.
    # Shows how to include a link to the uplaoded file.
    # I could swear that used to work, but now it doesn't.
    # TODO move to studies/, along with the template.
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(
            request,
            'run_make/upload_and_show_url.html',
            { 'uploaded_file_url' : uploaded_file_url } )
    return render(request, 'run_make/upload_and_show_url.html')

def upload_multiple_with_logging ( request ):
    # Demonstrates that the return value of "filename" is redundant;
    # only the IO performed before its assignment matters.
    # TODO move to studies/, along with a copy of the template.
    if request.method == 'POST':
      log = open ( "/mnt/web/logs/upload-var-names.txt", "a" )
      fs = FileSystemStorage()
      for fn in ["myfile","myfile2"]:
        if request . FILES [ fn ]:
          log . write("fn = " + fn + "\n")
          myfile = request.FILES[fn]
          filename = fs.save(
              fn, # Use myfile.name to save under the user-provided name.
              myfile )
          log . write("filename = " + filename + "\n")
          log . write("str(filename) = " + str(filename) + "\n")
          uploaded_file_url = fs.url(filename)
      log . close ()
      return render(
          request,
          'run_make/upload_multiple.html',
          { 'evidence_of_upload' : True } )
    return render(request, 'run_make/upload_multiple.html')
