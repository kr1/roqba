import os
import logging
import threading
import logging.config

from roqba.director import Director
from roqba.note_gateway import NoteGateway
from roqba.utilities.logger_adapter import StyleLoggerAdapter
import roqba.static.settings as default_settings


try:
    import static.local_settings as local_settings
except ImportError:
    local_settings = default_settings
else:
    default_settings.settings.update(local_settings.settings)
    default_settings.behaviour.update(local_settings.behaviour)

    # if a style-name is set in local_settings.py, its settings and behaviour
    # will overwrite the default settings and behaviour
    if getattr(local_settings, 'style', None):
        style = local_settings.style
        _, _, behaviour = default_settings.behaviour_and_settings_from_style(
            default_settings, style)


settings = default_settings.settings

if os.environ.get("ROQBA_NO_GUI"):
    settings['gui'] = False


def main():
    '''creates a director instance and starts the main thread of the application'''
    global director, behaviour

    default_settings.flatten_meters(behaviour)

    gateway = NoteGateway(settings, behaviour)

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger('startup')
    logger = StyleLoggerAdapter(logger, None)


    director = Director(gateway, behaviour, settings)
    shutdown_event = threading.Event()
    director_thread = threading.Thread(target=director._play, args=(shutdown_event,))
    director_thread.setDaemon(True)
    director_thread.start()
    return director_thread, shutdown_event


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
