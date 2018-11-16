from typing import Union
import numpy as np

def binarize(arr: Union[np.ndarray, list]):
    return np.asarray([tobin(x) for x in arr])

def debinarize(arr: Union[np.ndarray, list]):
    return p.asarray([frombin(x) for x in arr])

def tobin(label):
    if label == 'down':
        return np.asarray([1, 0, 0])
    if label == 'flat':
        return np.asarray([0, 1, 0])
    if label == 'up':
        return np.asarray([0, 0, 1])
    raise Exception

def frombin(bin):
    return '{{"down": {}, "flat": {}, "up": {}}}'.format(bin[0], bin[1], bin[2])

test_arr = np.asarray(['down',
 'flat',
 'up',
 'flat'])

binarized = binarize(test_arr)
# print(binarized)

# debinarized = debinarize(binarized)
# print(debinarized)

# print(type([1]))

