# encoding: utf-8

import collections
from . import metronome


class Notator(object):
    def __init__(self,
                 num_voices,
                 scroll_filename="scrolling.txt",
                 meter_filename="meter_monitor.txt",
                 sequence_filename="sequence_monitor.txt",
                 buffer_length=75,
                 num_lines=40):
        self.num_voices = num_voices
        self.buffer = collections.deque()
        self.buffer_length = buffer_length
        self.scroll_filename = scroll_filename
        self.meter_filename = meter_filename
        self.sequence_filename = sequence_filename
        self.num_lines = num_lines

    def add_note(self, note):
        self.buffer.append(note)
        if len(self.buffer) > self.buffer_length:
            self.buffer.popleft()
        return self.buffer

    def make_matrix(self):
        mat = {}
        for n in range(len(self.buffer)):
            for l in range(self.num_lines):
                try:
                    mat[l]
                except KeyError:
                    mat[l] = []
                mat[l].append(-1)
            for v in range(self.num_voices):
                if self.buffer[n][v] > 0:
                    try:
                        mat[int(self.buffer[n][v] / 2)][n] = self.buffer[n][v] % 2
                    except KeyError:
                        pass
        return mat

    def draw(self, mat, weight, cycle_pos):
        line_buffer = []
        for l in range(self.num_lines - 1, 0, -1):
            t = [{-1: " ", 0: "_", 1: "-"}[x] for x in mat[l]]
            if l == self.num_lines - 1 and len(t) > 6:
                t[0] = "w"
                t[1] = str(weight)
                t[4] = "p"
                t[5] = str(cycle_pos)
            line = "".join(t)
            line_buffer.append(line)
        return "\n".join(line_buffer)

    def write_to_file(self, filename, s):
        with open(filename, "w") as fi:
            fi.write(s)

    def note_to_file(self, data):
        """this method does the full service:

        0. adds a note to the buffer
        1. creates matrix
        2. draws the text
        3. writes the text to file
        NB: see the scrolling notation with:
        {0}""".format(self.get_unix_scroll_command())
        note = data["notes"]
        weight = data["weight"]
        cycle_pos = data["cycle_pos"]
        self.add_note(note)
        mat = self.make_matrix()
        txt = self.draw(mat, weight, cycle_pos)
        txt = self.post_process(txt, weight)
        self.write_to_file(self.scroll_filename, txt)

    def post_process(self, txt, weight):
        if weight == metronome.HEAVY:
            split = txt.split("\n")
            split[1] = split[1].replace(" ", ".")
            split[-2] = split[-2].replace(" ", ".")
            return "\n".join(split)
        return txt

    def get_unix_scroll_command(self):
        return "tail -f {0}".format(self.scroll_filename)

    def reset(self):
        self.buffer = collections.deque()

    def notate_rhythm(self, meter, position):
        meter_length = meter[0]
        meter = meter[1]
        chars_per_beat = self.buffer_length // meter_length
        grid = ["|"]
        for segment in meter:
            grid.append("{}|".format(" " * (int(chars_per_beat * segment) - 1)))
        current = "{}{}{}".format(" " * int(chars_per_beat * position),
                                  "X" * int(chars_per_beat),
                                  " " * int(chars_per_beat * (meter_length - position)))
        joined_grid = "".join(grid)
        text = "{}\n{}\n{}\n{}\n{}\n{}".format(
            joined_grid, joined_grid,
            current,
            joined_grid, joined_grid, "\n" * 20)
        self.write_to_file(self.meter_filename, text)

    def notate_bar_sequence(self, sequence, position, scale):
        sequence_length = len(sequence)
        chars_per_bar = self.buffer_length / sequence_length
        caption = ["{}{}".format(id_, " " * (chars_per_bar - 1)) for id_ in sequence]
        current = "{}{}{}".format(" " * chars_per_bar * position,
                                  "X" * chars_per_bar,
                                  " " * chars_per_bar * (sequence_length - position))
        caption = "".join(caption)
        text = "{}\n{}\n{}\n{}\n".format(caption, current, caption, scale)
        self.write_to_file(self.sequence_filename, text)
