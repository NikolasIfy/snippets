import nltk
from nltk.corpus import udhr
from nltk import FreqDist as fd
from nltk import spearman_correlation as cor


def guess_lang(text):
    '''Guess the language of the text. This version includes only Spanish,
    German and English and the sample needs to be quite big but it could be enhanced.'''
    Spanish = udhr.words('Spanish-Latin1')
    German = udhr.words('German_Deutsch-Latin1')
    English = udhr.words('English-Latin1')
    spanfd = fd(Spanish)
    small_spanfd = {}
    gerfd = fd(German)
    small_gerfd = {}
    enfd = fd(English)
    small_enfd = {}

    text_fd = fd(nltk.regexp_tokenize(text.lower(), r'\w+'))

    for key in spanfd.keys():
        if text_fd.has_key(key):
            small_spanfd[key] = spanfd[key]

    for key in enfd.keys():
        if text_fd.has_key(key):
            small_enfd[key] = enfd[key]

    for key in gerfd.keys():
        if text_fd.has_key(key):
            small_gerfd[key] = gerfd[key]

    corwithspan = cor(small_spanfd, text_fd)
    corwithen = cor(small_enfd, text_fd)
    corwithger = cor(small_gerfd, text_fd)

    if abs(corwithspan) == abs(corwithen) == abs(corwithger):
        print "I don't know..."
    elif max(abs(corwithspan), abs(corwithen), abs(corwithger)) == abs(corwithspan):
        print "It's Spanish!"
    elif max(abs(corwithspan), abs(corwithen), abs(corwithger)) == abs(corwithen):
        print "It's English!"
    elif max(abs(corwithspan), abs(corwithen), abs(corwithger)) == abs(corwithger):
        print "It's German!"
