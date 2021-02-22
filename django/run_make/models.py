from django . db import models


class TaxConfig ( models . Model ):
  user_email = models . EmailField (
      verbose_name = "Su correo electrónico",
      default = "quien@donde.net" )
  subsample = models . IntegerField (
      verbose_name = "Reciproca del tamaño de la submuestra (1, 10, 100 o 1000)",
      default = 1 )
  strategy = models . CharField (
      max_length = 64, # PITFALL: Mandatory for CharFields
      verbose_name = "Estrategia",
      default = "detail" )
  year = models . IntegerField (
      verbose_name = "Año de la ley de impuestos (2016, 2018, 2019)",
      default = 2019 )
