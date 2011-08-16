import socket
import json
from math import floor
from Tkinter import tkinter
from Tkinter import Frame, HORIZONTAL, IntVar, W, N, E
from Tkinter import Checkbutton, Scale, Button

# TODO?: integration into roqba
#from roqba.static.settings import settings

host = "localhost"
port = 12322
send_port = 12323


CHECK_BUTTONS = {'automate_speed_change': {'val': True, 'disable': True},
                 'automate_shuffle': True,
                 'automate_meters': True,
                 'automate_wavetables': True,
                 'automate_num_partials': True,
                 'automate_transpose': True,
                 'automate_slide': {'val': True, 'disable': True},
                 'automate_pan': True,
                 'automate_binaural_diffs': True,
                 'pan_controls_binaural_diff': True,
                 'common_wavetables': True,
                 'play': True}

SCALES = {'caesura_probability': {'min': 0.01, 'max': 1, 'start': 0.666, 'res': 0.001},
          'slide_in_msec': {'min': 0, 'max': 5000, 'start': 200, 'res': 1, 'enable':'automate_slide'},
          'transpose': {'min': -24, 'max': 24, 'start': 12, 'res': 1},
          'shuffle_delay': {'min': 0, 'max': 1, 'start': 0.2, 'res': 0.0001},
          'speed': {'min': 0.1, 'max': 1.2, 'start': 0.2, 'res': 0.0001, 'enable': 'automate_speed_change'},
          'max_shuffle': {'min': 0, 'max': 0.8, 'start': 0.2, 'res': 0.0001},
          'binaural_diff': {'min': 0, 'max': 66, 'start': 0.2, 'res': 0.01},
          'max_binaural_diff': {'min': 0, 'max': 66, 'start': 30, 'res': 0.01},
         }

