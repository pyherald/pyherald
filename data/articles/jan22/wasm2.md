title: CPython's main branch now compiles to webassembly! 
authors: tushar_sadhwani
note: Was much awaited!
source: https://twitter.com/sadhlife/status/1485336904342315009?s=20
tags: wasm
slug: ---


WebAssembly (WASM) is a type of code that can be run of browsers. Out there, a stack-based Virtual Machine [1] was created to run some bytecodes in the browser. Languages like C/C++, C# etc have been compiling their codes into WASM bytecodes. Something to aim for as it's supposed to have native speed [2] and is very secure. Using the JavaScript APIs allows you to interact with JS codes. There is also exitement as to it's use for server-side codes. Inside the browser it uses the JavaScript engine. Outside it needs to have it's own implementation and uses the WebAssembly System Interface (WASI) protocols for interacting with the operating system.


The PyHerald radar [detected](https://pyherald.com/articles/02_01_2022/) that awesome WASM works were in the pipeline and now's the cat is out! You can run CPython in the browser [[click-o-see]](https://repl.ethanhs.me/)! It's similar to PyOdide's console [[click-o-see]](https://pyodide.org/en/stable/console.html). PyOdide is a Python distribution for the browser and Node.js based on WebAssembly. It's much more advanced than the native CPython's version as for example it [supports](https://twitter.com/sadhlife/status/1485891963417415681?s=20) web requests. Our default one crashed on help for failing to import urllib in early versions.

It offers by default a posix system as `os.name` returns. Though limited, it's some really, really exciting news!

- [1] A Virtual Machine (VM) is just a piece of software, really.
- [2] https://developer.mozilla.org/en-US/docs/WebAssembly