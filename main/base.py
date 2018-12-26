import aiohttp
import asyncio
from random import randint
from typing import Dict, List, Generator, Any, Iterable

from .writer import BaseDriver

__all__ = ()


class BaseParser:
    base_link: str
    writer: BaseDriver

    def __init__(self, writen_queue, *args, **kwargs):
        self.session_cls = lambda: aiohttp.ClientSession(*args, **kwargs)
        self.writen_queue = writen_queue
        self.session = None

    def write_errors_logs(self, response):
        pass # TODO: mb we need to write some logs

    async def form_object_list(self, response) -> Iterable:
        raise NotImplemented()
        # return await response.text()

    def get_object_list_kwargs(self) -> Generator:
        """
            THIS IS GENERATOR
            implement pagination or anther shit

            yield: Dict
        """
        raise NotImplemented()

    async def get_object_list(self) -> Generator:
        """
            get list of objects
            implement pagination and ather logic
        """
        for kw in self.get_object_list_kwargs():
            async with self.session.get(**kw) as response:
                if response.status == 200:
                    objects = await self.form_object_list(response)  # TODO: remove me
                    for obj in objects:
                        yield obj
                else:
                    self.write_errors_logs(response)
                    next

    async def form_object(self, response, list_obj) -> Any:
        """form object data"""
        return await response.text(), list_obj

    def get_object_kwargs(self, obj) -> Dict:
        """get object kwargs for response"""
        raise NotImplemented()

    async def get_object(self, obj) -> Any:
        """
            get all `detail` information
        """
        async with self.session.get(**self.get_object_kwargs(obj)) as response:
            if response.status == 200:
                return await self.form_object(response, obj)
            else:
                self.write_errors_logs(response)
                return False

    async def write_object(self, queue, data, list_obj):  # DOTO: crap, refactor me
        """
            write inforamation
            use some writing driver
        """
        queue.put(self.writer(data=data, title=str(randint(1, 100))))
        # self.writen_queue.put(
        #     self.writer(data=data, title=title)
        # )


    async def parse(self, queue):
        """entery point"""
        async with self.session_cls() as session:
            self.session = session  # DSICUSE: mb shitty
            async for obj in self.get_object_list(): # generator with futures
                detail = await self.get_object(obj)
                if detail:
                    await self.write_object(queue, *detail)
        queue.put('END')
