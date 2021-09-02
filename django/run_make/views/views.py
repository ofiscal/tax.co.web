if True:
  from   datetime import datetime # for datetime.datetime.now
  from   django.http import HttpResponseRedirect
  from   django.shortcuts import render
  from   django.urls import reverse
  import os
  from   shutil import rmtree
  #
  import run_make.common as common
  from   run_make.forms import TaxConfigForm
  import run_make.views.lib as lib


# PITFALL: These start with '/'
# because Django treats as root every DocumentRoot folder
# configured in apache2.conf. Name collisions must be hell.
rate_tables = {
  "/config/marginal_rates/most.csv" :
    "El impuesto para la mayoría de las categorías de ingreso:",
  "/config/marginal_rates/dividend.csv" :
    "El impuesto para los dividendos:",
  "/config/marginal_rates/ocasional_high.csv" :
    "El impuesto más alto para los ingresos ocasionales:",
  "/config/marginal_rates/ocasional_low.csv" :
    "El impuesto más bajo para los ingresos ocasionales:",
  "/config/vat_by_coicop.csv" :
    "El IVA, asignado por código COICOP:",
  "/config/vat_by_capitulo_c.csv" :
    "El IVA, asignado por código 'capitulo c'. (La mayoría de las compras en la ENPH son identificados por el COICOP, pero algunos usan este sistema alternativo.)" }

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
      user_path = os . path . join ( common.tax_co_root,
                                     "users/",
                                     user_hash )

      rmtree( user_path, ignore_errors = True )
        # Remove the path; don't worry if it doesn't exist.
      for p in [                    user_path,
                 os . path . join ( user_path, "logs" ),
                 os . path . join ( user_path, "config" ),
                 os . path . join ( user_path, "config/marginal_rates" ) ]:
         if not os . path . exists ( p ):
             os . mkdir ( p )
      lib . write_form_to_user_folder ( user_path,
                                        advanced_specs_form )
      lib . write_uploaded_files_to_user_folder (
        table_rel_paths = list ( rate_tables . keys () ),
        user_path = user_path,
        request_files = request . FILES )
      lib . append_request_to_db ( user_hash )

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
