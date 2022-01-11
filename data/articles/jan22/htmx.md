title: HTMX: How Python Fueled the Rise of a JS Lib
authors: htmx_author
note: For a leaner future
source: https://www.reddit.com/r/django/comments/rxjlc6/comment/hrimfuf/?utm_source=share&utm_medium=web2x&context=3
tags: htmx
slug: ---


Hi there, I'm the creator of htmx.

I think htmx managed to catch a wave of discontent with existing javascript frameworks that are very complicated and often turn Django into a dumb-JSON producer. htmx plays better with Django out of the box because it interacts with the server via HTML, which Django is very, very good at producing, so it lets Django developers stay in Django & Python, rather than kicking out to Javascript for 50+% of their web applications.

I was invited on a few Django/Python podcasts and it kind of took off from there:

[https://djangochat.com/episodes/htmx-carson-gross](https://djangochat.com/episodes/htmx-carson-gross)

[https://talkpython.fm/episodes/show/321/htmx-clean-dynamic-html-pages](https://talkpython.fm/episodes/show/321/htmx-clean-dynamic-html-pages)

What's funny is that htmx is really intercooler.js 2.0, which I started working on back in 2013. In 2020, I rewrote intercooler.js without the jQuery dependency and renamed it to htmx, which I think better captures the idea (extending HTML). So this is another example of a decade-long overnight success :)

I'm very surprised and very glad that the Django community has embraced it as quickly and dramatically as they have!