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


def train_model(clxn):
    sents = chain(*(tokenize(item.text) for item in clxn))

    model = FastText(sents, size=300)

    return model


if __name__ == "__main__":
    with open('preprocessed_texts.pickle', 'rb') as f:
        clxn = pickle.load(f)

    model = train_model(clxn)

    with open('trained_model.pickle', 'wb') as g:
        pickle.dump(model, g)
