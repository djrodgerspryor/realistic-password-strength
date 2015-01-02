#!/usr/bin/python
"""
    Build bloom filters of passwords and dump them to disk.
"""
from __future__ import division, print_function

__author__ = 'Daniel Rodgers-Pryor'
__copyright__ = "Copyright (c) 2015, Daniel Rodgers-Pryor\nAll rights reserved."
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = __author__
__email__ = "djrodgerspryor@gmail.com"

import cPickle as pickle
from math import floor

bloom = __import__("python-simple-bloom")


FILENAME = "passwords/passwords.txt"
DIVISIONS = 10000
FALSE_POSITIVE_RATE = 0.001

def count_passwords():
    with open(FILENAME) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

if __name__ == '__main__':
    password_count = count_passwords()

    print("{:.2g} passwords".format(password_count))

    filters = [
        bloom.BloomFilter(
            max_entries = int(password_count / DIVISIONS),
            false_positive_rate=FALSE_POSITIVE_RATE
        )
        for i in range(DIVISIONS)
    ]

    print(
        "Filter size: {:.2}GB\n".format(
            sum(f.m for f in filters)
            / (8 * 10 ** 9)
        )
    )

    with open(FILENAME) as f:
        for i, line in enumerate(f):
            # TODO: this is broken - it assumes that passwords can't start with whitespace
            password = line.strip()
            division = int(floor(i * DIVISIONS / password_count))

            filters[division].append(password)

            if i % 10**5 == 0:
                print('{}M of {:.1f}M'.format(i / 10**6, password_count / 10**6))

    with open("filters.pckl", "wb") as f:
        pickle.dump(filters, f, protocol=-1)

    print("done!")
