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

from futaba import scrape_futaba
from futaba import get_threads

def main():
  parser = argparse.ArgumentParser(description='fetch threads from futaba image board and scrape to stdout.')
  parser.add_argument('-u', '--url',  help='url to fetch for scraping.', type=str, default='http://dat.2chan.net/img2/futaba.htm')
  args = parser.parse_args()

  url = args.url

  threads = get_threads(url)
  for thread in threads:
    print unicode(thread)

if __name__ == "__main__":
  main()
