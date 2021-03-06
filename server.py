#!/usr/bin/python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.options import define, options
import threading
from threadpool import ThreadPool
from statusobj import StatusObj
import signal
import sys
import config
import stupidDB

define("port", default=8887, help="run on the given port", type=int)
config_file_name = "config.cfg"

#ctrl-c!
def signal_handler(signal, frame):
        g_threadpool.stop()
        print 'You pressed Ctrl+C!'
        sys.exit(0)

#thread pool stuff
def executfunc(data):
    data.execute()

g_threadpool = ThreadPool(executfunc,4)

#tornado stuff
class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        query = None
        try:
            query = self.get_argument('query', True)
        except Exception:
            print "query not present"
                
        g_threadpool.put(StatusObj(self.callback,query))
	        
    def callback(self,workobj):
        self.finish(workobj.gettext()) 

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_argument("user")
        password = self.get_argument("password")
        print user,password
        return self.write("hello") 

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/service/status", StatusHandler),
            (r"/service/login", LoginHandler),
            (r"/(.*)",tornado.web.StaticFileHandler,{'path' : './client'})
        ]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)



def main():

    signal.signal(signal.SIGINT, signal_handler)

    #set up global config stuff
    config.init(config_file_name)

    #set up the "database"
    stupidDB.init(config.getDatabaseFilename())
    
    g_threadpool.start()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    g_threadpool.stop()


if __name__ == "__main__":
    main()

