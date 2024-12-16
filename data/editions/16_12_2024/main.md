## Conda: A Package Management Disaster?

_[src](https://mail.python.org/pipermail/python-list/2024-May/912306.html), by Left Right on the Python Mailing List_

The "problematic" part of your question is "with my Anaconda
distribution". Anaconda distribution comes with the conda program that
manages installed packages. A single Anaconda distribution may have
multiple NumPy versions installed at the same time, although only one
will be available to the Python process (note that this means that
sub-processes created in this Python process won't necessarily have
the same version of NumPy!). To make matters worse, it's common for
Anaconda users to use pip to install packages.

Now, Anaconda has a concept of virtual environments independent of
Python's venv module. In order to create such environments it can be
configured to either link (usually hard-link) installed packages into
the dedicated directory, or to copy these packages into the said
directory. This will become important once you inevitably ask the
follow-up question: "why do I have this version of NumPy?".

Unfortunately, you also need to consider setuptools. The traditional
setup.py install command may install multiple versions of the same
package into the same directory. Even worse, "pip install -e", the
glorified "setup.py develop", complicates things even further by
adding the "installed" package to the pth file, which can, again,
create ambiguities as to the resolution of the package location.

On top of this, there's an environment variable: PYTHONPATH that can
be set to add an arbitrary number of source directories for Python to
look up package location.

So, suppose you ran:

`python -c "import numpy; numpy.__version__"`

and then ran a Jupyter notebook and discovered that the version of
NumPy in that notebook is not the one you just saw in the previous
output... What went wrong?

You then may try:

`conda info numpy`

and get yet another answer.  And then you run

`pip show numpy`

And the answer is still different!

Of course, it's not necessary that all these answers are different.
And, in most circumstances they are going to be consistent... but they
don't have to be!

Below is the list of typical problems I encountered in my attempts to
resolve similar problems for Python users. Of course, this list is not
exhaustive.

1. If the version in the Jupyter notebook differs from the one in the
environment in which the Jupyter server was started, you need to look
for the Jupyter kernel definition. There are many ways in which the
Jupyter kernel definition may alter the module lookup locations, but
the most common one is that using Python from the active virtual
environment isn't the default for the default Jupyter kernel.

2. If installed modules in conda environments are hard-linked, and at
some point pip or setuptools were used to install extra packages, you
might have "botched" unrelated environments by overwriting files
through hard-links without you even knowing that.

3. conda will happily install outdated versions of conda into virtual
environments it creates. The format of conda virtual environments
changed over time, and older versions of conda are unaware of the new
format, while newer versions are unaware of the old format. If you
happen to run the conda command from the wrong environment you may get
unexpected results (especially if both the new and the old version of
conda have created environments with the same name!) To avoid this,
you'd want to deactivate all conda environments activated so far until
you are at least in the base environment.

4. Usually, some diagnostic information can be gleaned from printing
the value of PYTHONPATH environment variable, sys.paths list (inside
Python), sys.sysconfig.get_path('platlib') (and looking into this
directory for duplicate packages with different version or for the pth
files.) If you discover anomalies, try to figure out if you had to use
pip to install packages (this may indirectly mean using setuptools).
Similarly, running "conda build" may indirectly result in running
setuptools commands. Also, some popular tools like to do bad things to
packages and virtual environments: pytest and tox come to mind. pytest
can manipulate module lookup locations (and you will need to dissect
its configuration to figure this out). tox, afaik, is unaware of conda
virtual environments, and will try to create venv-style virtual
environments, which will have all the same problems as using pip in
conda environments does.

5. Final warning: no matter how ridiculous this is: the current
directory in Python is added to the module lookup path, and it
*precedes* every other lookup location. If, accidentally, you placed a
numpy.py in the current directory of your Python process -- that is
going to be the numpy module you import.  To make this even worse,
this behavior used to depend on whether you start Python with PDB
active or not (with PDB, the current working directory wasn't added to
the path, and module imports resolved differently). I'm not quite sure
which version of Python fixed that.


## Problems With Python's Package Management And Venv Philosophy

_[src](https://mail.python.org/pipermail/python-list/2024-May/912341.html), by Left Right on the Python Mailing List_


There are several independent problems here:

(1) Very short release cycle. This is independent of the Python venv
module but is indirectly influenced by Python's own release cycle.
Package maintainers don't have time for proper testing, they are
encouraged to release a bunch of new (and poorly tested) versions, and
they never get a break. So, when you install the latest, there will be
something else broken.  There's never a window to properly test
anything.

(2) Python made a very short-sighted decision about how imports work.
Python doesn't have a concept of "application", and therefore there's
no way to specify dependencies per application (and imports import
anything that's available, not versioned). That's why every Python
application ends up carrying its own Python, with the version of its
own dependencies around. Python's venv module is just an
acknowledgement of this design flaw.  I.e. the proper solution
would've been a concept of application and per-application dependency
specification, but instead we got this thing that doesn't really work
(esp. when native modules and shared libraries are considered), but it
"works" often enough to be useful.

(3) The Python community grew to be very similar to what PHP 4 was,
where there were several "poisonous" examples, which were very popular
on the Web, which popularized a way of working with MySQL databases
that was very conducive to SQL injections. Python has spread very bad
ideas about project management. Similar to how PHP came up with
mysql_real_escape() and mysql_this_time_promise_for_real_escape() and
so on functions, Python came up with bad solutions to the problems
that had to be fixed by removing bad functionality (or, perhaps,
education). So, for example, it's very common to use requirements.txt,
which is generated by running pip freeze (both practices are bad
ideas). Then PyPA came up with a bunch of bad ideas in response to
problems like this, eg. pyproject.toml.  In an absurd way very much
mirroring the situation between makefiles and makefiles generated by
autotools, today Python developers are very afraid of doing simple
things when it comes to project infrastructure (it absolutely has to
be a lot of configuration fed into another configuration, processed by
a bunch of programs to generate even more configuration...) And most
Python programmers don't really know how the essential components of
all of this infrastructure work. They rely on a popular / established
pattern of insane multi-step configuration generation to do simple
things. And the tradition thus developed is so strong, that it became
really cultish. This, of course, negatively contributes to the overall
quality of Python packages and tools to work with them.

Unfortunately, the landscape of Python today is very diverse.  There's
no universally good solution to package management because it's broken
in the place where nobody is allowed to fix it.  Commercial and
non-commercial bodies alike rely on people with a lot of experience
and knowledge of particular Python gotchas to get things done. (Hey,
that's me!) And in different cases, the answer to the problem will be
different. Sometimes venv is good enough. Other times you may want a
container or a vm image. Yet in a different situation you may want a
PyPA or conda package... and there's more.

## Markdown & Madness

_[src](https://mail.python.org/pipermail/python-list/2024-May/912352.html), by DN on the Python Mailing List_

With reference to another reply here, the "Weird stuff" came from 
reading the question, finding it unclear, and only later realising that 
whereas most people write Markdown-formatted documents for later 
processing, or perhaps docstrings in Markdown-format for collection by 
documentation systems; here, the objective appears to be using Python to 
generate Markdown.

How much have you used Markdown to any serious degree, before attempting 
this feat?


On 26/05/24 18:28, Gilmeh Serda via Python-list wrote:
> The web claims (I think on all pages I've read about Markdown and Python)
> that this code should work, with some very minor variants on the topic:

There are so many "variants", the problem is not "minor"!

Markdown users learn to use their tool (again, see @Grant's question) 
and work within the implementation of that "variant".

Like any other non-standardised tool, the users of some particular 
'version' often fail to realise that others using different versions may 
not enjoy the same experience. Plus-one for standardisation!


At the end of the message, the web.refs reveal use of a package which is 
based upon a variant of Markdown that is 20-years old(!), albeit with 
some updates to suit yet another variant. Neither variant-author famous 
for collaboration. The phrase YMMV springs to mind...


Some ten years ago, an effort was made to standardise Markup, and it 
ended-up being called CommonMark. Why is it not called "Standard 
Markdown" one might ask? Because the fellow who 'invented' Markdown 
objected. This very objection has likely led directly to your 
confusions, because the particular PyPi package is based upon that 
original definition...

Whereas, Markdown 3.6 is the most-recently updated Markdown search-hit 
on PyPi today, have you tried any of the others (which, ironically, may 
offer more recent and/or more standardised coverage)?


This has worked in all of the Markdown processors I have used or tried-out:

The (?reasonable) 'common-core', offers single back-ticks for code, 
triple back-ticks for a code-block, and the latter with or without a 
language specification which *usually* kicks-in syntax highlighting.


> ```python
> 
> import os
> 
> with open(os.path.join('/home/user/apath', 'somefile')) as f:
>      print(f.read())
> ```
> 
> However, that is not the case. At least not for me (using Python 3.12.3).

It's not Python 3 that is the problem. It is the "Markdown 3.6" package!


> If instead I type it:


I've not seen the hash-bang combination in-the-wild (but YMMV!)

>      #!python
>      
>      import os
>      
>      with open(os.path.join('/home/user/apath', 'somefile')) as f:
>          print(f.read())
> 
> As an indented block (four spaces) and a shebang, THEN it works. You even
> get line numbers by default.

An indented-block is NOT necessarily the same as a code-block - just as 
"code" is not necessarily "Python".

Line numbers are great - although if a code snippet is extracted from 
the middle of some example code-file, the original line-numbers won't 
line-up with Markdown's...


> N.b. if you don't know, you also need to generate a css file using
> pygments to make this work.

That's not what the package's docs suggest: 
[https://python-markdown.github.io/extensions/fenced_code_blocks/](https://python-markdown.github.io/extensions/fenced_code_blocks/)


> Not until I started to read the markdown source code and its docs pages,
> the coin dropped.
> 
> I'm posting this for other Markdown newbies that otherwise probably would
> spend hours trying to make it work.
> 
> 
> Speaking of Markdown. Does anybody out there have any idea how to turn on
> table borders, adjust them (color/width/etc.) and such things? Currently I
> have to add HTML to do so, which works, but isn't very nice. I'd hate to
> spend an additional day or two, hunting for this info.

Again, heavily dependent upon the tool in-use. For example, most SSGs 
and doc-tools (which accept Markdown) have a .css or theming-system 
which enables 'decorations'.


References
- [https://pypi.org/project/Markdown/](https://pypi.org/project/Markdown/)
- [https://python-markdown.github.io/](https://python-markdown.github.io/)

Further reading:

- [https://en.wikipedia.org/wiki/Markdown](https://en.wikipedia.org/wiki/Markdown)
- [https://commonmark.org](https://en.wikipedia.org/wiki/Markdown)
- [https://pypi.org/search/?q=markdown](https://en.wikipedia.org/wiki/Markdown)