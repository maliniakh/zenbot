from typing import Union
import numpy as np

def binarize(arr: Union[np.ndarray, list]):
    return [tobin(x) for x in arr]

def debinarize(arr: Union[np.ndarray, list]):
    return [frombin(x) for x in arr]

def tobin(label):
    if label == 'down':
        return [1, 0, 0]
    if label == 'flat':
        return [0, 1, 0]
    if label == 'up':
        return [0, 0, 1]
    raise Exception

def frombin(bin):
    if bin == [1, 0, 0]:
        return 'down'
    if bin == [0, 1, 0]:
        return 'flat'
    if bin == [0, 0, 1]:
        return 'up'
    raise Exception


test_arr = np.asarray(['down',
 'flat',
 'up',
 'flat'])

binarized = binarize(test_arr)
print(binarized)

debinarized = debinarize(binarized)
print(debinarized)

print(type([1]))

