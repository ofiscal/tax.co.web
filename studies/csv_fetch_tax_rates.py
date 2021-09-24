import csv
import os
import pandas
from   typing import List


# PITFALL: These absolute paths need a '.' prepended to them,
# in order to work with the Python `csv` library.
# But Django wants them to be absolute.
# They've been written Django-style to duplicate the environment
# in which I'll be using these functions.
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

def rate_ceiling_pairs_to_rate_floor_pairs (
    pairs : List[ List[ float ] ]
    ) ->    List[ List[ float ] ]:
  """
  Leaves the rates (first) column unchanged.
  Moves each ceiling down a cell,
  which means the last ceiling (which should be infinity) is lost,
  and sets the first ceiling to 0.
  """
  ceiling = 1 # Just an index, for the second elt of each pair.
  ln = len ( pairs )
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
  csvFileName = os.path.split ( csvFilePath ) [1]
  return [ csvFileName,
           rate_ceiling_pairs_to_rate_floor_pairs ( pairs ) ]

mrt_filepaths = list ( marginal_rate_tables
                       . keys () )
rates = []
for p in ( marginal_rate_tables . keys () ):
  rates . append (
    read_rate_ceiling_table ( "." + p ) )
