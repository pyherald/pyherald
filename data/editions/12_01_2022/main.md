## HTMX: How Python Fueled the Rise of a JS Lib

_[src](https://www.reddit.com/r/django/comments/rxjlc6/comment/hrimfuf/?utm_source=share&utm_medium=web2x&context=3), For a leaner future_


Hi there, I'm the creator of htmx.

I think htmx managed to catch a wave of discontent with existing javascript frameworks that are very complicated and often turn Django into a dumb-JSON producer. htmx plays better with Django out of the box because it interacts with the server via HTML, which Django is very, very good at producing, so it lets Django developers stay in Django & Python, rather than kicking out to Javascript for 50+% of their web applications.

I was invited on a few Django/Python podcasts and it kind of took off from there:

[https://djangochat.com/episodes/htmx-carson-gross](https://djangochat.com/episodes/htmx-carson-gross)

[https://talkpython.fm/episodes/show/321/htmx-clean-dynamic-html-pages](https://talkpython.fm/episodes/show/321/htmx-clean-dynamic-html-pages)

What's funny is that htmx is really intercooler.js 2.0, which I started working on back in 2013. In 2020, I rewrote intercooler.js without the jQuery dependency and renamed it to htmx, which I think better captures the idea (extending HTML). So this is another example of a decade-long overnight success :)

I'm very surprised and very glad that the Django community has embraced it as quickly and dramatically as they have!

---

## Normalisation In Distribution Filenames: Yet Another Packaging Vagary

_[src](https://discuss.python.org/t/revisiting-distribution-name-normalization/12348/3?u=abdur-rahmaanj), Post by C.A.M. Gerlach, Spyder core developer_

Just sharing my own personal experience as a Python package user, developer and maintainer in both the PyPI and conda ecosystems, consistent display of a package’s display name vs. its normalized name is certainly important.

However, particularly in the large scientific Python community where both users and package authors are typically less well versed in the details of Python packaging but require large and diverse dependency stacks across different package managers to do their work, package names not following a consistent, standardized convention has posed no end of practical problems, well beyond mere aesthetics. I’ve lost count of the number of times colleagues (and myself) have wasted time and effort over trying to remember whether the import, PyPI package or Conda package name did or didn’t contain a `_`, `-` or `.`, or was UpperCamelCase or lowercase (since each can be different).

Within the Conda ecosystem, names are generally normalized to lowercase, no dot, `-` as separators (though for common cases, auto-gendered metapackages exist as aliases for `_` vs `-`), same as Linux and other package managers and I’ve found it to be much easier and more consistent to recall package names than on PyPI. And in many cases, (e.g. QtPy, a top-200 PyPI download package I maintain that sees heavy use on conda as well) the normalized name (qtpy) is actually the import name, not the project name in the metadata (QtPy) that someone long-forgotten set nearly a decade ago, when packaging conventions and knowledge were not as established as they are now.

Certainly, I don’t suggest requiring existing projects change or normalize their names, but at least as both a package user and author, normalizing user-provided names more aggressively on input, rather than less, to reduce the chance of package name confusion over aesthetic differences and the amount that users need to recall and worry about such things, is preferable to always having the display name aesthetically match whatever I (or the original author, who’s long since moved on) typed into the name field many years ago (though of course, tools still can and should display that name to users).

To add, as a package user, I’d rather work with a package with a consistent name following standard conventions that was easy to remember, than one with oddball aesthetics. As a package author, I’d much rather minimize the frustration and maximize the ease at which users install and update my package than impose particular aesthetic sensibilities, and there being an established standard to follow is much preferable to having to Google and bikeshed over how I should capitalize and punctuate the name that I will be stuck with. In fact, more normalization rather than less actually would, if anything give me more confidence rather than less if I really did want to use less conventional punctuation or capitalization, as I would be more confident that users would still find my package and not one benignly or maliciously similar.

Finally, the risk of dependency confusion, typosquatting and infrastructure attacks are not merely theoretical, it has already caused major trouble for npm, there have been attacks on PyPI and it is only likely to increase. In my view, opening the door to a whole new class of such attacks, never mind a greatly increased chance of benign developer confusion and wasted effort, is simply not worth it for a small amount of additional “creativity” (or as many would see it, the lack of a consistent convention) in package naming.


Note: Gerlach, besides being a Spyder core developer is also an atmospheric scientist, Project Mjolnir remote sensor framework creator, Ph.D student, technical writer. Currently leading a NASA-funded effort to develop a deep-learning based groundside data processing and analysis system for the GLM instrument on the GOES-R-series weather satellites.

---

## Solving Local File Overshadowing Library Name

_[src](https://mail.python.org/archives/list/python-ideas@python.org/thread/UUVVJJRGZI23D64H43URWCEFGWPI27DS/), Issue raised by Florian Wetschoreck_


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

---

## What's Happening in PythonLand?

_[src](---), Guided tour_

Toml hopes to [find it's way](https://www.python.org/dev/peps/pep-0680/) in the standard library with PEP680, it has the wind at it's back. 

PEP669 for low impact monitoring is [still looking](https://discuss.python.org/t/pep-669-low-impact-monitoring-for-cpython/13018) for some last comments.

[PEP679](https://discuss.python.org/t/pep-679-allow-parentheses-in-assert-statements/13003) for allowing parentheses in assert statements seems a favourable addition with concerns about backward compatibility and notes on non-usefulness.


The [Pyston](https://github.com/pyston/pyston) project [requests](https://discuss.python.org/t/pep425-python-tag-for-pyston/13039) a [PEP425](https://www.python.org/dev/peps/pep-0425/) Python Tag after ongoing work adding it to manylinux.



PEP639 -- Improving License Clarity with Better Package Metadata is at [round 2](https://discuss.python.org/t/pep-639-round-2-improving-license-clarity-with-better-package-metadata/12622)

---

