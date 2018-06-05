import pickle
from copy import copy

import regex

from common import Item


def validate_text(item):
    return 'Источник:\n' in item.text


def returns_removed(item):
    new_text = item.text.replace('\r', ' ').replace('  ', ' ')

    return Item(item.title, new_text)


def title_and_text_trimmed(item):
    new_title = item.title.replace('Сталин И.В. ', '')

    text_pat = regex.compile(
        r'(?<=Источник:\n(.*\n){6})(?:.*\n)+?(?=\n{6}|\nПРИМЕЧАНИ[ЕЯ]\n)')
    text_match = text_pat.search(item.text)
    new_text = text_match.group() if text_match is not None else item.text

    return Item(new_title, new_text)


def page_numbers_removed(item):
    pat = regex.compile(r'\[c\..{,6}\]')
    new_text = regex.sub(pat, r'', item.text)

    return Item(item.title, new_text)


def initials_removed(item):
    pat = regex.compile(r'\p{lu}\.\p{lu}\. (?=\w)')
    new_text = regex.sub(pat, r'', item.text)

    return Item(item.title, new_text)


def newlines_removed(item):
    new_text = item.text.replace('\n', ' ').replace('  ', ' ')

    return Item(item.title, new_text)


def preprocess(item):
    funcs = [
        returns_removed,
        title_and_text_trimmed,
        page_numbers_removed,
        initials_removed,
        newlines_removed
    ]

    new_item = copy(item)

    for func in funcs:
        new_item = func(new_item)

    return new_item


def main():
    with open('raw_items.pickle', 'rb') as f:
        items = pickle.load(f)

    preprocessed_items = [*map(preprocess, filter(validate_text, items))]

    with open('preprocessed_items.pickle', 'wb') as g:
        pickle.dump(preprocessed_items, g)



if __name__ == "__main__":
    main()