import scsynth
import random
import time
import threading

RESERVED_IDS = map(lambda x: x + 2222, range(77))
DEFAULT_SCSYNTHDEF = "adsr"
DEFAULT_SCSYNTHDEF_PATH = "scsynthdefs/adsr.scsynthdef"


class SC_Gateway(object):
    def __init__(self, host="localhost",
                       port=57110,
                       sdef=DEFAULT_SCSYNTHDEF,
                       sdef_path=DEFAULT_SCSYNTHDEF_PATH
                ):

        self.host = host
        self.port = port

        self.server = self.default_server(self, host, port, verbose=False)
        self.sdef = sdef
        self.sdef_path = sdef_path
        self.id_pool = RESERVED_IDS
        self.node_ids = []
        self.playing = False

    def default_syn(self, name="adsr", freq=440):
        """constructs a synth for the adsr synthdef"""
        syn = scsynth.Synth()
        syn.name = name
        syn["amp"] = 0.1
        syn["freq"] = freq
        syn["a"] = 0.3
        syn["d"] = 0.3
        syn["s"] = 0.2
        syn["r"] = 0.2
        syn["gate"] = 1
        syn["pan"] = 0.5

        syn.node = "".join([str(n) for n in
                            [random.randint(0, 20) for n in xrange(20)]
                           ])
        #syn.node = 0
        return syn

    def load_scsyndef(self):
        """tells the scsynth-server to load the instance's scsynthdef"""
        print "loading: {0}".format(self.sdef_path)
        self.server.sendMsg('/d_load', self.sdef_path)

    def toggle_dump(self, bo_ol):
        """switch OSC message dumping on/off"""
        bo_ol = 1 if bo_ol else 0
        print bo_ol
        self.server.sendMsg('/dumpOSC', bo_ol)
        return True

    def reset_nodes(self, force=False):
        """frees(deletes) created nodes on the server"""
        pool = self.node_ids if not force else self.id_pool
        for nid in self.node_ids:
            self.send_value(nid, "/n_free", "")
            self.node_ids.remove(nid)

    def create_nodes(self, num):
        """creates a specified number of nodes with synths on the server"""
        self.reset_nodes()
        for n in xrange(num):
            syn = self.default_syn()
            nid = self.id_pool[n]
            start_message = self.assemble_start_message(syn, id=nid)
            self.server.sendMsg(*start_message)
            self.node_ids += [nid]

    def stop_note(self, nid):
        """send a "close gate"-message to a node/synth"""
        self.send_value(nid, "gate", 0)

    def stop_notes(self):
        """send a "close gate"-message to all registered nodes/synths"""
        for nid in self.node_ids:
            self.stop_note(nid)

    def send_value(self, id, *items):
        """helper method: send value(s) to the scsynth server"""
        return self.server.sendMsg("/n_set", id, *items)

    def play_note(self, id, freq):
        """play a single note on the synth"""
        self.send_value(id, "gate", 0)
        time.sleep(0.005)
        self.send_value(id, "freq", freq, "gate", 1)
        return True

    def play_rand_melody(self, ids=None, number=666, msec=300):
        """superfluous method: plays a random melody

        for specified nodes
        of a specified length
        with the specified speed"""
        ids = ids or self.node_ids
        for i in xrange(number):
            for id in ids:
                freq = random.randrange(200, 600)
                self.play_note(id, freq)
            time.sleep(msec / 1000.0)
        self.stop_notes()

    @staticmethod
    def default_server(self, host="192.168.0.104", port=57110, verbose=True):
        """initializes and returns a scosc-server instance"""
        return scsynth.connect(host, port, verbose)

    @staticmethod
    def expand_synth(syn):
        res = []
        for e in syn.items():
            res.append(e[0])
            res.append(e[1])
        return res

    def assemble_start_message(self, syn, sdef=None, id=None):
        sdef = sdef or self.sdef
        id = id or self.node_ids[0]
        l = self.expand_synth(syn)
        # set last item of the list to 4 in prder to replace the complete node
        prepend = ["/s_new", sdef, id, 0, 1]
        return prepend + l

if __name__ == "__main__":
    sc = SC_Gateway("192.168.0.104")
    sc.reset_nodes(force=True)
    sc.load_scsyndef()
    sc.create_nodes(3)
    sc.play_rand_melody(number=12)
    import sys
    sys.exit()
