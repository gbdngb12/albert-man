from albert import *
import os
import re
import subprocess

__title__ = "Linux manual"
__version__ = "0.1.1"
__triggers__ = "man "
__authors__ = "dong"

iconPath = iconLookup("terminal")

manPath = '/usr/share/man/man' # default man1, man2, man3, ... , man9

mandb = []

def initialize() :
    tmp = os.listdir(manPath+str(1))
    for i in range(2,9) :
        tmp = list(set(tmp + os.listdir(manPath+ str(i))))
    for s in tmp :
        # remove File extension
        mandb.append(re.sub(".(\w{1,10}.gz)|(.\d$)", "", s))
        

def defaultItem(query):
    item = Item()
    item.icon = iconPath
    item.text = 'Linux Manual (man) %s' % query
    item.subtext = 'Show Linux Manual'
    item.completion = __triggers__
    item.addAction(TermAction(text='show Manual',script="man %s" % query))
    return item

def search(query, result) :
    
    matching = [s for s in mandb if query.lower() in s.lower()]
    if len(matching) == 0:
        return result.append(defaultItem(query))
    for match in matching :
        #info(match)
        item = Item()
        item.icon = iconPath
        item.text = 'man %s' % match
        item.subtext = 'Show Linux Manual'
        item.completion = 'man %s' % match
        item.addAction(TermAction(text='show Manual',script="man %s" % match))
        item.addAction(ClipAction(text='command copy to Clipboard', clipboardText='man %s' % match))
        result.append(item)

def handleQuery(query) :
    if not query.isTriggered:
        return
    
    results = []
    if query.string == "" :    
        results.append(defaultItem(query.string))
        return results
    else :
        search(query.string, results)
        return results
