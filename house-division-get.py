#!/usr/bin/env python3

import requests
from datetime import date
import json

from os import listdir
from os.path import isfile, join
onlyfiles = [ f for f in listdir('.') if isfile(join('.',f)) ]

base = 'https://theyvoteforyou.org.au/api/v1/divisions/'
key = '.json?key=X3yrD2pfGQm%2Fnm0FVumJ'

for f in onlyfiles:
  if f.split('.')[-1] == 'json':
    print("FILE: " + f)
    divlist = json.loads(open(f).read())

    for d in divlist:
      r = requests.get(base+str(d['id'])+key)
      resp = r.json()
      name = resp['name']
      print(str(d['id']) + ': ' + name)
      with open('divisions/house-div-' + str(d['id']) + '.json', 'w') as of:
        json.dump(resp, of)

#
#
#for year in range(start_year, end_year):
#  for month in range(1, 13):
#    sd = str(year) + '-' + str(month) + '-01'
#    ed = str(year) + '-' + str(month) + '-' + str(days_in_month[month-1])
#    url = base + '&start_date=' + sd + '&end_date=' + ed
#    r = requests.get(url)
#    resp = r.json()
#    print("%r-%r: %r" % (month, year, len(resp)))
#    with open('house-'+str(month)+'-'+str(year)+'.json', 'w') as f:
#      json.dump(resp, f)
    