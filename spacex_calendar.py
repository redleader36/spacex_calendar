#!/usr/bin/python3
from urllib.request import urlopen
from lxml import etree
import json
import re
from icalendar import Calendar, Event
from datetime import datetime
# import pytz
from dateutil import parser
# import os

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

url = "https://spacexstats.com/missions/future"
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
with urlopen(url) as response:
    tree = etree.parse(response, etree.HTMLParser())
    list = tree.xpath('//script[1]/text()')[0]
    # list = list.replace("", "")
    regex = re.compile(".*?\[(.*?)\]")
    result = "[%s]"%re.findall(regex, list)[0]
    launches = json.loads(result)
    for launch in launches:
        if launch['launch_exact']:
            # print("%s at %s"%(launch['name'], launch['launch_exact']))
            launch_exact = parser.parse(launch['launch_exact']+" UTC")
            print(launch_exact)
            event = Event()
            event.add('uid', launch['mission_id'])
            event.add('summary', launch['name'])
            event.add('dtstart', launch_exact)
            # event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
            # event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))
            event.add('description', launch['summary'])
            cal.add_component(event)

    # print(display(cal))
    f = open('spacex.ics', 'wb')
    f.write(cal.to_ical())
    f.close()