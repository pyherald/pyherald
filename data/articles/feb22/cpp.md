title: Why No C++ For The CPython Codebase
authors: None
note: Discussion started by redradist
source: https://mail.python.org/archives/list/python-dev@python.org/thread/32XOK67BGMEX2UIYVVXMHOUME56O3GJ7/
tags: cpp, rust
slug: ---



Redradist brought up one more time the issue of rewriting the CPython codebase in C++. He evoked readability, maintainability and RAII - predictable allocation and freeing of resources. 

Using C++ raises the issue of binary compatibility. If there is no binary compatibility, you can't link object files, static libraries, dynamic libraries, and executables built by different versions of compiler toolsets [1]. A core dev who is always known to support the idea of a C++ transition stated that if we are not exposing C++ bits in the public API, it does not matter. While it does sound non-intuitive, he explained that C++ templates could improve the maintainability of the generic "stringlib" routines currently based on C macros. Another example is using RAII in function bodies to help clean up owned references. For cleanup, it was suggested that C has better ways, referencing GCC's `__attribute__(cleanup(cleanup_function))`. But it seems that RII is also about moving resources, made possible by  C++'s `std::move`. Using C++ internally assumes we will have to link with libstdc++ and use C++ compatible linkers. If these tools are of high quality, there should be no worry. Another solution for binary compatibility is just to enable compilation with popular compilers.

As C++ has much more features than pure C, it seems more daunting and complex to write. It is feared that this might reduce the number of contributors. But on the other hand, if the code is more understandable and maintainable, it might attract more people. It was noted that a large part of CPython is actually Python code. So, people can still contribute without worrying of C/C++.

People requested a clear proposal, something solid enough to move the dossier forward or not. It is not a simple matter as it will require lots of effort and volunteer time to effect the change, write tests, deal with 'deep' bugs. We don't know whether or not it will enlarge the family of core devs. In short it's time for a PEP to demonstrate examples of the maintainability of C++, metrics of users willing to contribute to the C++ version, and support for all platforms currently supported. There is also the extentions API to deal with.

A core dev noted that C build times seem to be better. But it was brushed off as 'using C++ one or two times'. If people want rich data structures, they can use Python instead of hammering on C's poor support, but it was not a good line of thought as the backend was crucial for performance. The solution lies not in using Python. The organisation of the codebase was described as a maze and the incoherence of the C API was blamed on it. C++ would solve the problem it seems. 

Two more ideas worth exploring is using Cython with the C API and using rust for memory safety. But then rust is yet another language in terms of familiarity. Something C++ enjoys.  There are also concerns about rust's target architectures. 

Gregory Smith reflected that after years of experience with huge C++ codebases, he did not find readability or maintainability advantages. RAII is something he wishes to have though. The CPython codebase drafted tests to check leaks over the years. RAII he says is not a magic pill and can be wrongly used.




[1] https://docs.microsoft.com/en-us/cpp/porting/binary-compat-2015-2017?view=msvc-170