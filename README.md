#### SSKJpy
A Slovenian dictionary API written in python

Uses [SSKJ](http://bos.zrc-sazu.si/sskj.html) website.

1. Installing
You can install it with pip:  
`pip install git+https://github.com/DefaltSimon/SSKJpy.git`


2. Use and simple examples:
```
sskj = SskjParser()

data = sskj.get_definition("test")  

data.word
"test"
data.summary
"Postopek za ugotavljanje določenih lastnosti, [...]"
```

#####Full documentation can be found on the [wiki](https://github.com/DefaltSimon/SSKJpy/wiki) (not yet updated for the new version)
