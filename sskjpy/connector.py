# coding=utf-8
import logging

try:
    import requests

    mode = "requests"

    # Suppress logging
    logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)
except ImportError:
    requests = None
    from urllib.request import urlopen

    mode = "urllib"

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def requests_get(url):
    return requests.get(url).text


def urllib_get(url):
    return urlopen(url)


class Connector:
    def __init__(self, fn):
        self.requester = fn

    @classmethod
    def find_best(cls):
        if mode == "requests":
            return Connector(requests_get)
        elif mode == "urllib":
            return Connector(urllib_get)

    @classmethod
    def find_requests(cls):
        return Connector(requests_get)\

    @classmethod
    def find_urllib(cls):
        return Connector(urllib_get)

    def get(self, url):
        return self.requester(url)
