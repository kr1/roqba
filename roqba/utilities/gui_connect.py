import socket
import time

import json

from roqba.static.settings import settings

class GuiConnect(object):
    def __init__(self):
        self.gui_host = settings['GUI_HOST'] 
        self.send_port = settings['TO_GUI_PORT'] 
        self.receive_port = settings['FROM_GUI_PORT'] 
        self.sock = socket.socket(socket.AF_INET, # Internet
                                   socket.SOCK_DGRAM) # UDP
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind((self.gui_host, self.receive_port))
        self.receive_exit_requested = False

    def send(self, msg):  
        self.sock.sendto(msg, (self.gui_host, self.send_port))

    def handle_caesura(self, director):
        print "caesura"
        director_fields_to_transmit = ['speed']#,'transpose']
        for field in director_fields_to_transmit:
            self.send(json.dumps({field:getattr(director, field)}))
        voice_fields_to_transmit = ['pan_pos', 'binaural_diff']
        for field in voice_fields_to_transmit:
            for v in director.composer.voices.values():
                dic = {'voice_' + str(v.id) + '_' + field: getattr(v, field)}
                self.send(json.dumps(dic))

    def send_cycle_pos(self, director):
        director_state_fields_to_transmit = ['weight', 'cycle_pos']#,'transpose']
        for field in director_state_fields_to_transmit:
            val = director.state[field]
            if field == 'cycle_pos':
                val += 1
            self.send(json.dumps({field: val}))

    def read_incoming_messages(self, q):
        while not self.receive_exit_requested:
            time.sleep(0.2)
            msg = self.receiver.recv(1024)
            q.append(json.loads(msg))
