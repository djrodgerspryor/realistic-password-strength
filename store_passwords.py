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
from math import floor, ceil
from collections import OrderedDict

bloom = __import__("python-simple-bloom")


FILENAME = "passwords/passwords.txt"
FALSE_POSITIVE_RATE = 0.001
MIN_DIVISION = 1000

# Logarithmically-spaced divisions will grow by this factor.
#   smaller factor => more divisions, larger factor => fewer divisions.
DIVISION_FACTOR = 2.0

def count_passwords():
    with open(FILENAME) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

if __name__ == '__main__':
    password_count = count_passwords()

    print("{:.2g} passwords".format(password_count))

    # Ordered dict of bloom filters, keyed-by un-normalised quantile; the total number of preceding hashes (inclusive)
    filters = OrderedDict()

    # Create filters with exponentially increasing size
    division_size = int(MIN_DIVISION)
    total_hashes = 0
    while total_hashes < password_count:
        filter = bloom.BloomFilter(max_entries=division_size, false_positive_rate=FALSE_POSITIVE_RATE)

        # Use the full capacity of the space allocated to the filter
        total_hashes += filter.capacity()

        # Ensure that the largest quantile is always the password count
        if total_hashes > password_count:
            total_hashes = password_count

        filters[total_hashes] = filter

        division_size *= DIVISION_FACTOR

        # Prevent wasted space in the last filter
        division_size = min(division_size, password_count - total_hashes)

    print(
        "Filter size: {:.2}GB\n".format(
            sum(f.m for f in filters.values())
            / (8 * 10**9)
        )
    )

    with open(FILENAME) as f:
        for i, line in enumerate(f):
            # Strip trailing newline but assume that all other whitespace is part of the password
            password = line[:-1]

            # Smallest quantile larger than i
            key = (quantile for quantile in filters if quantile > i).next()

            filters[key].append(password)

            if i % 10**5 == 0:
                print('{}M of {:.1f}M'.format(i / 10**6, password_count / 10**6))

    with open("filters.pckl", "wb") as f:
        pickle.dump(filters, f, protocol=-1)

    print("done!")
