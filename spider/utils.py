import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Crawler:
    pages_to_visit = []
    max_depth = 1
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def spider(self, url, current_depth=1):
        response = requests.head(url)
        if response.headers.get('Content-Type').split(';')[0] =='text/html':
            self.pages_to_visit.append(url)
            if current_depth >= self.max_depth:
                return
            for link in self.get_links(url):
                self.spider(link, current_depth+1)


    def get_links(self, url):
        scheme, host = urlparse(url)[:2]
        response = requests.get(url)
        s = BeautifulSoup(response.text, "html.parser")
        for link in s.findAll('a'):
            href = link.get('href')
            if href:
                # if links start with '//', strip '//'
                if href.startswith('//'):
                    href = href[2:]
                href_host = urlparse(href)[1]
                # Check if links are of the same site
                if href_host == host:
                    yield link.get('href')
                # if links start with '/', it is the same site
                elif href.startswith('/'):
                    yield scheme + '://' + host + link.get('href')

        def get_images(self, url):
            pass

if __name__ == "__main__":
    c = Crawler(max_depth=2)
    c.spider('https://www.google.com')
    print(c.pages_to_visit)


