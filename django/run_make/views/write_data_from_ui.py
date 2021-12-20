import csv
import os
from   typing import List, Dict

from   run_make.forms import TaxConfigForm


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
  l = []
  for (key,value) in d.items():
    ht = key.split( splitter,
                    1 ) # max number of splits
    l.append( ( ht[0], ht[1], value) )

  # It would be nicer to write the above the following way,
  # but until Apache starts using the right version of Python,
  # I can't -- the walrus operator was only introduced in 3.8.
  #
  # l = ( [ (ht[0], ht[1], value)
  #         for (key,value) in d.items()
  #         if ( ht := # "head and tail"
  #              key.split( splitter,
  #                         1 ) ) ] ) # max number of splits

  dd : Dict = {} # Can't get more specific because it could be
                 # nested to any depth.
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

def list_of_floors_to_list_of_ceilings (
    floors : List[float]
    ) -> List[float]:
  """
  Turn each list of floors (which is nice for the UI)
  to a list of ceilings (which is what tax.co uses).
  """
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

def prefix_non_tax_fields ( d : Dict ) -> Dict:
  """
  PITFALL: Destructive, because `rename_key_in_dict` is.
  PURPOSE: I would prefer to prefix "non-tax" to these fields
  in the definition of `TaxConfigForm`, but I can't,
  because Django treats a string with a comma in it as two separate strings
  when passing the string to Javascript.
  The "non-tax" prefix will distinguish these kinds of fields
  from the "income tax" and "VAT" fields,
  which will be prefixed as such.
  """
  for s in TaxConfigForm () . fields . keys ():
    rename_key_in_dict ( s, "non-tax, " + s, d )
  return d

def test_prefix_non_tax_fields ():
  d = {'user_email': ['quien@donde.net'],
       'subsample': ['1'],
       'strategy': ['detail'],
       'regime_year': ['2019'],
       'income tax, most, tax rate': [] } # list not important
  assert ( prefix_non_tax_fields ( d ) ==
           {'non-tax, user_email': ['quien@donde.net'],
            'non-tax, subsample': ['1'],
            'non-tax, strategy': ['detail'],
            'non-tax, regime_year': ['2019'],
            'income tax, most, tax rate': [] } )

# PITFALL: Destructive.
def rename_key_in_dict ( old_name, new_name, d : Dict ) -> Dict:
  d[new_name] = d.pop( old_name )
  return d

def rate_threshold_column_dict_to_row_list (
    col_names : List[str],
    d : Dict[ str, List[float] ]
) -> List[ List ]: # Can't get more specific because the first inner list
                   # is of strings (column names), the rest of numbers.
  """
PURPOSE:
This inputs a dictionary representing a table,
the keys of which are column names
and the values of which are columns of numbers.
It returns a list of rows -- mostly numbers,
except for the first row, which is a list of the column names.
The result is thus suitable for export via the `csv` library.

PITFALL: Assumes d is a map from strings to lists,
where each list is the same length.
  """
  d0 = d.copy()
  acc = []
  while d0[ col_names[0] ]:
    r = []
    for n in col_names: # pop the front of d[n], stick it onto the end of r
      r.append( d0[n].pop(0) )
    acc.append(r)
  acc.insert(0, col_names)
  return acc

def test_rate_threshold_column_dict_to_row_list ():
  d = { "a" : [1,2],
        "b" : [3,4] }
  assert (
    rate_threshold_column_dict_to_row_list (
      ["b","a"], d )
    == [ [ "b", "a" ],
         [  3 ,  1  ],
         [  4 ,  2  ] ] )

def flat_marginal_rates_dict_to_csv_writeable_lists (
    flat_marginal_rates_dict ):
  marginal_rates = (
    make_dict_one_level_hierarchical_from_top (
      flat_marginal_rates_dict, ", " ) )
  for k in marginal_rates.keys():
    marginal_rates[k]["min income"] = (
      list_of_floors_to_list_of_ceilings(
        marginal_rates[k]["min income"] ) )
    marginal_rates[k] = (
      rate_threshold_column_dict_to_row_list(
        ["ceiling", "rate"],
        rename_key_in_dict (
          "tax rate", "rate",
          rename_key_in_dict (
            "min income", "ceiling",
            marginal_rates[k] ) ) ) )
  return marginal_rates

