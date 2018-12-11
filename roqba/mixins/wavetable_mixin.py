from random import choice, randint

from roqba.utilities import pd_wavetables as wavetables


class WavetableMixin(object):
    def set_voice_auto_wavetable(self, voice_id):
        self.set_wavetables(vid=voice_id, manual=True)

    def set_wavetables(self, vid=None, voices=None, manual=False, wavetable=None):
        '''sets new wavetables for those voices that have the

        wavetable automation flag turned on (or the manual flag set).
        when a voice-id is specified only this voice is considered'''
        incoming_wavetable = wavetable
        voices = voices if voices else [self.composer.voices[vid]]
        if self.behaviour["common_wavetables"] and not vid:
            if not wavetable:
                wt_item = choice(self.behaviour["wavetable_specs"])
                wavetable_generation_type = wt_item[0]
                fun = getattr(wavetables, wt_item[0] + '_wavetable')
                num_partials = (self.behaviour["automate_num_partials"] and
                                randint(1, self.behaviour["max_num_partials"]) or
                                self.behaviour["default_num_partial"])
                partial_pool = choice(wt_item[1])
                wavetable = fun(num_partials, partial_pool)
        else:
            wavetable = None
        for voice in voices:
            wt = wavetable  # this is used to maintain the original state for every voice
            if self.behaviour.voice_get(voice.id, "automate_wavetables") or manual:
                if not wavetable:
                    wavetable = self.determine_new_voice_wavetable(voice)
                self.gateway.stop_notes_of_voice(voice.id)
                # print voice.id, wavetable
                self.gateway.pd_send_wavetable(voice.id, wavetable)
                wavetable = wt

    def determine_new_voice_wavetable(self, voice):
        wt_sample = self.behaviour.voice_get(voice.id, "wavetable_specs")
        wt_item = choice(wt_sample)
        # print "set wavetables, voice: ", voice.id, wt_item
        wavetable_generation_type = wt_item[0]
        fun = getattr(wavetables, wavetable_generation_type + '_wavetable')
        max_partials = self.behaviour.voice_get(voice.id, "max_num_partials")
        voice.num_partials = (self.behaviour.voice_get(voice.id, "automate_num_partials") and
                        randint(1, max_partials) or
                        self.behaviour.voice_get(voice.id, "default_num_partial"))
        voice.partial_pool = choice(wt_item[1])

        wavetable = fun(voice.num_partials, voice.partial_pool)
        return wavetable
