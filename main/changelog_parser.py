import asyncio

from bs4 import BeautifulSoup

if __name__ == '__main__':
    from base import BaseParser
else:
    from .base import BaseParser


class ChangeLogParser(BaseParser):
    base_link = 'https://changelog.com/'

    def write_errors_logs(self, response):
        print(f"ERROR: {response}")

    async def form_object_list(self, response):
        text = await response.text()
        soup = BeautifulSoup(text)
        data = [
            {'url': (
                soup
                .find_all('article')[0]
                .find_all(class_='news_item-title')[0]
                .a.get('href')
            )}
            for obj in soup.find_all('article')
        ]
        return data

    def get_object_list_kwargs(self):
        yield {"url": f"{self.base_link}"}
        for page in range(2, 10):
            yield {"url": f"{self.base_link}?page={page}#feed"}

    def get_object_kwargs(self, obj):
        return obj

    async def write_object(self, data):
        print('=====')
        print(data[:15])


# only for test
loop = asyncio.get_event_loop()
tasks = asyncio.gather(
    ChangeLogParser().parse()
)
loop.run_until_complete(tasks)
