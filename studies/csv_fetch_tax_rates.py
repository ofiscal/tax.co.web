import csv
import os
import pandas
from   typing import List


# PITFALL: These absolute paths need a '.' prepended to them,
# in order to work with the Python `csv` library.
# But Django wants them to be absolute.
marginal_rate_tables = {
  "/config/marginal_rates/most.csv" :
    "El impuesto para la mayoría de las categorías de ingreso:",
  "/config/marginal_rates/dividend.csv" :
    "El impuesto para los dividendos:",
  "/config/marginal_rates/ocasional_high.csv" :
    "El impuesto más alto para los ingresos ocasionales:",
  "/config/marginal_rates/ocasional_low.csv" :
    "El impuesto más bajo para los ingresos ocasionales:",
}

mrt_filepaths = list ( marginal_rate_tables
                       . keys () )

def rate_ceiling_pairs_to_rate_floor_pairs (
  """
  Leaves the rates (first) column unchanged.
  Moves each ceiling down a cell,
  which means the last ceiling (which should be infinity) is lost,
  and sets the first ceiling to 0.
  """
    pairs : List[ List[ float ] ]
    ) ->    List[ List[ float ] ]:
  for i in range( 0, ln-1 ):
    pairs  [ ln-i-1 ] [ ceiling ] = (
      pairs[ ln-i-2 ] [ ceiling ]  )
  pairs    [ 0 ]      [ ceiling ]  = 0
  return pairs

def read_rate_ceiling_table (
    csvFilePath : str
    ) -> List: # Sadly, this list cannot be typed further,
               # as it is not homogenous,
               # because it is pretending to be a tuple,
               # which Javascript does not support.
  #
  # Fetch some portion of each row.
  with open( csvFilePath ) as csvFile:
    reader = csv . DictReader ( csvFile )
    pairs = []
    for row in reader:
      pairs . append ( [ row [ "rate" ],
                         row [ "ceiling" ] ] )
  return [ csvFileName,
           rate_ceiling_pairs_to_rate_floor_pairs ( pairs ) ]
