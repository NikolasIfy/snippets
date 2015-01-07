# -*- coding: utf-8 -*-
import xml.etree.ElementTree as Etree
import re
import codecs
import gc


def getabbrevs(inputtmx, outputfile, abbrevfile=None):
    # create abbreviation dictionary from file or start with empty dictionary
    abbrevdict = {}
    if abbrevfile is not None:
        abbrevfile_read = codecs.open(outputfile, 'r', 'utf16')
        lines = abbrevfile_read.readlines()
        for line in lines:
            regex = re.compile(r'(\w+\.)\t([0-9]+)', re.U)
            matchobj = re.match(regex, line)
            abbreviation = matchobj.group(1)
            count = int(matchobj.group(2))
            abbrevdict[abbreviation] = count
        abbrevfile_read.close()

    # read TMX 1.4b:
    tree = Etree.parse(inputtmx)
    for tuv in tree.iter(u'tuv'):
        if tuv.attrib == {u'{http://www.w3.org/XML/1998/namespace}lang': 'DE-DE'}:
            seg = tuv.find(u'seg')
            if seg.text:
                abbrevsintarget = re.compile(r'\w+\.', re.U).findall(seg.text)
                for abbrev in abbrevsintarget:
                    if abbrev not in abbrevdict:
                        abbrevdict[abbrev] = 1
                    else:
                        abbrevdict[abbrev] = abbrevdict[abbrev] + 1
        gc.collect()

    # create output abbreviation file and store found abbreviations
    abbrevfile = codecs.open(r'abbreviations.txt', 'w', 'utf16')
    for key in abbrevdict:
        abbrevfile.write(key + '\t' + str(abbrevdict[key]) + '\r\n')
    abbrevfile.close()
