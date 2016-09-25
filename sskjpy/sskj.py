# coding=utf-8
import time
import logging
import urllib.request
import unittest

from bs4 import BeautifulSoup
from urllib.parse import quote as url_encode

__author__ = "DefaltSimon"
__version__ = "0.2"
__license__ = "MIT"


SEARCH_URL = "http://sskj.si/?s={}"
MAX_DEFINITIONS = 50

REPLACEMENTS = {
    "\xa0": " "
}

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Utility


def remove_num(d):
    for n in range(1, MAX_DEFINITIONS):
        if str(d).startswith(str(n) + "."):
            return str(d).strip(str(n) + ".")


def parse_encoding(data):
    for target, replacement in REPLACEMENTS.items():
        data = str(data).replace(target, replacement)

    return data


def clean(data):
    return str(data).strip(" ").strip("\n")


class NotFound(Exception):
    pass


class Definition(object):
    """
    A word definition
    """
    def __init__(self, **kwargs):
        # The term you searched for
        self.word = kwargs.get("word")
        # The closest word
        self.keyword = kwargs.get("keyword")

        # Summary is the first definitions
        self.summary = kwargs.get("summary")
        # A list of definitions
        self.definitions = kwargs.get("definitions")
        # The word's attributes
        self.attributes = kwargs.get("attributes")

        # And its terminology and slang
        self.terminology = kwargs.get("terminology")
        self.slang = kwargs.get("slang")

        # Developer things...
        self._timestamp = kwargs.get("timestamp")


class SSKJParser:
    """
    The main class that gets definitions.
    """

    def __init__(self, max_cache_age=43200):
        self.cache = {}
        self.ages = {}

        self.max_age = max_cache_age

    def get_definition(self, word, allow_cache=True):
        """
        Gets the definition
        :param word: str
        :param allow_cache: bool
        :return: Definition object
        """
        # Return from cache if valid
        if allow_cache and (str(word) in self.cache.keys()):
            if (time.time() - self.ages.get(str(word))) < self.max_age:

                log.info("Using cache for '{}'".format(str(word)))
                return self.cache.get(str(word))

        log.info("Requesting definition for '{}'".format(word))

        word = str(word)
        encoded = SEARCH_URL.format(url_encode(word))

        html = urllib.request.urlopen(encoded)
        bs_html = BeautifulSoup(html, "html.parser").find("div", {"class": "list-group results"})

        try:
            keyword = bs_html.find("span", {"class": "font_xlarge"}).text
        except AttributeError:
            # Return None as the word cannot be found
            return None

        attributes = bs_html.find("span", {"data-group": "header"}).text

        # Find out if there are multiple definitions
        try:
            sub = bs_html.find("ol", {"class": "manual"}).find_all("li")
            only_one = False
        except AttributeError:
            sub = None
            only_one = True

        if not only_one:
            # Multiple definitions
            definitions = [parse_encoding(a).capitalize() for a in [remove_num(a.text) for a in sub]]

            # Last item also includes terminology and slang so we filter it
            last_definition = definitions.pop().split("●")
            # Then we add the last definition back
            definitions.append(last_definition[0])

            # And define terminology and slang
            terminology = last_definition[1].split("♦")[0]
            slang = last_definition[1].split("♦")[1]

        else:
            # This word has only one definition
            paragraph = str(bs_html.find("div", {"class": "list-group-item entry"})
                            .text[len(keyword + attributes):]).replace(attributes, "")

            # Figure out all types of definitions
            if len(paragraph.split("●")) == 1:
                slang = None

                if len(paragraph.split("♦")) == 1:
                    terminology = None
                    definitions = [str(paragraph)]

                else:
                    terminology = paragraph.split("♦")[1]
                    definitions = [paragraph.split("♦")[0]]

            else:
                definitions = [paragraph.split("●")[0]]

                if len(paragraph.split("♦")) == 1:
                    terminology = None
                    slang = paragraph.split("●")[1]

                else:
                    terminology = paragraph.split("♦")[1]
                    slang = paragraph.split("●")[1].split("♦")[0]
            # Uf.
            definitions = [parse_encoding(a) for a in definitions]

            # print(paragraph)

        # Create object and remember time
        timestamp = time.time()
        obj = Definition(
            word=word,
            keyword=keyword,
            attributes=attributes,
            summary=clean(definitions[0]),
            definitions=[clean(d) for d in definitions],
            terminology=clean(terminology),
            slang=clean(slang),
            html=html,
            timestamp=timestamp
        )

        # Store in cache if allowed
        if allow_cache:
            self.cache[str(word)] = obj
            self.ages[str(word)] = timestamp

        return obj

    @staticmethod
    def _set_max_definition_limit(limit):
        """
        Sets MAX_DEFINITIONS to the specified limit.
        :param limit: int
        :return: None
        """
        global MAX_DEFINITIONS
        MAX_DEFINITIONS = int(limit)

# Tests


class SSKJTest(unittest.TestCase):
    def test_dictionary(self):
        self.assertIsNotNone(SSKJParser().get_definition("test"))

    def test_max_definition_limit(self):
        SSKJParser()._set_max_definition_limit(55)
        self.assertEqual(MAX_DEFINITIONS, 55)


# logging.basicConfig(level=logging.INFO)
# parser = SSKJParser()
# while True:
#     inn = input(">")
#     de = parser.get_definition(inn)
#
#     for k, v in de.__dict__.items():
#         print("{}:{}".format(k, v))
#