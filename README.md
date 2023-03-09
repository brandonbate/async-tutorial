# Async Tutorial

A **coroutine** is a function that can run concurrently with other coroutines.
These are designated in Python by ```async def```.
Whenever we call a coroutine ```f()```, we must write ```await f()``` or ```out = await f()```
(if we want to save the coroutine output).
The following example shows how coroutines can behave just like regular functions, albeit with extra keywords:

https://github.com/brandonbate/async-tutorial/blob/17bc30030bf8966b02e78524514f30fe909866f7/example1.py#L1-L9

Simply using they keywords ```async``` and ```await will not cause coroutines to execute concurrently.
In the following example, the two function calls to ```say_after``` do not run concurrently:

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example2.py#L1-L12

We can allow coroutines to run concurrently if we create **tasks** for them.
Behind the scence, Python runs an **event loop** that executes tasks concurrent.
Notice that simply creating a task automatically causes our coroutines to be executed concurrently
by the event loop:

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example3.py#L1-L16

Suppose we have a function ```g()``` in which we have an ```await f()```.
Program execution of ```g()``` will be paused once we encounter ```await f()```.
At this point, Python will begin execting ```f()```.
If we have a single-core machine, Python may temporarily switch between executing ```f()``` and other coroutines.
If we have a multi-core machine, Python may allow ```f()``` to execute on one of these cores while other
coroutines execute on other cores.
Whatever the case, execution in ```g()``` will remained pause until the ```f()``` coroutine completes.

	asyncio.run(...) runs a single coroutine to the exclusion of other coroutines.
	asyncio.create(...) initiates a single coroutine to run concurrently with other coroutines.
	asyncio.gather(...) initiates mutliple coroutines to run concurrently with other coroutines.
