## On Poor Error Reporting

_[src](https://mail.python.org/pipermail/python-list/2024-November/912987.html), by Left Right the Python Mailing List_

Poor error reporting is a very common problem in programming.  Python
is not anything special in this case.  Of course, it would've been
better if the error reported what file wasn't found.  But, usually
these problems are stacking, like in your code.  Unfortunately, it's
your duty, as the language user, to anticipate those problems and act
accordingly. Now you've learned that the one file you believe that
could be the source for the error isn't the only one--well, adjust
your code to differentiate between those two (and potentially other?)
cases.  There's very little else you can do beside that.

NB. On the system level, the error has no information about what file
wasn't found.  It simply returns some numeric value (the famous
ENOENT) in case when the system call to open a file fails.  Python
could've been more helpful by figuring out what path caused the
problem and printing that in the error message, but it doesn't...
That's why I, myself, never use the vanilla FileNotFoundError, I
always re-rise it with a customized version that incorporates the
information about the missing file in the error message.

NB2. It's always a bad idea to print logs to files.  Any sysadmin /
ops / infra person worth their salt will tell you that.  The only
place the logs should go to is the standard error.  There are true and
tried tools that can pick up logs from that point on, and do with them
whatever your heart desires.  That is, of course, unless you are
creating system tools for universal log management (in which case, I'd
question the choice of Python as a suitable language for such a task).
Unfortunately, even though this has been common knowledge for decades,
it's still elusive in the world of application development :|

First, the problem with writing to files is that there is no way to
make these logs reliable.  This is what I mean by saying these are
unreliable: since logs are designed to grow indefinitely, the natural
response to this design property is log rotation.  But, it's
impossible to reliably rotate a log file.  There's always a chance
that during the rotation some log entries will be written to the file
past the point of rotation, but prior to the point where the next logs
volume starts.

There are similar reliability problems with writing to Unix or
Internet sockets, databases etc.  For different reasons, but at the
end of the day, whoever wants logs, they want them to be reliable.
Both simplicity and convention selected for stderr as the only and the
best source of logging output.

Programs that write their output to log files will always irritate
their users because users will have to do some detective work to
figure out where those files are, and in some cases they will have to
do administrative works to make sure that the location where the
program wants to store the log files is accessible, has enough free
space, is speedy enough etc.  So, from the ops perspective, whenever I
come across a program that tries to write logs to anything other than
stderr, I make an earnest effort to throw that program into the gutter
and never touch it again.  It's too much headache to babysit every
such program, to remember the location of the log files of every such
program, the required permissions, to provision storage.  If you are
in that line of work, you just want all logs to go to the same place
(journal), where you can later filter / aggregate / correlate and
perform other BI tasks as your heart desires.

Of course, if you only administer your own computer, and you have low
single digits programs to run, and their behavior doesn't change
frequently, and you don't care to drop some records every now and
then... it's OK to log to files directly from a program.  But then you
aren't really in the sysadmin / infra / ops category, as you are more
of a hobby enthusiast.

Finally, if you want your logs to go to a file, and currently, your
only option is stderr, your shell gives you a really, really simple
way of redirecting stderr to a file.  So, really, there aren't any
excuses to do that.

---

## A Good Reminder of Why Dead Batteries Are Being Removed: The Case of nntplib

