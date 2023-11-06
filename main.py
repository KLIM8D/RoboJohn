#!/usr/bin/env python3
import random
import sys
import time
import json


class KVItem:
    def __init__(self, count, value):
        self.count = count
        self.value = value

    def __str__(self):
        return "count: %s - value: %s" % (self.count, self.value)


class Word:
    def __init__(self, term, plural, sentences):
        self.term = term
        self.plural = plural
        self.sentences = sentences


class Dictionary:
    words = {}

    def __init__(self, filepath):
        i = 0
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

                for key, value in dict.items(data):
                    term = value["x"]
                    plural = value["y"]
                    sentences = value["z"]

                    self.words[key] = (Word(term, plural, sentences))
        except Exception as e:
            print(e)
            print("line:", i)
            sys.exit()


class RoboJohn:
    chain = {}

    def read_dictionary(self, dicionary):
        for k, v in dicionary.items():
            for sentence in v.sentences:
                item = []
                for word in sentence.split():
                    if len(item) < 3:
                        item.append(word)
                    else:
                        key = (item[0], item[1])
                        self.add_word(key, item[2])
                        del item[0]

    def read_file(self, filepath):
        i = 0
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    i += 1
                    item = []
                    for word in line.split():
                        if len(item) < 3:
                            item.append(word)
                        else:
                            key = (item[0], item[1])
                            self.add_word(key, item[2])
                            del item[0]
        except Exception as e:
            print(e)
            print("line:", i)
            sys.exit()

    def add_word(self, key, value):
        if key not in self.chain:
            self.chain[key] = {KVItem(1, value)}
        else:
            followers = [x for x in self.chain[key] if x.value == value]
            if followers:
                for i, v in enumerate(followers):
                    v.count += 1
            else:
                self.chain[key] = self.chain[key] | {KVItem(1, value)}

    def list(self):
        for k, v in self.chain.items():
            print("{key} {value} #{count}".format(key=k,
                  value=[x.value for x in v], count=[c.count for c in v]))

    def sentence(self, word, length):
        s = []
        o = [x for x in self.chain if x[0] == word]

        if not o:
            key = random.choice(list(self.chain.keys()))
            o = [x for x in self.chain if x[0] == key[0]]

        if o:
            rnd = random.randint(0, len(o)-1)
            key = o[rnd]
            v = sorted(self.chain[key], key=lambda x: x.count, reverse=True)
            s.append(key[0])
            s.append(key[1])
            s.append(v[0].value)

            o = (key[1], v[0].value)
            while len(s) < length:
                if o in self.chain:
                    #obj = sorted(self.chain[o],
                    #             key=lambda x: x.count, reverse=True)
                    w = []
                    for x in self.chain[o]:
                        for i in range(x.count):
                            w.append(x)

                    random.shuffle(w)

                    i = random.randint(0, len(w)-1)
                    obj = w[i]
                    s.append(obj.value)
                    o = (o[1], obj.value)
                else:
                    s.append(".")
                    keys = [x for x in self.chain.keys()]
                    i = random.randint(0, len(keys)-1)
                    l = self.chain[keys[i]]
                    obj = sorted(l, key=lambda x: x.count, reverse=True)
                    s.append(keys[i][0])
                    s.append(keys[i][1])
                    s.append(obj[0].value)

                    o = (o[1], obj[0].value)

            return (" ".join(s))


def main():
    #d = Dictionary("dict.json")
    o = RoboJohn()
    #o.read_dictionary(d.words)
    o.read_file("data.txt")

    o.list()
    for i in range(100):
        sentence = o.sentence("I", 2)
        time.sleep(5)


if __name__ == "__main__":
    main()
