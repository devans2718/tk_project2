import pickle
from itertools import chain

from gensim.models import FastText
from nltk import sent_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem.snowball import RussianStemmer

from common import Item

tokenizer = ToktokTokenizer()
stemmer = RussianStemmer()


def tokenize(text):
    sents = sent_tokenize(text)
    tokens = [[token.lower() for token in tokenizer.tokenize(sent)]
              for sent in sents]

    return tokens


def train_model(items):
    sents = chain(*(tokenize(item.text) for item in items))
    model = FastText(sents, size=300)

    return model


def main():
    with open('preprocessed_items.pickle', 'rb') as f:
        items = pickle.load(f)

    model = train_model(items)

    with open('trained_model.pickle', 'wb') as g:
        pickle.dump(model, g)


if __name__ == '__main__':
    main()