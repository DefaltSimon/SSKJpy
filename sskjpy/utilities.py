# coding=utf-8


BASE_ENDPOINT = "http://sskj.si/?s={}"

MAX_DEFINITIONS = 50
MAX_CACHE_AGE = 43200


class SpecialChars:
    TERMINOLOGY = u"\u25CF"
    SLANG = u"\u2666"

REPLACEMENTS = {
    # no-break space replacement with normal space
    "\xa0": " "
}


def remove_num(d):
    for n in range(1, MAX_DEFINITIONS):
        if str(d).startswith(str(n) + "."):
            return str(d).strip(str(n) + ".")


def parse_encoding(data):
    for target, replacement in REPLACEMENTS.items():
        data = str(data).replace(target, replacement)

    return data

strip_chars = [
    " ", "\n", "\t",
]


def clean(data):
    data = str(data)
    for char in strip_chars:
        data = data.strip(char)

    return data
