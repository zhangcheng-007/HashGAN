import matplotlib
import numpy as np
import collections
import pickle as pickle
import os

matplotlib.use('Agg')
import matplotlib.pyplot as plt


_since_beginning = collections.defaultdict(lambda: {})
_since_last_flush = collections.defaultdict(lambda: {})

_iter = [0]


def tick():
    _iter[0] += 1


def plot(name, value):
    _since_last_flush[name][_iter[0]] = value


def flush(path=""):
    prints = []

    for name, vals in list(_since_last_flush.items()):
        prints.append("{}\t{:.4f}".format(name, np.mean(list(vals.values()))))
        _since_beginning[name].update(vals)

        x_vals = np.sort(list(_since_beginning[name].keys()))
        y_vals = [_since_beginning[name][x] for x in x_vals]

        plt.clf()
        plt.plot(x_vals, y_vals)
        plt.xlabel('iteration')
        plt.ylabel(name)
        plt.savefig(os.path.join(path, name.replace(' ', '_') + '.jpg'))

    print("iter {}\t{}".format(_iter[0], "\t".join(prints)))
    _since_last_flush.clear()

    with open('log.pkl', 'wb') as f:
        pickle.dump(dict(_since_beginning), f, pickle.HIGHEST_PROTOCOL)