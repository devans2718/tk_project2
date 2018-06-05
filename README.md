# Totalitarianism and Culture
## NLP project by Daniel Evans

During my final semester at University of Missouri - Columbia, I took a course on Totalitarianism and culture, where we explored the relationship between totalitarian governments their substrate cultures. For my final project, I combined ideas from language acquisition, distributional semantics, and computational linguistics in a discussion of the sociolinguistic effects of totalitarian propaganda and indoctrination.

The main goal of the project is to compare an "average" Russian linguistic profile against a "Soviet" Russian linguistic profile. For the average profile, I use word embeddings provided by Facebook trained on the Russian [Wikipedia](https://ru.wikipedia.org/) and [Common Crawl](http://commoncrawl.org/) datasets. For the Soviet profile, I use train embeddings on a collection of Joseph Stalin's essays, speeches, letters, and other works.

The project consists mainly of a paper/discussion component and the code component. I wrote code to collect, process, and vectorize the Stalin corpus. Then, in a python shell, I explored the differences between average and Soviet embeddings.

The scripts are excecuted in this order:
1. `pull_raw_tomes.py` - using BeautifulSoup and pickle, look at each of the 18 contents-pages of a collection of Stalin's works hosted at [an online library](http://grachev62.narod.ru/), find all links to individual texts, save text-content from each link.
2. `preprocess.py` - using regex and pickle, remove garbage data from saved webcontent and save it.
3. `vectorize.py` - use NLTK for low-mid level NLP tasks, use gensim's implementation of FastText to find word embeddings from the Stalin corpus, then save word embeddings.

`common.py` simply defines the `Item` class used by other scripts.  
`analysis.py` loads the Stalin corpus embeddings and Facebook's pretrained embeddings - since loading facebook's pretrained vectors takes several minutes, this code is most useful when loaded into an interactive python terminal.

The code component has room for improvement
* The code poorly handles Russian derivational morphology - long words with similar internal structure like *бдительный (bditel'nyy)* 'vigilant' and *решительный (reshitel'nyy)* 'decisive' have similar embeddings mostly because they share five derivational morphemes *и-т-ель-н-ый (i-t-el'-n-yy)* 'VRB-INF-AG-ADJ-MASC.NOM' despite having different roots *бд (bd)* 'awake' and *реш (resh)* 'unravel'.
* In a couple places, the code could be sped up with multi-threading or -processing.
* General clean-up and rewriting using best practices, idioms, conventions