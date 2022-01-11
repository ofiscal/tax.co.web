from   datetime import datetime # for datetime.datetime.now
import os
import sys
import pickle
import subprocess

from   django.core.files.storage import FileSystemStorage
from   django.http import HttpResponseRedirect
from   django.shortcuts import render
from   django.urls import reverse

from   run_make.forms import TaxConfigForm
import run_make.views.lib as lib


def render_content_argument ( request ):
  """ This demonstrates how to pass in (at least somewhat) arbitrary data from Django to Javascript. Happily, non-strings are not converted to strings."""
  return render (
    request,
    'run_make/render_content_argument.html',
    { "the_string" : "A string.",
      "the_number" : 33,
      "the_list"   : [1,2],
      "the_dict"   : {"a":"b"} # PITFALL: Dictionaries cannot be transferred.
     } )

def write_time ( request ):
  """Demonstrates how visiting a URL can be made to (create and) write to a file."""
  now = datetime . now () . timestamp()
  with open( "/home/jeff/" + str ( now ),
             'w' ) as f:
    f . write( "Writing time (for run_make/write_time.html)\n" )
  return render (
    request,
    'run_make/write_time.html',
    { "wd"      : os . getcwd (),
      "version" : str ( sys.version ),
      "now"     : now } )

def download ( request ):
  return render ( request,
                  'run_make/download.html' )


########################
#### Radio buttons #####
########################

def radio_table ( request ):
  """
  The template draws a table,
  with mutually exclusive radio buttons in each row.
  This view, when it receives a POST,
  converts the data to an ordinary dictionary,
  pickles that, and writes it to a file,
  so that I can see from a REPL what the table output looks like.

  # Test this from Bash by pasting the following after visiting the page:

cd /mnt/django
python3 manage.py shell

import pickle
filename = '/home/jeff/radio_table.pickle'
with open(filename,'rb') as file_object:
  req = pickle.loads( file_object . read () )

req
  """

  if request . method == 'POST':
    filename = 'radio_table.pickle'
    d = dict ( request.POST )
    d.pop( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
    with open ( filename,'wb' ) as f:
      f.write (
        pickle.dumps ( d ) )
    return HttpResponseRedirect (
      reverse (
        'run_make:thank-for-spec',
        kwargs = { "user_email" : "whoever@wherever.net" } ) )
  else: return render (
      request,
      'run_make/radio_table.html' )

def radio_table_transposed ( request ):
  """
  The template draws a table,
  with mutually exclusive radio buttons in each *column*,
  except for the first column, which lets the user select a VAT rate.

  This view, when it receives a POST,
  converts the data to an ordinary dictionary,
  pickles that, and writes it to a file,
  so that I can see from a REPL what the table output looks like.

  # Test this from Bash by pasting the following after visiting the page:

cd /mnt/django
python3 manage.py shell

import pickle
filename = '/home/jeff/radio_table_transposed.pickle'
with open(filename,'rb') as file_object:
  req = pickle.loads( file_object . read () )

req
  """

  if request . method == 'POST':
    filename = 'radio_table_transposed.pickle'
    d = dict ( request.POST )
    d.pop( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
    with open ( filename,'wb' ) as f:
      f.write (
        pickle.dumps ( d ) )
    return HttpResponseRedirect (
      reverse (
        'run_make:thank-for-spec',
        kwargs = { "user_email" : "whoever@wherever.net" } ) )
  else: return render (
      request,
      'run_make/radio_table_transposed.html' )

def radio_table_generated ( request ):
  """
  This is like radio_table(),
  but uses Javascript to automate some tasks,
  so that they can be fed parameters from Django or user input.

  The template draws a table,
  with mutually exclusive radio buttons in each row,
  using Javascript to "reduce" the amount of work involved.

  This view, when it receives a POST,
  converts the data to an ordinary dictionary,
  pickles that, and writes it to a file,
  so that I can see from a REPL what the table output looks like.

  # Test this from Bash by pasting the following after visiting the page:

cd /mnt/django
python3 manage.py shell

import pickle
filename = '/home/jeff/radio_table_generated.pickle'
with open(filename,'rb') as file_object:
  req = pickle.loads( file_object . read () )

req
  """

  if request . method == 'POST':
    filename = 'radio_table_generated.pickle'
    d = dict ( request.POST )
    d.pop( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
    with open ( filename,'wb' ) as f:
      f.write (
        pickle.dumps ( d ) )
    return HttpResponseRedirect (
      reverse (
        'run_make:thank-for-spec',
        kwargs = { "user_email" : "whoever@wherever.net" } ) )
  else: return render (
      request,
      'run_make/radio_table_generated.html' )


######################
#### Dynamic form ####
######################

def dynamic_form ( request ):
  """
  This draws a dynamic (the user can add and delete rows)
  table of numeric input boxes.
  It then converts the POST data to an ordinary dictionary,
  pickles that, and writes it to a file,
  so that I can see from a REPL what the table output looks like.

  Test it from Bash by pasting the following after visiting the page:
cd /mnt/django
python3 manage.py shell
import pickle
filename = '/home/jeff/dynamic_table.pickle'
with open(filename,'rb') as file_object:
  req = pickle.loads( file_object . read () )

req
  """
  if request . method == 'POST':
    filename = 'dynamic_table.pickle'
    d = dict ( request.POST )
    d.pop( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
    with open ( filename,'wb' ) as f:
      f.write (
        pickle.dumps ( d ) )
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
