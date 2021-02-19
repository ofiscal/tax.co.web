from django . db import models


class TaxConfig ( models . Model ):
  user_email = models . EmailField (
      default = "quien@donde.net" )
  subsample = models . IntegerField (
      "Reciproca del tamaño de la submuestra (1, 10, 100 o 1000)",
      default = 1 )
#  strategy = models . CharField ( "Estrategia",
#                                   default = "detail" )
#  year = models . IntegerField (
#      "Año de la ley de impuestos (2016, 2018, 2019)",
#      default = 2019 )
#  More await in tax.co ...
