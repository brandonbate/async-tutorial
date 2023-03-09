# Async Tutorial

In traditional programming, when a function ```f()``` calls another function ```g()```, our program will
immediately pass execution to the ```g()```. Once ```g()``` completes, execution will be returned to ```f()```.
By using the ```ayncio``` library, we can allow a function ```f()``` to call two functions ```g()```
and ```h()``` so that the execution of ```g()``` and ```h()``` appears simultaneous (or concurrent).
In reality, however, execution is not simultaneous. Instead, ```g()``` and ```h()``` are designed to
implicitly pass execution between each other.

To explain this in more detail, we need use terminology.
A **coroutine** is a function that can can pause its execution while other coroutines execute.
In the above paragraph, we say would say that ```g()``` and ```h()``` are coroutines.
These are designated in Python by ```async def```.
Whenever we call a coroutine ```f()```, we must write ```await f()``` or ```out = await f()```
(if we want to save the coroutine output).
The following example shows how coroutines can behave just like regular functions, albeit with extra keywords:

https://github.com/brandonbate/async-tutorial/blob/17bc30030bf8966b02e78524514f30fe909866f7/example1.py#L1-L9

Simply using they keywords ```async``` and ```await``` will not cause coroutines to pass execution to
each other. In the following example, the two function calls to ```say_after``` do not appear to run
simultaneously:

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example2.py#L1-L12

We can allow coroutines to pass off execution to each other by creating **tasks** for them.
Behind the scence, Python runs an **event loop** that executes the coroutine to each task.
Simply creating a task automatically causes our coroutines to be called by the event loop.
When 

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example3.py#L1-L16

The following example gives a more explicit description of how this event loop works.

https://github.com/brandonbate/async-tutorial/blob/fc5afd01257e3228bcb1bb5676d89f14b6b60d67/example4.py#L1-L14

In the above example, we use ```asyncio.gather(...)``` to create three tasks for the ```count``` coroutine.
The event loop hands off execution to the first task. This first task runs uninterrupted until it encounters
```await asyncio.sleep(1)```. 

This results in the ```count``` coroutine being executed concurrently. We have two ```sleep``` commands
in ```count```. The first


	asyncio.run(...) runs a single coroutine to the exclusion of other coroutines.
	asyncio.create(...) initiates a single coroutine to run concurrently with other coroutines.
	asyncio.gather(...) initiates mutliple coroutines to run concurrently with other coroutines.
