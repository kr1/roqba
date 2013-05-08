import os
import json
import cherrypy

cherrypy_config = {'global': {
                      'server.socket_host': "127.0.0.1",
                      'server.socket_port': 8088,
                      'server.log_to_screen': False,
                      'log.log_to_screen': False,
                      'log.access_file': os.path.join(".", "access.log"),
                      'log.screen': False},
                   '/': {
                      'tools.staticdir.root': os.path.join(os.getcwd(), '.')},
                   '/static': {
                      'tools.staticdir.on': True,
                      'tools.staticdir.dir': "static"}}
#server.thread_pool = 10


class BufferedServer(object):
    "main class for the cherrypy server"
    def __init__(self, msg_queue):
        self.msg_queue = msg_queue

    def webBuffer(self, timestamp=None):
        """responds to requests to the `webBuffer` path

        returns all currently buffered messages later than
        the specified timestamp (nanoseconds since epoch)
        """
        timestamp = int(timestamp) // 1000000
        json_encoded = json.dumps(
                         filter(lambda x: x[0] > timestamp,
                         self.msg_queue))
        return json_encoded
    webBuffer.exposed = True


def start_server(queue):
    "wrapper function to start the cherrypy server in a separate thread"
    cherrypy.quickstart(BufferedServer(queue), '', cherrypy_config)

if __name__ == "__main__":
    import cherrypy
    cherrypy.quickstart(BufferedServer(None), '', cherrypy_config)
