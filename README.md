Documentation
=============

see the [documentation](http://kr1.github.com/roqba/docs/build/html/index.html)

Dependencies:
============

You'll need [**Pure Data**](http://puredata.info/) for the sound-production.
Some objects rely on external libraries of *Pure Data*. Please see the documentation for details.

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
