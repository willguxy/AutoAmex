#!/usr/bin/env python

import sys
import csv

def main():
  if len(sys.argv) != 1:
    sys.exit()

  file_name = sys.argv[0]

  with open(file_name, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
      print ','.join(row)

if __name__ == '__main__':
  main()