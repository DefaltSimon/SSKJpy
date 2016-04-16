#### SSKJpy
A Slovenian dictionary parser written in python

Uses [SSKJ](http://bos.zrc-sazu.si/sskj.html) website.

1. Use and simple examples:
```
import sskj
```  
```
sskj = SskjParser("test")
```
```
summary = sskj.shortsum()  
```
Returns `"postopek za ugotavljanje določenih lastnosti, sposobnosti, znanja koga, preizkus"  `
  ```
result = sskj.result()  
```
Returns `tést  -a m (ẹ̑) 1. postopek za ugotavljanje določenih lastnosti, sposobnosti, znanja koga, preizkus: opraviti test...`

More things will be documented when I make the wiki.