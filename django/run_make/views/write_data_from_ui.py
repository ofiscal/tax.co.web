###
### Fetch the data created by views.manual_ingest().
### For testing purposes; won't be part of the library.
###

from typing import List, Dict, Any
import pickle
pickle_path = '/home/appuser/dynamic_table.pickle'
with open(pickle_path,'rb') as pickle_being_read:
  req = pickle.loads( pickle_being_read . read () )

del(pickle_being_read)
req

###
### Turn that flat list of columns into a dictionary
### from rate names (e.g. "most", "dividends")
### to dictionaries with two "columns":
### rate and income floor at which the rate starts applying.
###

def make_dict_one_level_hierarchical_from_top (
    d : Dict, # Alas, too polymorphic to be more specific than `Dict`.
    splitter : str
) -> Dict:
  """
  (This is probably easier to understand by seeing the test, defined immediately below this function..)

  MOTIVATION:
  The Django/Javascript UI returns in its `request.POST` object
  a flat dictionary from column names to values. That is, nothing but the name distinguishes a column in one table from another column in a different table. I've therefore used an organizing strategy whereby column names are hierarchical, using commas to separate levels.
  For instance,       "marginal income tax, ocasional_low, rate"
  will be paired with "marginal income tax, ocasional_low, threshold",
  while one level up, "marginal income tax, dividend, rate"
  will be paired with "marginal income tax, dividend, threshold",
  and yet a further level up there will be
                      "vat, something, something".

  WHAT IT DOES:
  Given a dict with keys that are strings, this first splits each key at the first instance of `splitter`. If we call that key's "head" the part before the splitter, and its "tail" the part after, then this returns a new dictionary the keys of which are all the heads, and the values of which are dictionaries from the tails to the values that were previously paired with those tails (and their heads).

  This operates "from the top" in the sense that, if you call it on a dictionary whose values are further dictionaries, it splits the top dictionary, and none of its dictionary values.
  """
  l = ( [ (ht[0], ht[1], value)
          for (key,value) in d.items()
          if ( ht :=
               key.split( splitter,
                          1 ) ) ] ) # max number of splits
  dd = {}
  for (a,b,c) in l:
    new_pair = {b:c}
    dd[a] = ( { **dd[a], **new_pair }
              if dd.get(a)
              else         new_pair )
  return dd

def test_make_dict_one_level_hierarchical_from_top():
  d = { "a,b,c":1, # This key splits into the head "a" and the tail "b, c".
        "a,c"  :2, # This key splits into the head "a" and the tail "c".
        "d,e"  :3} # This key splits into the head "b" and the tail "b".
  # `make_dict_one_level_hierarchical_from_top` should put the first two items
  # into one dictionary, and the third into its own,
  # stripping the heads from each.
  assert (
    make_dict_one_level_hierarchical_from_top(
      d, "," ) ==
    { "a" : { "b,c":1, # Note that the second comma is ignored.
              "c"  :2 },
      "d" : { "e"  :3 } } )

marginal_rates = (
  make_dict_one_level_hierarchical_from_top (
    req, ", " ) )


###
### Turn each list of floors (which is nice for the UI)
### to a list of ceilings (which is what tax.co uses).
###

def list_of_floors_to_list_of_ceilings (
    floors : List[float]
    ) -> List[float]:
  if floors == []: # Without this, an empty list would trigger an out-of-range error.
    return []
  acc = floors.copy()
  for i in range( 0, len(floors)-1 ):
    acc[i] = floors[i+1]
  acc[-1] = 9e99 # infinity, basically
  return acc

def test_list_of_floors_to_list_of_ceilings():
  assert list_of_floors_to_list_of_ceilings( [] ) == []
  assert list_of_floors_to_list_of_ceilings( [0] ) == [9e99]
  assert list_of_floors_to_list_of_ceilings( [0,10] ) == [10,9e99]

def rename_key_in_dict ( old_name, new_name, d ):
  d[new_name] = d.pop( old_name )
  return d

for k in marginal_rates.keys():
  marginal_rates[k]["min income"] = (
    list_of_floors_to_list_of_ceilings(
      marginal_rates[k]["min income"] ) )
  marginal_rates[k] = rename_key_in_dict (
    "tax rate", "rate", marginal_rates[k] )
  marginal_rates[k] = rename_key_in_dict (
    "min income", "ceiling", marginal_rates[k] )

###
### Write the marginal rates to a user's folder.
###

import os
import csv

user_folder = "/mnt/tax_co/temp/"
rates_folder = os.path.join( user_folder, "config/marginal_rates/" )
marginal_rate_to_write = "most"
file_to_write = os.path.join(
  rates_folder, marginal_rate_to_write, ".csv" )

with open( file_to_write, 'w'
          ) as csvfile:
  spamwriter = csv.writer(
    csvfile, delimiter=',',
    # PITFALL: I'm not sure I trust this quote algorithm for strings, because it writes the last item below as "quote char "" yeah". However, reading it back with the `csv` library or `pandas` both seem to work -- the ("") becomes a single (").
    quotechar = '\"',
    quoting = csv.QUOTE_MINIMAL)
  spamwriter.writerow(["rate",
  spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam',
                       "quote char \" yeah"])
  spamwriter.writerow(['a2','b2','c2','d2'])
