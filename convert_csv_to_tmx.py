# -*- coding: utf-8 -*-

# This script converts CSV export with ItemSpecifics to TMX.

import os
import re
import fileinput
import codecs

filename = raw_input("File name: ")

# Example: 'EN-GB'
srclangcode = raw_input("Source language code: ")
# Example: 'DE-DE'
tgtlangcode = raw_input("Target language code: ")

# TMX structural parts
tmxheader = ur'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version = "1.4">
<header creationtool="Logoport"
creationtoolversion="5.30"
segtype="sentence"
o-tmf="Logoport"
adminlang="EN-US"
srclang="''' + srclangcode + ur'''"
datatype="rtf">
<prop type="RTFFontTable">
{\fonttbl
{\f1\fmodern\fcharset0\fprq1{\*\panose 02070309020205020404}Courier New;}
{\f2\froman\fcharset0\fprq2{\*\panose 02020603050405020304}Times New Roman;}
{\f3\fswiss\fcharset0\fprq2{\*\panose 020b0604020202020204}Arial;}
{\f4\fbidi\fcharset204\fprq1{\*\panose 02070309020205020404}Courier New{\*\falt Courier New};}}
</prop>
<prop type="RTFStyleSheet">
{\stylesheet
{\St \cs1 {\StB \v\f1\fs20\cf12\lang1024\sub }{\StN tw4winMark}}
{\St \cs2 {\StB \f1\cf6\lang1024 }{\StN tw4winInternal}}
{\St \cs3 {\StB \f1\cf15\lang1024 }{\StN tw4winExternal}}
{\St \cs4 {\StB \v\f1\cf11\lang1024 }{\StN tw4winPopup}}
{\St \cs5 {\StB \v\f1\cf10\lang1024 }{\StN tw4winJump}}
{\St \cs6 {\StB \f1\cf13\lang1024 }{\StN DO_NOT_TRANSLATE}}
{\St \cs7 {\StN LogoportTMX}}
{\St \cs8 {\StB \v\f1\fs20\cf12\lang1024\sub }{\StN LogoportFootnote}}}
</prop>
</header>
'''
tmxfooter = ur'''
<body>
</body>
</tmx>'''
segmentheader = ur'<tu creationdate="20140522T083545Z" creationid="TMS_USER" ' \
                + ur'datatype="x-lptmx" srclang="' \
                + srclangcode + ur'"><tuv xml:lang="' \
                + srclangcode + ur'"><seg>eBayCategoryID'
segmentfooter = ur'</seg></tuv></tu>'

src_nametag_open = r'<bpt i="1" x="1">&lt;Name&gt;</bpt>'
src_nametag_close = r'<ept i="1">&lt;/Name&gt;</ept>'
# if no value, discard this part:
src_valuetag_open = r'<bpt i="2" x="2">&lt;Value&gt;</bpt>'
# if no value, discard this part:
src_valuetag_close = r'<ept i="2">&lt;/Value&gt;</ept>'
end_src_segment = r'</seg></tuv>'

beg_tgt_segment = r'<tuv xml:lang="' + tgtlangcode + '"><seg>eBayCategoryID'  # with tgtlangcode
tgt_nametag_open = r'<bpt i="1" x="1">&lt;Name&gt;</bpt>'
tgt_nametag_close = r'<ept i="1">&lt;/Name&gt;</ept><ph>&lt;TBD /&gt;</ph>'  # with added <TBD> tag
tgt_valuetag_open = r'<bpt i="2" x="2">&lt;Value&gt;</bpt>'  # if no value, discard
tgt_valuetag_close = r'<ept i="2">&lt;/Value&gt;</ept>'  # if no value, discard


def entitize(a_string):
    if a_string is None:
        return None
    else:
        repl_lt = re.sub(r'<', r'&amp;lt;', a_string)
        repl_gt = re.sub(r'>', r'&amp;gt;', repl_lt)
        repl_and = re.sub(r'&', r'&amp;amp;', repl_gt)
        repl_quot = re.sub(r'""', r'"', repl_and)
        return repl_quot


def process(a_line):
    parsedline = re.search(r'^"?(.*?)"?\t"?(.*?)"?\t"?(.*?)"?\t"?(.*?)"?\t"?(.*?)"?\t"?'
                           '(.*?)"?\t"?(.*?)"?\t"?(.*?)"?\t"?(.*?)"?', a_line)
    if parsedline is None:
        return None
    else:
        # src_cat_name = entitize(parsedline.group(1))
        src_cat_id = entitize(parsedline.group(2))
        src_is_name = entitize(parsedline.group(3))
        src_is_value = entitize(parsedline.group(4))
        # tgt_cat_name = entitize(parsedline.group(5))
        tgt_cat_id = entitize(parsedline.group(6))
        tgt_is_name = entitize(parsedline.group(7))
        tgt_is_value = entitize(parsedline.group(8))
        if src_is_name == "" or src_is_value == "" or tgt_is_name == "" \
                or tgt_is_name == "" or src_cat_id == "Source category ID":
            a_line = ""
        else:
            a_line = segmentheader + src_cat_id \
                + src_nametag_open + src_is_name + src_nametag_close \
                + src_valuetag_open + src_is_value + src_valuetag_close + end_src_segment \
                + beg_tgt_segment + tgt_cat_id \
                + tgt_nametag_open + tgt_is_name + tgt_nametag_close \
                + tgt_valuetag_open + tgt_is_value + tgt_valuetag_close + segmentfooter
        return a_line

tmxfilename, tmxfileextension = os.path.splitext(filename)
newtmx = codecs.open(tmxfilename + ".tmx", "w+", "utf-8")
newtmx.write(tmxheader)

for line in fileinput.FileInput(filename, mode="U", openhook=fileinput.hook_encoded("utf-16")):
    newline = process(line)
    if newline is None or newline == "":
        pass
    else:
        newtmx.write(newline + "\n")
newtmx.write(tmxfooter)
newtmx.close()

print "New TMX ready."
