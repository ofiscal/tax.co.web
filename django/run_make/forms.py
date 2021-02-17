from django.forms import ModelForm
from .models import TaxConfig


class TaxConfigForm ( ModelForm ):
  class Meta:
    model = TaxConfig
    fields = [ 'email', 'vatRate', 'incomeTaxRate' ]
