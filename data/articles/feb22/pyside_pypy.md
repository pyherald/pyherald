title: PyPy on PySide6 is there: PyPy with a Gui
authors: christian_tismer
note: Mail by Christian Tismer
source: https://mail.python.org/archives/list/python-dev@python.org/thread/32XOK67BGMEX2UIYVVXMHOUME56O3GJ7/
tags: stanford, google
slug: ---

Since May 2021 I have been working at running PyPy on PySide6,
which was a difficult undertaking, since PyPy internally is quite
a bit different.

I declared the project to be ready-to-use when the Mandelbrot
example of the PySide examples
	
	(examples/corelib/threads/mandelbrot.py)
is working.

This was finally solved this week on 2022-02-01, so we have the

    first advanced Gui working with PyPy

and with the amazing result of speed:

PyPy 3.8 works
     
    10 times faster than the identical code on Python 3.10
and
    
    5.5 times slower than the same example in C++ Qt.

I think to send an official announce when this is available on pip.

This effort marks the completion of my PyPy support, which began
in 2003 and ended involuntarily in 2006 due to a stroke.

All the best 


-- Christian Tismer

Note: Tismer is the creator of Stackless Python and maintainer of PySide