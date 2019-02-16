from random import random


def get_random_adsr(min_adsr, max_adsr):
    return [random() * (max_adsr[index] - min_adsr[index]) + min_adsr[index]
            for index in range(len(max_adsr))]


class ADSRMixin(object):
    def new_random_adsr_for_all_voices(self):
        voices = list(self.composer.voices.values())
        if self.behaviour['common_adsr']:
            new_adsr = get_random_adsr(self.behaviour['min_adsr'],
                                       self.behaviour['max_adsr'])
            for voice in voices:
                self.new_adsr_for_voice(voice, new_adsr)
        else:
            for voice in voices:
                self.new_random_adsr_for_voice(voice)

    def new_random_adsr_for_voice(self, voice):
        new_adsr = adsr.get_random_adsr(
            self.behaviour.voice_get(voice.id, 'min_adsr'),
            self.behaviour.voice_get(voice.id, 'max_adsr'))
        self.new_adsr_for_voice(voice, new_adsr)

    def new_adsr_for_voice(self, voice, adsr):
        voice.current_adsr = adsr
        self.apply_voice_adsr(voice)

    def apply_voice_adsr(self, voice):
        self.gateway.send_voice_adsr(voice, voice.current_adsr)
