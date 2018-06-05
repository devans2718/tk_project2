# this is very disorganized

import pickle

import regex

from common import Item


def load_items():
    for n in range(18):
        with open(f'raw_tomes/t{n+1}.pickle', 'rb') as f:
            for v in pickle.load(f).values():
                yield Item(*v.values())


def validate_text(item):
    pat = regex.compile(r'Источник:\n')
    search = pat.search(item.text)

    return False if search is None else True


def remove_returns(item):
    pat = regex.compile(r'\r')
    new_text = regex.sub(pat, r'', item.text)

    return Item(item.title, new_text)


def trim(item):
    title_pat = regex.compile(r'(?<=Сталин И.В. ).*')
    title_match = title_pat.search(item.title)
    new_title = item.title if title_match is None else title_match.group()

    text_pat = regex.compile(
        r'(?<=Источник:\n(.*\n){6})(?:.*\n)+?(?=\n{6}|\nПРИМЕЧАНИ[ЕЯ]\n)')
    text_match = text_pat.search(item.text)
    new_text = item.text if text_match is None else text_match.group()

    return Item(new_title, new_text)


def remove_page_numbers(item):
    pat = regex.compile(r'\[c\..{,6}\]')
    new_text = regex.sub(pat, r'', item.text)

    return Item(item.title, new_text)


def remove_initials(item):
    pat = regex.compile(r'\p{lu}\.\p{lu}\. (?=\w)')
    new_text = regex.sub(pat, r'', item.text)

    return Item(item.title, new_text)


def remove_newlines(item):
    new_text = item.text.replace('\n', ' ')
    new_text = new_text.replace('  ', ' ')

    return Item(item.title, new_text)


def preprocess(item):
    item = remove_returns(item)
    item = trim(item)
    item = remove_page_numbers(item)
    item = remove_initials(item)
    item = remove_newlines(item)
    return item


if __name__ == "__main__":
    clxn = [preprocess(item) for item in load_items()
            if validate_text(item)]

    with open('preprocessed_texts.pickle', 'wb') as f:
        pickle.dump(clxn, f)
