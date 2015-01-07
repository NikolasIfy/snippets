from nltk.corpus import wordnet as wn
import nltk


def novelwords(text):
    '''Returns sorted set of words according to their "sense score".
    Based on Wordnet corpus.'''
    def meansimilarity(word):
        # Helper function. Calculate mean path similarity of first synset
        # of the word with all synsets of this word.
        sums = 0.0
        synsets = wn.synsets(word)
        index = 0
        for synset in range(0, len(synsets)):
            if index < len(synsets) - 1:
                ps = wn.path_similarity(synsets[0], synsets[index + 1])
                if ps is not None:
                    sums = sums + ps
            index += 1
        return sums / len(synsets)

    # Tokenize text ignoring sentence boundaries.
    tokens = nltk.regexp_tokenize(text, r"[a-zA-Z'-]+")

    # Filter out tokens without synsets.
    filtered = []
    for token in tokens:
        if wn.synsets(token) != []:
            filtered.append(token)

    result = {}

    # Define words - main, previous, next
    ind = 0
    for token in range(0, len(filtered)):
        mainstring = filtered[ind]
        prevstring = ""
        nextstring = ""
        if ind > 0 and ind < len(filtered):
            prevstring = filtered[ind-1]
        if ind < len(filtered) - 1:
            nextstring = filtered[ind+1]
        ind += 1

        # Calculate mean path similarities:
        for synset in wn.synsets(mainstring):
            if prevstring != "" and nextstring != "":
                result[mainstring] = [meansimilarity(mainstring),
                                      meansimilarity(prevstring),
                                      meansimilarity(nextstring)]
            elif prevstring == "" and nextstring != "":
                result[mainstring] = [meansimilarity(mainstring),
                                      meansimilarity(nextstring)]
            elif prevstring != "" and nextstring == "":
                result[mainstring] = [meansimilarity(mainstring),
                                      meansimilarity(prevstring)]
    for key in result.keys():
        valuesum = 0.0
        valuenum = 0
        for value in result[key]:
            valuesum = valuesum + value
            valuenum += 1
        result[key] = valuesum / valuenum
    sortedbyvalue = sorted(result.items(), key=lambda x: x[1])

    return sortedbyvalue
