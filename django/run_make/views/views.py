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
  """ For commentary and simpler illustrations, see the functions
      ingest_json() and upload_multiple() in examples.py.
  """

  # PITFALL: Django treats as root every DocumentRoot folder
  # configured in apache2.conf. Name collisions must be hell.
  vat_tables = {
      "El IVA asignado por código COICOP:" : "/vat-by-coicop.csv",
      "El IVA asignado por código 'capitulo c'. (La mayoría de las compras en la ENPH son identificados por el COICOP, pero algunos usan este sistema alternativo.)" : "/vat-by-capitulo-c.csv" }

  marginal_rate_tables = {
      "El impuesto para la mayoría de las categorías de ingreso:" : "/marginal_rates/most.csv",
      "El impuesto para los dividendos:" : "/marginal_rates/dividend.csv",
      "El impuesto más alto para los ingresos ocasionales:" : "/marginal_rates/ocasional_high.csv",
      "El impuesto más bajo para los ingresos ocasionales:" : "/marginal_rates/ocasional_low.csv" }

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
                        "vat_tables" : vat_tables,
                        "marginal_rate_tables" : marginal_rate_tables
                      } )
