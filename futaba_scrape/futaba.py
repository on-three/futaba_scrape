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
from time import strftime
import urllib2

DATE_TIME_NUMBER_REGEX = ur'.*?(?P<date>(?P<year>\d{2})/(?P<month>\d{2})/(?P<day>\d{2})).*?(?P<time>(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})).*?No.(?P<number>\d*)'
THREAD_START_MARKER_REGEX = ur'\u753B\u50CF\u30D5\u30A1\u30A4\u30EB\u540D\uFF1A'
RESPONSE_MARKER_REGEX = ur'.*?\u2026.*?'

#basic futaba url
#http://dat.2chan.net/16/futaba.htm
#http://dat.2chan.net/16/2.htm (where number can be 1-10 (higher?)
FUTABA_BOARD_URL_REGEX = ur'^http://.*?\.2chan.net/.*?/(futaba|\d{1,2}).htm$'
#futaba respond page url (on same board as above)
#http://dat.2chan.net/16/res/476764.htm
FUTABA_THREAD_URL_REGEX = ur'^http://.*?\.2chan.net/.*?/res/\d*?\.htm$'

def is_futaba_board(url):
  '''
  Return boolean corresponsind to wether the board URL is 
  a futaba image boad page or not.
  '''
  futaba_board_url_regex = re.compile(FUTABA_BOARD_URL_REGEX, re.UNICODE)
  return re.match(futaba_board_url_regex, url) != None

def response_url_from_board(url, post_id):
  '''
  Provided a given futaba bas page url and a post id
  on that page, form the url of the response page.
  This is to give us URLs of _complete_ response pages
  '''
  if not is_futaba_url(url):
    return ''
  pass
  

class Post(object):
  '''
  the usual. encapsulates an image board post.
  '''
  def __init__(self, time, number, text, image, responses={}):
    '''
    constructor
    '''
    self.time = time
    self.number = number
    self.text = text
    self.image = image
    #a dictionary of responses. Keys are meant to be
    #post number, and values are Post objects.
    #in responses this will typically remain empty.
    self.responses = responses

  def __unicode__(self):
    '''
    Direct printing of class
    '''
    date_time = unicode(strftime(u"%a, %d %b %Y %H:%M:%S", self.time))
    post_number = unicode(self.number)
    s = u'{d} {p} {t}\n'.format(d=date_time, p=post_number, t=unicode(self.text))
    for post_number, response in self.responses.iteritems():
      pn = unicode(post_number)
      date_time = unicode(strftime(u"%a, %d %b %Y %H:%M:%S", response.time))
      s += u'===>{d} {p} {t}\n'.format( \
        d=date_time, \
        p=pn, \
        t=response.text)
    return s

  @staticmethod
  def from_block(html):
    '''
    Extract a Post object from a thread response table cell ('td')
    These response table cells can be found as the td following a td
    which contains the '...' elipsis unicode symbol
    arg: html a bs4 node representing the cell
    '''
    text = html.findNext('blockquote')
    contents = u''.join([unicode(x) for x in text.contents])
    img = html.findNext('a')
    date_number = html.findNext(text=re.compile(DATE_TIME_NUMBER_REGEX))
    time, number = extract_date_time_number(date_number)
    return Post(time, number, contents, img)
    

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

def extract_threads(url, html):
  '''
  Draw thread starting posts out of current html document
  Returns a list of Post objectes, each one being a thread.
  The Post objects responses will be populated with all _available_
  information. i.e. hidden responses will not be populated.
  :arg url base url of board we're extracting threads from
  :arg html html response with page cotents
  the url is included becase we need it to form urls for full
  response pages
  '''
  results = []
  soup = BeautifulSoup(html)
  markers = soup(text=re.compile(THREAD_START_MARKER_REGEX))
  for marker in markers:
    img = marker.findNext('a')
    text = marker.findNext('blockquote')
    contents = u''.join([unicode(x) for x in text.contents])
    date_number = marker.findNext(text=re.compile(DATE_TIME_NUMBER_REGEX))
    time, number = extract_date_time_number(date_number)
    responses = extract_responses(url, marker)
    results.append(Post(time, number, contents, img, responses))
  return results

def extract_responses(url, thread_start_marker):
  '''
  arg: thread_start_marker is a bf4 object that represents the start
  of a thread in a bf4 'soup' object.
  We want to proceed through the thread and get all visible responses
  before the start of the next thread.
  returns: a dictionary of Post objects, with keys = response post number
  and value equal to a Post object for each response.
  '''
  responses = {}
  #fetch html from the response page of this thread start and then parse
  #it for _all_ responses
  #response_url = 

  thread_start = re.compile(THREAD_START_MARKER_REGEX, re.UNICODE|re.DOTALL)
  response_start = re.compile(RESPONSE_MARKER_REGEX, re.UNICODE|re.DOTALL)
  next = thread_start_marker.nextSibling
  while next:
    ustr = unicode(next)
    if re.match(thread_start, ustr):
      break
    if re.match(response_start, ustr):
      block = next.findNext('td').findNext('td')
      if block:
        response = Post.from_block(block)
        responses[response.number] = response
    next = next.nextSibling
  
  return responses

def scrape_futaba(html):
  '''
  Draw posts, responses and images out of typical futaba page.
  There can be N posts, M respones per post, 0 or 1 thumbnail and image per post and response.
  arg: html: unicode encoded html from futaba
  Note that futaba is typically encoded in shift-jis, so it's got to be decoded before
  passing to this method.
  '''
  return extract_threads(html)

def get_threads(url):
  '''
  Get the threads from a futaba image board page
  arg: html url of page.
  returns list of Post objects describing threads
  Post.responses dictionary will be filled with responses
  '''
  threads = []
  if not is_futaba_board(url):
    return threads

  req = urllib2.Request(url)
  try:
    response = urllib2.urlopen(req)
    html = response.read()
    threads = extract_threads(url, html)
  except urllib2.HTTPError as e:
    print e.code
    print e.read()
  return threads

def get_responses(board_url, post_num):
  '''
  Return all responses to a thread given a board url and its post number
  :arg board_url base url of yotsuba board (NOT url of respond page)
  :post_num post id of original thread
  '''
  


