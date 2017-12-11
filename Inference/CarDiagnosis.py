#!/Applications/anaconda2/bin/python
# coding=utf-8

"""
Blatt 08: Propositions and Inference
Thomas Hofmann, Yannic Boysen

####################################Versuch der Implementation des bottom-up Algorithmus zur
Lösung der car diagnosis Aufgabe.

Diagnose wird durch einen eigenen Algorithmus gelöst.
"""

from itertools import islice


class Diagnosis:

    components = ['battery', 'ignition', 'regulation', 'starter', 'engine', 'filter', 'pump', 'tank']

    noises = [0, 0, 0]

    # initialize
    def __init__(self, noise1, noise2, noise3):
        # self.diagnosis = 0  # Consider using an enum for this
        self.noises = [noise1, noise2, noise3]
        # dictionary of all components and corresponding boolean if it is working
        self.cs = dict(zip([x[0] for x in self.components], [0]*len(self.components)))
        # set aof assumables
        self.queue = {self.battery, self.ignition, self.regulation, self.starter,
                      self.engine, self.filter, self.pump, self.tank}

    # # Hornklauseln:
    # def setupHorn(self):
    #     hornClausues = [
    #         (lambda: 1 if self.noises[0] else 0),
    #
    #
    #     ]

    # Assumables
    def battery(self):
        if self.cs['i'] | self.cs['r']:
            self.cs['b'] = 1
            return 1
        else:
            return 0

    def ignition(self):
        if self.cs['s'] | self.cs['r']:
            self.cs['i'] = 1
            return 1
        else:
            return 0

    def regulation(self):
        if self.cs['p']:
            self.cs['r'] = 1
            return 1
        else:
            return 0

    def starter(self):
        if self.noises[0]:
            self.cs['s'] = 1
            return 1
        else:
            return 0

    def engine(self):
        if self.noises[2]:
            self.cs['e'] = 1
            return 1
        else:
            return 0

    def filter(self):
        if self.cs['e']:
            self.cs['f'] = 1
            return 1
        else:
            return 0

    def pump(self):
        if self.noises[1]:
            self.cs['p'] = 1
            return 1
        else:
            return 0

    def tank(self):
        if self.noises[1]:
            self.cs['t'] = 1
            return 1
        else:
            return 0

    # diagnosis system
    def diagnose(self):
        # basically: check all assumables as long as there have been changes made last time
        while 1:
            changes = 0
            q = set(self.queue)
            for assumable in self.queue:
                if assumable():
                    changes = 1
                    q.remove(assumable)
            self.queue = set(q)
            if not changes:
                break
        self.result()

    # print diagnosis result
    def result(self):
        comps = []
        for key in self.cs.keys():
            if not self.cs[key]:
                comps.append(key)
        print "One of", comps, "or a combination of those, is broken!"

    # bottom-up diagnosis algorithm (assumption-based truth maintenance system)
    # def proveConflict(self):
    #     # local
    #     c = []
    #     while 1:
    #         for f in self.queue:
    #             if f():
    #                 c.append(f)
    #             # else:
    #                 # break
    #     return self.cs
    #     for x in c:
    #         if x[0] == 0:
    #             return x
    #
    # def make(self):
    #     queue_iter = iter(self.queue)
    #     for func in queue_iter:
    #         skip = func()
    #         # return -1 if you want to break the queue
    #         if skip == -1:
    #             break
    #         if skip > 0:
    #             next(islice(queue_iter, skip, skip + 1))
    #     return self.diagnosis


# Making diagnoses for all different cases

print "\nTesting observation set 1:"
d0 = Diagnosis(0, 0, 0)
# print d0.make()
d0.diagnose()

print "\nTesting observation set 2:"
d1 = Diagnosis(1, 0, 0)
d1.diagnose()

print "\nTesting observation set 3:"
d2 = Diagnosis(0, 1, 0)
d2.diagnose()

print "\nTesting observation set 4:"
d3 = Diagnosis(1, 1, 0)
d3.diagnose()
