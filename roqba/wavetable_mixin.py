from random import choice, randint

from roqba.utilities import pd_wavetables as wavetables


class WavetableMixin(object):
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
        for v in voices:
            wt = wavetable  # this is used to maintain the original state for every voice
            if self.behaviour.voice_get(v.id, "automate_wavetables") or manual:
                if not wavetable:
                    wt_sample = self.behaviour.voice_get(v.id, "wavetable_specs")
                    wt_item = choice(wt_sample)
                    #print "set wavetables, voice: ", v.id, wt_item
                    wavetable_generation_type = wt_item[0]
                    fun = getattr(wavetables, v.wavetable_generation_type + '_wavetable')
                    max_partials = self.behaviour.voice_get(v.id, "max_num_partials")
                    num_partials = (self.behaviour.voice_get(v.id, "automate_num_partials") and
                                    randint(1, max_partials) or
                                    self.behaviour.voice_get(v.id, "default_num_partial"))
                    partial_pool = choice(wt_item[1])

                    wavetable = fun(v.num_partials, v.partial_pool)
                if not incoming_wavetable:
                    v.num_partials = num_partials
                    v.partial_pool = partial_pool
                    v.wavetable_generation_type = wavetable_generation_type
                self.gateway.stop_notes_of_voice(v.id)
                #print v.id, wavetable
                self.gateway.pd_send_wavetable(v.id, wavetable)
                wavetable = wt
