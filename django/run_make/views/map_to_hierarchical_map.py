from typing import List, Dict, Any


def make_dict_one_level_hierarchical_from_top (
    d : Dict, # Alas, too polymorphic to be more specific than `Dict`.
    splitter : str
) -> Dict:
  """
  (This is probably easier to understand by seeing the test,
  defined immediately below this function..)

  MOTIVATION:
  The Django/Javascript UI returns in its `request.POST` object
  a flat dictionary from column names to values.
  That is, nothing but the name distinguishes a column in one table
  from another column in a different table.
  I've therefore used an organizing strategy whereby column names
  are hierarchical, using commas to separate levels.
  For instance,       "marginal income tax, ocasional_low, rate"
  will be paired with "marginal income tax, ocasional_low, threshold",
  while one level up, "marginal income tax, dividend, rate"
  will be paired with "marginal income tax, dividend, threshold",
  and yet a further level up there will be
                      "vat, something, something".

  WHAT IT DOES:
  Given a dict with keys that are strings,
  this first splits each key at the first instance of `splitter`.
  If we call that key's "head" the part before the splitter,
  and its "tail" the part after,
  then this returns a new dictionary the keys of which are all the heads,
  and the values of which are dictionaries from the tails to the values
  that were previously paired with those tails (and their heads).

  This operates "from the top" in the sense that,
  if you call it on a dictionary whose values are further dictionaries,
  it splits the top dictionary,
  and none of its dictionary values.
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
