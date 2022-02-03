title: C API: The ABI Masterplan
authors: victor_stinner
note: Mail by Victor Stinner
source: https://mail.python.org/archives/list/python-dev@python.org/thread/DN6JAK62ZXZUXQK4MTGYOFEC67XFQYI5/
tags: c-api, abi
slug: ---


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