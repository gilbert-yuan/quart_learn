# modified fetch function with semaphore
from datetime import datetime
import asyncio
from aiohttp import ClientSession

async def fetch(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def bound_fetch(sem, url):
    # getter function with semaphore
    async with sem:
        await fetch(url)

async def run(loop,  r):
    url = "http://localhost:5000/get/sale/order/line/S17112224002"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)
    for i in range(r):
        # pass Semaphore to every GET request
        task = asyncio.ensure_future(bound_fetch(sem, url.format(i)))
        tasks.append(task)
    responses = asyncio.gather(*tasks, return_exceptions=True)
    await responses

print(datetime.now(), '--------')
number = 10000
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
future = asyncio.ensure_future(run(loop, number))
loop.run_until_complete(future)
print(datetime.now(), '--------')


