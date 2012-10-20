MAIN CALL CHAINS AND SEQUENCES
==============================

**director**: *_play*
    - cycle_pos, weight = **metronome**.*beat*()
    - IF meter-position is HEAVY (a ***2*** n the meter):
        - **composer**: *choose_rhythm*
            - **voice**: 
                1. *set_rhythm_grouping*
                2. *apply_overhanging_notes*
    - **composer**: *generate* (main method - coroutine - that generates the next polyphonic step)
        - **voices**: 
            - *generate* (the single voices generate their next step)
              the harmony is cumulatively created and later voices have to move their notes 
              to comply with harmonic necessities
            - eventual "SLAVE" voice is made to follow another voice for some notes
        - note duration is registered for the each note
        - *apply_scale()*
        - *embellish(state)*
        - *stream_analyzer()* : decision if a caesura should take place (by setting <comment>-attribute to 'caesura')
        - **drummer**: *generate*
        - **percussion_hub**: send drum-frame to sound-engine
        - **hub**: send voices to sound-engine
        - **notator**: *note_to_file*
        - **returns "caesura" or "normal"**
    - IF "caesura":
        - *sleep*: 6 basic time-units
        - new *shuffle_delay*
        - new speed
        - **metronome**: reset
        - **composer**
            - *gateway.stop_all_notes*
            - *set_scale* (choice(composer.SCALES_BY_FREQUENCY))
            - *new_random_meter*
            - IF automate pan:
                - each voice new pan
            - IF automate binaural diffs:
                - each voice new binaural diff
            - IF automate note duration prop:
                - each voice new note_duration_prop
            - IF automate transpose:
                - new transpose
            - IF automate wavetables
                - each voice new wavetable
    - *check_incoming_messages*
