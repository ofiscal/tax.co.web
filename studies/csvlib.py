# This demonstrates how the `csv` library can be used as a simpler,
# compatible alternative to `pandas` for reading and writing csv data.
# Crucially for tax.co.web, and unlike `pandas`,
# `csv` is available from the strange Python environment that Apache uses.

# PITFALL: The documentation[1] passes the argument `newline=''`
# to a lot of these commands. I tested a lot, and it seems to have no effect,
# so I have omitted that argument.
# [1] https://docs.python.org/3/library/functions.html#open

import csv
import pandas


filename = "csvlib-test.csv"

with open( filename, 'w',
          ) as csvfile:
  spamwriter = csv.writer(
    csvfile, delimiter=',',
    # PITFALL: I'm not sure I trust this quote algorithm for strings,
    # because it writes the last item below as "quote char "" yeah".
    # However, reading it back with the `csv` library or `pandas`
    # both seem to work -- the ("") becomes a single (").
    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['a','b','c','fourth column'])
  spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam',
                       "quote char \" yeah"])
  spamwriter.writerow(['a2','b2','c2','d2'])

# Print all rows, whole.
with open( filename,
          ) as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    print(', '.join(row))

# Dump data (strictly) into a variable.
with open( filename,
          ) as csvfile:
  x = []
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    x.append( row )

for i in x: print(i)

# Fetch some portion of each row.
with open(filename,
          ) as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    print(row['a'], "|", row['c'])

# Pandas understands this file format.
x = pandas.read_csv( filename )
x
