from roqba.utilities.behaviour_dict import BehaviourDict


class IncomingMessagesMixin(object):
    def handle_incoming_message(self, msg):
        """handles incoming messages from the gui interface

        TODO: keep a current-settings dataobject where to track
        all current settings and which can be used to write a snapshot
        of a particular moment
        """
        key, val = msg.items()[0]
        self.gui_logger.info("incoming message '{0}' with value '{1}'".format(key, val))
        if key[0:6] == 'voice_':
            split = key.split("_")
            vid = int(split[1])
            voice = self.composer.voices[vid]
            v_key = "_".join(split[2:])
            self.behaviour_logger.info("setting {0} of voice {1} to {2}".format(v_key, vid, val))
            if v_key in ['wavetable_generation_type',
                         'num_partials',
                         'partial_pool']:
                setattr(self.composer.voices[vid], v_key, val)
                wavetable = voice.make_wavetable()
                self.set_wavetables(manual=True, wavetable=wavetable, vid=vid)
                return
            # settings that must be transmitted to the sound-engine
            if v_key in ['volume']:
                voice.volume = val
                self.gateway.send_voice_volume(voice, val)
                return
            # this is the standard handling
            self.behaviour["per_voice"][vid][v_key] = val
            if v_key == "mute":
                self.gateway.mute_voice(vid, val is True)
            elif v_key == "trigger_wavetable":
                self.set_wavetables(vid=vid, manual=True)
                self.gui_sender.update_gui(self)
        elif key in self.allowed_incoming_messages:
            if key in self.behaviour.keys():
                self.behaviour_logger.info("setting {0} to {1}".format(key, val))
                self.behaviour[key] = val
            elif key == "play":
                val and self.unpause() or self.pause()
            elif key == "sys":
                if val == 'update':
                    self.gui_sender.update_gui(self)
                elif val == 'save_behaviour':
                    self.behaviour.save_current_behaviour()
                elif val[0] == 'save_behaviour':
                    self.behaviour.save_current_behaviour(name=val[1])
                elif val[0] == 'change_behaviour':
                    new_behaviour = val[1]
                    self.behaviour_logger.info("setting behaviour to: {0}".format(new_behaviour))
                    self.behaviour = BehaviourDict(self.behaviour.saved_behaviours[new_behaviour])
                    for key, per_voice in self.behaviour['per_voice'].items():
                        per_voice = BehaviourDict(per_voice)
                    self.gui_sender.update_gui(self)
                    #TODO: apply new behaviour (attention recreation of behaviour dicts?)
            elif key == 'scale':
                self.composer.set_scale(val)
            elif key == "force_caesura":
                self.force_caesura = True
            elif key == "trigger_wavetable":
                self.behaviour_logger.info("setting a new wavetable for all voices")
                self.set_wavetables(manual=True, voices=self.composer.voices.values())
                self.gui_sender.update_gui(self)
