dependencies:
============

you'll need pure-data for the sound-production

getting started:
===============

open a python shell (I recommend Ipython) in this folder.
to start the app:
    from roqba import main
    main.main()
to pause:
    main.director.pause()
tu resume:
    main.director.unpause()
to stop:
    main.director.stop()

adjust speed by:
    main.director.speed = <speed>  # length of the shortest note-length in seconds.

follow the log-messages with:
    tail -f log.txt

follow a graphical (scrolling) representation on the notes played by:
    tail -f scrolling.txt 

note that on some systems (e.g. Ubuntu 10.4) tail will not continuously follow the file and it is necessary to run for example a repeated cat: 
    watch -n 0.1 cat scrolling.txt


further commands
----------------

I run puredata with the padsp oss-wrapper, after loading the oss kernel module:
    sudo modprobe -v snd-pcm-oss

puredata is started as a background process:
    padsp -n "puredata"  pd -oss -audiobuf 80 -noadc roqba.pd &

