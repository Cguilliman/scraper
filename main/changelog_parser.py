import asyncio

from bs4 import BeautifulSoup

from .base import BaseParser
from .writer import SimpleFileDriver


class ChangeLogParser(BaseParser):
    base_link = 'https://changelog.com/'
    writer = SimpleFileDriver

    def write_errors_logs(self, response):
        print(f"ERROR: {response}")

    async def form_object_list(self, response):
        text = await response.text()
        soup = BeautifulSoup(text)
        data = []

        for obj in soup.find_all('article'):
            blocks = obj.find_all(class_='news_item-title')
            if blocks:
                data.append({'url': blocks[0].a.get('href')})

        return data

    def get_object_list_kwargs(self):
        yield {"url": f"{self.base_link}"}
        # for page in range(2, 10):
        #     yield {"url": f"{self.base_link}?page={page}#feed"}

    def get_object_kwargs(self, obj):
        return obj

    async def form_object(self, response, list_obj):
        """form object data"""
        text = await response.text()
        return text, list_obj['url']

