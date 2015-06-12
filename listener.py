# Okay Google hotword activation script
# Josh Chen, 14 Feb 2014
# Feel free to modify as you need

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import *
from os.path import expanduser
import sys, subprocess, os, json, urllib2, unicodedata, time, gettext, locale, gettext

p = os.path.dirname(os.path.abspath(__file__))

sys.path.append( p +'/librairy')
from localehelper import LocaleHelper

localeHelper = LocaleHelper()
lang = localeHelper.getLocale()

t=gettext.translation('google2ubuntu',p +'/i18n/',languages=[lang])
t.install()

hotword = _('ok start')
config_file = expanduser('~') + '/.config/google2ubuntu/google2ubuntu.conf'
try:
    if os.path.exists(config_file):
        f=open(config_file,'r')
        for line in f.readlines():
            line = line.strip('\n')
            field = line.split('=')
            if field[0] == 'hotword':  
                hotword = field[1].replace('"','')
            if field[0] == 'key':  
                key = field[1].replace('"','')
        f.close()
except Exception:
    print "Error loading", config_file
    sys.exit(1)


# lecture du fichier audio
filename='/tmp/pingvox.flac'
f = open(filename)
data = f.read()
f.close()

try:
    # Send request to Google
    fail = 'req'
    req = urllib2.Request('https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&key=' + key +'&lang='+lang, data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})
    
    fail = 'ret'
    # Return request
    ret = urllib2.urlopen(req)
    
    # Google translate API sometimes returns lists of phrases, thus we choose the first item
    text = ret.read()
    text = text.split('"transcript":"',2)[1].split('"',2)[0]
            
    fail = 'parse'
    
    print "hotword:", hotword
    print "detected:", text   
    
    if text == hotword: 
        os.system('python ' + p + '/google2ubuntu.py')

except Exception:
    os.system('echo Fail:'+fail) # for debugging
    #message = _('unable to translate')
    if fail == 'req':
        message = _('Cannot connect to Google Translate')
    elif fail == 'parse':
        message = _('Phrase parsing failed')
    elif fail == 'ret':
        message = _('Error processing value returned by Google Translate')
    
    print message
    sys.exit(1)
