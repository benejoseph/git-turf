#!/usr/bin/python
import subprocess
import json
g_gitdir = '/home/bjoseph/git-turf'

g_pretty_format = '--pretty=format:\"},%n {\"commit\": \"%H\",%n  \"author\": \"%an \",%n  \"date\": \"%ad\",%n  \"message\": \"%s\"%n \"files\":\"'

def getGitLogs():
    output = subprocess.check_output(['git','log','--name-status','--since=1.days'],cwd=g_gitdir)
   
    return str(output)

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
        
