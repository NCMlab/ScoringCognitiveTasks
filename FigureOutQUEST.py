#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 11:23:14 2022

@author: jasonsteffener
"""

import pytest
import scipy.stats
import numpy as np
from questplus.qp import QuestPlus, QuestPlusWeibull
from questplus import _constants
import matplotlib.pyplot as plt
import numpy as np

threshold = np.arange(-40, 0, 0.2)
slope, guess, lapse = 5.5, 0.5, 0.02
contrasts = threshold.copy()

expected_contrasts = [-18, -22, -25, -28, -30, -22, -13, -15, -16, -18,
                      -19, -20, -21, -22, -23, -19, -20, -20, -18, -18,
                      -19, -17, -17, -18, -18, -18, -19, -19, -19, -19,
                      -19, -19]

responses = ['Correct', 'Correct', 'Correct', 'Correct', 'Incorrect',
             'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct',
             'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect',
             'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct',
             'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct',
             'Correct', 'Correct', 'Correct', 'Correct', 'Correct',
             'Correct', 'Correct']

expected_mode_threshold = -20




stim_domain = dict(intensity=contrasts)
param_domain = dict(threshold=threshold, slope=slope,
                    lower_asymptote=guess, lapse_rate=lapse)
outcome_domain = dict(response=['Correct', 'Incorrect'])

f = 'weibull'
scale = 'dB'
stim_selection_method = 'min_entropy'
param_estimation_method = 'mode'


q = QuestPlus(stim_domain=stim_domain, param_domain=param_domain,
              outcome_domain=outcome_domain, func=f, stim_scale=scale,
              stim_selection_method=stim_selection_method,
              param_estimation_method=param_estimation_method)

# for expected_contrast, response in zip(expected_contrasts, responses):
#     assert q.next_stim == dict(intensity=expected_contrast)
#     q.update(stim=q.next_stim,
#              outcome=dict(response=response))
    
    
    
PrevStim = []
Threshs = []
for i in range(0,100):
    print("Threshold: %0.3f"%(q.param_estimate['threshold']))
    #print(q.next_stim)
    Threshs.append(q.param_estimate['threshold'])
    PrevStim.append(q.next_stim['intensity'])
    resp = input('Enter response: ')
    if resp == '1':
        response = 'Correct'
    elif resp == '2':
        response = 'Incorrect'
    else:
        break
    q.update(stim = q.next_stim, outcome=dict(response = response))
    #plt.hist(q.marginal_posterior['threshold'])
   # plt.hist(q.marginal_posterior['threshold'],40)
    #plt.plot(q.marginal_posterior['threshold'])
    plt.plot(Threshs,label = 'Thresholds')
    plt.plot(PrevStim,label = 'Stimuli')
    plt.legend()
    plt.show()
    #print("ConfInt: %0.3f"%(np.quantile(q.marginal_posterior['threshold'],0.95) - np.quantile(q.marginal_posterior['threshold'],0.05)))
    s = q.marginal_posterior['threshold']
    
    # Find the FWHM of the max os the posterior
    smax = s.max()
    #print(smax)
    imax = np.argmin(s < smax)
    shalfmax = smax/2

    iLow = np.argmax(s > shalfmax)
    #print(iLow)
    iHigh = np.argmin(s[imax:] > shalfmax) + imax
    #print(iHigh)    
    print(threshold[iHigh] - threshold[iLow])
    