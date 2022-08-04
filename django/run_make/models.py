from django.db import models


class TaxConfig ( models . Model ):
  # With the except of the user's email, these specs are "advanced" --
  # without studying the tax.co code,
  # users won't have any idea what they are about.
  user_email = models . EmailField (
      verbose_name = "Su correo electrónico",
      default = "quien@donde.net" )
  subsample = models . IntegerField (
      verbose_name = "Tamaño de la submuestra usado",
      default = 1,
      choices =
          [ (1, "Use todos los datos del ENPH." )
          , (10, "Use 1/10 de los datos del ENPH.")
          , (100, "Use 1/100 de los datos del ENPH.")
          , (1000, "Use 1/1000 de los datos del ENPH.") ] )
  strategy = models . CharField (
      max_length = 64, # PITFALL: Mandatory for CharFields
      verbose_name = "Estrategia",
      default = "detail",
      choices = [
        ("detail",
         "El defecto."),
        ("single_2052_UVT_income_tax_deduction",
         "Solamente 2052 UVTs deducible de la renta laboral."),
        ("second_stage_2052_UVT_income_tax_deduction",
         "Solamente 2052 UVTs deducible en la segunda etapa de deducciones.")
      ] )
  regime_year = models . IntegerField (
      verbose_name = "Año de la ley de impuestos",
      default = 2019,
      choices = [ (2019,"2019")
                , (2018,"2018")
                , (2016,"2016") ] )
