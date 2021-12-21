title: So, Julia is the magic pill?
authors: benjamin_oscar
note: Mail by Oscar Benjamin
source: https://mail.python.org/pipermail/python-list/2021-December/904690.html
tags: julia
slug: ---


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

So according to btime this operation takes 90 microseconds. I can only
presume that the b is short for bullshit because that timing is out by
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
