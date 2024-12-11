## So, Julia is the magic pill?

_[src](https://mail.python.org/pipermail/python-list/2021-December/904690.html), Mail by Oscar Benjamin_


Like others here I don't have any particular advice to offer for the
actual question you have asked. Probably you would get better answers
on a Julia mailing list.


Before you consider rewriting any of your Python code in Julia I
suggest trying it out to see if you can actually demonstrate a proof
of concept that it can even be faster for your particular problem.
Also like others here I suggest that you explore the options for
speeding things up within Python. Putting together a Frankenstein
application that's half in Julia and half in Python might be worth it
but that approach has significant costs so make sure you are clear
that there are going to be benefits before you go down that road.

I do have a very small amount of experience using Julia. As a
maintainer of SymPy I was very interested by Symbolics.jl which was
created in an attempt to be faster than SymPy. I spent some time going
through tutorials for Julia and making toy programs and then I tried
out Symbolics.jl. I also had various discussions with those involved
in Symbolics.jl on Julia mailing lists and GitHub.

Based on my experience with Julia the immediate conclusion I have that
is relevant for you is this:

Do *not* presume that writing your code in Julia rather than Python
will make it faster.

There is a lot of hype about Julia and its proselytisers will claim
that it "runs at the speed of C". That might be sort of true for
certain specific kinds of code or particular kinds of problems but it
is certainly not true in general that Julia runs at the speed of C. In
fact I have seen plenty of basic cases where Julia is slower than
Python.

The other thing that I have seen plenty of in discussions about
performance in both Python and Julia is poor use of benchmark results.
The big culprit is timeit and its equivalent btime in Julia. When I
tried to discuss the speed of operations in Julia it was suggested
that I should use btime but there are so many different levels of
caching in Julia (at least in Symbolics.jl) that the btime results are
meaningless. It seems to be common practice in the Julia community to
refer to btime results just as it is in Python to refer to timeit
results.

I think that there is a specific class of problems where Julia is
significantly faster than (CPython) which in practice is mostly around
intensive non-vectorisable floating point calculations. Note that
these are the same kind of things that can be made a lot faster if you
use PyPy or Numba or any of the related options that can be done
without rewriting your existing Python code in another language. In
Julia just as in PyPy/Numba etc it's important for the speed gain that
you can actually reduce your operations down to low-level machine
types like float64, int32 etc.

I tried writing a matrix multiplication routine in Julia to see how it
would compare with Python. I used a straight-forward dumb
implementation in both languages. I wanted to compare with something
like this which is pure Python:
[https://github.com/sympy/sympy/blob/88ed7abb488da615b007dd2ed5404312caef473c/sympy/polys/matrices/dense.py#L85-L91](https://github.com/sympy/sympy/blob/88ed7abb488da615b007dd2ed5404312caef473c/sympy/polys/matrices/dense.py#L85-L91)
Note that in that particular application it isn't possible to use
something like int32 because it's part of a symbolic library that
performs exact calculations that can easily overflow any standard
machine types e.g. the determinant of a 20x20 matrix of integers
between 0 and 100 easily overflows the range of a 64 bit integer:

    >>> from sympy import *
    >>> det(randMatrix(20, 20))
    1389363438512397826059139369892638115688

When I timed the result in Julia and in Python I found that the Julia
code was slower than the Python code. Of course I don't know how to
optimise Julia code so I asked one of my colleagues who does (and who
likes to proselytise about Julia). He pointed me to here where the
creator of Julia says "BigInts are currently pretty slow in Julia":
[https://stackoverflow.com/questions/37193586/bigints-seem-slow-in-julia#:~:text=BigInts%20are%20currently%20pretty%20slow,that%20basic%20operations%20are%20fast](https://stackoverflow.com/questions/37193586/bigints-seem-slow-in-julia#:~:text=BigInts%20are%20currently%20pretty%20slow,that%20basic%20operations%20are%20fast).
I should make clear here that I used the gmpy2 library in Python for
the basic integer operations which is a wrapper around the same gmp
library that is used by Julia. That means that the basic integer
operations were being done by the same gmp library (a C library) in
each case. The timing differences between Python and Julia are purely
about overhead around usage of the same underlying C library.

The Julia code was 2x slower than Python in this task. By comparison
flint is a library that actually runs at the speed of C (because it's
written in C) is about 100x faster than Python for this particular
operation:
[https://www.flintlib.org/](https://www.flintlib.org/)
Regardless of the explanation by Stefan Karpinski about Python's
optimisations for small integers it is very clear to me that the
"speed of C" claim needs significant qualification.

Here is another demonstration: hello world. Let's compare this between
C, Python and Julia. First C:

```
$ cat hello.c
#include <stdio.h>

int main(int argc, char *argv[])
{
  printf("hello\n");
  return 0;
}
$ gcc hello.c -o hello
$ time ./hello
hello
real 0m0.085s
user 0m0.001s
sys 0m0.003s
$ time ./hello
hello
real 0m0.012s
user 0m0.002s
sys 0m0.004s
```

So with warm file system cache (the second run) we see that it takes
around 10ms to run a hello world on this particular MacBook. If we try
the same for Python it's:

```
$ cat hello.py
print('hello')
$ time python hello.py
hello
real 0m0.050s
user 0m0.031s
sys 0m0.014s
```

Now in Python it takes 50ms for hello world and subsequent runs are
similar. Now in Julia it's:

```
$ cat hello.jl
print("hello")
$ time julia hello.jl
hello
real 0m4.264s
user 0m0.327s
sys 0m1.346s
$ time julia hello.jl
hello
real 0m0.303s
user 0m0.164s
sys 0m0.098s
```

So the first time running Julia it took 4 seconds. The second time 0.3
seconds. That's a lot slower than C and Python. These timings are no
doubt specific to OSX and my hardware to some extent. On my Linux
desktop I can get significantly shorter times for C and Python but not
for Julia (last time I tried, I don't currently have a recent version
of Julia there for testing).

For many applications this start up cost is already a dealbreaker. It
doesn't stop there though as you get the same every time you try to
import something e.g. from the repl:

```
julia> @time using Symbolics
  4.997553 seconds (7.87 M allocations: 563.148 MiB, 2.19% gc time,
16.74% compilation time)
```

Note that this time doesn't get any faster with a warm filesystem. So
if I quit Julia and restart it then "using Symbolics" will still take
5 seconds. I think that the idea is that Julia takes some time to warm
up but then does things very fast so this startup time is amortised in
some way. Clearly though it needs to be a long running process for
this 5 second startup time to become insignificant.

Even then when I try to do things with Symbolics I get more start up
costs. The first time you try to call anything it's really slow. Let's
use solve_for to solve a system of 2 linear equations in 2 unknowns:

```
julia> using Symbolics

julia> @variables x, y
2-element Vector{Num}:
 x
 y

julia> @time Symbolics.solve_for([x + y ~ 1, x - y ~ 0], [x, y])
  4.944882 seconds (8.13 M allocations: 466.870 MiB, 5.71% gc time,
99.90% compilation time)
2-element Vector{Float64}:
 0.5
 0.5

That's definitely not the speed of C but if we rerun that:

julia> @time Symbolics.solve_for([x + y ~ 1, x - y ~ 0], [x, y])
  0.000301 seconds (539 allocations: 22.828 KiB)
2-element Vector{Float64}:
 0.5
 0.5
```

Okay so the second time we call the function it returns in 0.3
milliseconds. Now all of a sudden it starts to look possibly faster
than Python but wait a minute... What happens if I change the
equations? In practice I don't want to solve the exact same equations
over and over again because once I have the answer I don't need to
recompute it. Let's change the number on the right hand side of one of
the equations:

```
julia> @time Symbolics.solve_for([x + y ~ 1, x - y ~ 3], [x, y])
  0.150477 seconds (348.17 k allocations: 17.864 MiB, 99.60% compilation time)
2-element Vector{Float64}:
  2.0
 -1.0
```

Okay so this is a lot slower than when repeatedly solving the exact
same equations. We see now that it takes about 150 milliseconds to
solve a system of 2 equations for 2 unknowns (after around 10 seconds
of startup overhead just to get to this point). That's slow compared
to SymPy which is a pure Python library (note that Symbolics.jl was
created because SymPy was considered too slow by the Julia folks). In
fact, given that it's actually just computing the result in machine
precision floating point, that's slow compared to any language that I
know.

When I asked about this slowness on the Julia mailing lists I was told
that I should be using btime instead of time to measure the time taken
by these functions:

```
julia> using BenchmarkTools

julia> @btime Symbolics.solve_for([x + 3*y ~ 1, x - y ~ 3], [x, y])
  94.245 μs (611 allocations: 25.02 KiB)
2-element Vector{Float64}:
  2.5
 -0.5
```

So according to btime this operation takes 90 microseconds. <mark>I can only
presume that the b is short for bullshit</mark> because that timing is out by
a factor of 1000 compared to a reasonable assessment of how long this
actually takes (150 milliseconds). The reason btime reports a much
lower time is because it's repeatedly solving the exact same
equations: we've already seen that a trivial change in the equations
makes it take much longer. Clearly this is reporting the time taken to
do something that is fully cached in some way.

It is standard practice in the Julia community to report btime timings
because they eliminate (ignore) all of the startup overhead that I've
discussed above. I don't know whether btime is more accurate for other
situations but at least with Symbolics it's wildly out which makes me
question any timings that I see reported by proselytisers of Julia.

I don't want to knock Julia as a language or the Symbolics.jl library.
I think it's a nice language and I'm sure it's well suited to certain
applications. I'm also sure that many of the things I've mentioned
above are being worked on and will improve over time. However the idea
that Julia is faster than Python in general should not go
unquestioned.


---

## Fredrik Lundh's passing

_[src](https://mail.python.org/pipermail/python-list/2021-December/904660.html), Mail by Skip Montanaro_

Like many others, I'm saddened to hear of Fredrik Lundh's passing. I
vaguely recall meeting him just once, probably at a Python workshop,
before they grew big enough to be called conferences. Effbot.org was
my Tkinter, ElemenTree, and PIL reference and cheat sheet.

My attention to Python development has waxed and waned over the years.
Most of the time, the trip through the Python folder in my mail
program was generally pretty quick, hitting the 'd' key far more often
than I'd stop to read a message. There are only a few people whose
messages I'd always read. Effbot was one. In my opinion, Fredrik ranks
up there with Guido, Tim Peters and Barry Warsaw.

I went to effbot.org and saw the "on hiatus" message. Searching
through The Wayback Machine, it seems it went on hiatus in late
November, 2020. The 11 November 2020 snapshot appears to be the last
usable version:

[https://web.archive.org/web/20201111145627/http://effbot.org/](https://web.archive.org/web/20201111145627/http://effbot.org/)

Probably worth a bookmark in your browser.

Rest easy /F ...

Skip

---

## Instagram: Type Hints for Compiler Optimisation

_[src](https://mail.python.org/archives/list/python-ideas@python.org/message/ZM22AKAFIQDHF2E7VPHQ2DZJNBXPTRFM/), Mail by Carl Meyer_


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

---

## Preventing Unicode-related Gotchas

_[src](https://mail.python.org/archives/list/python-dev@python.org/message/GBLXJ2ZTIMLBD2MJQ4VDNUKFFTPPIIMO/), Mail by Paul McGuire_



As part of working on the next edition of “Python in a Nutshell” with Steve, Alex Martelli, and Anna Ravencroft, Alex suggested that I add a cautionary section on homoglyphs, specifically citing “`A`” (LATIN CAPITAL LETTER A) and “`Α`” (GREEK CAPITAL LETTER ALPHA) as an example problem pair. I wanted to look a little further at the use of characters in identifiers beyond the standard 7-bit ASCII, and so I found some of these same issues dealing with Unicode NFKC normalization. The first discovery was the overlapping normalization of “`ªº`” with “`ao`”. This was quite a shock to me, since I assumed that the inclusion of Unicode for identifier characters would preserve the uniqueness of the different code points. Even ligatures can be used, and will overlap with their multi-character ASCII forms. So we have added a second note in the upcoming edition on the risks of using these “homonorms” (which is a word I just made up for the occasion).

To explore the extreme case, I wrote a pyparsing transformer to convert identifiers in a body of Python source to mixed font, equivalent to the original source after NFKC normalization. Here are hello.py, and a snippet from unittest/utils.py:


```
def 𝚑𝓮𝖑𝒍𝑜():

	try:

		𝔥e𝗅𝕝𝚘︴ = "Hello"

		𝕨𝔬r𝓵ᵈ﹎ = "World"

		ᵖ𝖗𝐢𝘯𝓽(f"{𝗵ｅ𝓵𝔩º_}, {𝖜ₒ𝒓lⅆ︴}!")

	except 𝓣𝕪ᵖｅ𝖤𝗿ᵣ𝖔𝚛 as ⅇ𝗑c:

		𝒑rℹₙₜ("failed: {}".𝕗𝗼ʳᵐªｔ(ᵉ𝐱𝓬))

if _︴ⁿ𝓪𝑚𝕖__ == "__main__":

	𝒉eℓˡ𝗈()

# snippet from unittest/util.py

_𝓟Ⅼ𝖠𝙲𝗘ℋ𝒪Lᴰ𝑬𝕽﹏𝕷𝔼𝗡 = 12

def _𝔰ʰ𝓸ʳ𝕥𝙚𝑛(𝔰, p𝑟𝔢ﬁ𝖝𝕝𝚎𝑛, ｓᵤ𝑓𝗳𝗂𝑥𝗹ₑ𝚗):

	ˢ𝗸ｉ𝗽 = 𝐥ｅ𝘯(𝖘) - ｐr𝚎𝖋𝐢x𝗅ᵉ𝓷 - 𝒔𝙪ﬀｉ𝘅𝗹𝙚ₙ

	if sｋi𝘱 > _𝐏𝗟𝖠𝘊𝙴H𝕺Ｌ𝕯𝙀𝘙﹏L𝔈𝒩:

		𝘴 = '%s[%d chars]%s' % (𝙨[:𝘱𝐫𝕖𝑓𝕚ｘℓ𝒆𝕟], ₛ𝚔𝒊p, 𝓼[𝓁𝒆𝖓(𝚜) - 𝙨𝚞𝒇ﬁx𝙡ᵉ𝘯:])

	return ₛ

```

You should able to paste these into your local UTF-8-aware editor or IDE and execute them as-is.

(If this doesn’t come through, you can also see this as a GitHub gist at Hello, World rendered in a variety of Unicode characters (github.com) https://gist.github.com/ptmcg/bf35d5ada416080d481d789988b6b466 . I have a second gist containing the transformer, but it is still a private gist atm.)

Some other discoveries:

“`·`” (ASCII 183) is a valid identifier body character, making “`_···`” a valid Python identifier. This could actually be another security attack point, in which “`s·join(‘x’)`” could be easily misread as “`s.join(‘x’)`”, but would actually be a call to potentially malicious method “`s·join`”.

“`_`” seems to be a special case for normalization. Only the ASCII “`_`” character is valid as a leading identifier character; the Unicode characters that normalize to “`_`” (any of the characters in “`︳︴﹍﹎﹏＿`”) can only be used as identifier body characters. “`︳`” especially could be misread as “`|`” followed by a space, when it actually normalizes to “`_`”.

Potential beneficial uses:

I am considering taking my transformer code and experimenting with an orthogonal approach to syntax highlighting, using Unicode groups instead of colors. Module names using characters from one group, builtins from another, program variables from another, maybe distinguish local from global variables. Colorizing has always been an obvious syntax highlight feature, but is an accessibility issue for those with difficulty distinguishing colors. Unlike the “ransom note” code above, code highlighted in this way might even be quite pleasing to the eye.

-- Paul McGuire

---

## Why Remove Deprecated Functions

_[src](https://mail.python.org/archives/list/python-dev@python.org/message/TYHN7S3BEW7E3LAGAESZFYHPVP5MRI42/), Mail by Victor Stinner_


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

---

