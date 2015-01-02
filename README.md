Realistic Password-Strength Tester
==================================

Test password strength (cracking-time) using real guess-dictionaries and mangling rules.

A large dictionary of password-guesses is stored in a bloom filter -- at constant space per-item of ~10 bits -- password-vulnerability can then be quickly checked with a membership test.

For granular results, bloom filters are segmented and ordered; the first filter containing the best-guesses* and the last one containing the worst guesses. Strength is estimated by the number of hashes (in previous bloom filter segments) that an attack will have to compute if they try the given guesses in order.

\* The passwords file (specified by FILENAME in store_passwords.py) is assumed to be ordered from best to worst.

Dependencies
------------
* babel (for human-readable cracking-time description only)
* python-simple-bloom (included as a submodule)
    * scikit-learn
    * bitarray

Install them with:

    pip install babel bitarray scikit-learn

Author
-------------
Daniel Rodgers-Pryor (2015)