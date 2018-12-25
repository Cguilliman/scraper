import aiohttp
import asyncio


class BaseParser:
	base_link: str
	writer = None

	def __init__(self, *args, **kwargs):
		self.session_cls = lambda: aiohttp.ClientSession(*args, **kwargs)
		self.session = None

	def write_errors_logs(self, response):
		pass # TODO: mb we need to write some logs

	def form_object_list(self, response):
		return response.text()

	# def get_object_list_url(self, )

	async def get_object_list(self):
		"""
			get list of objects
			implement pagination and ather logic
		"""
		# await for  
		async with self.session.get() as response:
			if response.status == 200:
				return self.form_object_list(response)
			else:
				self.write_errors_logs(response)

	async def get_object(self, obj):
		"""
			get all `detail` information
		"""
		raise NotImplemented()

	async def write_object(self, data):
		"""
			write inforamation
			use some writing driver
		"""
		raise NotImplemented()

	async def prase(self):
		"""entery point"""
		async with self.session_cls() as session:
			self.session = session  # DSICUSE: mb shitty
			await for obj in self.get_object_list(): # generator with futers
				detail = await self.get_object(obj)
				await self.write_object(detail)


# async def fetch(session, url):
# 	async with session.get(url) as response:
# 		if response.status == 200:
# 			return await response.text()
# 		else:
# 			return f"ERROR: {response.status}"


# async def download(article):
# 	async with aiohttp.ClientSession() as session:
# 		html = await fetch(session, f"https://ru.wikipedia.org/{article}")
# 		return html[:15]


# loop = asyncio.get_event_loop()
# tasks = asyncio.gather(
# 	download('wiki/Космическое_пространство'),
# 	download('asdasd'),
# )
# print(tasks)
# loop.run_until_complete(tasks)