import threading
from time import sleep
import asyncio
import aiohttp


async def fetch(num: str):
	async with aiohttp.ClientSession() as session:
		async with session.get('https://habr.com/post/149420/') as response:
			if response.status == 200:
				text = await response.text()
				print(num, ': ', text[:20])


def some():
	for i in range(15):
		sleep(0.1)
		print(i)


loop = asyncio.get_event_loop()
tasks1 = asyncio.gather(
    fetch('11'),
    fetch('12'),
    fetch('13'),
    fetch('14'),
    fetch('15'),
    fetch('16')
)

e1 = threading.Event()
e2 = threading.Event()

t1 = threading.Thread(target=loop.run_until_complete, args=(tasks1, ))
t2 = threading.Thread(target=some)

t1.start()
t2.start()

e1.set()

t1.join()
t2.join()