_[src](https://mail.python.org/pipermail/python-list/2024-August/912636.html), by Keith Thompson on the Python Mailing List_


nntplib is not vanishing into thin air.  It's just not going to be part
of a default Python installation.  (It's not there in Python 3.13.0rc1.)

In my opinion the use of the word "deprecated" is misleading.

```
$ python3
Python 3.12.4 (main, Jun 27 2024, 13:53:59) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import nntplib
<stdin>:1: DeprecationWarning: 'nntplib' is deprecated and slated for removal in Python 3.13
>>>
$ 
```

[https://pypi.org/project/nntplib/](https://pypi.org/project/nntplib/)

The rationale for removing nntplib and other modules from the default
installation is explained in [PEP 0594](https://peps.python.org/pep-0594/).

"""
Back in the early days of Python, the interpreter came with a large
set of useful modules. This was often referred to as “batteries
included” philosophy and was one of the cornerstones to Python’s success
story. Users didn’t have to figure out how to download and install
separate packages in order to write a simple web server or parse email.

Times have changed. With the introduction of PyPI (née Cheeseshop),
setuptools, and later pip, it became simple and straightforward to
download and install packages. Nowadays Python has a rich and vibrant
ecosystem of third-party packages. It’s pretty much standard to either
install packages from PyPI or use one of the many Python or Linux
distributions.

[...]

The nntplib module implements the client side of the Network News
Transfer Protocol (nntp). News groups used to be a dominant platform for
online discussions. Over the last two decades, news has been slowly but
steadily replaced with mailing lists and web-based discussion
platforms. Twisted is also planning to deprecate NNTP support and pynntp
hasn’t seen any activity since 2014. This is a good indicator that the
public interest in NNTP support is declining.

The nntplib tests have been the cause of additional work in the recent
past. Python only contains the client side of NNTP, so the tests connect
to external news servers. The servers are sometimes unavailable, too
slow, or do not work correctly over IPv6. The situation causes flaky
test runs on buildbots.
"""

---

## Separating F-strings From The Format

_[src](https://mail.python.org/pipermail/python-list/2024-August/912687.html), by DN on the Python Mailing List_

With recent improvements to the expressions within F-strings, we can 
separate the string from the format required. (reminiscent of FORTRAN 
which had both WRITE and FORMAT statements, or for that matter HTML 
which states the 'what' and CSS the 'how')

Given that the int() instance-creation has a higher likelihood of 
data-error, it is recommended that it be a separate operation for ease 
of fault-finding - indeed some will want to wrap it with try...except.

```
 >>> s = "123456789" # arrives as str
 >>> s_int = int( s )  # makes the transformation obvious and distinct

 >>> s_format = ">20,"  # define how the value should be presented

 >>> F"{s_int:{s_format}}"
'         123,456,789'
```

Further, some of us don't like 'magic-constants', hence (previously):

```
 >>> S_FIELD_WIDTH = 20
 >>> s_format = F">{S_FIELD_WIDTH},"
```

and if we really want to go over-board:

```
 >>> RIGHT_JUSTIFIED = ">"
 >>> THOUSANDS_SEPARATOR = ","
 >>> s_format = F"{RIGHT_JUSTIFIED}{S_FIELD_WIDTH}{THOUSANDS_SEPARATOR}"

or (better) because right-justification is the default for numbers:

 >>> s_format = F"{S_FIELD_WIDTH}{THOUSANDS_SEPARATOR}"
```

To the extreme that if your user keeps fiddling with presentations (none 
ever do, do they?), all settings to do with s_format could be added to a 
config/environment file, and thus be even further separated from 
program-logic!

---

## A Gem On Clear Requirements

_[src](https://mail.python.org/pipermail/python-list/2024-June/912413.html), by Avi gross on the Python Mailing List_

As someone who has spent lots of time writing code OR requirements of various levels or having to deal with the bugs afterwards, there can be a huge disconnect between the people trying to decide what to do and the people having to do it. It is not necessarily easy to come back later and ask for changes that wewre not anticipated in the design or implementation.

I recently wrote a program where the original specifications seemed reasonable. In one part, I was asked to make a graph with some random number (or all) of the data shown as a series of connected line segments showing values for the same entity at different measurement periods and then superimpose the mean for all the original data, not just the subsample shown. This needed to be done on multiple subsamples of the original/calculated data so I made it into a function. 

One of the datasets contained a column that was either A or B and the function was called multiple times to show what a random sample of A+B, just A and just B graphed like along with the mean of the specific data it was drawn from. But then, I got an innocuously simple request.

Could we graph A+B and overlay not only the means for A+B as was now done, but also the mean for A and the mean for B. Ideally, this would mean three bolder jaged lines superimposed above the plot and seemed simple enough.

But was it? To graph the means in the first place, I made a more complex data structure needed so when graphed, it aligned well with what was below it. But that was hard coded in my function, but in one implementation, I now needed it three times. Extracting it into a new function was not trivial as it depended initially on other things within the body of the function. But, it was doable and might have been done that way had I known such a need might arise. It often is like that when there seems no need to write a function for just one use. The main function now needed to be modified to allow optionally adding one or two more datasets and if available, call the new function on each and add layers to the graph with the additional means (dashed and dotted) if they are called while otherwise, the function worked as before.

But did I do it right? Well, if next time I am asked to have the data extended to have more measurements in more columns at more times, I might have to rewrite quite a bit of the code. My localized change allowed one or two additional means to be plotted. Adding an arbitrary number takes a different approach and, frankly, there are limits on how many kinds of 'line" segments can be used to differentiate among them.

Enough of the example except to make a point. In some projects, it is not enough to tell a programmer what you want NOW. You may get what you want fairly quickly but if you have ideas of possible extensions or future upgrades, it would be wiser to make clear some of the goals so the programmer creates an implementation that can be more easily adjusted to do more. Such code can take longer and be more complex so it may not pay off immediately.

But, having said that, plenty of software may benefit from looking at what is happening and adjusting on the fly. Clearly my client cannot know what feedback they may get when showing an actual result to others who then suggest changes or enhancements. The results may not be anticipated so well in advance and especially not when the client has no idea what is doable and so on. 

A related example was a request for how to modify a sort of Venn Diagram  chart to change the font size. Why? Because some of the labels were long and the relative sizes of the pie slices were not known till an analysis of the data produced the appropriate numbers and ratios. This was a case where the documentation of the function used by them did not suggest how to do many things as it called a function that called others to quite some depth. A few simple experiments and some guesses and exploration showed me ways to pass arguments along that were not documented but that were passed properly down the chain and I could now change the text size and quite a few other things. But I asked myself if this was really the right solution the client needed. I then made a guess on how I could get the long text wrapped into multiple lines that fit into the sections of the Venn Diagram without shrinking the text at all, or as much. The client had not considered that as an option, but it was better for their display than required. But until people see such output, unless they have lots of experience, it cannot be expected they can tell you up-front what they want.

One danger of languages like Python is that often people get the code you supply and modify it themselves or reuse it on some project they consider similar. That can be a good thing but often a mess as you wrote the code to do things in a specific way for a specific purpose ...
