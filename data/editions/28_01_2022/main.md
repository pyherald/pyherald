## CPython's main branch now compiles to webassembly!

_[src](https://twitter.com/sadhlife/status/1485336904342315009?s=20), Was much awaited!_


WebAssembly (WASM) is a type of code that can be run of browsers. Out there, a stack-based Virtual Machine [1] was created to run some bytecodes in the browser. Languages like C/C++, C# etc have been compiling their codes into WASM bytecodes. Something to aim for as it's supposed to have native speed [2] and is very secure. Using the JavaScript APIs allows you to interact with JS codes. There is also exitement as to it's use for server-side codes. Inside the browser it uses the JavaScript engine. Outside it needs to have it's own implementation and uses the WebAssembly System Interface (WASI) protocols for interacting with the operating system.


The PyHerald radar [detected](https://pyherald.com/articles/02_01_2022/) that awesome WASM works were in the pipeline and now's the cat is out! You can run CPython in the browser [[click-o-see]](https://repl.ethanhs.me/)! It's similar to PyOdide's console [[click-o-see]](https://pyodide.org/en/stable/console.html). PyOdide is a Python distribution for the browser and Node.js based on WebAssembly. It's much more advanced than the native CPython's version as for example it [supports](https://twitter.com/sadhlife/status/1485891963417415681?s=20) web requests. Our default one crashed on help for failing to import urllib in early versions.

It offers by default a posix system as `os.name` returns. Though limited, it's some really, really exciting news!

- [1] A Virtual Machine (VM) is just a piece of software, really.
- [2] https://developer.mozilla.org/en-US/docs/WebAssembly

---

## The Perfect Example To Understand AsyncIO

_[src](https://twitter.com/mathsppblog/status/1484237419494838272?s=20), A well-cooked analogy_


Rodrigo (@Mathsppblog) came up with the perfect thread on understanding AsyncIO:

I just came up with the perfect analogy to help you understand asyncio in Python 🐍

You can thank me later 😊

Buckle up 🚀

Let me tell you about my lunch today.

For lunch, I had some pasta, some meatloaf, and some avocado. The meatloaf was in the fridge, I only had to reheat it. The avocado needed peeling. I had no pasta already cooked, so I had to cook it before lunch.

Here's how I did it:

I got up from the computer, walked into the kitchen. Filled a pot with water, brought the water to a boil, and put some pasta in. Stared at the pot while the pasta cooked for like 10min, or something. When done, I put the pasta aside.

Then, I opened the fridge, took some meatloaf, put it on my plate. Put the plate in the microwave. Stared at it.

DING 🛎️

Got the plate out. Served some recently-cooked pasta.

Went to the fridge, grabbed an avocado 🥑. Peeled it and sliced it. Served it on my plate. Had lunch. 🍽️

Now, if you are ANYTHING like me, you are staring at your screen, screaming 😨😨😨

Why the heck did I stare at the pot of cooking pasta? Why didn't I take care of the meatloaf while the pasta cooked? Or peeled the avocado?

You know why? Because this is MY ANALOGY.

In my cooking analogy, the story I just told you about is that of a program that does things one after the other, always in sequence.

It's a synchronous program.

Here is what this could look like in code 👇

```python
import time

def cook_pasta():
    print("Filled pot with water. Pasta will now cook.")
    time.sleep(10)  # Pasta takes 10 min to cook.
    print("Pasta ready.")

def heat_meatloaf():
    print("Took meatloaf out of the fridge. Into the microwave it goes.")
    time.sleep(3)  # Meatloaf takes 3 min to heat.
    print("Meatloaf heated.")

def peel_avocado():
    print("Grabbed avocado. Now peeling and slicing.")
    time.sleep(2)  # Avocado takes 2 min to peel <- I'm slow.
    print("Avocado sliced.")

def lunch():
    print("Preparing lunch.")
    start = time.time()
    cook_pasta()
    heat_meatloaf()
    peel_avocado()
    end = time.time()
    print(f"Eating after {round(end - start)} min of prep time.")

lunch()
```

By the time the program is ran, can you tell how much time it says I took preparing my lunch?

10 min for the pasta, followed by
3 min for the meatloaf, followed by
2 min for the avocado:
15 min in total.

Here is the output of the code 👇

```
Preparing lunch.
Filled pot with water. Pasta will now cook.
Pasta ready.
Took meatloaf out of the fridge. Into the microwave it goes.
Meatloaf heated.
Grabbed avocado. Now peeling and slicing.
Avocado sliced.
Eating after 15 min of prep time.
Seems rather inefficient, right?
```

I agree... But I'm just not organised enough to know what to do while I'm waiting, so I need your help, ok?

I'll prepare lunch, and whenever I have to wait for something, I'll ask YOU what to do next, and you'll let me know what to do, ok?

Here we go!

I start by cooking the pasta in the pot. When the pasta is starting to cook, I notify you: hey, I'm waiting for the pasta. What can I do meanwhile?

You look around and say: go take care of the meatloaf. Your wish is my command!

I open the fridge, take the meatloaf out. Put it in the microwave. When the microwave starts going, I notify you: hey, I'm waiting for the meatloaf. What can I do meanwhile?

You look around and say: go take care of the avocado. Your wish is my command!

I open the fridge, take the avocado out. Peel it and slice it. When I'm done, I notify you: I'm done with the avocado. What now?

You look around and say: check the meatloaf. Your wish is my command!

I walk up to the microwave, and notice it's about to finish heating the meatloaf.

DING 🛎️

It's done. I put the meatloaf and avocado in a plate.

You then look around and say: go check the pasta! (Right, it's the only thing missing!) Your wish is my command!

I walk up to the pot of boiling water and cooking pasta, and just wait for it to finish. When it's done, I serve some pasta and go have lunch.

How much time did I spend in the kitchen, now? Only 10 min!

While the pasta was boiling, I managed to turn my attention to other stuff, because you 🧑‍🍳 helped me!

Your job was to manage me and optimise the times I was standing by and waiting for things outside of my control:

boiling pasta
heating in the microwave
That is what asyncio is for. To use asyncio, you need two ingredients:

tasks that take time but don't depend on you;

someone, or something, to order you around while you are waiting for some things to finish.

Your job was VERY important, although nuanced.

Let's take the synchronous code I had from before, and write it as an asynchronous piece of code.

First, let's look at cook_pasta and heat_meatloaf.

For those two, I had moments when I was doing nothing, right? That's why I notified you and asked for other tasks.

This “notification” is a very important step, and you do it with the keyword await.

When the pasta is put to boil, you “await” for it to be ready and do something else. When the meatloaf is put in the microwave, you “await” for it to be ready and do something else.

```python
import time
import asyncio

async def cook_pasta():
    print("Filled pot with water. Pasta will now cook.")
    await asyncio.sleep(10)  # Pasta takes 10 min to cook.
    print("Pasta ready.")

async def heat_meatloaf():
    print("Took meatloaf out of the fridge. Into the microwave it goes.")
    await asyncio.sleep(3)  # Meatloaf takes 3 min to heat.
    print("Meatloaf heated.")
```

But wait, what's that asyncio.sleep? Why can't I just use time.sleep?

Do you understand the idea of me asking for your help to decide what to do next while I'm waiting for the pasta to boil/meatloaf to reheat?

Well, that's done with the await keyword, BUT ... It needs something specific on the right of await!

It needs an object that is aware of this whole situation, and that understands that I might have better things to do than just stand still while waiting.

Because that's what time.sleep does. It just waits quietly.

However, the coroutine asyncio.sleep is more understanding: it understands you might have better things to do.

That is also why your cook_pasta and heat_meatloaf now have the keyword async to the left of def:

They build coroutines. Try to run cook_pasta():

```
>>> cook_pasta()
<coroutine object cook_pasta at 0x000001DDE47571C0>
```

It doesn't “run” in the sense we are used to. It just builds a coroutine that will start running when you tell me to start working on it.

Coroutines are just objects that make part of this whole “notify me of what to do next” game.

So, inside your async def definitions, you just put an await when you know you can do something else while waiting for that to finish.

You just have to be careful, though: what's on the right of await needs to be aware of the async game going on.

After you define your tasks and determine in what places you can switch focus, you just have to take care of:

👉 the someone, or something, that decides on what I should focus next.

That's a job asyncio already knows how to do, thankfully 😅 It's called the event loop.

We have a series of tasks that we want to switch back and forth from, right? It's a bunch of them.

So, we use asyncio.gather to literally gather all those tasks together, and let the event loop (you, the manager) switch the focus back and forth.


```python
async def lunch():
    print("Preparing lunch.")
    start = time.time()
    await asyncio.gather(
        cook_pasta(),
        heat_meatloaf(),
        peel_avocado(),
    )
    end = time.time()
    print(f"Eating after {round(end - start)} min of prep time.")

```
Finally, to get the program going, we need to call asyncio.run, which takes a coroutine and kicks things off.

It is essentially equivalent to the moment you walk up to me and say: Rodrigo, go in the kitchen and starting preparing lunch.

```python
# ...

async def lunch():
    print("Preparing lunch.")
    start = time.time()
    await asyncio.gather(
        cook_pasta(),
        heat_meatloaf(),
        peel_avocado(),
    )
    end = time.time()
    print(f"Eating after {round(end - start)} min of prep time.")

asyncio.run(lunch())
```

This stuff isn't easy.

Convince yourself that the cooking analogy makes sense. When it does, slowly compare the analogy with the code. You will get some intuition behind what's happening. That's how “understanding” starts.

Now, what about peel_avocado? I left it out 👇


```python
async def peel_avocado():
    print("Grabbed avocado. Now peeling and slicing.")
    time.sleep(2)  # Avocado takes 2 min to peel <- I'm slow.
    print("Avocado sliced.")
```

Wait, what?! peel_avocado has async def but no await?! What?!

It has async def because it is aware of this whole game of switching back and forth. Thus, it's a coroutine function.

However, it has no await because I can't walk away from the avocado!

The avocado won't peel itself, right? I have to do it. I have to spend 2 whole minutes peeling the avocado and slicing it. That's what time.sleep does.

Only when I'm completely done with the avocado, and the coroutine finishes, you can tell me to do something else.

This is another key idea:

I can only switch to work on something else at specific points in the program. And I mark those times with await.

And that only works as long as I am “awaiting” for something that actually speaks the async language.

Here is all the async code 👇


```python
import time
import asyncio

async def cook_pasta():
    print("Filled pot with water. Pasta will now cook.")
    await asyncio.sleep(10)  # Pasta takes 10 min to cook.
    print("Pasta ready.")

async def heat_meatloaf():
    print("Took meatloaf out of the fridge. Into the microwave it goes.")
    await asyncio.sleep(3)  # Meatloaf takes 3 min to heat.
    print("Meatloaf heated.")

async def peel_avocado():
    print("Grabbed avocado. Now peeling and slicing.")
    time.sleep(2)  # Avocado takes 2 min to peel <- I'm slow.
    print("Avocado sliced.")

async def lunch():
    print("Preparing lunch.")
    start = time.time()
    await asyncio.gather(
        cook_pasta(),
        heat_meatloaf(),
        peel_avocado(),
    )
    end = time.time()
    print(f"Eating after {round(end - start)} min of prep time.")

asyncio.run(lunch())

```

And this is the output it produces 👇

```
Preparing lunch.
Filled pot with water. Pasta will now cook.
Took meatloaf out of the fridge. Into the microwave it goes.
Grabbed avocado. Now peeling and slicing.
Avocado sliced.
Meatloaf heated.
Pasta ready.
Eating after 10 min of prep time.
The pasta still takes 10 minutes.
The meatloaf still takes 3 minutes.
The avocado still takes 2 minutes.
I'm just being smarter about managing my time.
```

Some conclusions:

👉 async def defines coroutine functions

👉 coroutine functions build coroutines

👉 coroutines are better at managing time

👉 with await, you can do something useful while waiting for something else to finish

👉 await obj needs obj to be awaitable



---

## Don't Shut Up Warnings You Don't Care About

_[src](https://mail.python.org/archives/list/python-dev@python.org/message/BCEKHDT76GGG2E65DCCIX4DC6OL5CIW4/), Mail by Steven D'Aprano_


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

---

## What's happening in PythonLand?

_[src](---), _

There is an [ongoing vote](https://discuss.python.org/t/vote-to-promote-dennis-sweeney/13351) to promote Phd student [Dennis Sweeney](https://github.com/sweeneyde). Coming from Tim Peters and publicly approved by Guido, we expect him on the core devs list soon!

With [less than 1%](https://twitter.com/di_codes/status/1486398470479130624?s=20&t=b_GFjGyWkOj9c_3gXdvRtg) of builds on pypi, .egg might vanish very soon! The Warehouse is looking [to hear](https://github.com/pypa/warehouse/issues/10653) from the last .egg folks.


Python2.7 [refuses to die](https://github.com/JulienPalard/python-versions) according to pypi downloads

[PEP 678](https://www.python.org/dev/peps/pep-0678/) -- Enriching Exceptions with Note appears. Basically adding `.__note__` to exceptions.

---

