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
  from   run_make.forms import TaxConfigForm
  import run_make.views.lib as lib
  import run_make.views.write_data_from_ui as write_ui


###
### Paths
###

# PITFALL: These start with '/'
# because Django treats as root every DocumentRoot folder
# configured in apache2.conf. Name collisions must be hell.

marginal_rate_tables = {
  "/config/marginal_rates/most.csv" :
    "la mayoría de los ingresos",
  "/config/marginal_rates/dividend.csv" :
    "dividendos",
  "/config/marginal_rates/ocasional_high.csv" :
    "tasa alta de ingresos ocasionales",
  "/config/marginal_rates/ocasional_low.csv" :
    "tasa baja de ingresos ocasionales",
}

vat_tables = {
  "/config/vat/vat_by_coicop.csv" :
    "El IVA, asignado por código COICOP:",
  "/config/vat/vat_by_capitulo_c.csv" :
    "El IVA, asignado por código 'capitulo c'. (La mayoría de las compras en la ENPH son identificados por el COICOP, pero algunos usan este sistema alternativo.)" }

# A union of two dicts.
rate_tables = { **marginal_rate_tables,
                **vat_tables }

def manual_ingest ( request ):
  """
  A view that lets a user manually enter marginal rates in a GUI,
  as well as non-tax details like their email address,
  and submit a request to the microsimulation.

  If `pickle_debug` below is set to True,
  then this can be tested from Bash,
  by pasting the following after visiting the page:

cd /mnt/django
python3 manage.py shell

import pickle
filename = "/home/jeff/manual_ingest.pickle"
with open(filename,"rb") as file_object:
  req = pickle.loads( file_object . read () )

  """
  if request . method == "POST": # once user submits form
    advanced_specs_form = TaxConfigForm ( request . POST )

    pickle_debug = False
    if pickle_debug:
      filename = "manual_ingest.pickle"
      d = dict ( request.POST )
      d.pop( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
      with open ( filename,"wb" ) as f:
        f.write ( pickle.dumps ( d ) )

    if advanced_specs_form . is_valid ():
      # Compute / get user data.
      user_email = ( advanced_specs_form
                     . cleaned_data [ "user_email" ] )
      user_hash = lib . hash_from_str ( user_email )
      user_path = os . path . join ( tax_co_root,
                                     "users/",
                                     user_hash )
      (non_tax, income_tax, vat) = (
        write_ui . divide_post_object_into_dicts (
          request . POST ) )

      if pickle_debug:
        for (name,obj) in [ ( "non_tax", non_tax ),
                            ( "income_tax", income_tax ),
                            ( "vat", vat ) ]:
          with open ( name + ".pickle", "wb" ) as f:
            f.write ( pickle.dumps ( obj ) )

      # Write user data.
      lib . create_user_folder_tree ( user_path )
      if True: # non-tax data
        for k in non_tax.keys():
          non_tax[k] = non_tax[k][0] # Unwrap lists.
        non_tax [ "strategy" ]    = "detail"
        non_tax [ "regime_year" ] = 2019
        non_tax [ "subsample" ]   = int ( non_tax [ "subsample" ] )
        with open ( os.path.join ( user_path,
                                   "config/config.json" ),
                    "w" ) as f:
          json.dump ( non_tax, f )
      write_ui . write_marginal_rates_to_user_folder (
        user_path,
        write_ui . flat_marginal_rates_dict_to_csv_writeable_lists (
          income_tax ) )
      write_ui . write_vat_rates_to_user_folder (
        user_path,
        write_ui . flat_vat_dict_to_consumables_list ( vat ) )
      lib . append_request_to_db ( user_hash )

    return HttpResponseRedirect (
      reverse (
        "run_make:thank-for-spec",
        kwargs = {
          "user_email" : user_email } ) )

  else: # Before user submits form
    marginal_rate_floor_taxes = (
      lib . fetch_marginal_rate_floor_taxes (
        [ ( tax_co_root + abs_path,
           marginal_rate_tables [ abs_path ] )
          for abs_path
          in marginal_rate_tables . keys () ] ) )

    return render (
      request,
      "run_make/manual_tax_tables.html",
      { "advanced_specs_form" : TaxConfigForm (),
        "income_taxes" : marginal_rate_floor_taxes,
          # PITFALL: Django cannot pass dictionaries to Javascript.
          # PITFALL: Javascript does not offer tuples, only lists.
          # That's why `marginal_rate_tables` is an inhomogeneous list.
          # (Django can handle those things in the HTML,
          # to at least some extent, within constructs like
          # {% for ... %} ... {% endfor %},
          # but sticking to lists seems safer.)
        "vat_rate_groups"             : lib . get_VAT_rate_groups (),
        "consumable_groups_by_coicop" : lib . get_consumable_groups_by_coicop (),
        "consumable_groups_other"     : lib . get_consumable_groups_other (),
        "explainiers"                 : lib . get_csv (
          "/mnt/tax_co/config/vat/grouped/dicc_non_coicop.csv" ),
       } )

def thank_for_spec ( request, user_email ):
  return render ( request,
                  "run_make/thank_for_spec.html",
                  { "user_email" :  user_email } )
