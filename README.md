## SSKJpy
A Slovenian dictionary API written in python

Uses [sskj.si](http://sskj.si).
---
###1. Installing  
You can install it with pip:  
`pip install git+https://github.com/DefaltSimon/SSKJpy.git`  


Or clone the repo and run:  
  `python setup.py install`  

###2. Use and simple examples:
```
sskj = SskjParser()

data = sskj.get_definition("test")  

data.word
"test"
data.summary
"Postopek za ugotavljanje določenih lastnosti, [...]"
```

####Full documentation can be found on the [wiki](https://github.com/DefaltSimon/SSKJpy/wiki) (not yet updated for the new version)
