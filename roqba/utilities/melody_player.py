"""this file defines a utility class that can be used in writing melodies


its main target is to play melodies defined in static.melodies
NB: the sound-engine has to be on to hear the melody
usage:
  1. create an instance of melody player.
  2. set its melody attribute
  3. call play()
"""
import time
from roqba.composer import Composer
from roqba.static.scales_and_harmonies import SCALES
from roqba.static.settings import settings
from roqba.utilities.pdsender import PdSender


class MelodyPlayer():
    def __init__(self, speed=0.1):
        self.melody = None
        self.speed = speed
        self.static_start_note = 61
        self.transpose = 0
        self.pd = PdSender(settings["PD_HOST"], settings["PD_PORT"])

    def play(self):
        """plays the melody given in the self.melody attribute

        by sending the necessary messages to the roqba-sound-engine"""
        if not self.melody:
            raise "ImpossibleRequestError", "no melody given"
        self.real_scale = Composer.assemble_real_scale(
                              SCALES[self.melody['scale']])
        start_note_index = (self.real_scale.index(self.static_start_note) +
                            self.melody['start_note'])
        real_start_note = self.real_scale[start_note_index]
        current_note = real_start_note
        self.pd.send("sound 1")
        for note in self.melody['melody']:
            next_note_idx = self.real_scale.index(current_note) + note[0]
            next_note = self.real_scale[next_note_idx]
            print next_note + self.transpose,
            self.pd.send(["voice", 1, "dur", self.speed * note[1] * 1000])
            self.pd.send(["voice", 1, next_note + self.transpose])
            time.sleep(self.speed * note[1])
            current_note = next_note
