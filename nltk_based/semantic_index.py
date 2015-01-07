# Modification of concordance function, including Wordnet synset form.

from nltk.corpus import wordnet as wn
import nltk


# Original class
class IndexedText(object):

    def __init__(self, stemmer, text):
        self._text = text
        self._stemmer = stemmer
        self._index = nltk.Index((self._stem(word), i) for (i, word)
                                 in enumerate(text))

    def concordance(self, word, width=40):
        key = self._stem(word)
        wc = width/4  # words of context
        # modification: adding synsets
        if wn.synsets(word)[0]:
            synword = wn.synsets(word)[0]
        else:
            synword = word
        # end of modification
        for i in self._index[key]:
            # changed the display to include the synset
            lcontext = ' '.join(self._text[i-wc:i-1])
            rcontext = ' '.join(self._text[i+1:i+wc])
            ldisplay = '%*s' % (width, lcontext[-width:])
            rdisplay = '%-*s' % (width, rcontext[:width])
            print ldisplay, synword, rdisplay

    def _stem(self, word):
        return self._stemmer.stem(word.lower())

porter = nltk.PorterStemmer()
grail = nltk.corpus.webtext.words('grail.txt')
text = IndexedText(porter, grail)
# example:
text.concordance('soldier')
