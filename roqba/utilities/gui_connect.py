import socket
import time
import logging

import json

from roqba.static.settings import settings


class GuiConnect(object):
    '''synchronizing the GUI'''
    def __init__(self):
        self.gui_host = settings['GUI_HOST']
        self.send_port = settings['TO_GUI_PORT']
        print "GUI: sending to:", self.gui_host, self.send_port
        self.receive_port = settings['FROM_GUI_PORT']
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                   socket.SOCK_DGRAM)  # UDP
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(('0.0.0.0', self.receive_port))
        self.receive_exit_requested = False
        self.musical_logger = logging.getLogger('musical')
        self.gui_logger = logging.getLogger('gui')

    def send(self, msg):
        '''send 'raw' messages over the socket

        message should be a dict {key: value} for json encoding'''
        self.sock.sendto(json.dumps(msg), (self.gui_host, self.send_port))

    def handle_caesura(self, director):
        '''update the GUI when a caesura happens'''
        director_fields_to_transmit = ['speed']  # ,'transpose']
        for field in director_fields_to_transmit:
            self.send({field: getattr(director, field)})
        voice_fields_to_transmit = ['pan_pos', 'binaural_diff']
        for field in voice_fields_to_transmit:
            for v in director.composer.voices.values():
                dic = {'voice_' + str(v.id) + '_' + field: getattr(v, field)}
                #print "handle caesura, voice-fields: ", dic
                self.send(dic)
        self.update_gui(director)

    def send_cycle_pos(self, director):
        '''sends a position int on every beat'''
        director_state_fields_to_transmit = ['weight',
                                             'cycle_pos']  # ,'transpose']
        for field in director_state_fields_to_transmit:
            val = director.state[field]
            if field == 'cycle_pos':
                val += 1
            self.send({field: val})

    def read_incoming_messages(self, q):
        '''reads incoming messages on the socket'''
        while not self.receive_exit_requested:
            time.sleep(0.2)
            msg = self.receiver.recv(1024)
            q.append(json.loads(msg))

    def update_gui(self, director):
        '''sends messages for a complete update of the GUI'''
        beh = director.behaviour
        for field in beh.keys():
            if (field in ['per_voice', 'meter', 'meters', 'speed'] or
                type(beh[field]).__name__ in ['list', 'dict']):
                continue
            self.send({field: beh[field]})
        for vid in beh['per_voice'].keys():
            voice = director.composer.voices[vid]
            v_beh = beh['per_voice'][vid]
            prefix = 'voice_' + str(vid) + '_'
            for field in v_beh.keys():
                if (field in ['max_num_partials'] or
                    type(v_beh[field]) in ['list', 'dict']):
                    continue
                name = prefix + field
                self.send({name: v_beh[field]})
            for field in ['num_partials',
                          'wavetable_generation_type',
                          'partial_pool']:
                do = {prefix + field: getattr(voice, field)}
                #print "update gui: ", do
                self.send(do)
        # self.gui_logger.info("sending behaviours: {0}".format(
        #         beh.saved_behaviours.keys()))
        self.send({'saved_behaviours': beh.saved_behaviours.keys()})
        self.send({'scale': director.composer.scale})
