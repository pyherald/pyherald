title: When Dependencies Bite!
authors: 
note: Health & moods. They were always a nightmare.
source: ---
tags: black, ipython
slug: ---

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