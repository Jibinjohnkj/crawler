import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Crawler:
    max_links = 25

    def __init__(self, url, max_depth=1):
        self.max_depth = max_depth
        self.url = url
        self.pages_to_visit = []

    def get_links(self):
        # If max_links reached return
        duplicate, limit_reached = self.check_if_duplicate_and_add(self.url)
        if limit_reached:
            return self.pages_to_visit

        self.links_spider(self.url, 1)
        return self.pages_to_visit

    def links_spider(self, url, current_depth):
        """
        Recursively parse all links until max_depth is reached
        """

        # Exit if max_depth reached
        if current_depth >= self.max_depth:
            return

        response = requests.head(url)
        # Ignore non html content
        if response.headers.get('Content-Type').split(';')[0] =='text/html':

            # Two loops for the same thing
            # This is a conscious choice. As we want the spider to crawl only if max_links not reached and
            # also avoid crawling duplicate links
            links = []
            for link in self.parse_links(url):
                # Add to self.pages_to_visit, if max_links reached return
                duplicate, limit_reached = self.check_if_duplicate_and_add(link)
                if limit_reached:
                    return
                if not duplicate:
                    links.append(link)

            for link in links:
                self.links_spider(link, current_depth + 1)

    def parse_links(self, url):
        """
        Given a url retrieve all links
        """
        scheme, host = urlparse(self.url)[:2]
        response = requests.get(url)
        s = BeautifulSoup(response.text, "html.parser")
        # Get all links
        for link in s.findAll('a'):
            href = link.get('href')
            if href:
                # If links starts with '//', add scheme
                if href.startswith('//'):
                    href = scheme + ':' + href

                # If links starts with '/', its in the same domain, so just add scheme and host
                if href.startswith('/'):
                    yield scheme + '://' + host + href
                else:
                    # Check if links are of the same domain
                    href_host = urlparse(href)[1]
                    if href_host == host:
                        yield href

    def check_if_duplicate_and_add(self, url):
        """
        Given a url, Check if duplicate, if not add to self.pages_to_visit. Also check if max_links reached
        """
        duplicate = False
        for item in self.pages_to_visit:
            # Check if the url already exist in self.pages_to_visit after stripping unnecessary bits
            if self.__class__.process_url(url) == self.__class__.process_url(item):
                duplicate = True
        if duplicate:
            return True, False,
        else:
            # Safety precaution against timeout
            if len(self.pages_to_visit) < self.max_links:
                self.pages_to_visit.append(url)
                return False, False,
            else:
                return False, True,

    @staticmethod
    def process_url(url):
        """
        Given a url, strip scheme, 'www' and ending '/'
        """
        # Remove scheme before comparison
        if url.startswith('http://'):
            url = url.lstrip("http://")
        # Remove scheme before comparison
        if url.startswith('https://'):
            url = url.lstrip("https://")
        # Remove 'www' before comparison
        if url.startswith('www.'):
            url = url.lstrip("www.")
        # Remove ending '/' before comparison
        if url.endswith('/'):
            url = url.rstrip('/')
        return url

    def get_images(self):
        """
        Get all images from self.url
        """
        scheme, host = urlparse(self.url)[:2]
        response = requests.get(self.url)
        s = BeautifulSoup(response.text, "html.parser")
        for link in s.findAll('img'):
            src = link.get('src')
            if src:
                # If base64 encode images, skip
                if src.startswith('data:'):
                    continue
                # If src start with '//', add scheme
                elif src.startswith('//'):
                    yield scheme + ':' + src
                # If links starts with '/', add scheme and host
                elif src.startswith('/'):
                    yield scheme + '://' + host + src
                else:
                    yield src



