## Why No C++ For The CPython Codebase

_[src](https://mail.python.org/archives/list/python-dev@python.org/thread/32XOK67BGMEX2UIYVVXMHOUME56O3GJ7/), Discussion started by redradist_



Redradist brought up one more time the issue of rewriting the CPython codebase in C++. He evoked readability, maintainability and RAII - predictable allocation and freeing of resources. 

Using C++ raises the issue of binary compatibility. If there is no binary compatibility, you can't link object files, static libraries, dynamic libraries, and executables built by different versions of compiler toolsets [1]. A core dev who is always known to support the idea of a C++ transition stated that if we are not exposing C++ bits in the public API, it does not matter. While it does sound non-intuitive, he explained that C++ templates could improve the maintainability of the generic "stringlib" routines currently based on C macros. Another example is using RAII in function bodies to help clean up owned references. For cleanup, it was suggested that C has better ways, referencing GCC's `__attribute__(cleanup(cleanup_function))`. But it seems that RII is also about moving resources, made possible by  C++'s `std::move`. Using C++ internally assumes we will have to link with libstdc++ and use C++ compatible linkers. If these tools are of high quality, there should be no worry. Another solution for binary compatibility is just to enable compilation with popular compilers.

As C++ has much more features than pure C, it seems more daunting and complex to write. It is feared that this might reduce the number of contributors. But on the other hand, if the code is more understandable and maintainable, it might attract more people. It was noted that a large part of CPython is actually Python code. So, people can still contribute without worrying of C/C++.

People requested a clear proposal, something solid enough to move the dossier forward or not. It is not a simple matter as it will require lots of effort and volunteer time to effect the change, write tests, deal with 'deep' bugs. We don't know whether or not it will enlarge the family of core devs. In short it's time for a PEP to demonstrate examples of the maintainability of C++, metrics of users willing to contribute to the C++ version, and support for all platforms currently supported. There is also the extentions API to deal with.

A core dev noted that C build times seem to be better. But it was brushed off as 'using C++ one or two times'. If people want rich data structures, they can use Python instead of hammering on C's poor support, but it was not a good line of thought as the backend was crucial for performance. The solution lies not in using Python. The organisation of the codebase was described as a maze and the incoherence of the C API was blamed on it. C++ would solve the problem it seems. 

Two more ideas worth exploring is using Cython with the C API and using rust for memory safety. But then rust is yet another language in terms of familiarity. Something C++ enjoys.  There are also concerns about rust's target architectures. 

Gregory Smith reflected that after years of experience with huge C++ codebases, he did not find readability or maintainability advantages. RAII is something he wishes to have though. The CPython codebase drafted tests to check leaks over the years. RAII he says is not a magic pill and can be wrongly used.




[1] https://docs.microsoft.com/en-us/cpp/porting/binary-compat-2015-2017?view=msvc-170

---

## What's New In Django Security Releases

_[src](https://twitter.com/AdamChainz/status/1488622545289060357?s=20&t=LhdIkz7aKdMcV9BTovEwfA), By Adam Johnson_

1 🔒 The `{% debug %}` tag was found to be an XSS vector, since it didn't escape variables. I don't recall seeing anyone use the tag, so you're probably safe... But it still could easily be in a template somewhere!

Thanks to @kezabelle, @m_holtermann and @MariuszFelisiak

2 🔒 Files uploaded using 'Content-Transfer-Encoding: baes64' but not enough data could cause an infinite loop. This is a bad DoS vector!

Thanks to Alan Ryan and @MariuszFelisiak

3 🧪 TestCase.captureOnCommitCallbacks() didn't handle recursive callbacks correctly.

Thanks to Petter Friberg for the report and PR, and @MariuszFelisiak for review. I backported the fix to my Django <4.0 package: https://pypi.org/project/django-capture-on-commit-callbacks/

4 ...and a bunch of other small regressions in Django 4.0. I guess a bunch have been discovered as folks upgrade and start to use new features.

I discovered one on friday [for QuerySet.aggregate()], which 
@MariuszFelisiak fixed real quick in time for the release Clapping hands sign


-- Adam Johnson, [@AdamChainz](https://twitter.com/AdamChainz)

---

## David Beazley: When I Was A Nobody

_[src](https://twitter.com/dabeaz/status/1489198730955960332?s=20&t=LhdIkz7aKdMcV9BTovEwfA), When big names don't shine always_


> I tell this story a lot as to why I choose not to work at Google. When I was an undergraduate and went to GHC, I gave a recruiter my CV and asked how I can do R&D there one day. She said "We don't hire from State Unis" and tossed my CV in the bin. In front of me. -- Dr Heidy Khlaaf (هايدي خلاف)


I went to a state university and apropos of nothing, <mark>the most disrespect I've ever received in my entire career was while giving a talk at Stanford</mark>.  

"I'm don't really have a question about your talk, but who the fuck are you?"

Not only was I unqualified to walk the sacred fucking grounds of Stanford, my talk was too stupid to even merit listening to.  They suddenly cut me off and everyone left before I finished.

This was c/1997. I was talking about Python+Scientific Computing. Touché motherf\*ckers.

To be fair, the topic was kinda stupid. I mean, I gave a talk on the same topic to a room of 500 empty chairs at the Supercomputing conference the year before. Bah! Python.

Also, <mark>the \*only\* time I have ever received disrespect while teaching a training course was at Google</mark>.  Kinda the same attitude to be honest.


---

Q: Really curious about the standing of that person that was rude to you in the python or scientific computing communities these days

I was a PhD student at that time. A nobody. Got the same respect as the restaurant wait staff I'd be

Q: ugh i am sorry.  i am not nearly as accomplished, or as ahead of the cutting edge as you were when you gave your presentation (holy moly). but my experience was the similar. the disrespect and arrogance i saw on day 1's interviews almost drove me to skip day 2.

I can't even imagine interviewing there. I was just talking. Not part of anything else. My advisor thought it would be good to network I think. Uh, sure.


-- David Beazley [@dabeaz](https://twitter.com/dabeaz)


---

## PyPy on PySide6 is there: PyPy with a Gui

_[src](https://mail.python.org/archives/list/python-dev@python.org/thread/32XOK67BGMEX2UIYVVXMHOUME56O3GJ7/), Mail by Christian Tismer_

Since May 2021 I have been working at running PyPy on PySide6,
which was a difficult undertaking, since PyPy internally is quite
a bit different.

I declared the project to be ready-to-use when the Mandelbrot
example of the PySide examples
	
	(examples/corelib/threads/mandelbrot.py)
is working.

This was finally solved this week on 2022-02-01, so we have the

    first advanced Gui working with PyPy

and with the amazing result of speed:

PyPy 3.8 works
     
    10 times faster than the identical code on Python 3.10
and
    
    5.5 times slower than the same example in C++ Qt.

I think to send an official announce when this is available on pip.

This effort marks the completion of my PyPy support, which began
in 2003 and ended involuntarily in 2006 due to a stroke.

All the best 


-- Christian Tismer

Note: Tismer is the creator of Stackless Python and maintainer of PySide

---

## C API: The ABI Masterplan

_[src](https://mail.python.org/archives/list/python-dev@python.org/thread/DN6JAK62ZXZUXQK4MTGYOFEC67XFQYI5/), Mail by Victor Stinner_


Hi,

There is a reason why I'm bothering C extensions maintainers and
Python core developers with my incompatible C API changes since Python
3.8. Let me share my plan with you :-)


In 2009 (Python 3.2), Martin v. Löwis did an amazing job with the PEP
384 "Defining a Stable ABI" to provide a "limited C API" and a "stable
ABI" for C extensions: build an extension once, use it on multiple
Python versions. Some projects like PyQt5 and cryptograpy use it, but
it is just a drop in the PyPI ocean (353,084 projects). I'm trying to
bend the "default" C API towards this "limited C API" to make it
possible tomorrow to build *more* C extensions for the stable ABI.

My goal is that the stable ABI would be the default, and only a
minority of C extensions would opt-out because they need to access to
more functions for best performance.

The basic problem is that at the ABI level, C extensions must only
call functions, rather than getting and setting directly to structure
members. Structures changes frequently in Python (look at changes
between Python 3.2 and Python 3.11), and any minor structure change
breaks the ABI. The limited C API hides structures and only use
function calls to solve this problem.


Since 2020, I'm modifying the C API, one function by one, to slowly
hide implementations (prepare the API to make strutures opaque). I
focused on the following structures:

* PyObject and PyVarObject (bpo-39573)
* PyTypeObject (bpo-40170)
* PyFrameObject (bpo-40421)
* PyThreadState (bpo-39947)

The majority of C extensions use functions and macros, they don't
access directly structure members. There are a few members which are
sometimes accessed directly which prevents making these structures
opaque. For example, some old C extensions use obj->ob_type rather
than Py_TYPE(obj). Fixing the minority of C extensions should benefit
to the majority which may become compatible with the stable ABI.

I am also converting macros to static inline functions to fix their
API: define parameter types, result type and avoid surprising macros
side effects ("macro pitfalls"). I wrote the PEP 670 "Convert macros
to functions in the Python C API" for these changes.


I wrote the upgrade_pythoncapi.py tool in my pythoncapi_project (\*)
which modify C code to use `Py_TYPE()`, `Py_SIZE()` and `Py_REFCNT()` rather
than accessing directly PyObject and PyVarObject members.

(\*) [https://github.com/pythoncapi/pythoncapi_compat](https://github.com/pythoncapi/pythoncapi_compat)

In this tool, I also added "Borrow" variant of functions like
`PyFrame_GetCode()` which returns a strong reference, to replace
`frame->f_code` with `_PyFrame_GetCodeBorrow()`. In Python 3.11, you
cannot use the `frame->f_code` member anymore, since it has been
removed! You must call `PyFrame_GetCode()` (or `pythoncapi_compat
_PyFrame_GetCodeBorrow()` variant).


There are also a few macros which can be used as l-values like
`Py_TYPE()`: `"Py_TYPE(type1) = type2"` must now be written
`"Py_SET_TYPE(type1, type2)"` to avoid setting directly the tp_type type
at the ABI level. I proposed the PEP 674 "Disallow using `Py_TYPE()` and
`Py_SIZE()` macros as l-values" to solve these issues.


Currently, many "functions" are still implemented as macros or static
inline functions, so C extensions still access structure members at
the ABI level for best Python performance. Converting these to regular
functions has an impact on performance and I would prefer to first
write a PEP giving the rationale for that.


Today, it is not possible yet to build numpy for the stable ABI. The
gap is just too large for this big C extension. But step by step, the
C API becomes closer to the limited API, and more and more code is
ready to be built for the stable ABI.


Well, these C API changes have other advantages, like preparing Python
for further optimizations, ease Python maintenance, clarify the
seperation between the limited C API and the default C API, etc. ;-)

-- Victor

---

## What's Happening in PythonLand

PEP 668 -Graceful cooperation between external and Python package managers is [being proposed](https://discuss.python.org/t/graceful-cooperation-between-external-and-python-package-managers-pep-668/10302) but at the same time it [is suggested](https://discuss.python.org/t/renaming-pep-668/13474) that the name be changed for being too vague.


Tomáš Hrnčiar, Red Hat engineer submits [his report](https://discuss.python.org/t/experience-with-python-3-11-in-fedora/12911) of Python 3.11 on Fedora


The community [needs help](https://discuss.python.org/t/community-testing-of-packaging-tools-against-non-warehouse-indexes/13442) testing packages against indexes other than the warehouse. A weird and virtually unknown [PEP 503](https://www.python.org/dev/peps/pep-0503/) was not being followed and disaster ensured.

---

