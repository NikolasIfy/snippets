import nltk
import re


def unhyphenate(string):
    '''Returns string in single line form with removed hyphens
    if such a form of the word exists. Based on comparison with Brown corpus.'''
    allwords = ([word.lower() for word in nltk.corpus.brown.words()])
    check = re.findall(r'(\w+)-\r?\n(\w+)', string)
    newstring = string
    for item in check:
        if (item[0] + item[1]).lower() in allwords:
            newstring = re.sub("(" + item[0] + ')-\r?\n(' + item[1] + ")",
                               r'\1\2', newstring)
        else:
            newstring = re.sub("(" + item[0] + ')-\r?\n(' + item[1] + ")",
                               r'\1-\2', newstring)
    newstring = re.sub(r'\s*\r?\n', r' ', newstring)
    return newstring
