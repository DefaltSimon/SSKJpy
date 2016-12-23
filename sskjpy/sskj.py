# coding=utf-8
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote as url_encode

# Module imports
from sskjpy.utilities import BASE_ENDPOINT, MAX_DEFINITIONS, MAX_CACHE_AGE, parse_encoding, remove_num, clean, SpecialChars as Sc
from sskjpy.connector import Connector
from sskjpy.errors import NotFound


# Logging setup
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Definition(object):
    """
    Definition of a word
    """
    __slots__ = (
        "base_word", "keyword", "summary",
        "definitions", "definition",
        "attributes", "terminology",
        "slang", "_timestamp"
    )

    def __init__(self, **kwargs):
        # The term you searched for
        self.base_word = kwargs.get("base_word")
        # The closest word
        self.keyword = kwargs.get("keyword")

        # Summary is the first definitions
        self.summary = kwargs.get("summary")
        # A list of definitions
        self.definitions = kwargs.get("definitions")
        self.definition = self.definitions[0]

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

    def __init__(self, max_cache_age: int=MAX_CACHE_AGE, max_definitions: int=MAX_DEFINITIONS):
        self.cache = {}
        self.def_ages = {}

        self.max_age = max_cache_age
        self.MAX_DEFINITIONS = int(max_definitions)

        self.req = Connector.find_best()

    def _in_cache(self, keyword) -> bool:
        return str(keyword) in self.cache.keys()

    def _cache_age(self, word: str) -> float or None:
        if self.def_ages.get(str(word)):
            return time.time() - self.def_ages.get(str(word))
        else:
            return None

    def get_definition(self, word: str, allow_cache: bool=True, store_in_cache: bool=True) -> Definition or None:
        """
        Gets the definition of some word from SSKJ.

        :param word: The keyword to search for
        :type word: str
        :param allow_cache: Indicates if you want to check the cache for already-fetched definitions
        :type allow_cache: bool
        :param store_in_cache: Indicates if you want to save the definition in the cache after getting it

        :return: Definition object
        """
        word = str(word)

        # Return from cache if valid
        if allow_cache and self._in_cache(word):
            if self._cache_age(word) < self.max_age:

                log.debug("Using cache for '{}'".format(word))
                return self.cache.get(word)

        log.debug("Requesting definition for '{}'".format(word))
        encoded = BASE_ENDPOINT.format(url_encode(word))

        html = self.req.get(encoded)
        bs_html = BeautifulSoup(html, "html.parser").find("div", {"class": "list-group results"})

        try:
            keyword = bs_html.find("span", {"class": "font_xlarge"}).text
        except AttributeError:
            # Return None as the word cannot be found
            raise NotFound("no result: {}".format(word))

        attributes = bs_html.find("span", {"data-group": "header"}).text

        # Find out if there are multiple definitions
        try:
            sub = bs_html.find("ol", {"class": "manual"}).find_all("li")
        except AttributeError:
            sub = None

        if sub:
            # Multiple definitions
            definitions = [parse_encoding(a).capitalize() for a in [remove_num(a.text) for a in sub]]

            # Last item also includes terminology and slang so we filter it
            last_definition = definitions.pop().split("●")
            definitions.append(last_definition[0])

            # And define terminology and slang
            terminology = last_definition[1].split("♦")[0]
            slang = last_definition[1].split("♦")[1]

        else:
            # Only one definition
            paragraph = str(bs_html.find("div", {"class": "list-group-item entry"})
                            .text[len(keyword + attributes):]).replace(attributes, "")

            if len(paragraph.split(Sc.SLANG)) == 1:
                slang = None

                if len(paragraph.split(Sc.TERMINOLOGY)) == 1:
                    terminology = None
                    definitions = [str(paragraph)]

                else:
                    terminology = paragraph.split(Sc.TERMINOLOGY)[1]
                    definitions = [paragraph.split(Sc.TERMINOLOGY)[0]]

            else:
                definitions = [paragraph.split(Sc.SLANG)[0]]

                if len(paragraph.split(Sc.TERMINOLOGY)) == 1:
                    terminology = None
                    slang = paragraph.split(Sc.SLANG)[1]

                else:
                    terminology = paragraph.split(Sc.TERMINOLOGY)[1]
                    slang = paragraph.split(Sc.SLANG)[1].split(Sc.TERMINOLOGY)[0]

            definitions = [parse_encoding(a) for a in definitions]

        # Create the Definition object
        timestamp = time.time()
        obj = Definition(
            base_word=word,
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
        if store_in_cache:
            self.cache[str(word)] = obj
            self.def_ages[str(word)] = timestamp

        return obj

    def _set_max_definition_limit(self, limit: int) -> None:
        """
        Sets SSKJParser.MAX_DEFINITIONS to the specified limit.

        :param limit: How long the cache should be valid for.
        :type limit: int
        :return: None
        """
        self.MAX_DEFINITIONS = int(limit)
