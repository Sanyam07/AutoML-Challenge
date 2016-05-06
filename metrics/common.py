# -*- encoding: utf-8 -*-
from __future__ import print_function

import numpy as np

from constants import *


def binarize_predictions(array, task=BINARY_CLASSIFICATION):
    """
    Turn predictions into decisions {0,1} by selecting the class with largest
    score for multi class problems and thresh holding at 0.5 for other cases.

    :param array:
    :param task:
    :return:
    """
    # add a very small random value as tie breaker (a bit bad because
    # this changes the score every time)
    # so to make sure we get the same result every time, we seed it
    # eps = 1e-15
    # np.random.seed(sum(array.shape))
    # array = array + eps*np.random.rand(array.shape[0],array.shape[1])
    bin_array = np.zeros(array.shape)
    if (task != MULTICLASS_CLASSIFICATION) or (array.shape[1] == 1):
        bin_array[array >= 0.5] = 1
    else:
        sample_num = array.shape[0]
        for i in range(sample_num):
            j = np.argmax(array[i, :])
            bin_array[i, j] = 1
    return bin_array


def acc_stat(solution, prediction):
    """
    Return accuracy statistics TN, FP, TP, FN Assumes that solution and
    prediction are binary 0/1 vectors.
    :param solution:
    :param prediction:
    :return:
    """
    # This uses floats so the results are floats
    tn_value = sum(np.multiply((1 - solution), (1 - prediction)))
    fn_value = sum(np.multiply(solution, (1 - prediction)))
    tp_value = sum(np.multiply(solution, prediction))
    fp_value = sum(np.multiply((1 - solution), prediction))
    return tn_value, fp_value, tp_value, fn_value


def tied_rank(a):
    """Return the ranks (with base 1) of a list resolving ties by averaging.

    This works for numpy arrays.

    """
    m = len(a)
    # Sort a in ascending order (sa=sorted vals, i=indices)
    i = a.argsort()
    sa = a[i]
    # Find unique values
    uval = np.unique(a)
    # Test whether there are ties
    R = np.arange(m, dtype=float) + 1  # Ranks with base 1
    if len(uval) != m:
        # Average the ranks for the ties
        oldval = sa[0]
        newval = sa[0]
        k0 = 0
        for k in range(1, m):
            newval = sa[k]
            if newval == oldval:
                # moving average
                R[k0:k + 1] = R[k - 1] * (k - k0) / (k - k0 +
                                                     1) + R[k] / (k - k0 + 1)
            else:
                k0 = k
                oldval = newval
    # Invert the index
    S = np.empty(m)
    S[i] = R
    return S

