import asyncio

async def aa():
	for i in range(10):
		yield i


async def bb():
	s = aa()
	print(s)
	async for i in s:
		print(i)



loop = asyncio.get_event_loop()
tasks = asyncio.gather(
	bb()
)
loop.run_until_complete(tasks)