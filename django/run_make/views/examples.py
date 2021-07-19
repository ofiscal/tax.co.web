from   datetime import datetime # for datetime.datetime.now
import os
import subprocess

from   django.core.files.storage import FileSystemStorage
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

def download ( request ):
  return render ( request,
                  'run_make/download.html' )

######################
#### Dynamic form ####
######################

def dynamic_form ( request ):
  if request . method == 'POST':
    advanced_specs_form = TaxConfigForm ( request . POST )
    if advanced_specs_form . is_valid ():
      user_email = advanced_specs_form . cleaned_data [ "user_email" ]
      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "user_email" : "dynamic-form-user@nowhere.net" } ) )
  else: return render (
      request,
      'run_make/dynamic_form.html' )

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
    table_names = [ "myfile", "myfile2" ]
    if request.method == 'POST':
      fs = FileSystemStorage ()
      for fn in table_names:
        if request . FILES [ fn ]:
          myfile = request.FILES[fn]
          filename = fs.save(
              fn, # Use myfile.name to save under the user-provided name.
              myfile )
          uploaded_file_url = fs.url(filename)
      return render(
          request,
          'run_make/upload_multiple.html',
          { "table_names" : table_names,
            'evidence_of_upload' : True } )
    return render(
        request,
        'run_make/upload_multiple.html',
        { 'table_names' : table_names } )

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
    table_names = [ "myfile", "myfile2" ]
    if request.method == 'POST':
      log = open ( "/mnt/django/logs/upload-var-names.txt", "a" )
      fs = FileSystemStorage()
      for fn in table_names:
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
          { 'evidence_of_upload' : True,
            "table_names" : table_names } )

    return render(
        request,
        'run_make/upload_multiple.html',
        { "table_names" : table_names } )
