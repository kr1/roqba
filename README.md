Documentation
=============

see the [documentation](http://kr1.github.com/roqba/docs/build/html/index.html)

Dependencies:
============

you'll need [**Pure Data**](http://puredata.info/) for the sound-production.
some objects rely on libraries that come with the extended Pure Data version known as [**pd-extended**](http://puredata.info/community/projects/software/pd-extended).

getting started:
===============

open a python shell (I recommend [**Ipython**](http://ipython.scipy.org/moin/)) in this folder.
to start the app:  
<code>
    from roqba import main  
    main.main()  
</code>
to pause:  
<code>
    main.director.pause()  
</code>
to resume:  
<code>
    main.director.unpause()  
</code>
to stop:  
<code>
    main.director.stop()  
</code>

adjust speed by:  
<code>
    main.director.speed = <speed>  # length of the shortest note-length in seconds.
</code>

follow the log-messages with:  
<code>
    tail -f log.txt
</code>

follow a graphical (scrolling) representation on the notes played by: 
<code>
    tail -f scrolling.txt 
</code>

note that on some systems (e.g. Ubuntu 10.4) tail will not continuously follow the file and it is necessary to run for example a repeated cat: 
<code>
    watch -n 0.1 cat scrolling.txt
</code>


further commands
----------------

I run puredata with the padsp oss-wrapper, after loading the oss kernel module:
<code>
    sudo modprobe -v snd-pcm-oss
</code>

puredata is started as a background process:
<code>
    padsp -n "puredata"  pd -oss -audiobuf 80 -noadc roqba.pd &
</code>

