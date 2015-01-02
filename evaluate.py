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

import cPickle as pickle
from datetime import timedelta
from babel.dates import format_timedelta

bloom = __import__("python-simple-bloom")

from store_passwords import DIVISIONS, count_passwords

# Cache counting the passwords-file
_password_count = None
def get_password_count():
    global _password_count

    if not _password_count:
        _password_count = count_passwords()
    return _password_count

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

def password_strength_in_hashes(password):
    """
        Estimate the number of hashes required to crack a given password.

        Returns (estimate, quantifier) where quantifier is a string describing the estimate.
    """
    division = password_strength_division(password)

    if division < 0:
        hashes_required = get_password_count()
        quantifier = "more than"
    else:
        hashes_required = get_password_count() * (division + 1) / DIVISIONS
        quantifier = "less than"

    return hashes_required, quantifier

def describe_password_strength(
        password,
        nominal_hash_rate = 5 * 10**3): # Approx for bcrypt on a decent desktop PC
    hashes_required, quantifier = password_strength_in_hashes(password)

    result = "{:.0%}".format(hashes_required / get_password_count())

    crack_time = timedelta(seconds = hashes_required / nominal_hash_rate)

    result += " - cracking would take {} {}".format(
        quantifier,
        format_timedelta(crack_time, locale='en_US')
    )

    return result

if __name__ == "__main__":
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

    heading = "Password: Strength - Cracking time"
    heading += '\n' + '-' * len(heading)
    print(heading)
    print(
        '\n'.join(
            "{password}: {description}".format(
                password=password,
                description=describe_password_strength(password)
            )
            for password in test_passwords
        )
    )