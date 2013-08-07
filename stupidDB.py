import pickle
import os
import hashlib
import threading
import copy

def init(dbfile):
    global g_db
    g_db = StupidDB(dbfile)

def get():
    global g_db
    return g_db

class StupidDB():
    def __init__(self,dbfile):
        self.filename = dbfile
        self.lock = threading.Lock()
        self.filelock = threading.Lock()
        print "init database from %s" % dbfile
        if (os.path.isfile(filename)):
            self.data = pickle.load(dbfile)
        else:
            self.data.user = {}
            self.data.sessions = {}
        

    def addUser(self,username,password):
        salt = os.urandom(512).encode('utf-8')
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()

        self.lock.acquire()
        self.data.user[username] = {'hash' : hashed_password, 'salt' : salt }
        self.lock.release()

        save()

    def save(self):
        self.filelock.acquire()
        pickle.dump(self.data,self.filename)
        self.filelock.release()

    def checkUser(self,username,password):
        self.lock.acquire()
        userdata = copy.deepcopy(data.user[username])
        self.lock.release()

        if userdata is None:
            print 'Did not find user data of user'
            return False

        salt = userdata['salt']
        myhash = userdata['hash']
        
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()

        if (userdata['hash'] == hashed_password):
            return True
        else:
            return False

    def checkSession(self,sessionid):
        self.lock.acquire()
        username = self.data.sessions[sessionid]
        self.lock.release()
        return username

    def getNewSession(self,username):
        sessionid = os.urandom(512).encode('utf-8').hexdigest()
        self.lock.acquire()
        self.data.sessions[sessionid] = username
        self.lock.release()
        return randomnumber

    def removeSession(self,sessionid):
        self.lock.acquire()
        if sessionid in self.data.sessions:
            del self.data.sessions[sessionid]
            
        self.lock.release()

        
