# Example of comparison of reading difficulty score (ARI) for two NLTK corpora.

from nltk.corpus import abc


def avg(lst):
    lentotal = 0.0
    for word in lst:
        lentotal = lentotal + len(word)
    return lentotal / len(lst)


def ari(corpus_words, corpus_sents):
    avgchar = avg(corpus_words)
    avgsent = avg(corpus_sents)
    ari = 4.71 * avgchar + 0.5 * avgsent - 21.43
    return ari

print ari(abc.words('rural.txt'), abc.sents('rural.txt'))
print ari(abc.words('science.txt'), abc.sents('science.txt'))
