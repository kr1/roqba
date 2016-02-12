Overview
========

Audio-Samples
-------------

.. raw:: html

   <p>
   <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/245319230&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>
   </p>
   <p>
   <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/73454551&amp;color=ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false"></iframe>
   </p>

Dependencies
------------

You'll need `Pure Data <http://puredata.info/>`_ for sound-production.
Some objects rely on external *puredata* libraries. These can be installed with the deken plugin.

Getting started
---------------

Open a python shell (I recommend `Ipython <http://ipython.scipy.org/moin/>`_) in this folder.
to start the app::

    from roqba import main
    main.main()

..

to pause::

    main.director.pause()

..

to resume::

    main.director.unpause()

..

to stop::

    main.director.stop()

..

adjust speed by::

    main.director.speed = <speed>  # length of the shortest note-length in seconds.

..

follow the log-messages with::

    tail -f log.txt

..

follow a graphical (scrolling) representation on the notes played by:

    tail -f scrolling.txt

..

note that on some systems tail will not continuously follow
the file and it is necessary to run for example a repeated cat::

    watch -n 0.1 cat scrolling.txt

..


diagram
-------

.. image:: _static/roqba_highlevel.png
   :width: 700



_`introduction`
---------------

| main starts a thread in which the app runs.
| director contains the main loop in its `_play` method. 
| `_play` calls the _Composers_ (synchronous) `generate` method following the metronome's clock
| `generate` calls the voices' coroutines until a satisfactory harmonic result is obtained.
| the stream-analyzer (and performer) controls if there are drum-fills or embellishments to be added. it also checks for conditions of a ceasura.
| If a caesura is given, a flag is set which the director uses to modify its behaviour.
| Finally the musical frame is sent to both the Note-Gateway and the Notator module.

.. toctree::
    :maxdepth: 1

    events_and_messages
