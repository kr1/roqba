# About

Roqba is a realtime music machine (composer, synthesizer and player)

# How does it sound?

Hear some snippets [here](http://kr1.github.io/roqba/docs/build/html/readme.html#audio-samples)

# Documentation

see the [documentation](http://kr1.github.com/roqba/docs/build/html/index.html)

# Dependencies

You'll need [**Pure Data**](http://puredata.info/) for the sound-production.
Some objects rely on external libraries of *Pure Data*.
Please see the documentation for details.

# Getting started

## puredata

install puredata with the following extension libraries (example for a debian based linux)  
```bash
    apt-get install pd-unauthorized pd-motex pd-zexy pd-cyclone pd-ext13 pd-list-abs pd-pan pd-creb
```

puredata creates the sounds, run it with  
```bash
    pd pd/roqba.pd
```

or without a GUI:
```bash
    pd -noadc -nodac -nogui -stderr pd/roqba.pd
```

## start the music

open a python shell (I recommend [**IPython**](http://ipython.org)) in this folder.

to start the app  
```python
    from roqba import main  
    main.main()  
```

## control from the shell

to pause  
```python
    main.director.pause()  
```

to resume  
```python
    main.director.unpause()  
```

to stop  
```python
    main.director.stop()  
```

adjust speed by  
```python
    main.director.speed = <speed>  # length of the shortest note-length in seconds.
```

### control with GUI

start the GUI  
```python
    python roqba/ui/main.py
```

### logging

follow the log-messages with  
```python
    tail -f log.txt
```

follow a graphical (scrolling) representation on the notes played by  
```python
    tail -f scrolling.txt  
```
