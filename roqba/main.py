import logging
import threading
import logging.config

from voice import Voice
from composer import Composer
from director import Director
from note_gateway import NoteGateway
from utilities.behaviour_dict import BehaviourDict
from webserver.rogba_server import start_server
import static.settings as default_settings

try:
    import static.local_settings as local_settings
except ImportError:
    local_settings = default_settings


default_settings.settings.update(local_settings.settings)
default_settings.behaviour.update(local_settings.behaviour)

settings = default_settings.settings
behaviour = BehaviourDict(default_settings.behaviour.items(), name='global')

gateway = NoteGateway(settings, behaviour)
gateway.hub().next()


def startup():
    '''creates the composer instance and the voices'''
    logger.info("starting up ===========------------------->>>>>>>>>>>>>>>")
    c = Composer(gateway, settings, behaviour)
    for voice_idx in xrange(settings["number_of_voices"]):
        Voice(voice_idx + 1, c,
              note_length_grouping=behaviour["meter"][1],
              register=settings["voice_registers"][voice_idx],
              behaviour=settings['voice_behaviours'][voice_idx])
    return c

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

go = True
composer = startup()
state = {"comp": composer, "speed": behaviour["speed"]}
director = Director(composer, state, behaviour, settings)


def add_setters():
    behaviour.real_setters["meter"] = director.set_meter
    behaviour.real_setters["transpose"] = director.gateway.set_transpose
    behaviour.real_setters["speed"] = director.new_speed
    behaviour.real_setters["binaural_diff"] = composer.set_binaural_diffs
    behaviour.real_setters["slide_duration_msecs"] = gateway.set_slide_msecs_for_all_voices
    for vid in behaviour['per_voice'].keys():
        behaviour['per_voice'][vid].real_setters["pan_pos"] = [composer.voices[vid].set_pan_pos, director.gateway]
        behaviour['per_voice'][vid].real_setters["slide_duration_msecs"] = [director.gateway.set_slide_msecs, vid]

def main():
    '''starts the main thread of the application'''
    add_setters()
    threading.Thread(target=director._play, args=()).start()
    threading.Thread(target=start_server, args=(gateway.pd.msg_queue,)).start()
    composer.report()

if __name__ == "__main__":
    print '''please run this app from the interpreter as:
    \b\b\b\bfrom roqba import main
    \b\b\b\bmain.main()
    \b\b\bstop it with:
    \b\b\b\bmain.director.stop()
    '''
