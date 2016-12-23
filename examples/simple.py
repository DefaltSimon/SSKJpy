# coding=utf-8
from sskjpy import sskj
import logging


logging.basicConfig(level=logging.INFO)
parser = sskj.SSKJParser()

while True:
    inn = input(">")
    de = parser.get_definition(inn)

    keys = de.__slots__
    values = {}
    for key in keys:
        values[key] = getattr(de, key)

    for k, v in values.items():
        print("{}:{}".format(k, v))
