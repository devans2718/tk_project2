"""Collect and pickle Stalin's works as a list of Items"""

from itertools import chain
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

import regex
import requests
from bs4 import BeautifulSoup

from common import Item


def get_urls(n):
    """Generate the urls for each item in tome n"""

    BASE_URL = f'http://grachev62.narod.ru/stalin/t{n}'

    req = requests.get(f'{BASE_URL}/cont_{n}.htm')
    soup = BeautifulSoup(req.content, 'lxml')
    pat = regex.compile(fr't{n}_(\d+).htm')

    a_tags = soup.find_all('a')
    hrefs = (a.get('href') for a in a_tags)
    matches = (pat.match(h) for h in hrefs if h)
    indices = sorted(set((m.group(1) for m in matches if m)))

    yield from (f'{BASE_URL}/t{n}_{i}.htm' for i in indices)


def get_items(urls):
    """Generate the items found at urls"""
    with ThreadPoolExecutor(20) as executor:
        futures = {executor.submit(requests.get, url): url for url in urls}

        for fut in as_completed(futures):
            soup = BeautifulSoup(fut.result().content, 'lxml')
            yield Item(soup.title.get_text(),
                       soup.get_text().replace('\xa0', ' '),
                       futures[fut])


def main():
    print('Starting...')

    urls = chain(*(get_urls(t+1) for t in range(18)))
    items = [*get_items(urls)]

    print(f'Collected {len(items)} items.')

    filename = 'raw_items.pickle'

    with open(filename, 'wb') as f:
        pickle.dump(items, f)

    print(f'Pickled {len(items)} items at {filename}')


if __name__ == "__main__":
    main()
