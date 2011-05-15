
import logging
import threading
import logging.config

from voice import Voice
from composer import Composer
from director import Director
#from settings_and_behaviour import settings, behaviour, BehaviourDict
from behaviour_dict import BehaviourDict
import note_gateway


#print behaviour
#print behaviour.real_setters

settings = {'number_of_voices': 4,
            'voice_registers': ['BASS', 'MID', 'MID', 'HIGH'],
            'PD_HOST': 'localhost',
            'PD_PORT': 12321,
            'track_voices_length': 666,
            'lowest_note_num': 0,
            'highest_note_num': 127,
            }

behaviour = {"speed": 0.3,
             "max_speed": 0.8,
             "min_speed": 0.14,
             # speed-target:
             # 0.5 means that the average of all speeds will be
             # +/- in the middle of the given range
             # 0.25 means that the average of speeds will be at the first
             # quarter of the range
             "speed_target": 0.35,
             'slide_in_msecs': 200,
             "speed_change": "leap",  # alt:"transition"
             "shuffle_delay": 0.1,  # keep this between 0 and MAX_SHUFFLE
             "max_shuffle": 0.1,
             'meter': (5, (2, 3)),
             'transpose': 12,
             'binaural_diff': 0.666,
             'max_binaural_diff': 10,
             'slide_duration_msecs': 100,
             'automate_binaural_diffs': True,  # alt: False
             'default_slide_duration_prop': 0.666,  # proportion
             'embellishment_speed_lim': 0.666,
             'default_pause_prob': 0.03,
             'default_embellishment_prob': 0.005
            }

behaviour = BehaviourDict(behaviour.items())

gateway = note_gateway.NoteGateway(settings, behaviour)
gateway.hub().next()

def startup():
    '''created the composer instance and the voices'''
    logger.info("starting up ===========------------------->>>>>>>>>>>>>>>")
    c = Composer(gateway, settings, behaviour)
    for voice_idx in xrange(settings["number_of_voices"]):
        Voice(voice_idx + 1, c,
              register=settings["voice_registers"][voice_idx])
    return c

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

go = True
composer = startup()
state = {"comp": composer, "speed": behaviour["speed"]}
director = Director(composer, state, behaviour, settings)


def add_setters():
    behaviour.real_setters["meter"] = director.set_meter
    behaviour.real_setters["binaural_diff"] = director.set_meter
    behaviour.real_setters["slide_duration_msecs"] = gateway.set_slide_msecs_for_all_voices

def main():
    '''starts the main thread of the application'''
    add_setters()
    threading.Thread(target=director._play, args=()).start()
    composer.report()

if __name__ == "__main__":
    print '''please run this app from the interpreter as:
    \b\b\b\bimport main
    \b\b\b\bmain.main()
    \b\b\bstop it with:
    \b\b\b\bmain.director.stop()
    '''
