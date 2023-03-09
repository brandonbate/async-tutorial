import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    await say_after(2, 'hello')
    await say_after(6, 'world')

if __name__ == "__main__":
	asyncio.run(main())