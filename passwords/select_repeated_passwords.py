#!/usr/bin/python
"""
    Filter the password list for passwords that were used at least twice.
"""
from __future__ import division, print_function

__author__ = 'Daniel Rodgers-Pryor'
__copyright__ = "Copyright (c) 2015, Daniel Rodgers-Pryor\nAll rights reserved."
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = __author__
__email__ = "djrodgerspryor@gmail.com"

import numpy as np


counts = []

with open('rockyou-withcount.txt') as f:
    with open('rockyou-repeated.txt', 'w') as fout:
        for line in f:
            split_line = line.split()
            count = int(split_line.pop(0))
            password = ' '.join(split_line)
            
            counts.append(count)
            
            if count > 1:
                print(password, file=fout)

            if len(counts) % 10**5 == 0:
                print(len(counts) / 10**6, 'M')
    
counts = np.array(counts)

print('Repeated count:', np.sum(counts > 1), '{:%}'.format(np.sum(counts > 1) / len(counts)))
