# crawler
A simple web crawler based on Django


Installation
------------
pip install pipenv

git clone https://github.com/Jibinjohnkj/crawler.git

cd crawler

pipenv install --ignore-pipfile

pipenv shell

python manage.py migrate

python manage.py runserver


Introduction
------------

The web crawler will require two inputs:

1. The URL to crawl.
2. The depth the crawler should go into. 


A depth level of 1 means that the crawler would fetch the images from the supplied URL and show them. A depth level of 2 would mean the crawler would follow links to pages found in the first page and fetch images from them. Likewise, 3 would mean the crawler would follow links found in the second level page and fetch images from them and so on.

The maximum depth has been restricted to 3 and the maximum links generated has been restricted to 25 to promote fair usage

Duplicates links has been removed.
http://example.com, https://example.com, https://example.com/, example.com, www.example.com all are considered duplicates

The crawler would be limited to the domain in the provided URL. The crawler would not crawl external site’s content.

For images starting with '/' or '//', domains and scheme have been added appropriately.

Base64 encoded images have been ignored

