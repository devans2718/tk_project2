import pickle
from copy import copy

import regex

from common import Item, compose


def validate_text(item):
    return 'Источник:\n' in item.text


def returns_removed(item):
    new_text = item.text.replace('\r', ' ').replace('  ', ' ')

    return item._replace(text=new_text)


def title_and_text_trimmed(item):
    new_title = item.title.replace('Сталин И.В. ', '')

    text_pat = regex.compile(
        r'(?<=Источник:\n(.*\n){6})(?:.*\n)+?(?=\n{6}|\nПРИМЕЧАНИ[ЕЯ]\n)')
    text_match = text_pat.search(item.text)
    new_text = text_match.group() if text_match is not None else item.text

    return item._replace(title=new_title, text=new_text)


def page_numbers_removed(item):
    pat = regex.compile(r'\[c\..{,6}\]')
    new_text = regex.sub(pat, r'', item.text)

    return item._replace(text=new_text)


def initials_removed(item):
    pat = regex.compile(r'\p{lu}\.\p{lu}\. (?=\w)')
    new_text = regex.sub(pat, r'', item.text)

    return item._replace(text=new_text)


def newlines_removed(item):
    new_text = item.text.replace('\n', ' ').replace('  ', ' ')

    return item._replace(text=new_text)


funcs = [
    returns_removed,
    title_and_text_trimmed,
    page_numbers_removed,
    initials_removed,
    newlines_removed
]


def main():
    _infile = 'raw_items.pickle'
    with open(_infile, 'rb') as f:
        items = pickle.load(f)

    print(f'Preprocessing {len(items)} items (before validation)')

    preprocessed_items = [*map(compose(*funcs), filter(validate_text, items))]

    print(f'Preprocessed {len(preprocessed_items)} items (after validation)')

    _outfile = 'preprocessed_items.pickle'
    with open(_outfile, 'wb') as g:
        pickle.dump(preprocessed_items, g)

    print(f'Items saved at {_outfile}')



if __name__ == "__main__":
    main()
