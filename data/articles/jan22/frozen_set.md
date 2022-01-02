title: Frozenset Can Be Altered by |=
authors: marco_sulla
note: Mail by  Marco Sulla
source: https://mail.python.org/pipermail/python-list/2021-November/904379.html
tags: frozen_set
slug: ---


```
(venv_3_10) marco at buzz:~$ python
Python 3.10.0 (heads/3.10-dirty:f6e8b80d20, Nov 18 2021, 19:16:18)
[GCC 10.1.1 20200718] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> a = frozenset((3, 4))
>>> a
frozenset({3, 4})
>>> a |= {5,}
>>> a
frozenset({3, 4, 5})
```

--Marco