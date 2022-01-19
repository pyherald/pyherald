title: Asserts Beyond Tests: Good or Evil?
authors: mariatta
note: People sure asserted many things
source: https://twitter.com/mariatta/status/1481422508976787458?s=20
tags: assert
slug: ---


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

