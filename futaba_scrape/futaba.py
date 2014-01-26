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
import romkan

DATE_TIME_NUMBER_REGEX = ur'.*?(?P<date>\d{2}/\d{2}/\d{2}).*?(?P<time>\d{2}:\d{2}:\d{2}).*?No.(?P<number>\d*)'

class Post(object):
  '''
  the usual. encapsulates data from a futaba post
  '''
  def __init__(self, date, time, number, text, image):
    '''
    constructor
    '''
    self.date = date
    self.time = time
    self.number = number
    self.text = text
    self.image = image

def extract_date_time_number(text):
  '''
  return a 3 tuple of post (date, time, number)
  '''
  date = ''
  time = ''
  number = ''
  m = re.match(re.compile(DATE_TIME_NUMBER_REGEX, re.UNICODE), text)
  if m:
    date=m.groupdict()['date'].encode('utf-8')
    time=m.groupdict()['time'].encode('utf-8')
    number=m.groupdict()['number'].encode('utf-8')
  return (date, time, number)

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
    date, time, number = extract_date_time_number(date_number)
    results.append(Post(date, time, number, text, img))
  return results