def write_marginal_rates_to_user_folder (
    user_folder,
    marginal_rates ):
  """
  The `marginal_rates` argument should be a weird ill-typed list,
  such as is output by `reqest_to_csv_writeable_lists`.
  """
  def rate_filepath ( rate_name : str ):
    return os.path.join(
      user_folder, "config/marginal_rates",
      rate_name + ".csv" )
  for kind_of_income in marginal_rates.keys():
    with open( rate_filepath( kind_of_income ), 'w'
              ) as csvfile:
      w = csv.writer( csvfile, delimiter=',', quotechar = '\"',
                      lineterminator="\n",
                      quoting = csv.QUOTE_MINIMAL)
      for row in marginal_rates[ kind_of_income ]:
        w.writerow( row )

def flat_vat_dict_to_consumables_list ( vat_dict ):
  """
  The test (next) *used to* explain what this does.
  """
  vat = make_dict_one_level_hierarchical_from_top ( vat_dict, ", " )
  rates                        = vat["rate"]
  consumables_by_coicop_prefix = vat["coicop_prefix"]
  consumables_other_groups     = vat["other_groups"]
  for d in ( rates,
             consumables_by_coicop_prefix,
             consumables_other_groups ):
    for k in d.keys ():
      d[k] = d[k][0] # Unwrap the list.
  for d in ( consumables_by_coicop_prefix,
             consumables_other_groups ):
    for k in d.keys():
      # Replace an integer rate group name (e.g. "2")
      # with a percentage rate (e.g. "0.19").
      d [k] = float ( rates [ d [ k ] ] )
  return ( ( [ [ "group", "vat" ] ] +
             [ [ k, consumables_by_coicop_prefix [ k ] ]
               for k in consumables_by_coicop_prefix.keys() ] ),
           ( [ [ "group", "vat" ] ] +
             [ [ k, consumables_other_groups [ k ] ]
               for k in consumables_other_groups.keys() ] ) )

# TODO: This is obsolete.
# It worked when the input data was only a single table,
# but now it's a pair of tables.
def test_flat_vat_dict_to_consumables_list ():
  flat = {"rate, 0": ["0.0"],
          "consumable, food": ["0"],
          "rate, 1": ["0.05"],
          "consumable, medicine": ["1"],
          "rate, 2": ["0.19"],
          "consumable, travel": ["2"],
          "consumable, entertainment": ["2"]}
  assert ( flat_vat_dict_to_consumables_list ( flat )
           == [ ["consumable", "vat"],
                ["food", 0.0],
                ["medicine", 0.05],
                ["travel", 0.19],
                ["entertainment", 0.19 ] ] )

def write_vat_rates_to_user_folder (
    user_folder,
    consumable_groups ):
  for (data, name) in [
      ( consumable_groups[0], "consumable_groups_by_coicop_prefix" ),
      ( consumable_groups[1], "consumable_groups_other" ) ]:
    with open (
        os.path.join (
          user_folder, "config/vat",
          name + ".csv" ),
        mode = 'w',
        encoding = "utf-8" ) as csvfile:
      w = csv.writer( csvfile, delimiter=',', quotechar = '\"',
                      lineterminator="\n",
                      quoting = csv.QUOTE_MINIMAL)
      for row in data:
        w.writerow ( row )

def divide_post_object_into_dicts ( post_object ):
  d = dict ( post_object )
  d . pop ( "csrfmiddlewaretoken" ) # No need to keep the CSRF token.
  d = prefix_non_tax_fields ( d )
  d = make_dict_one_level_hierarchical_from_top ( d, ", " )
  return ( d["non-tax"],
           d["income tax"],
           d["VAT"] )

### # Here's a way to test the IO in this module.
### # (The non-IO can be tested by simply running the functions
### # whose names begin with "test_".)
### #
### # First, the view that handles the request.POST object
### # must cast it as an ordinary dict and pickle it:
#
#   d = dict ( request.POST )
#   d.pop( "csrfmiddlewaretoken" ) # drop the CSRF token
#    filename = 'dynamic_table.pickle'
#   with open ( filename,'wb' ) as f:
#     f.write (
#       pickle.dumps ( d ) )
#
### # Provided that's done, this (which can be run from any Python shell)
### # will write the data to a `marginal_rates/` folder:
#
#   import pickle
#   pickle_path = '/home/appuser/dynamic_table.pickle'
#   with open(pickle_path,'rb') as pickle_being_read:
#     req = pickle.loads( pickle_being_read . read () )
#
#   del(pickle_being_read)
#   write_marginal_rates_to_user_folder(
#     "/mnt/tax_co/temp/config/marginal_rates/",
#     reqest_to_csv_writeable_lists( req ) )
