title: Why Remove Deprecated Functions
authors: victor_stinner
note: Mail by Victor Stinner
source: https://mail.python.org/archives/list/python-dev@python.org/message/TYHN7S3BEW7E3LAGAESZFYHPVP5MRI42/
tags: deprecated
slug: ---


For me, deprecated functions cause me a lot of thinking when I met
them as a Python maintainer and as a Python user. Why is it still
there? What is its purpose? Is there a better alternative? It's
related to the Chesterton's fence principle. Sometimes, reading the
doc is enough. Sometimes, I have to dig into the bug tracker and the
Git history.

In Python, usually, there is a better alternative. A recent example is
the asyncore module that I'm proposing to remove. This module has
multiple design flaws which cause bugs in corner cases. It's somehow
dangerous to use this module. Deprecating the module doesn't help
users who continue to use it and may get bugs in production. Removing
the module forces user to think about why they chose asyncore and if
they can switch to a better alternative. It's supposed to help users
to avoid bugs.

The gray area is more about "deprecated aliases" and having two ways
to do the same things, but one way is deprecated. One example is the
removal of collections.MutableMapping: you must now use
collections.abc.MutableMapping. Another example is the removal the "U"
mode in the open() function: the flag was simply ignored since Python
3.0. So far, the trend is to remove these "aliases" and force users to
upgrade this code. Not removing these aliases has been discussed, and
it seems like each time, it was decided to remove them. Usually, the
"old way" is deprecated for many Python versions, like 5 years if not
longer.

Using deprecated functions is a threat in terms of technical debt. An
application using multiple deprecated functions will break with a
future Python version. It's safe to avoid deprecated functions
whenever possible. Some deprecated functions have been removed but
then restored for 1 or 2 more Python releases, to give more time to
users to upgrade their code. At the end, the deprecated code is
removed.

We can warn developers to pay attention to DeprecationWarning
warnings, but sadly, in my experience, the removal is the only trigger
which works for everybody.

Do you have to repeat "You should check for DeprecationWarning in your
code" in every "What's New in Python X.Y?" document? Python 3.9 has
such section:
[https://docs.python.org/dev/whatsnew/3.9.html#you-should-check-for-deprecationwarning-in-your-code](https://docs.python.org/dev/whatsnew/3.9.html#you-should-check-for-deprecationwarning-in-your-code)

Victor