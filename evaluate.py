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

bloom = __import__("python-simple-bloom")

# Cache counting the passwords-file
_password_count = None
def get_password_count():
    global _password_count

    if not _password_count:
        _password_count = max(get_filters().keys())
    return _password_count

# Cache loading filters
_filters = None
def get_filters():
    global _filters

    if not _filters:
        with open("filters.pckl", "rb") as f:
            _filters = pickle.load(f)
    return _filters

def _password_strength(password):
    """
        Return an upper-bound on the number of hashes required to crack the password or a negative lower-bound (if the
        password can't be found).
    """
    for quantile, filter in get_filters().items():
        if password in filter:
            return quantile

    return -get_password_count() # Lower bound

def password_strength_bound(password):
    """
        Estimate the number of hashes required to crack a given password.

        Returns (estimate, quantifier) where quantifier is a string describing the estimate.
    """
    hashes_required = _password_strength(password)
    quantifier = "more than" if hashes_required < 0 else "less than"
    hashes_required = abs(hashes_required)

    return hashes_required, quantifier

def describe_password_strength(
        password,
        nominal_hash_rate = 5 * 10**3): # Approx for bcrypt on a decent desktop PC
    from babel.dates import format_timedelta

    hashes_required, quantifier = password_strength_bound(password)

    result = "{:.0%}".format(hashes_required / get_password_count())

    # Minimum time of 1 second because babel can't format shorter times
    crack_time = timedelta(seconds=max(hashes_required / nominal_hash_rate, 1))

    result += " - cracking would take {} {}".format(
        quantifier,
        format_timedelta(crack_time, locale='en_US', granularity='millisecond')
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