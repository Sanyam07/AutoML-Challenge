# -*- encoding: utf-8 -*-
# REGRESSION METRICS (work on raw solution and prediction)
# These can be computed on all solutions and predictions
# (classification included)
from __future__ import print_function

import numpy as np

from constants import REGRESSION, METRIC_TO_STRING


def calculate_score(metric, solution, prediction):
    metric = METRIC_TO_STRING[metric]
    return globals()[metric](solution, prediction)


def r2_metric(solution, prediction, task=REGRESSION):
    """
    1 - Mean squared error divided by variance
    :param solution:
    :param prediction:
    :param task:
    :return:
    """
    mse = np.mean((solution - prediction) ** 2, axis=0)
    var = np.mean((solution - np.mean(solution)) ** 2, axis=0)
    score = 1 - mse / var
    return np.mean(score)


def a_metric(solution, prediction, task=REGRESSION):
    """
    1 - Mean absolute error divided by mean absolute deviation
    :param solution:
    :param prediction:
    :param task:
    :return:
    """
    mae = np.mean(np.abs(solution - prediction))  # mean absolute error
    mad = np.mean(
        np.abs(solution - np.mean(solution)))  # mean absolute deviation
    score = 1 - mae / mad
    return np.mean(score)