RANGES = {'speed': {'min': 0.1, 'max': 1.2, 'min_start': 0.2, 'max_start': 1.1, 'res': 0.001, 'disable': 'automate_speed_change'}}

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.grid()
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        self.columnconfigure(2, minsize=200)
        self.columnconfigure(3, minsize=150)
        self.columnconfigure(4, minsize=150)
        self.columnconfigure(5, minsize=150)
        self.columnconfigure(6, minsize=150)
        self.createWidgets()

    def createWidgets(self):
        self.create_check_buttons()
        self.create_ranges()
        self.create_scales()
        self.create_voices()
        self.create_monitor()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(columnspan=7, sticky=E+W)

    def create_monitor(self):
        this= Scale(self, label='cycle_pos', orient=HORIZONTAL,
                         from_=1, to=16, resolution=1)
        this.disable, this.enable = (None, None)
        this.ref = 'cycle_pos'
        this.grid(column=0, row=10,sticky=E+W)

    def create_voices(self):
        voice_ids = ['1','2','3','4']  
        elements = {'pan_pos': {'min': -1, 'max': 1, 'start': 0.5, 'res': 0.001},
                    'binaural_diff': {'min': 0, 'max': 66, 'start': 0.2, 'res': 0.01}}
        for vid in voice_ids:
            counter = 0
            for ele in elements:
                name = 'voice_' + vid + '_' + ele
                setattr(self, 'min_' + name, elements[ele]['min'])
                setattr(self, 'max_' + name, elements[ele]['max'])
                this_ele = Scale(self, label=name, orient=HORIZONTAL,
                                        from_=getattr(self, 'min_' + name), to=getattr(self, 'max_' + name), 
                                        resolution=elements[ele]['res'])
                this_ele.enable = ('enable' in elements[ele].keys() and elements[ele]['enable'] or None)
                this_ele.disable = ('disable' in elements[ele].keys() and elements[ele]['disable'] or None)
                this_ele.grid(column=int(2 + int(vid)), row=counter, sticky=E+W)
                this_ele.ref = name
                counter += 1

    def create_check_buttons(self):
        counter = 0
        self.cb_frame = Frame(self)
        for cb in CHECK_BUTTONS:
            setattr(self, cb, IntVar(value=type(CHECK_BUTTONS[cb]) == dict and CHECK_BUTTONS[cb]['val'] or CHECK_BUTTONS[cb]))
            self.this_cb = Checkbutton(self.cb_frame, text=cb, variable=getattr(self, cb))
            self.this_cb.bind('<Button-1>', self.check_boxes_handler)
            self.this_cb.disable = type(CHECK_BUTTONS[cb]) == dict and 'disable' in CHECK_BUTTONS[cb].keys()
            self.this_cb.grid(sticky=W, column=0, row=counter)
            self.this_cb.ref = cb
            counter += 1
        self.cb_frame.grid(column=0, rowspan=10, sticky=N)

    def set_value(self, name, val):
        '''set a scale to the specified value'''
        for w in self.children.values():
            if w.__class__.__name__ == 'Scale' and w.ref == name:
                w.set(val)
        
    def check_boxes_handler(self, event):
        '''handles checkbox events.
        
        shows and hides gui elements according to their enable/disable fields'''
        #print event.__dict__
        #print event.widget.__dict__
        ref = event.widget.ref
        val = not getattr(self, ref).get() # because is read before the var is changed
        self.send({ref: val})
        print ref, val 
        # handle gui elements
        if event.widget.disable:
            for w in self.children.values():
                # this try clause is for debugging, remove when stable 
                try:
                    w.ref
                    #print w.ref
                except:
                    pass
                if (w.__class__.__name__ == 'Scale' and 
                    (w.disable or w.enable)):
                    if w.disable == ref:
                        if val:
                            w.grid_remove()
                        else:
                            w.grid()
                    elif w.enable == ref:
                        if val:
                            w.grid()
                        else:
                            w.grid_remove()
                    #print w.disable, w.enable

    def create_scales(self): 
        counter = 0
        for sca in SCALES:
            setattr(self, 'min_' + sca, SCALES[sca]['min'])
            setattr(self, 'max_' + sca, SCALES[sca]['max'])
            self.this_scale = Scale(self, label=sca, orient=HORIZONTAL,
                                    from_=getattr(self, 'min_' + sca), to=getattr(self, 'max_' + sca), 
                                    resolution=SCALES[sca]['res'])
            self.this_scale.set(SCALES[sca]['start'])
            self.this_scale.enable = ('enable' in SCALES[sca].keys() and SCALES[sca]['enable'] or None)
            self.this_scale.disable = ('disable' in SCALES[sca].keys() and SCALES[sca]['disable'] or None)
            self.this_scale.grid(column=1, row=counter, sticky=E+W)
            self.this_scale.ref = sca
            self.this_scale.bind("<ButtonRelease>", self.scale_handler)
            counter += 1

    def scale_handler(self, event):
        self.send({event.widget.ref: event.widget.get()})
        print event.widget.ref, event.widget.get()

    def send(self, msg):
        self.send_sock.sendto(json.dumps(msg), (host, send_port))
        pass

    def create_ranges(self): 
        counter = 0
        for ran in RANGES:
            setattr(self, 'min_' + ran, RANGES[ran]['min'])
            setattr(self, 'max_' + ran, RANGES[ran]['max'])
            self.this_min_scale = Scale(self, label='min ' + ran, orient=HORIZONTAL,
                                        from_=getattr(self, 'min_' + ran), to=getattr(self, 'max_' + ran), 
                                        resolution=RANGES[ran]['res'])
            self.this_max_scale = Scale(self, label='max ' + ran, orient=HORIZONTAL, 
                                        from_=getattr(self, 'min_' + ran), to=getattr(self, 'max_' + ran), 
                                        resolution=RANGES[ran]['res'])
            self.this_min_scale.set(RANGES[ran]['min_start'])
            self.this_max_scale.set(RANGES[ran]['max_start'])
            self.this_min_scale.enable = ('enable' in RANGES[ran].keys() and RANGES[ran]['enable'] or None)
            self.this_min_scale.disable = ('disable' in RANGES[ran].keys() and RANGES[ran]['disable'] or None)
            self.this_max_scale.enable = ('enable' in RANGES[ran].keys() and RANGES[ran]['enable'] or None)
            self.this_max_scale.disable = ('disable' in RANGES[ran].keys() and RANGES[ran]['disable'] or None)
            self.this_min_scale.grid(column=2, row=counter, sticky=E+W)
            self.this_max_scale.grid(column=2, row=counter + 1, sticky=E+W)
            self.this_min_scale.ref = 'min_' + ran
            self.this_max_scale.ref = 'max_' + ran
            counter += 2

    def socket_read_handler(self, file, mask):
        data_object = json.loads(file.recv(1024))
        do = data_object.items()[0]
        self.set_value(do[0], do[1])

app = Application()
tkinter.createfilehandler(app.sock, tkinter.READABLE, app.socket_read_handler)
app.master.title("Roqba Controls")
app.mainloop()

