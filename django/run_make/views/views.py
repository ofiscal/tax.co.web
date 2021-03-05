from   datetime import datetime # for datetime.datetime.now
from   django.http import HttpResponseRedirect
from   django.shortcuts import render
from   django.urls import reverse
import os
import subprocess

from   run_make.forms import TaxConfigForm
import run_make.views.lib as lib


# PITFALL: These paths are simpler than one would expect because
# Django treats as root every DocumentRoot folder
# configured in apache2.conf. Name collisions must be hell.
rate_tables = {
      "/marginal_rates/most.csv" : "El impuesto para la mayoría de las categorías de ingreso:",
      "/marginal_rates/dividend.csv" : "El impuesto para los dividendos:",
      "/marginal_rates/ocasional_high.csv" : "El impuesto más alto para los ingresos ocasionales:",
      "/marginal_rates/ocasional_low.csv" : "El impuesto más bajo para los ingresos ocasionales:",
      "/vat-by-coicop.csv" : "El IVA, asignado por código COICOP:",
      "/vat-by-capitulo-c.csv" : "El IVA, asignado por código 'capitulo c'. (La mayoría de las compras en la ENPH son identificados por el COICOP, pero algunos usan este sistema alternativo.)" }

def ingest_full_spec ( request ):
  """
  SEE ALSO:
  To understand this it might be helpful to look at `upload_multiple` in `run_make.views.examples` too.

  PITFALL: Strange, slightly-recursive call structure.
  The user first visits this URL with a GET.
  They see a blank form, corresponding to the second ("else") branch below.
  Once they fill out and submit the form, it is sent via POST
  to this same function, and goes through the first ("if") branch.
  """

  if request . method == 'POST':
    advanced_specs_form = TaxConfigForm ( request . POST )

    if advanced_specs_form . is_valid ():

      user_email = advanced_specs_form . cleaned_data [ "user_email" ]
      user_hash = lib . hash_from_str ( user_email )
      user_path = os . path . join ( '/mnt/tax_co/users/',
                                     user_hash )

      if not os . path . exists ( user_path ):
        os . mkdir (                    user_path )
        os . mkdir ( os . path . join ( user_path, "marginal_rates" ) )
      lib . write_form_to_user_folder ( user_path,
                                        advanced_specs_form )
      lib . write_uploaded_files_to_user_folder (
        table_rel_paths = list ( rate_tables . keys () ),
        user_path = user_path,
        default_tables_path = "/mnt/tax_co/to-serve",
        request_files = request . FILES )

      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "user_email" : user_email } ) )

  else: return render (
      request,
      'run_make/ingest_full_spec.html',
      { 'advanced_specs_form' : TaxConfigForm (),
        "rate_tables"         : rate_tables
       } )

def thank_for_spec ( request, user_email ):
  return render ( request,
                  'run_make/thank_for_spec.html',
                  { 'user_email' :  user_email } )
