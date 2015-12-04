# SenryuGenerator

### How to use
  Clone this repository and install dependencies.
```
$ python setup.py install
```
  
  Replace your yahoo application ID with default one in ``make_morph_db.py``.
```python
# Yahoo! Developer Network Application ID
appid = ''
```
  
  Set your text equaled to the variable sentence in the same file.  
```python
sentence = '''
  
'''
```
  
  Then your can generate word data base(morph.db) and senryu from your text by following command :
```
$ python make_morph_db.py
$ python make_random.py
```
