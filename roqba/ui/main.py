import socket
import json
from collections import OrderedDict
from re import match
from Tkinter import tkinter
from Tkinter import Frame, HORIZONTAL, IntVar, StringVar, W, N, E
from Tkinter import LabelFrame, Checkbutton, Radiobutton, Scale, Button

# TODO?: integration into roqba
#from roqba.static.settings import settings

host = "localhost"
port = 12322
send_port = 12323


CHECK_BUTTONS = OrderedDict([
                 ('automate_speed_change', {'val': True, 'disable': True}),
                 ('automate_shuffle', True),
                 ('automate_meters', True),
                 ('automate_wavetables', True),
                 ('automate_num_partials', False),
                 ('automate_transpose', True),
                 ('automate_slide', {'val': True, 'disable': True}),
                 ('automate_pan', True),
                 ('automate_binaural_diffs', True),
                 ('pan_controls_binaural_diff', True),
                 ('common_wavetables', True),
                 ('play', {'val': True, 'sub_frame': 'monitor_frame'})
               ])

SCALES = {'caesura_prob': {'min': 0.01, 'max': 1, 'start': 0.666, 'res': 0.001, 'label': 'probability of a caesura'},
          'slide_duration_msecs': {'min': 0, 'max': 5000, 'start': 200, 'res': 1, 'enable':'automate_slide', 'label': 'slide duration in msecs'},
          'transpose': {'min': -24, 'max': 24, 'start': 12, 'res': 1},
          'shuffle_delay': {'min': 0, 'max': 1, 'start': 0.2, 'res': 0.0001},
          'speed': {'min': 0.1, 'max': 1.2, 'start': 0.2, 'res': 0.0001, 'enable': 'automate_speed_change'},
          'max_shuffle': {'min': 0, 'max': 0.8, 'start': 0.2, 'res': 0.0001},
          'binaural_diff': {'min': 0, 'max': 66, 'start': 0.2, 'res': 0.01},
          'max_binaural_diff': {'min': 0, 'max': 66, 'start': 30, 'res': 0.01},
          'speed_target': {'min': 0,'max': 1, 'start': 0.5, 'res': 0.001,
                           'label': 'distort speed (slower/faster)', 'pos': {'c':2,'r':2}}
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
        self.create_widgets()
        self.settables = self.assemble_settables()
        self.request_update()

    def create_widgets(self):
        self.create_monitor()
        self.create_check_buttons()
        self.create_ranges()
        self.create_scales()
        self.create_radio_buttons()
        self.create_voices()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(columnspan=7, sticky=E+W)

    def assemble_settables(self):
        settables = self.winfo_children()
        for w in settables:
            settables += w.winfo_children()
        return filter(lambda w: w.__class__.__name__ in ['Scale', 'Checkbutton'], settables)

    def create_radio_buttons(self):
        # Scale related
        entries =  ['DIATONIC', 'HARMONIC', 'MELODIC', 'PENTATONIC', 'PENTA_MINOR']
        self.scale = StringVar()
        self.scale.set('DIATONIC')
        self.rb_frame = Frame(self)
        for e in entries:
            rb = Radiobutton(self.rb_frame, value=e, text=e, anchor=W, command=self.send_scale, variable=self.scale)
            rb.grid(row=len(self.rb_frame.winfo_children()), sticky=W)
        self.rb_frame.grid(column=1, row=len(self.grid_slaves(column=1)),rowspan=3)

    def create_monitor(self):
        self.monitor_frame = LabelFrame(self, text="Monitor and Transport")
        this_cycle = Scale(self.monitor_frame, label='cycle_pos', orient=HORIZONTAL,
                         from_=1, to=16, resolution=1)
        this_cycle.disable, this_cycle.enable = (None, None)
        this_cycle.ref = 'cycle_pos'
        this_cycle.grid(column=0, row=0, sticky=E+W)
        self.updateButton = Button(self.monitor_frame, text='Reload all Settings', command=self.request_update)
        self.updateButton.grid(row=1, sticky=E+W)
        self.ForceCaesuraButton = Button(self.monitor_frame, text='Force Caesura', command=self.force_caesura)
        self.ForceCaesuraButton.grid(row=2, sticky=E+W)
        self.monitor_frame.grid(column=0, row=10, sticky=E+W)

    def request_update(self):
        self.send({'sys': 'update'})

    def force_caesura(self):
      self.send({'force_caesura': True})

    def create_voices(self):
        voice_ids = ['1','2','3','4']  
        SCALES = OrderedDict([
                  ('pan_pos', {'min': -1, 'max': 1, 'start': 0.5, 'res': 0.001}),
                  ('slide_duration_msecs', {'min': 0, 'max': 2000, 'start': 60, 'res': 1}),
                  ('slide_duration_prop', {'min': 0, 'max': 2, 'start': 0.666, 'res': 0.001}),
                  ('binaural_diff', {'min': 0, 'max': 66, 'start': 0.2, 'res': 0.01})
                ])
        
        for vid in voice_ids:
            counter = 0
            for sca in SCALES:
                name = 'voice_' + vid + '_' + sca
                setattr(self, 'min_' + name, SCALES[sca]['min'])
                setattr(self, 'max_' + name, SCALES[sca]['max'])
                this_sca = Scale(self, label=sca, orient=HORIZONTAL,
                                        from_=getattr(self, 'min_' + name), to=getattr(self, 'max_' + name), 
                                        resolution=SCALES[sca]['res'])
                this_sca.enable = ('enable' in SCALES[sca].keys() and SCALES[sca]['enable'] or None)
                this_sca.disable = ('disable' in SCALES[sca].keys() and SCALES[sca]['disable'] or None)
                this_sca.grid(column=int(2 + int(vid)), row=counter, sticky=E+W)
                this_sca.bind("<ButtonRelease>", self.scale_handler)
                this_sca.ref = name
                counter += 1
        CHECK_BUTTONS = OrderedDict(
                 [('mute', False),
                  ('automate_binaural_diffs', True),
                  ('automate_note_duration_prop', True),
                  ('use_proportional_slide_duration', {'val': True, 'label': 'proportional slide'}),
                  ('automate_pan', True),
                  ('automate_wavetables', True)])
        for vid in voice_ids:
            counter = 0
            cb_frame = LabelFrame(self, text="Voice {0} - Automation".format(vid))
            setattr(self, 'voice_' + vid + '_cb_frame', cb_frame)
            for cb in CHECK_BUTTONS:
                options = CHECK_BUTTONS[cb]
                name = 'voice_' + vid + '_' + cb 
                label = (options['label'] if isinstance(options, dict) and 'label' in options.keys() else
                                              (cb[9:] if cb[:9] == 'automate_' else cb))
                setattr(self, name, IntVar(value=type(options) == dict and options['val'] or options))
                self.this_cb = Checkbutton(cb_frame, text=label, variable=getattr(self, name))
                self.this_cb.bind('<Button-1>', self.check_boxes_handler)
                self.this_cb.disable = None
                self.this_cb.grid(sticky=W, column=0, row=counter)
                self.this_cb.ref = name
                counter += 1
            # add trigger wavetable-button
            trigWavetableButton = Button(cb_frame, text='Random Wavetable')
            trigWavetableButton.bind('<Button-1>', self.trigger_waveform_handler)
            trigWavetableButton.ref = 'voice_' + vid + "_trigger_wavetable"
            trigWavetableButton.grid(row=counter)
            cb_frame.grid(column=int(vid) + 2, row=4, sticky=N, rowspan=8)
        for vid in voice_ids:
            generation_types =  ["random", "random_harmonic", "harmonic"]
            partial_pools = ["even", "odd", "all"]
            types_name = 'voice_' + vid + '_' + 'wavetable_generation_type'
            pools_name = 'voice_' + vid + '_' + 'partial_pool'
            setattr(self, types_name , StringVar())
            getattr(self, types_name).set("random")
            setattr(self, pools_name , StringVar())
            getattr(self, pools_name).set("all")
            target_frame = getattr(self, 'voice_' + vid + '_cb_frame')
            for gen_t in generation_types:
                gen_t_entry = Radiobutton(target_frame, value=gen_t, text=gen_t, anchor=W,
                                          variable=getattr(self, types_name))
                gen_t_entry.bind('<ButtonRelease-1>', self.wt_handler)
                gen_t_entry.ref = types_name
                gen_t_entry.grid(row=len(target_frame.winfo_children()), sticky=W)
            for pp in partial_pools:
                pp_entry = Radiobutton(target_frame, value=pp, text=pp, anchor=W,
                                        variable=getattr(self, pools_name))
                pp_entry.bind('<ButtonRelease-1>', self.wt_handler)
                pp_entry.ref = pools_name
                pp_entry.grid(row=len(target_frame.winfo_children()), sticky=W)

    def wt_handler(self, event):
        print event.widget.tk
        ref = event.widget.ref
        self.send({ref: getattr(self, ref).get()})

    def create_check_buttons(self):
        self.cb_frame = LabelFrame(self, text="Global Settings")
        for cb in CHECK_BUTTONS:
            label = cb 
            target_parent = self.cb_frame
            if isinstance(CHECK_BUTTONS[cb], dict) and  'sub_frame' in CHECK_BUTTONS[cb].keys():
                target_parent = getattr(self, CHECK_BUTTONS[cb]['sub_frame'])
            setattr(self, cb, IntVar(value=type(CHECK_BUTTONS[cb]) == dict and CHECK_BUTTONS[cb]['val'] or CHECK_BUTTONS[cb]))
            self.this_cb = Checkbutton(target_parent, text=label, variable=getattr(self, cb))
            self.this_cb.bind('<Button-1>', self.check_boxes_handler)
            self.this_cb.disable = type(CHECK_BUTTONS[cb]) == dict and 'disable' in CHECK_BUTTONS[cb].keys()
            self.this_cb.grid(sticky=W, column=0, row=len(target_parent.winfo_children()))
            self.this_cb.ref = cb
        self.cb_frame.grid(column=0, row=0, rowspan=10, sticky=N)

    def set_value(self, name, val):
        '''set a widget to the specified value'''
        direct = ['scale', 'wavetable_generation_type', 'partial_pool']
        if filter(lambda x: match("(voice_\d_|)" + x, name), direct):
            print "setting:" , name, " to: ", val
            getattr(self, name).set(val)
            return
        for w in self.settables:
            typ = w.__class__.__name__
            if w.ref == name:
                #print "setting '{0}' of type: '{1}' to: {2}".format(name, typ, val)
                if typ == 'Scale':
                    w.set(val)
                elif typ == "Checkbutton":
                    w.select() if val else w.deselect()

        
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
        # enable/disable functionality temporarily(?) commented on: 
        # Wed Aug 17 09:39:54 CEST 2011
#        if event.widget.disable:
#            for w in self.children.values():
#                
#                # this try clause is for debugging, remove when stable 
#                try:
#                    w.ref
#                    #print w.ref
#                except:
#                    pass
#                if (w.__class__.__name__ == 'Scale' and 
#                    (w.disable or w.enable)):
#                    if w.disable == ref:
#                        if val:
#                            w.grid()
#                        else:
#                            w.grid_remove()
#                    elif w.enable == ref:
#                        if val:
#                            w.grid_remove()
#                        else:
#                            w.grid()
#                    #print w.disable, w.enable

    def create_scales(self): 
        counter = 0
        for sca in SCALES:
            label = SCALES[sca]['label'] if 'label'  in SCALES[sca].keys() else sca
            setattr(self, 'min_' + sca, SCALES[sca]['min'])
            setattr(self, 'max_' + sca, SCALES[sca]['max'])
            self.this_scale = Scale(self, label=label, orient=HORIZONTAL,
                                    from_=getattr(self, 'min_' + sca), to=getattr(self, 'max_' + sca), 
                                    resolution=SCALES[sca]['res'])
            self.this_scale.set(SCALES[sca]['start'])
            self.this_scale.enable = ('enable' in SCALES[sca].keys() and SCALES[sca]['enable'] or None)
            self.this_scale.disable = ('disable' in SCALES[sca].keys() and SCALES[sca]['disable'] or None)
            if 'pos' in SCALES[sca].keys():
                pos =  SCALES[sca]['pos']
                col = pos['c']
                row = pos['r']
            else:
                row = counter
                col = 1
                counter += 1
            self.this_scale.grid(column=col, row=row, sticky=E+W)
            self.this_scale.ref = sca
            self.this_scale.bind("<ButtonRelease>", self.scale_handler)

    def scale_handler(self, event):
        self.send({event.widget.ref: event.widget.get()})
        print event.widget.ref, event.widget.get()

    def trigger_waveform_handler(self, event):
        self.send({event.widget.ref: True})
        #print event.widget.ref, "- triggering wavetable"

    def send_scale(self):
        do = {'scale':self.scale.get()}
        self.send(do)
        #print do

    def send(self, msg):
        print "sending: ", msg
        self.send_sock.sendto(json.dumps(msg), (host, send_port))

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
            self.this_min_scale.bind("<ButtonRelease>", self.scale_handler)
            self.this_max_scale.bind("<ButtonRelease>", self.scale_handler)
            counter += 2

    def socket_read_handler(self, file, mask):
        data_object = json.loads(file.recv(1024))
        do = data_object.items()[0]
        #print do
        self.set_value(do[0], do[1])

app = Application()
tkinter.createfilehandler(app.sock, tkinter.READABLE, app.socket_read_handler)
app.master.title("Roqba Controls")
app.mainloop()

