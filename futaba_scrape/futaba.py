# vim: set ts=2 expandtab:
'''

Module: futaba.py
Desc: extract info from futaba html
Author: on_three
Email: on.three.email@gmail.com
DATE: Saturday, January 25th 2014
  
'''
from bs4 import BeautifulSoup
import string
import re
from time import strptime
import romkan

DATE_TIME_NUMBER_REGEX = ur'.*?(?P<date>(?P<year>\d{2})/(?P<month>\d{2})/(?P<day>\d{2})).*?(?P<time>(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})).*?No.(?P<number>\d*)'

class Post(object):
  '''
  the usual. encapsulates data from a futaba post
  '''
  def __init__(self, time, number, text, image):
    '''
    constructor
    '''
    self.time = time
    self.number = number
    self.text = text
    self.image = image

def extract_date_time_number(text):
  '''
  return a 2 tuple of post (datetime, post_number)
  '''
  time = None
  number = 0
  m = re.match(re.compile(DATE_TIME_NUMBER_REGEX, re.UNICODE), text)
  if m:
    #I'm drawing out more info here than necessary
    #this is in case I need the data at some point
    #Note the groupdict dictionary entries originate
    #in the DATE_TIME_NUMBER_REGEX above
    d=m.groupdict()['date'].encode('utf-8')
    #year=m.groupdict()['year'].encode('utf-8')
    #month=m.groupdict()['month'].encode('utf-8')
    #day=m.groupdict()['day'].encode('utf-8')
    t=m.groupdict()['time'].encode('utf-8')
    #hour=m.groupdict()['hour'].encode('utf-8')
    #minute=m.groupdict()['minute'].encode('utf-8')
    #second=m.groupdict()['second'].encode('utf-8')
    n=m.groupdict()['number'].encode('utf-8')

    #form a datetime structure from the extracted data
    date_time = strptime('{d} {t}'.format(d=d, t=t), '%y/%m/%d %H:%M:%S')
    number = int(n)  
  return (date_time, number)

def scrape_futaba(html):
  '''
  Draw posts, responses and posts out of typical futaba page.
  There can be N posts, M respones per post, 0 or 1 thumbnail and image per post and response.
  arg: html: unicode encoded html from futaba
  Note that futaba is typically encoded in shift-jis, so it's got to be decoded before
  passing to this method.
  '''  
  results = []
  soup = BeautifulSoup(html)
  markers = soup(text=re.compile(ur'\u753B\u50CF\u30D5\u30A1\u30A4\u30EB\u540D\uFF1A'))
  for marker in markers:
    img = marker.findNext('a')
    text = marker.findNext('blockquote')
    date_number = marker.findNext(text=re.compile(DATE_TIME_NUMBER_REGEX))
    time, number = extract_date_time_number(date_number)
    results.append(Post(time, number, text, img))
  return results

