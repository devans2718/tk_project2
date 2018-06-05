# rewrite using either multithreading or asyncio

import pickle

import attr # rewrite without using attr
import regex
import requests
from bs4 import BeautifulSoup


@attr.s
class TomeCollector():
    n = attr.ib()
    base_url = attr.ib(f'http://grachev62.narod.ru/stalin')
    indices = attr.ib()
    items = attr.ib()

    @indices.default
    def get_indices(self):
        url = f'{self.base_url}/t{self.n}/cont_{self.n}.htm'

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        pat = regex.compile(fr't{self.n}_(\d+).htm')

        a_tags = soup.find_all('a')
        hrefs = (a.get('href') for a in a_tags)
        matches = (pat.match(h) for h in hrefs if h)
        indices = (m.group(1) for m in matches if m)

        return sorted(set(indices))

    @items.default
    def get_items(self):
        def get_item(index):
            url = f'{self.base_url}/t{self.n}/t{self.n}_{index}.htm'
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'lxml')

            title = soup.title.get_text()
            raw = soup.get_text().replace('\xa0', '')

            item = {'title': title, 'raw': raw}

            return item

        items = {index: get_item(index) for index in self.indices}

        return items


def get_tome(n): # there's gotta be a better place for this
    print(n, end='\t')

    collector = TomeCollector(n)
    indices = collector.indices

    print(f'{indices[0]}\t{indices[-1]}\t{len(indices)}')  

    return collector.items


if __name__ == "__main__":
    print('Starting...')

    for t in range(18):
        t += 1
        tome = get_tome(t)

        with open(f'raw_tomes/t{t}.pickle', 'wb') as f:
            pickle.dump(tome, f)

    print('Done.')
