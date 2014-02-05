#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
from workWithModule import workWithModule
from basicCommands import basicCommands
from Googletts import tts
import xml.etree.ElementTree as ET
import os, gettext, time, sys, subprocess
gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# Permet d'exécuter la commande associée à un mot prononcé
class stringParser():
    """
    @author: Benoit Franquet
    
    @description: This class parse the text pronounced by the user
    it looking for the key sentence stored in the xml config file
    We choose the command associated to the key sentence that share the 
    maximum of words with the text pronounced
    """
    def __init__(self,text,File,PID):
        # read configuration files
        self.pid=PID
        try:
            max = 0
            text=text.lower()
            tree = ET.parse(File)
            root = tree.getroot()
            tp = ''
            
            for entry in root.findall('entry'):
                score = 0
                Type=entry.get('name')
                Key=entry.find('key').text
                Command=entry.find('command').text
                key=Key.split(' ')
                for j in range(len(key)):
                    score += text.count(key[j])
                        
                if max < score:
                    max = score
                    do = Command
                    tp = Type
            
            # on regarde si la commande fait appel à un module
            # si oui, alors on lui passe en paramètre les dernier mots prononcé
            # ex: si on prononce "quelle est la météo à Paris"
            # la ligne de configuration dans le fichier est: [q/Q]uelle*météo=/modules/weather/weather.sh
            # on coupe donc l'action suivant '/'
            do=do.encode('utf8') 
            print tp, do
            os.system('echo "'+do+'" > /tmp/g2u_cmd_'+self.pid)
            if _('modules') in tp:
                check = do.split('/')
                # si on trouve le mot "modules", on instancie une classe workWithModule et on lui passe
                # le dossier ie weather, search,...; le nom du module ie weather.sh, search.sh et le texte prononcé
                wm = workWithModule(check[0],check[1],text,self.pid)
            elif _('internal') in tp:
                # on execute une commande intene, la commande est configurée
                # ainsi interne/batterie, on envoie batterie à la fonction
                b = basicCommands(do,self.pid)
            elif _('external') in tp:
                os.system(do)
             
                
            os.system('> /tmp/g2u_stop_'+self.pid)
            
            
        except Exception:
            message = _('Setup file missing')
            os.system('echo "'+message+'" > /tmp/g2u_error_'+self.pid)
            sys.exit(1)   
