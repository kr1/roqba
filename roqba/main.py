import logging
import threading
import logging.config

from roqba.director import Director
from roqba.note_gateway import NoteGateway
from roqba.utilities.behaviour_dict import BehaviourDict
import roqba.static.settings as default_settings

try:
    import static.local_settings as local_settings
except ImportError:
    local_settings = default_settings


default_settings.settings.update(local_settings.settings)
default_settings.behaviour.update(local_settings.behaviour)

settings = default_settings.settings
behaviour = BehaviourDict(default_settings.behaviour.items(), name='global')

gateway = NoteGateway(settings, behaviour)

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('startup')

director = Director(gateway, behaviour, settings)


def main():
    '''starts the main thread of the application'''
    director_thread = threading.Thread(target=director._play, args=())
    director_thread.start()

if __name__ == "__main__":
    print '''running this application from the interpreter lets you interact with it directly.

    In the interpreter - from the project-root run as:
    \b\b\b\bfrom roqba import main
    \b\b\b\bmain.main()
    \b\b\bstop it with:
    \b\b\b\bmain.director.stop()

    There is also a tk based gui available (start with python rogba/ui/main.py)
    '''
    main()
