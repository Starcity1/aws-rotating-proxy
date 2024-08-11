from config import PROXY_URLS
from random import randint
import requests
from bs4 import BeautifulSoup


class RotatingProxy:

    def __init__(self, verbose: bool = False):
        # Verbose variable allows us to see which proxy received the request.
        self.verbose = verbose

    def send_post(self, url: str) -> str:
        proxy_url = self._get_random_proxy_url()
        response = requests.post(proxy_url, data={'url': url})

        if self.verbose:
            print(f"Sent POST request to proxy {proxy_url}\n")

        if response.status_code != 200:
            raise requests.RequestException(f"Could not get page: HTTP Errno {response.status_code}")

        return BeautifulSoup(response.content, 'html.parser')

    @staticmethod
    def _get_random_proxy_url() -> str:
        index = randint(0, len(PROXY_URLS) - 1)
        return PROXY_URLS[index]
