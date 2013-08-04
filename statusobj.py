#!/usr/bin/python
import subprocess
import json
from gitparse import parsegitlog
g_gitdir = '/home/bjoseph/git-turf'

def getGitLogs():
    output = subprocess.check_output(['git','log','--name-status','--since=2.weeks'],cwd=g_gitdir)

    records = parsegitlog(str(output))
   
    return str(records)

class StatusObj():
    def __init__(self,callback):
        print "init"
        self.text = getGitLogs()
        
        if self.text == None:
            self.text = 'None'
            
        #return via callback
        callback(self)


    def gettext(self):
        return self.text
        
