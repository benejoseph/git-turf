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

mymongotable = 'rawheaders'
mymongoserver = 'localhost'
mymongodatabase = 'context'
mymongoport = 27017
define("port", default=8887, help="run on the given port", type=int)

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
        g_threadpool.put(StatusObj(self.callback))
	        
    def callback(self,workobj):
        self.finish(workobj.gettext()) 

 

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/status", StatusHandler),
            (r"/(.*)",tornado.web.StaticFileHandler,{'path' : './'})
        ]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)



def main():

    signal.signal(signal.SIGINT, signal_handler)

    g_threadpool.start()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    g_threadpool.stop()


if __name__ == "__main__":
    main()

