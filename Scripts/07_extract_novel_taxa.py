import sys
import csv
import pandas
'''Extract taxa that is not existing in the repbase database'''

with open(sys.argv[1]) as rep_f:
    rep_base = pandas.read_csv(rep_f, delimiter=',')
    print(rep_base['Crypton name', 'Discovered in'])
