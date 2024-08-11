"""
This is a proof of concept on using my Zappa, AWS Lambda proxy server to implement a rotating IP server and avoid web-
scrapping nasty stuff..
"""

from typing import Optional, List
from RotatingProxy import RotatingProxy

URL = "https://en.wikipedia.org/wiki/Main_Page"


class WikiWebScraper:
    def __init__(self,
                 url: Optional[str] = None,
                 verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.proxy = RotatingProxy(self.verbose)

    def get_http(self, new_url: Optional[str] = None) -> bytes:
        if new_url is not None:
            self.url = new_url

        return self._get_http().prettify()

    def get_all_links(self, new_url: Optional[str] = None) -> List:
        if new_url is not None:
            self.url = new_url
        return self._get_all_links()

    def _check_url(self):
        if not self.url:
            raise RuntimeError("URL was not provided")

    def _get_http(self):
        self._check_url()
        return self.proxy.send_post(self.url)

    def _get_all_links(self) -> List:
        self._check_url()
        content = self._get_http()
        hypertexts = content.find_all('a')
        links = list()

        for hypertext in hypertexts:
            if 'https' in hypertext['href']:
                links.append(hypertext['href'])
        return links


# MAIN FUNCTION WORKS FOR TESTING PURPOSES ONLY
def main() -> None:
    scraper = WikiWebScraper(URL, True)
    for _ in range(100):
        scraper.get_http()


if __name__ == "__main__":
    main()
