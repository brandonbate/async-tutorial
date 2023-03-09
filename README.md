# Async Tutorial

A **coroutine** is a function that can run concurrently with other coroutines.
These are designated in Python by ```async def```.
**Tasks** are used to schedule coroutines concurrently.
This is done "behind the scences" using an **event loop**.
Whenever we call a coroutine ```f()```, we must write ```await f()``` or ```out = await f()``` (if we want to
save the coroutine output).

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
