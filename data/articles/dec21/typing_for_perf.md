title: Instagram: Type Hints for Compiler Optimisation
authors: carl_meyer
note: Mail by Carl Meyer
source: https://mail.python.org/archives/list/python-ideas@python.org/message/ZM22AKAFIQDHF2E7VPHQ2DZJNBXPTRFM/
tags: typing
slug: ---


I think there's an important distinction to be made between "enforcing
types" as in "type annotations that are present are checked for
consistency at compile time and enforced at runtime, instead of only
being checked by a linter and possibly totally wrong at runtime" vs
"enforcing types" as in "everything must always be fully typed." It
seems that you are proposing both together, and so far readers are
mostly reacting against the second. But I would like to observe that
the one does not have to imply the other.

I think requiring types everywhere is pretty much a non-starter for
the Python language and community; the resulting language would no
longer be Python, it would be a very different language with Python's
syntax.

But I think integrating optional types more closely into the language,
so that users can trust that the type annotations that are present are
not well-intentioned lies, and the compiler can make use of them to
optimize some operations, increases the value of type annotations and
the experience of using them, and can still fully allow for untyped
and partially-typed code in the places where static types don't make
sense (because the code is highly dynamic or because its just a quick
script or prototype.)

I currently work on a project we call "Static Python" (not a great
name, since really it's fully dynamic Python with optional static
types) which does exactly this. Types remain fully optional, the type
system is gradual, but where you do specify annotations of types that
are built-ins or are defined in modules opted into the Static Python
compiler, you get compile-time type checking and runtime checks that
the values used match the annotated types. This is currently only
available if you use the fork of CPython in which we develop it [1].
We hope that at some point it may be possible to instead make it
available as a pip-installable extension to normal CPython, but this
is probably a long ways out yet. We are building this primarily for
the performance benefits. The benefit of being able to use statically
known and trusted type information to elide some costly dynamic
operations more than makes up for the cost of the added runtime type
checks, partly because our compiler is able to intelligently elide
those runtime type checks in static-to-static calls, only checking
when values first are passed in from untyped sources.

This is early experimental work, and very far from anything that might
be considered for mainstream CPython, but if you're interested in this
area, you might find it worth taking a look at this early stage!

Carl

[1] [https://github.com/facebookincubator/cinder](https://github.com/facebookincubator/cinder)