import asyncio
import time

async def count():
    print("One")
    time.sleep(1)
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    asyncio.run(main())
