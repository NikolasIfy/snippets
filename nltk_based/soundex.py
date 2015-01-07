import re


def findval(singlechar):
    # Returns numerical value of character
    if singlechar.isalpha() and len(singlechar) == 1:
        if singlechar.lower() in 'bfpv':
            return '1'
        elif singlechar.lower() in 'cgjkqsxz':
            return '2'
        elif singlechar.lower() in 'dt':
            return '3'
        elif singlechar.lower() == 'l':
            return '4'
        elif singlechar.lower() in 'mn':
            return '5'
        elif singlechar.lower() == 'r':
            return '6'
    else:
        return singlechar.lower()


def prestring(string):
    # If two or more letters with the same number are adjacent in the original name
    # (before step 1), only retain the first letter; also two letters with the same number
    # separated by 'h' or 'w' are coded as a single number, whereas such letters
    # separated by a vowel are coded twice. This rule also applies to the first letter.
    sub1 = re.sub(r'([bfpv])[hw]?[bfpv]', r'\1', string)
    sub2 = re.sub(r'([cgjkqsxz])[hw]?[cgjkqsxz]', r'\1', sub1)
    sub3 = re.sub(r'([dt])[hw]?[dt]', r'\1', sub2)
    sub4 = re.sub(r'([mn])[hw]?[mn]', r'\1', sub3)
    return sub4


def soundex(string):
    '''Algorithm returning Soundex value for names, e.g. Caroline -> C645.'''
    # Retain the first letter of the name and drop all other occurrences of a, e, i, o, u, y, h, w
    string = prestring(string)
    string = string[0] + re.sub('[aeiouyhw]', '', string[1:])
    newstring = string[0].upper()
    for char in string[1:]:
        newstring = newstring + findval(char)
    if len(newstring) > 4:
        newstring = newstring[:4]
    while len(newstring) < 4:
        newstring = newstring + "0"
    return newstring
