# asyncio Tutorial

In this tutorial, I used and modified examples from
the [Python documentation](https://docs.python.org/3/library/asyncio.html) and
[this github page](https://gist.github.com/showa-yojyo/4ed200d4c41f496a45a7af2612912df3).
I recommend exploring these pages/examples to get a better understanding of ```asyncio```.

In traditional Python program, when a function ```f()``` calls another function ```g()```, the Python
interpreter will immediately pass execution to ```g()```. Once ```g()``` completes, execution will return to ```f()```.
By using the ```asyncio``` library, we can allow a function ```f()``` to call two functions ```g()```
and ```h()``` so that the execution of ```g()``` and ```h()``` appears simultaneous (or concurrent).
In reality, however, execution is not simultaneous. Instead, ```g()``` and ```h()``` are designed to
implicitly pass execution between each other.

To explain this in more detail, we need some terminology.
A **coroutine** is a function that can can pause its execution to let other coroutines execute.
In the above paragraph, ```g()``` and ```h()``` are coroutines.
Coroutines are designated in Python by ```async def```.
Whenever we call a coroutine ```f()```, we must write ```await f()``` or ```out = await f()```
(if we want to save the coroutine output).
The following example shows how coroutines can behave just like regular functions, albeit with extra keywords:

https://github.com/brandonbate/async-tutorial/blob/17bc30030bf8966b02e78524514f30fe909866f7/example1.py#L1-L9

Simply using they keywords ```async``` and ```await``` will not cause coroutines to pass execution to
each other. In the following example, the two function calls to ```say_after``` do not appear to run
simultaneously:

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example2.py#L1-L12

We allow coroutines to pass off execution to each other by creating **tasks** for them.
Behind the scene, Python runs an **event loop** that keeps a list of our tasks.
When the coroutine of a task reaches a point where it pauses execution, the event loop takes over and
runs the next task. Iteration through the list of tasks will continue in this way until we return to the
original coroutine.

In the following example, we create two tasks.
Execution in ```task1``` is paused when we reach ```await asyncio.sleep(delay)``` in the ```say_after``` coroutine.
This command allows the event loop to begin executing ```task2```.
In ```task2```, once we reach ```await asyncio.sleep(delay)``` in the ```say_after```
coroutine, the event loop passes execution back to ```task1```.
If the desired delay amount has not yet elapsed within ```task1```, control will once again be returned
to the event loop, which will then return execution to ```task2```. After many iterations, ```task1``` will
eventually satisfy the sleep requirement, and so execution of ```say_after``` will proceed
and thereby terminate ```task1```. The same will occur for ```task2```.

https://github.com/brandonbate/async-tutorial/blob/a7309a3c0f8fbaddfb0c9e604d27c1e41534b6c8/example3.py#L1-L16

Execution of ```task1``` begins when ```await task1``` is called within ```main```.
Execution in ```main``` is paused until ```task1``` completes, but remarkably,
```task2``` executes as well. That's because ```task2 = asyncio.create_task(say_after(3, 'world'))```
adds ```task2``` to the event loop (without executing it). Once ```task1``` pauses execution,
```task2``` will immediately take over.
When running on my local machine, I can see the output of ```task2``` even if the ```await task2``` line is
removed. The ```await task2``` command exists simply to ensure that your Python program doesn't end
before task2 completes. It doesn't actually cause ```task2``` to execute.

Here is another example that illustrates ```asyncio``` operates:

https://github.com/brandonbate/async-tutorial/blob/fc5afd01257e3228bcb1bb5676d89f14b6b60d67/example4.py#L1-L14

In the above example, we use ```asyncio.gather(...)``` to automatically create and execute three tasks for
the ```count``` coroutine.
The event loop hands off execution to the first task. This first task runs uninterrupted until it encounters
```await asyncio.sleep(1)```. It then passes execution to event loop which passes execution to the second task.
This pattern continues until sleep requirements are satisified.
Because ```time.sleep``` is not a coroutine, execution of coroutines is not passed to the event loop when this
command executes.

Here is a breif description of some of the important commands needed to create and manage tasks in ```asyncio```:

* ```asyncio.run(...)``` runs a single coroutine to the exclusion of other coroutines.
* ```asyncio.create(...)``` initiates a single task that runs a coroutine through the event loop.
* ```asyncio.gather(...)``` initiates mutliple tasks that run coroutines through the event loop.

In Django, we use ```sync_to_async``` to make a traditional function (defined by ```def```) appear as though
its a coroutine (defined by ```async def```). But if ```f(input)``` is a traditional function, then it has no
```await``` methods within it to pause execution. Thus ```sync_to_async(f)(input)``` will never return
control to the event loop when it executes. We use ```sync_to_async``` when working with ASGI applications
because such programs require all functions to be coroutines.
A similar function is ```async_to_sync```. This allows a coroutine to NOT pass control to the event loop when it executes.

The ```asyncio``` library is ideal in applications where there are potentially long delays due to communication.
That's why ```asyncio``` is used with to create ASGI applications.
The next example is meant to simulate the a processing scenario that deals with communcation/processing delays.
To model this, we need to understand queues.
A queue is a data structure where items are added in a "first-in"/"first-out" basis. The ```asycio.Queue``` allows
coroutines to add and remove from the queue. In the following example, we create tasks that call the ```consume```
and ```produce``` functions. We call these tasks "consumers" and "producers". A producer will wait a random length
of time and then add a random letter to the queue. A consumer will wait a random length of time then take an item
from the queue. We use infinite loops to make this behavior continue. You can stop execution of this program by
typing ```CTL + C```.

https://github.com/brandonbate/async-tutorial/blob/9db3525f8c581196ae784cf0ad97a22667afb3c9/example5.py#L1-L31
