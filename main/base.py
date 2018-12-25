import aiohttp
import asyncio
from typing import Dict, List, Generator, Any, Iterable

__all__ = ()


class BaseParser:
    base_link: str
    writer = None

    def __init__(self, *args, **kwargs):
        self.session_cls = lambda: aiohttp.ClientSession(*args, **kwargs)
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

    async def form_object(self, response) -> Any:
        """form object data"""
        return await response.text()

    def get_object_kwargs(self, obj) -> Dict:
        """get object kwargs for response"""
        raise NotImplemented()

    async def get_object(self, obj) -> Any:
        """
            get all `detail` information
        """
        async with self.session.get(**self.get_object_kwargs(obj)) as response:
            if response.status == 200:
                return await self.form_object(response)
            else:
                self.write_errors_logs(response)
                return False

    async def write_object(self, data):
        """
            write inforamation
            use some writing driver
        """
        raise NotImplemented()

    async def parse(self):
        """entery point"""
        async with self.session_cls() as session:
            self.session = session  # DSICUSE: mb shitty
            async for obj in self.get_object_list(): # generator with futures
                detail = await self.get_object(obj)
                if detail:
                    await self.write_object(detail)
