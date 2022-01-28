title: Don't Shut Up Warnings You Don't Care About 
authors: steven_daprano
note: Mail by Steven D'Aprano
source: https://mail.python.org/archives/list/python-dev@python.org/message/BCEKHDT76GGG2E65DCCIX4DC6OL5CIW4/
tags: warnings
slug: ---


Or maybe, as a developer (not an end-user of an app), you could be more
proactive in reporting those warnings to the third party, and
encouraging them to fix them. Maybe even submitting a patch?

If we use a library, then we surely care about that library working
correctly, which means that if the library generates warnings, we
*should* care about them. They are advanced notice that the library is
going to break in the future.

Of course I understand that folks are busy maintaining their own
project, and have neither the time nor the inclination to take over the
maintenance of every one of their dependencies. But we shouldn't just
dismiss warnings in those dependencies as "warnings I don't care about"
and ignore them as Not My Problem.

Like it or not, it is My Problem and we should care about them.

Especially in the case of open source software, the lines of
responsibility are blurred. Open source libraries are not proprietary
black boxes with a strict division between the vender that supplies the
library and the people who use the library. They are fully transparent,
we can see the warnings and, at least potentially, see how to fix them.
And we have the legal right to.

This is a hard problem, but it is not solely a technical problem. It is
partly a social problem, and you cannot fix social problems with
technology. People are ignoring the warnings, and not just the immediate
developers of the software, but their downstream users.

The open source mantra about many eyes making bugs shallow doesn't work
when everyone is intentionally closing their eyes to the warnings of
pending bugs.

-- Steve