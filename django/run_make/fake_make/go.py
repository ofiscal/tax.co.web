# PITFALL: Currently this operates from /home/jeff,
# so it requires copying the code
# (specifically go.py and the Makefile) to that folder,
# before visiting the view will trigger this code.
import json


with open ( 'input.json', 'r' ) as f:
    data = json . load ( f )

data2 = { "vatRate"       : data["vatRate"]       / 3,
          "incomeTaxRate" : data["incomeTaxRate"] / 3 }

with open ( 'output.json', 'w' ) as f:
    json . dump ( data2, f )
