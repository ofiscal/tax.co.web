from django . db import models


class TaxConfig ( models . Model ):
  email = models . EmailField (
      default = "someone@somewhere.net" )
  vatRate = models . FloatField ( "VAT rate",
                                  default = 0.19 )
  incomeTaxRate = models . FloatField ( "income tax rate",
                                        default = 0 )
