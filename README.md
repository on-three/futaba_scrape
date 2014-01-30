futaba_scrape
=============

Futaba (ふたば) image board scraping utility in Python.

Intallation
-----------

To install point pip to this github. Cautions regarding loading a virtualenv are as usual.
```
sudo pip install git+https://github.com/on-three/futaba_scrape.git
```
Or clone the repository and install via python setup.py as usual
```
git clone https://github.com/on-three/futaba_scrape.git
...
cd futaba_scrape
sudo python setup.py install
```

Using
-----
The one primary method the package provides is get_threads(url). Pass this method the URL of a futaba board page (either the front page or any numbered page) and it returns a list of Post objects, each representing a thread.
```
from futaba_scrape import get_threads

futaba_page = 'http://dat.2chan.net/16/futaba.htm' #2D Gag board
#this would also be acceptable:
#futaba_page = 'http://dat.2chan.net/16/1.htm'
threads = get_threads(futaba_page)

#threads is a list of Post objects from which we can get post number, text, date (as datetime) etc.
for thread in threads:
  date_string = strftime(u"%a, %d %b %Y %H:%M:%S", thread.time)
  post_number = thread.number
  post_text = thead.text
  image_url = thread.img 
  thumbnail_url = thread.thumbnail
  thread_poster = thread.name
  thread_title = thread.title
```

We also currently fetch all responses from the associated thread URL. These are available in the Post.responses dictionary. The diciontary keys are post id numbers, and the values are Post objects, one for each response.

```
responses = thread.responses
for post_number, response in responses.iteritems():
  response_text = response.text

```

Post objects leave all html and escapes in place in Post.text
