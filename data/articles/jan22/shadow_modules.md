title: Solving Local File Overshadowing Library Name
authors: arj
note: Issue raised by Florian Wetschoreck
source: https://mail.python.org/archives/list/python-ideas@python.org/thread/UUVVJJRGZI23D64H43URWCEFGWPI27DS/
tags: imports
slug: ---


Many of us have had the error of having a local file name 'over-shadowing' a library name. In the case we have

```
|_ main.py
|_ random.py
```

If in main.py we write


```python
from random import shuffle
```

Python will complain

```
    from random import shuffle
ImportError: cannot import name 'shuffle' from 'random' (/path/to/random.py)
```


If we instead alias the import


```python
import random as rn

print(rn.shuffle())
```

Python now complains that:

```
    print(rn.shuffle())
AttributeError: module 'random' has no attribute 'shuffle'
```

But, instead of as in the first example, we don't have an idea of what's wrong exactly. 

Florian proposed changing the resolution order of imports which is a breaking change, with far-reaching consequences. Chris Angelico proposed turning the scripts directory into an automatic package to make the following work

```
# demo.py
print("Hello, world")

# example.py
from . import demo
```

Ethan Furman proposed including the whole path to the module being imported. Chris Angelico noted that it indeed is already happening on a from-import error. Ricky Teachy floated the idea that on error, show the module waiting to be imported if any, which requires some lookup.

Ethan's suggestion seems straight to the point and in line with the import error as it's already being flagged as an import attribute error. I am a bit curious that the thread is kind of forgotten.

-- by [Abdur-Rahmaan Janhangeer](https://twitter.com/osdotsystem)