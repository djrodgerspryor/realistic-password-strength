#!/usr/bin/python
"""
    Load bloom filters and test a password for presence in each to generate a difficulty score.
"""
from __future__ import division, print_function

__author__ = 'Daniel Rodgers-Pryor'
__copyright__ = "Copyright (c) 2015, Daniel Rodgers-Pryor\nAll rights reserved."
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = __author__
__email__ = "djrodgerspryor@gmail.com"

import sys
import numpy as np
import cPickle as pickle
from math import floor
from datetime import timedelta
from babel.dates import format_timedelta

bloom = __import__("python-simple-bloom")

from store_passwords import DIVISIONS, count_passwords

password_count = count_passwords()

# Cache loading filters
_filters = None
def get_filters():
    global _filters

    if not _filters:
        with open("filters.pckl", "rb") as f:
            _filters = pickle.load(f)
    return _filters

def password_strength_division(password):
    for i, f in enumerate(get_filters()):
        if password in f:
            return i
    return -1

if __name__ == "__main__":
    nominal_hash_rate = 5 * 10 ** 3  # Approx for bcrypt on a decent desktop PC

    test_passwords = [
        "test1",
        "thisismypassword",
        "password99",
        "gibberishnerguoiwheoifjhewoifjh",
        "diane99",
        "12hello345",
        "batteryhorsestaple",
        "133Tspe3k",
        "mypassword",
        "s3cret",
        "mypa55word"
    ]

    for password in test_passwords:
        division = password_strength_division(password)

        if division < 0:
            result = "Excellent!"
            hashes_required = password_count
            time_estimate_quantifier = "more than"
        else:
            result = "{}/{}".format(division + 1, DIVISIONS)
            hashes_required = password_count * (division + 1) / DIVISIONS
            time_estimate_quantifier = "less than"

        print("Password strength (%s): " % password, result)

        crack_time = timedelta(seconds = hashes_required / nominal_hash_rate)

        print("Cracking would take {} {}\n".format(time_estimate_quantifier, format_timedelta(crack_time, locale='en_US')))