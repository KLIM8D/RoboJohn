#!/usr/bin/env python3
from random import randint


class KVItem:
    count = 0
    value = None

    def __init__(self, count, value):
        self.count = count
        self.value = value


class RoboJohn:
    words = {}

    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                item = []
                for word in line.split():
                    if len(item) < 3:
                        item.append(word)
                    else:
                        key = (item[0], item[1])
                        self.add_word(key, item[2])
                        del item[0]

    def add_word(self, key, value):
        if key not in self.words:
            self.words[key] = {KVItem(1, value)}
        else:
            followers = [x for x in self.words[key] if x.value == value]
            if len(followers) > 0:
                for i, v in enumerate(followers):
                    v.count += 1
            else:
                self.words[key] = self.words[key] | {KVItem(1, value)}

    def list(self):
        for k, v in self.words.items():
            print("{key} {value} #{count}".format(key=k,
                  value=[x.value for x in v], count=[c.count for c in v]))

    def sentence(self, word, length):
        s = []
        o = [x for x in self.words if x[0] == word]
        if len(o) > 0:
            rnd = randint(0, len(o)-1)
            key = o[rnd]
            v = sorted(self.words[key], key=lambda x: x.count, reverse=True)
            s.append(key[0])
            s.append(key[1])
            s.append(v[0].value)

            o = (key[1], v[0].value)
            while len(s) < length:
                if o in self.words:
                    obj = sorted(self.words[o],
                                 key=lambda x: x.count, reverse=True)
                    s.append(obj[0].value)
                else:
                    s.append(".")
                    keys = [x for x in self.words.keys()]
                    i = randint(0, len(keys)-1)
                    l = self.words[keys[i]]
                    obj = sorted(l, key=lambda x: x.count, reverse=True)
                    s.append(keys[i][0])
                    s.append(keys[i][1])
                    s.append(obj[0].value)

                o = (o[1], obj[0].value)

            print(" ".join(s))


o = RoboJohn("test.txt")
o.add_word(("John", "hader"), "sne")
o.add_word(("John", "hader"), "sne")
o.add_word(("John", "hader"), "sne")
o.add_word(("John", "hader"), "sne")
o.add_word(("John", "hader"), "is")
o.add_word(("John", "hader"), "regn")
o.add_word(("John", "hader"), "regn")
o.add_word(("hader", "sne"), "helt")
o.add_word(("sne", "helt"), "ekstremt")
o.add_word(("sne", "helt"), "vildt")
o.add_word(("sne", "helt"), "vildt")
o.add_word(("sne", "helt"), "meget")

o.list()
o.sentence("John", 20)
