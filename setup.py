# coding=utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# with open("README.md") as rdm:
#     long_desc = rdm.read()


setup(
    name='sskjpy',
    author="DefaltSimon",
    version='0.2.1',
    license='MIT',

    packages=["sskjpy"],

    description="A Slovenian dictionary parser written in python",
    # long_description=long_desc,

    install_requires=[
        "beautifulsoup4 >= 4.4.1",
    ],
    extras_require={
        "requests": ["requests >= 2.9.1"],
    }
)
