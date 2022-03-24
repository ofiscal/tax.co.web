import json


with open( "/mnt/paths/paths.json" ) as f:
  paths_dict = json.load( f )

tax_co_root = paths_dict["paths"]["docker"]["tax_co"]

def readOneLineFile ( filename : str ) -> str:
  """ The file should contain a single string -- no comments, etc.
Surrounding whitespace is probably harmless but ugly.)

PITFALL: If the file does not exist, this will fail.
"""
  return ( open ( filename )
           . read ()
           . strip () )
