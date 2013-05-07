import os
import base64
import json
import cherrypy

cherrypy_config = {'global': {'server.socket_host' : "127.0.0.1",
                              'server.socket_port' : 8088,
                              'log.access_file' : os.path.join(".", "access.log"),
                              'log.screen': False },
                   '/':{'tools.staticdir.root' : os.path.join(os.getcwd(), '.')},
                   '/static': {'tools.staticdir.on' : True,
                               'tools.staticdir.dir' : "static"}}
#server.thread_pool = 10

class BufferedServer(object):
    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
    def webBuffer(self, timestamp=None):
        timestamp_ms = int(timestamp)//1000000
        #print self.msg_queue[0][0]
        json_encoded = json.dumps(list(self.msg_queue))
        base64_encoded = base64.encodestring(json_encoded)
        return base64_encoded
    webBuffer.exposed = True

def start_server(queue):
    cherrypy.quickstart(BufferedServer(queue),'', cherrypy_config)

if __name__ == "__main__":
    import cherrypy
    cherrypy.quickstart(BufferedServer(None),'', cherrypy_config)
