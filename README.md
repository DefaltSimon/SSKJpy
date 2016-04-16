#### SSKJpy
A Slovenian dictionary API written in python

Uses [SSKJ](http://bos.zrc-sazu.si/sskj.html) website.

1. Installing
You can install it with pip:  
```pip install SSKJpy```  

2. Use and simple examples:
```
sskj = SskjParser("test")
```  
```
summary = sskj.shortsum()  
"postopek za ugotavljanje določenih lastnosti, sposobnosti, znanja koga, preizkus"  `
  ```  
  ```
result = sskj.result()  
`tést  -a m (ẹ̑) 1. postopek za ugotavljanje določenih lastnosti, sposobnosti, znanja koga, preizkus: opraviti
test...
```

#####Full documentation can be found on the [wiki](https://github.com/DefaltSimon/SSKJpy/wiki)
