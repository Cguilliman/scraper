from typing import Iterable, Tuple, Dict
from multiprocessing import Process, Queue
import asyncio

from main.changelog_parser import ChangeLogParser
from main.writer import BaseDriver


scrapers = [
	(ChangeLogParser, (), {}),
]


def writen_worker(queue: Queue):
	while True:
		driver = queue.get()
		if driver == 'END':
			return
		driver.write()


class Main:

	def init_writer(self):
		"""init addition mrocess for writing in files"""
		writen_queue = Queue()
		writen_process = Process(
			target=writen_worker, 
			args=(writen_queue, ))
		
		return writen_queue, writen_process

	def init_scrapers(self, scrapers, writen_queue):
		"""Init scrapers like tasks"""
		tasks = asyncio.gather(*[
			scraper(writen_queue, *args, **kwargs).parse(writen_queue)
			for scraper, args, kwargs in scrapers
		])
		return tasks

	def run(self, scrapers: Iterable):
		"""program entery point

			args:
				scrapers: Iterable(BaseParser, Tuple, Dict)
		"""
		writen_queue, writen_process = self.init_writer()
		writen_process.start()
		loop = asyncio.get_event_loop()
		tasks = self.init_scrapers(scrapers, writen_queue)
		loop.run_until_complete(tasks)
		writen_process.join()


if __name__ == "__main__":
	Main().run(scrapers)
