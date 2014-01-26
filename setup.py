# vim: set ts=2 expandtab:
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='futaba_scrape',
  version='0.1',
  description='Scrape Futaba image board of standard style.',
  long_description = readme(),
	classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
  ],
  keywords = 'futaba image board parsing scrape',
  url='https://github.com/on-three/futaba_scrape',
  author='on_three',
  author_email='on.three.email@gmail.com',
  license='MIT',
  packages=[
    'futaba_scrape',
  ],
  install_requires=[
    'twisted',
    'argparse',
    'romkan',
    'beautifulsoup4',
    'pytz',
  ],
  #entry_points = {
  #  'console_scripts': [
  #    'futaba-scrape=futaba_scrape.:main',
  #  ],
  #},
  zip_safe=True)
