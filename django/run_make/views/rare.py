# These views (or at least this view -- so far there's only one here)
# are rarely used. I'm separating it from views.ply because I spent two days
# chasing a bug that arose because I was confusing this view with another
# similar-looking one that's still in views.py.
#
# TODO ? More elegant would be to factor out whatever common code they have.
# But even if I did that as well as possible,
# they still might look pretty similar.

if True:
  from   datetime import datetime # for datetime.datetime.now
  from   django.http import HttpResponseRedirect
  from   django.shortcuts import render
  from   django.urls import reverse
  import json
  import os
  import pickle
  #
  from   run_make.common import tax_co_root
  from   run_make.forms  import TaxConfigForm
  import run_make.views.lib                as lib
  import run_make.views.views              as views
  import run_make.views.write_data_from_ui as write_ui


def ingest_spec_as_tables ( request ):
  """
  SEE ALSO:
  To understand this it might be helpful to look at
  `upload_multiple` in `run_make.views.examples` too.

  PITFALL: Strange, slightly-recursive call structure.
  The user first visits this URL with a GET.
  They see a blank form, corresponding to the second ("else") branch below.
  Once they fill out and submit the form, it is sent via POST
  to this same function, and goes through the first ("if") branch.
  """

  if request . method == "POST":
    advanced_specs_form = TaxConfigForm ( request . POST )

    if advanced_specs_form . is_valid ():

      user_email = ( advanced_specs_form
                     . cleaned_data [ "user_email" ] )
      user_hash = lib . hash_from_str ( user_email )
      user_path = os . path . join ( tax_co_root,
                                     "users/",
                                     user_hash )

      lib . create_user_folder_tree ( user_path )
      lib . write_form_to_user_folder ( user_path,
                                        advanced_specs_form )
      lib . write_uploaded_files_to_user_folder (
        table_rel_paths = list ( views.rate_tables . keys () ),
        user_path = user_path,
        request_files = request . FILES )
      lib . append_request_to_db ( user_hash )

      return HttpResponseRedirect (
        reverse (
          "run_make:thank-for-spec",
          kwargs = { "user_email" : user_email } ) )

  else: return render (
      request,
      "run_make/ingest_spec_as_tables.html",
      { "advanced_specs_form" : TaxConfigForm (),
        "rate_tables"         : views.rate_tables
       } )
