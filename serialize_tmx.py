# -*- coding: utf-8 -*-
import gtk
import re


def convert(tmx):
# inputfile = r'c:\!work\@CurrentIssues\2014-08-29_NAP_TM\NAP_TM_update_fr-FR_2014-08-26.tmx'
    inputtmx = open(tmx, 'r').read()
    #pseudoconvert to TMX 1.4 - change header only
    tmx14_1 = re.sub(r'<!DOCTYPE tmx SYSTEM "tmx11.dtd">', r'<!DOCTYPE tmx SYSTEM "tmx14.dtd">', inputtmx)
    tmx14 = re.sub(r'<tmx version = "1.1">', r'<tmx version = "1.4">', tmx14_1)

    tmx14split = tmx14.splitlines()

    tmx14lines = []
    for line in tmx14split:
        if re.match(r'<seg>', line):
            phid = 1
            newline = line
            for tag in re.findall(r'&lt;(.*?)&gt;', line):
                newline = re.sub(r'&lt;(.*?)&gt;', r'<ph x="' + str(phid) +r'">&amp;lt;\1&amp;gt;</ph>', newline, 1)
                phid = phid + 1
            tmx14lines.append(newline)
        else:
            tmx14lines.append(line)
       
    outputtmx = open(tmx, 'w')
    for item in tmx14lines:
        outputtmx.write(item + '\n')
    outputtmx.close()

def ChooseDialog():
    choosedialog = gtk.FileChooserDialog('Show me the TMX to process.', None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    filter = gtk.FileFilter()
    filter.set_name('TMX files')
    filter.add_pattern('*.tmx')
    choosedialog.add_filter(filter)
    choosedialog.set_current_name('.tmx')
    choosedialog.set_default_response(gtk.RESPONSE_OK)
    choosedialog.show_all()
    chooseresponse = choosedialog.run()
    if chooseresponse == gtk.RESPONSE_OK:
        convert(choosedialog.get_filename())
        print "TMX converted."
    else:
        print "So long."
    choosedialog.destroy()

ChooseDialog()
