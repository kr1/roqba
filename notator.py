import collections

class Notator(object):
    def __init__(self, num_voices, 
                       scroll_filename = "scrolling.txt",
                       buffer_length = 75,
                       num_lines = 40):
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
                except KeyError: mat[l] = []
                mat[l].append(-1)
            for v in xrange(self.num_voices):
                mat[int(self.buffer[n][v]/2)][n] = self.buffer[n][v] % 2
        return mat

    def draw(self, mat):
        text = ""
        line_buffer = []
        for l in xrange(self.num_lines):
            t = map(lambda x: {-1:" ", 0:"_", 1:"-"}[x], mat[l])
            line = "".join(t)
            line_buffer.append(line)
        return "\n".join(line_buffer)
              
    def write_to_file(self, s):
        fi = open(self.scroll_filename, "w")
        fi.write(s)
        fi.close()

    def get_unix_scroll_command(self):
        return "tail -f {0}".format(self.scroll_filename)

def main():
    import random
    nt = Notator(3, num_lines = 41)
    for n in xrange(80):
        nt.add_note([random.randint(0, 80), random.randint(0, 80), random.randint(0, 80)])
    mat = nt.make_matrix()
    s = nt.draw(mat)
    nt.write_to_file(s)
    #print mat

    

if __name__ == "__main__":
    main()
