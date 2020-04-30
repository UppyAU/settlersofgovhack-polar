#!/usr/bin/env python3

import requests
from datetime import date
import json

base = 'https://theyvoteforyou.org.au/api/v1/divisions.json?key=X3yrD2pfGQm%2Fnm0FVumJ&house=senate'

start_year = 2006
end_year = 2016

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for year in range(start_year, end_year):
  for month in range(1, 13):
    sd = str(year) + '-' + str(month) + '-01'
    ed = str(year) + '-' + str(month) + '-' + str(days_in_month[month-1])
    url = base + '&start_date=' + sd + '&end_date=' + ed
    r = requests.get(url)
    resp = r.json()
    print("%r-%r: %r" % (month, year, len(resp)))
    with open('senate-'+str(month)+'-'+str(year)+'.json', 'w') as f:
      json.dump(resp, f)
    