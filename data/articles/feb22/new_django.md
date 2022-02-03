title: What's New In Django Security Releases
authors: adam_johnson
note: By Adam Johnson
source: https://twitter.com/AdamChainz/status/1488622545289060357?s=20&t=LhdIkz7aKdMcV9BTovEwfA
tags: django, security
slug: ---

1 🔒 The {% debug %} tag was found to be an XSS vector, since it didn't escape variables. I don't recall seeing anyone use the tag, so you're probably safe... But it still could easily be in a template somewhere!

Thanks to @kezabelle, @m_holtermann and @MariuszFelisiak

2 🔒 Files uploaded using 'Content-Transfer-Encoding: baes64' but not enough data could cause an infinite loop. This is a bad DoS vector!

Thanks to Alan Ryan and @MariuszFelisiak

3 🧪 TestCase.captureOnCommitCallbacks() didn't handle recursive callbacks correctly.

Thanks to Petter Friberg for the report and PR, and @MariuszFelisiak for review. I backported the fix to my Django <4.0 package: https://pypi.org/project/django-capture-on-commit-callbacks/

4 ...and a bunch of other small regressions in Django 4.0. I guess a bunch have been discovered as folks upgrade and start to use new features.

I discovered one on friday [for QuerySet.aggregate()], which 
@MariuszFelisiak fixed real quick in time for the release Clapping hands sign


-- Adam Johnson, [@AdamChainz](https://twitter.com/AdamChainz)