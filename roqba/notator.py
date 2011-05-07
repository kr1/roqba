# encoding: utf-8

import collections
import metronome


class Notator(object):
    def __init__(self, num_voices,
                       scroll_filename="scrolling.txt",
                       buffer_length=75,
                       num_lines=40):
        self.num_voices = num_voices
        self.buffer = collections.deque()
        self.buffer_length = buffer_length
        self.scroll_filename = scroll_filename
        self.num_lines = num_lines

    def add_note(self, note):
        self.buffer.append(note)
        if len(self.buffer) > self.buffer_length:
            self.buffer.popleft()
        return self.buffer

    def make_matrix(self):
        mat = {}
        for n in xrange(len(self.buffer)):
            for l in xrange(self.num_lines):
                try:
                    mat[l]
                except KeyError:
                    mat[l] = []
                mat[l].append(-1)
            for v in xrange(self.num_voices):
                if self.buffer[n][v] > 0:
                    mat[int(self.buffer[n][v] / 2)][n] = self.buffer[n][v] % 2
        return mat

    def draw(self, mat, weight, cycle_pos):
        text = ""
        line_buffer = []
        for l in xrange(self.num_lines-1, 0, -1):
            t = map(lambda x: {-1: " ", 0: "_", 1: "-"}[x], mat[l])
            if l == self.num_lines - 1 and len(t) > 6:
                t[0] = "w"
                t[1] = str(weight)
                t[4] = "p"
                t[5] = str(cycle_pos)
            line = "".join(t)
            line_buffer.append(line)
        return "\n".join(line_buffer)

    def write_to_file(self, s):
        fi = open(self.scroll_filename, "w")
        fi.write(s)
        fi.close()

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
        self.write_to_file(txt)

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


def main():
    import random
    nt = Notator(3, num_lines=41)
    for n in xrange(80):
        nt.add_note([random.randint(0, 80),
                     random.randint(0, 80),
                     random.randint(0, 80)])
    mat = nt.make_matrix()
    s = nt.draw(mat)
    nt.write_to_file(s)
    #print mat


if __name__ == "__main__":
    main()
