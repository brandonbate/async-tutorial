import asyncio
import random
import string

async def produce(name, queue):

    while True:
        await asyncio.sleep(random.uniform(1,5))
        random_letter = random.choice(string.ascii_letters)
        print("P" + str(name) + " produced " + str(random_letter))
        await queue.put((name, random_letter))
        
async def consume(name, queue):

    while True:
        producer_name, random_letter = await queue.get()
        print("C" + str(name) + " got " + str(random_letter) + " made by P" + str(producer_name))
        await asyncio.sleep(random.uniform(1,5))
        queue.task_done()

async def main():
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(3)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(2)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    asyncio.run(main())
