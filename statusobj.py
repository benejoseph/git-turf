#!/usr/bin/python
import subprocess
import json
from gitparse import parsegitlog
g_gitdir = '/home/bjoseph/sideproject/git-turf'

def getGitLogs():
    output = subprocess.check_output(['git','log','--name-status','--since=2.weeks'],cwd=g_gitdir)

    return parsegitlog(str(output))
           

class StatusObj():
    def __init__(self,callback):
        
        logs = getGitLogs()

        self.text = json.dumps(logs)
        
        if self.text == None:
            self.text = '{}'
            
        #return via callback
        callback(self)


    def gettext(self):
        return self.text
        
