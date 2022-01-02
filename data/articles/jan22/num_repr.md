title: Representing Numbers: The Complexity Behind
authors: avi_gross
note: Mail by  Avi Gross
source: https://mail.python.org/pipermail/python-list/2021-November/904404.html
tags: maths, repr
slug: ---

Mathematics is a pristine world that is NOT the real world. It handles
near-infinities fairly gracefully but many things in the real world break
down because our reality is not infinitely divisible and some parts are
neither contiguous nor fixed but in some sense wavy and probabilistic or
worse.

So in any computer, or computer language, we have realities to deal with
when someone asks for say the square root of 2 or other transcendental
numbers like pi or e or things like the sin(x) as often they are numbers
which in decimal require an infinite number of digits and in many cases do
not repeat. Something as simple as the fractions for 1/7, in decimal, has an
interesting repeating pattern but is otherwise infinite.

```
.142857142857142857 ... ->> 1/7
.285714285714285714 ... ->> 2/7
.428571 ...
.571428 ...
.714285 ...
.857142 ...
```

No matter how many bits you set aside, you cannot capture such numbers
exactly IN BASE 10.

You may be able to capture some such things in another base but then yet
others cannot be seen in various other bases. I suspect someone has
considered a data type that stores results in arbitrary bases and delays
evaluation as late as possible, but even those cannot handle many numbers.

So the reality is that most computer programming is ultimately BINARY as in
BASE 2. At some level almost anything is rounded and imprecise. About all we
want to guarantee is that any rounding or truncation done is as consistent
as possible so every time you ask for pi or the square root of 2, you get
the same result stored as bits. BUT if you ask a slightly different
question, why expect the same results? sqrt(2) operates on the number 2. But
`sqrt(6*(1/3))` first evaluates 1/3 and stores it as bits then multiplies it
by the bit representation of 6 and stores a result which then is handed to
`sqrt()` and if the bits are not identical, there is no guarantee that the
result is identical.

I will say this. Python has perhaps an improved handling of large integers.
Many languages have an assortment of integer sizes you can use such as 16
bits or 32 or 64 and possibly many others including using 8 or 1bits for
limited cases. But for larger numbers, there is a problem where the result
overflows what can be shown in that many bits and the result either is seen
as an error or worse, as a smaller number where some of the overflow bits
are thrown away. Python has indefinite length integers that work fine. But
if I take a real number with the same value and do a similar operation, I
get what I consider a truncated result:

```
>>> 256**40
2135987035920910082395021706169552114602704522356652769947041607822219725780
640550022962086936576
>>> 256.0**40
2.13598703592091e+96
```

That is because Python has not chosen to implement a default floating point
method that allows larger storage formats that could preserve more digits.

Could we design a more flexible storage form? I suspect we could BUT it
would not solve certain problems. I mean Consider these two squarings:

```
>>> .123456789123456789 * .123456789123456789
0.015241578780673677
>>> 123456789123456789 * 123456789123456789
15241578780673678515622620750190521
```

Clearly a fuller answer to the first part, based on the second, is
.015241578780673678515622620750190521

So one way to implement such extended functionality might be to have an
object that has a storage of the decimal part of something as an extended
integer variation along with storage of other parts like the exponent. SOME
operations would then use the integer representation and then be converted
back as needed. But such an item would not conform to existing standards and
would not trivially be integrated everywhere a normal floating point is
expected and thus may be truncated in many cases or have to be converted
before use.

But even such an object faces a serious problem as asking for a fraction
like 1/7 might lead to an infinite regress as the computer keeps lengthening
the data representation indefinitely. It has to be terminated eventually and
some of the examples shown where the whole does not seem to be the same
when viewed several ways, would still show the anomalies some invoke.

Do note pure Mathematics is just as confusing at times. The number
.99999999... where the dot-dot-dot notation means go on forever, is
mathematically equivalent to the number 1 as is any infinite series that
asymptotically approaches 1 as in 

```
1/2 + 1/4 + 1/8 + ... + 1/(2**N) + ...
```
It is not seen by many students how continually appending a 9 can ever be
the same as a number like 1.00000 since every single digit is always not a
match. But the mathematical theorems about limits are now well understood
and in the limit as N approaches infinity, the two come to mean the same
thing. 

Python is a tool. More specifically, it is a changing platform that hosts
many additional tools. For the moment the tools are built on bits which are
both very precise but also cannot finitely represent everything. Maybe if we
develop decent quantum computers and use QBITS, we might have a wider range
of what can be stored and used by programs using a language that can handle
the superpositions involved. But, I suspect even that kind of machine might
still not handle some infinities well as I suspect our real world, quantum
features and all, at some levels reduces to probabilities that at some level
are not exactly the same each time.

So, what should be stressed, and often is, is to use tools available that
let you compare numbers for being nearly equal. I have seen some where the
size in bits of the machine storage method is used  to determine if numbers
are equal until within a few bits of the end of the representation. But
other places should be noted such as a hill-climbing algorithm that is
looking for a peak or valley, cannot be expected to converge to exactly what
you want and you may settle for it getting close enough as in 0.1%, or stop
if it does not improve in the last hundred iterations. The Mathematics may
require a precise answer, such as a point around which the slope of a curve
is zero, but the algorithm, especially when used with storage of variables
limited to some precision, may not reliably be able to zero in on a much
better answer so again, not a test for actual equality is needed, but one
close enough to likely be good enough.

I note how unamused I was when making a small table in EXCEL (Note, not
Python) of credit card numbers and balances when I saw the darn credit card
numbers were too long and a number like:

```
4195032150199578 
```

was displayed by EXCEL as:

```
4195032150199570
```

It looks like I just missed having significant stored digits and EXCEL
reconstructed it by filling in a zero for the missing extra. The problem is
I had to check balances sometimes and copy/paste generated the wrong number
to use. I ended up storing the number as text using '4195032150199578 as I
was not doing anything mathematical with it and this allowed me to keep all
the digits as text strings can be quite long.

But does this mean EXCEL is useless (albeit some thing so) or that the tool
can only be used up to some extent and beyond that, can (silently) mislead
you?

Having said all that, this reminds me a bit about the Y2K issues where
somehow nobody thought much about what happens when the year 2000 arrives
and someone 103 years old becomes 3 again as only the final two digits of
the year are stored. We now have the ability to make computers with
increased speed and memory and so on and I wonder if anyone has tried to
make a standard for say a 256-byte storage for multiple-precision floating
point that holds lots more digits of precision as well as allowing truly
huge exponents. Of course, it may not be practical to have computers that
have registers and circuitry that can multiply two such numbers in a very
few cycles, and it may be done in stages in thousands of cycles, so use of
something big like that might not be a good default.


