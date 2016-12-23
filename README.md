## SSKJpy
A Slovenian dictionary API written in python
![Python 3.5](https://img.shields.io/badge/python-3.2%2C%203.3%2C%203.4%2C%203.5-blue.svg)
![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)

Uses [sskj.si](http://sskj.si).
---
###1. Installing
In order to run it you need [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), which is available from pypi.


You can install SSKJpy with pip:
`pip install git+https://github.com/DefaltSimon/SSKJpy.git`
Strongly recommended: install with requests module:
`pip install git+https://github.com/DefaltSimon/SSKJpy.git[requests]`


Or clone the repo and run:
  `python -m pip install .` (or `python -m pip install .[requests]` to get the "faster" implementation)  

###2. Use and simple examples:
```
sskj = SSKJParser()

data = sskj.get_definition("test")

data.keyword
"test"
data.summary
"Postopek za ugotavljanje določenih lastnosti, [...]"
```

####Full documentation can be found on the [wiki](https://github.com/DefaltSimon/SSKJpy/wiki)
