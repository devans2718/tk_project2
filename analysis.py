# it'd be best to %load this into an ipython shell
# the pretrained model takes about seven minutes to load on my computer

import pickle

from gensim.models import KeyedVectors

average = KeyedVectors.load_word2vec_format('cc.ru.300.vec')

with open('trained_model.pickle', 'rb') as f:
    soviet = pickle.load(f)