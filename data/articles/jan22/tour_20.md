title: What's Happening in PythonLand?
authors: abdur-rahmaanj
note: Guided tour
source: ---
tags: 
slug: ---

[PEP 665](https://www.python.org/dev/peps/pep-0665/) -- A file format to list Python dependencies for reproducibility of an application got rejected. Brett's [thinking](https://twitter.com/brettsky/status/1481069172314550276?s=20) of developing his own opinionated solution for wheel-only lock files. The [reason for rejection](https://discuss.python.org/t/pep-665-take-2-a-file-format-to-list-python-dependencies-for-reproducibility-of-an-application/11736/140) is the lack of sdist support which was enough to cause a lukewarm reception overall to the PEP. However, Paul Moore does concede that we definitely need a lockfile format that’s better than the current “pinned requirements file” approach, noting recent examples of supply chain issues with npm and similar demonstrate that locking is becoming far more critical.


 
[PEP 654](https://www.python.org/dev/peps/pep-0654/) -- Exception Groups and except* [gets accepted](https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813)


Brett is [stepping back](https://mail.python.org/archives/list/python-committers@python.org/thread/GB7T23XWLNKR24V5IWBADYSLFK6KWCY6/) from being the person in charge of infrastructure



[Arbitrary Literal Strings PEP](https://docs.google.com/document/d/1fbAbA2MCoAcSO1c8gecmUJYZ-Q0utT3CmaXlQ3IhzZw/edit) is still brewing.