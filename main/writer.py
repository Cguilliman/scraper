from multiprocessing import Process, Queue


class BaseDriver:

	def __init__(self, data, title):
		self.data = data
		self.title = title

	def write(self):
		raise NotImplemented()


class SimpleFileDriver(BaseDriver):

	def write(self):
		with open(f"parsed/{self.title}.txt", 'w') as _file:
			_file.write(self.data)
