# This demonstrates how the `csv` library can be used as a simpler,
# compatible alternative to `pandas` for reading and writing csv data.
# Crucially for tax.co.web, and unlike `pandas`,
# `csv` is available from the strange Python environment that Apache uses.

import csv
import pandas


filename = "csvlib-test.csv"

with open( filename, 'w',
           newline='' # magic
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

with open( filename, newline='' ) as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    print(', '.join(row))

with open(filename, newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    print(row['a'], "|", row['c'])

x = pandas.read_csv( filename )
x
