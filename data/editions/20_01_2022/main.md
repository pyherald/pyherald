## Asserts Beyond Tests: Good or Evil?

_[src](https://twitter.com/mariatta/status/1481422508976787458?s=20), People sure asserted many things_


Mariatta, core dev (whose name is also spelled as "[ice-cream-selfie-lady](https://mariatta.ca/pages/ice-cream-selfie.html#ice-cream-selfie)") raised the issue of raising assertions outside of unittests. She reasoned that you'd need to deal with catching `AssertionError` when things go wrong. Though i am a great fan of asserts outside tests, i was quite surprised by core dev Taskaya's [use of asserts](https://twitter.com/isidentical/status/1481578677695565829?s=20) for pattern matching. Elegant indeed. Steve Dower, yet another core dev summarised the issue with _finesse_

```
I use it regularly for validating internal state at a point where I know what it should be, and always in a way that is optional. A kind of inline unit test.

Never for input validation, including arguments coming through public APIs. Have to assume that asserts will be disabled.

Can also think of it as the difference between warnings.warn (for developers / assert) and logging.warn (for users / raise).
```


When running Python in optimised version (Using the `-O` flag), assert statements are skipped. Łukasz Langa pointed that when asserts statements alter codes, [you miss](https://twitter.com/llanga/status/1481684789262487556?s=20) certain execution pieces. This

```
assert code.do_something() == 1
```

compared to 

```
_temp_var = code.do_something()
assert  _temp_var == 1
```


Not Python fault's for sure. Beazly has a great story for us about enforcing invariants:

```
I have been saved by a few well-placed asserts in the past.

Coworker: "Hey the code crashed with this really weird AssertError."

Me: "Oh, I knew you were going to shoot yourself in the foot six months ago. That prevented you from destroying production."
```

Folks have also questioned the use of asserts for those cases. Mypy they tell, does a better job. If you are asserting types passed in all the times, it might be better to go full typing mode. Assuming of course you know the always morphing, incomplete and quirky beast. 

Using asserts for validation is a poor idea it seems. Some [people](https://twitter.com/GothAlice/status/1481619658297982986?s=20) have found a nice out-of-the view spot though


```
I use assert for validations that must happen, but do not need to happen in production, combined with “if __debug__” armour around debug level logging. Assuming good test suite coverage.
Certain things changing when run with “optimisations” enabled is damned useful.
```

Well, well ...

According to [(well founded) rumours](https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html) bandit whines about using asserts outside of tests.


```
It was discovered that some projects used assert to enforce interface constraints. However, assert is removed with compiling to optimised byte code (python -o producing *.pyo files). This caused various protections to be removed. Consider raising a semantically meaningful error or `AssertionError` instead.
```

That's news for sure. 

If you are using asserts outside tests it's _tolerance for users, brutality for devs_. Your app should refuse working if the devs are plain wrong.



---

## When Dependencies Bite!

_[src](---), Health & moods. They were always a nightmare._

```
Argh!  Who thought Black should be automatically applied to lines in the IPython CLI?
```

reputable core dev Hettinger [clamoured](https://twitter.com/raymondh/status/1482225220475883522?s=20). Users were surprised to wake up with no control over their cell codes. As a teacher for minds that mutates, black formatting cells was simply outrageous! He elaborated


```
In a #Python course, if you want to demonstrate that print('hello') and print("hello") are the same, then too bad.  The CLI rewrites both to use double quotes and the students can't see what you were demonstrating.

When doing math, you improve readability by grouping your terms as shown in PEP 8:

3*x**2 - 5*x + 10

However, the new #Ipython CLI immediately expands it to:

3 * x ** 2 - 5 * x + 10

Black's quotation rewrites are especially distracting in a REPL where it clearly conflicts the language's internal preferences:

In [11]: {"x": 10}
Out[11]: {'x': 10}

For teaching purposes, it is especially annoying to have in-line comments smushed to two spaces after the code ends. And more so, when it splits your input lines.

if n == 0: return 0   # 1st known case
if n == 1: return 1     # 2nd known case
return n * fact(n-1)   # Recurse

It's no longer possible to show students how to use the semicolon to separate statements:

>>> time.sleep(5); print("Done")

In #IPython, this gets rewritten to:

In [15]: sleep(5)
    ...: print("Done")
Done

```

Yes if it is optional, you can revert back but that's not acceptable 

```
Yes, this can be turned off, but you have to get a whole classroom of mixed Windows, Mac, and Linux users to monkey through the steps to get back to a normal environment where you can see what you typed into the computer rather than what it wanted you to type.

Even if you usually like how Black formats your scripts and modules, why would you ever do this line by line in a CLI?
```

And IDLE takes the bite too, which me too i feel for 

```

It wasn't long ago that IDLE became unusable for teaching.  And now IPython decides to rewrite my inputs so that students never see what I actually typed.

Argh!!!
```

Matthias Bussonnier, PhD in (Bio)Physics, Core developer of @ipython and @jupyter, alias [Carreau](https://github.com/Carreau), [broke down](https://github.com/ipython/ipython/issues/13463#issuecomment-1013742058)


```
The way Raymond Hettinger complained on Twitter is personally deeply hurtful.

...

But I much prefer a reaction like:

https://twitter.com/jnuneziglesias/status/1478867554009452545

"Black formatting by default is :nauseated_face: though :stuck_out_tongue_winking_eye: — made myself a todo to turn it off. :joy: Can yapf be configured in its place?"

Which I'm more likely to help with (and did in a thread). Than spitting on maintainers, which is painful and counter productive.

I'll try to restore some of my mental sanity. I was hoping to do a 8.1 around last Friday of January (release friday), we'll see what I can get in there.
```

And explained his point of view


```
"So, the actions IPython maintainers can take now are as follows:

1. make it explicitly opt-in;"

To this and similar suggestions, 'black' auto-formatting has been opt-in for 2 years (may 1st 2020, IPython 7.14).

I had thought it might be problematic, but in two years received almost no bug reports. I tried a few time to say I was considering making it default and only got positive feedback. So I did it, with extensive alpha, beta, and RC time to complain and ask for modifications.

So here is my challenge, if I don't make it the default, no-one know about it. It's astonishing that no-one found the bug @ehamiter described above in 2 years ! That alone would have definitely delayed the release, and at least I would have had tried to fix it.

I've also seen a number of new users misformating Python code and taking really bad habits in the Repl, including folks that did not even realise IPython terminal was multiline.

For many of those users black by default is much better. You get use to proper code formatting. So you learn to properly read python code.
And it is much easier to deactivate something you don't like than even figure out it something that may exists. For many users this benefits to, having this option be opt-in would make black auto formatting be part of the [unknown unknowns].(https://en.wikipedia.org/wiki/There_are_known_knowns). So I will never get feedback from these. This is in the same vein as "but you can configure vim to do so".

"2. make it much easier to opt out;"

It's really hard to make it much easier, there have been a long standing issue to have persistent config, but that's far beyond the time and funds we have for that in IPython. We could borrow a nice configuration interface like ptpython for the UI if Someone want to take a shot at ti.

"3. stop depending on Black by default."

(As black is beta I agree that this is a problem I did not foresaw and will likely be removing at least the dependency, though I don't really like that either).

As many have pointed out, it's expected for major release to receive feedback because few users try --pre, and other channel, and it's ok I expect it
```

Though not maliciously, Hettinger pushed forward. He [explained](https://github.com/ipython/ipython/issues/13463#issuecomment-1013975665) that if black auto applies to notebooks, the careful formattings of authors to communicate specifics will be lost to black's opinion. The black sheep is likely to be removed on the next release. Detecting if black is in the env to activate the feature also rings terribly bad as black might be present but as a dependency of another project and not of the author's own will. 

---

## Type Checking: What To Read To Stay Updated?

_[src](---), Quite a lot it seems_


Some copy-pastaing from [pyright](https://github.com/microsoft/pyright), a microsoft-backed static type checker. If you want to follow the Typing dossier, here's a nice starting point!


-   [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints including generics
-   [PEP 487](https://www.python.org/dev/peps/pep-0487/) simpler customization of class creation
-   [PEP 526](https://www.python.org/dev/peps/pep-0526/) syntax for variable annotations
-   [PEP 544](https://www.python.org/dev/peps/pep-0544/) structural subtyping
-   [PEP 561](https://www.python.org/dev/peps/pep-0561/) distributing and packaging type information
-   [PEP 563](https://www.python.org/dev/peps/pep-0563/) postponed evaluation of annotations
-   [PEP 570](https://www.python.org/dev/peps/pep-0570/) position-only parameters
-   [PEP 585](https://www.python.org/dev/peps/pep-0585/) type hinting generics in standard collections
-   [PEP 586](https://www.python.org/dev/peps/pep-0586/) literal types
-   [PEP 589](https://www.python.org/dev/peps/pep-0589/) typed dictionaries
-   [PEP 591](https://www.python.org/dev/peps/pep-0591/) final qualifier
-   [PEP 593](https://www.python.org/dev/peps/pep-0593/) flexible variable annotations
-   [PEP 604](https://www.python.org/dev/peps/pep-0604/) complementary syntax for unions
-   [PEP 612](https://www.python.org/dev/peps/pep-0612/) parameter specification variables
-   [PEP 613](https://www.python.org/dev/peps/pep-0613/) explicit type aliases
-   [PEP 635](https://www.python.org/dev/peps/pep-0635/) structural pattern matching
-   [PEP 646](https://www.python.org/dev/peps/pep-0646/) variadic generics
-   [PEP 647](https://www.python.org/dev/peps/pep-0647/) user-defined type guards
-   [PEP 655](https://www.python.org/dev/peps/pep-0655/) required typed dictionary items
-   [PEP 673](https://www.python.org/dev/peps/pep-0673/) Self type
-   [PEP 677](https://www.python.org/dev/peps/pep-0677/) callable type syntax
-   Type inference for function return values, instance variables, class variables, and globals
-   Type guards that understand conditional code flow constructs like if/else statements

---

## What's Happening in PythonLand?

_[src](---), Guided tour_

[PEP 665](https://www.python.org/dev/peps/pep-0665/) -- A file format to list Python dependencies for reproducibility of an application got rejected. Brett's [thinking](https://twitter.com/brettsky/status/1481069172314550276?s=20) of developing his own opinionated solution for wheel-only lock files. The [reason for rejection](https://discuss.python.org/t/pep-665-take-2-a-file-format-to-list-python-dependencies-for-reproducibility-of-an-application/11736/140) is the lack of sdist support which was enough to cause a lukewarm reception overall to the PEP. However, Paul Moore does concede that we definitely need a lockfile format that’s better than the current “pinned requirements file” approach, noting recent examples of supply chain issues with npm and similar demonstrate that locking is becoming far more critical.


 
[PEP 654](https://www.python.org/dev/peps/pep-0654/) -- Exception Groups and except* [gets accepted](https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813)


Brett is [stepping back](https://mail.python.org/archives/list/python-committers@python.org/thread/GB7T23XWLNKR24V5IWBADYSLFK6KWCY6/) from being the person in charge of infrastructure



[Arbitrary Literal Strings PEP](https://docs.google.com/document/d/1fbAbA2MCoAcSO1c8gecmUJYZ-Q0utT3CmaXlQ3IhzZw/edit) is still brewing.

---

