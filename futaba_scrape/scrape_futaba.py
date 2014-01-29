#!/usr/bin/python
# vim: set ts=2 expandtab:
"""

Module: scrape_futaba.py
Desc: use twisted to get futaba front page and scrape info
Author: on_three
Email: on.three.email@gmail.com
DATE: Saturday, January 25th 2014

  1. Initiate fetch of futaba board (which one tbd)
  2. Scrape contents (posts, responses, image urls)
  3. Dump scraped info to stdout (that's all, really)
  
""" 

import os
import os.path
from os.path import expanduser
import re
import uuid
import sys
from time import strftime
import argparse
import string

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc as twisted_irc
from twisted.web.client import getPage

from futaba import scrape_futaba

def on_html_response(html):
  '''
  take apart futaba html response
  '''
  #unicode_html = html.decode('shift-jis')
  unicode_html = html.decode('shift_jisx0213')
  posts = scrape_futaba(unicode_html)
  for post in posts:
    print unicode(post)
  reactor.stop()

def on_html_error(error):
  '''
  standard error handler
  '''
  print error
  reactor.stop()

def main():
  parser = argparse.ArgumentParser(description='Scrape jisho.org for japanese word (romaji) lookup.')
  parser.add_argument('-u', '--url',  help='url to fetch for scraping.', type=str, default='http://dat.2chan.net/img2/futaba.htm')
  args = parser.parse_args()

  #log.startLogging(sys.stdout)

  url = args.url
  result = getPage(url)
  result.addCallbacks(
      callback = on_html_response,
      errback = on_html_error)
  reactor.run()


if __name__ == "__main__":
  main()
