#!/usr/bin/env python3
from datetime import datetime, timedelta, date
import re


# Set Date format like: YYYY, MM, DD
# Note that FIND_FIRST_DATE uses START_DATE as default start date
avg_over_min = 1
days_look_back = 30
en_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
st_date = (datetime.now() - timedelta(days=days_look_back)
           ).strftime('%Y-%m-%dT%H:%M:%S')

# searching string
match_str = re.search(r'\d{4}-\d{2}-\d{2}', st_date)

# computed date
# feeding format
res = datetime.strptime(match_str.group(), '%Y-%m-%d').date()


START_DATE = res
END_DATE = date.today()

# set to "metric" or "imperial"
UNIT_SYSTEM = "metric"
# UNIT_SYSTEM = "imperial"

# Automatically find first date where data is logged
FIND_FIRST_DATE = True
