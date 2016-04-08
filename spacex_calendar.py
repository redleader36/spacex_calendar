#!/usr/bin/python
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from lxml import etree
import json
import re
from icalendar import Calendar, Event
from datetime import datetime
from dateutil import parser

url = "https://spacexstats.com/missions/future"
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
response = urlopen(url)
tree = etree.parse(response, etree.HTMLParser())
list = tree.xpath('//script[1]/text()')[0]
regex = re.compile(".*?\[(.*?)\]")
result = "[%s]"%re.findall(regex, list)[0]
launches = json.loads(result)
for launch in launches:
    if launch['launch_exact']:
        launch_exact = parser.parse(launch['launch_exact']+" UTC")
        event = Event()
        event.add('uid', launch['mission_id'])
        event.add('summary', launch['name'])
        event.add('dtstart', launch_exact)
        event.add('description', launch['summary'])
        cal.add_component(event)

f = open('spacex.ics', 'wb')
f.write(cal.to_ical())
f.close()