import ConfigParser
import os

#mah singleton

def init(filename):
    global g_config
    g_config = Config(filename)

def get():
    global g_config
    return g_config

server = 'server'
gitdir = 'git_directory'
dbfile = 'database_file'

class Config():
    def __init__(self,filename):
        config = ConfigParser.RawConfigParser()
        if (os.path.isfile(filename)):
            #read if I can
            print 'Reading ' + filename
            config.read(filename)
        else:
            #write a new one
            print 'Writing default ' + filename

            config.add_section('server')
            config.set(server,gitdir,'/opt/my_repo')
            config.set(server,dbfile,'database.dat')

            with open(filename, 'wb') as configfile:
                config.write(configfile)

        self.config = config

    def getGitDirectory(self):
        return self.config.get(server,gitdir)

    def getDatabaseFilename(self):
        return self.config.get(server,dbfile)
