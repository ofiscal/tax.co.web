import json


with open( "/mnt/paths/paths.json" ) as f:
  paths_dict = json.load( f )

tax_co_root = paths_dict["paths"]["docker"]["tax_co"]
