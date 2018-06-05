# Vernacular vs Propagandistic Word Embeddings

## NLP project by Daniel Evans

### Project overview

At University of Missouri - Columbia, I took a course that explored the relationship between totalitarian governments their substrate cultures. The final project was an open-ended assignment where students decided their own topic and format. I decided to run an experiment using word embeddings to explore the sociolinguistic effects of propaganda.

The core idea is that word embeddings derived from vernacular and propagandistic corpora have observable differences. In particular, the set of words with vectors most cosine-similar to the vector of a given word varies between corpora. The vernacular embedding used is provided by [Facebook](fasttext.cc) and was trained on the [Common Crawl](http://commoncrawl.org/) corpus. The propagandistic embedding was trained on the [complete works of Joseph Stalin](http://grachev62.narod.ru/stalin/index.htm).

In this repo I have provided both the paper submitted for the class and the code written to collect and process the Stalin corpus.

### Code overview

Below is a description of the main `.py` files in order of execution:

1. `collect.py`: Using `requests` and `BeautifulSoup`, parse the contents-pages of the online collection of Stalin's works, and find the links to individual texts. With the help of `concurrent.futures`, make over 1300 HTTP requests in a reasonable amount of time, then `pickle` the pages' contents. (This was previously implemented without concurrency and took quite a while to make all the requests.)
2. `preprocess.py` - Remove any item with no content, since a small number of pages are blank. Using `regex`, remove garbage (such as page numbers, newlines, publication notes) from each item. Then, `pickle` the items.
3. `vectorize.py` - Using `nltk`, tokenize by sentence and by word. Using `gensim`'s implementation of Facebook's FastText, train and save word embeddings from the Stalin corpus.

`common.py` simply defines the `Item` class used by other scripts.  
`analysis.py` Is essentially a dummy file whose content is best copy-pasted into an interactive shell, since loading up Facebook's pretrained vectors takes several minutes.

### Other notes

#### On issues with derivational morphology

Long words with similar internal structure like *bditel'nyy* 'vigilant' and *reshitel'nyy* 'decisive' have similar embeddings seemingly because they share five derivational morphemes *i-t-el'-n-yy* 'VRB-INF-AG-ADJ-MASC.NOM' despite having roots with different meanings *bd* 'awake' and *resh* 'unravel'.

This is likely a problem with how FastText takes advantage of "sub-word information". It does this by exploding input words into a large array of n-grams. For example, the FastText networks trains on the word "greetings" by training on the following table:

| whole word | 3-grams | 4-grams | 5-grams |
| ---        | ---     | ---     | ---     |
| greetings  | gre     | gree    | greet   |
|            | ree     | reet    | reeti   |
|            | eet     | eeti    | eetin   |
|            | eti     | etin    | eting   |
|            | tin     | ting    | tings   |
|            | ing     | ings    |         |
|            | ngs     |         |         |

This is certainly a clever approach that works well cross-linguistically, especially with smaller corpora and corpora with misspellings and rare words. Results could be improved by using internal word structure and learning morpheme embeddings (rather than whole-word embeddings). However, parsing morphology can be rather tricky because of nonlinear morphology and allomorphy.