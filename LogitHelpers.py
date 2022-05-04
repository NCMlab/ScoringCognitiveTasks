#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 14:11:09 2022

@author: jasonsteffener
"""
import numpy as np

def FindCap_CI(Thr, b0, b1, Cov):
    # Find the cognitive capacity
    CC = (np.log(Thr/(1-Thr)) - b0)/b1
    # Find the standard error around the predicted point
    L_T = np.array([1, CC])
    L_T = np.matrix(L_T)
    L = np.transpose(L_T)
    C = np.matrix(Cov)

    var_f = np.matmul(np.matmul(L_T, C), L)


    var_f = np.asarray(var_f)[0][0]
    pointwise_se = np.sqrt(var_f) 

    # Calculate the confidence intervals
    upper_limit = invlogit(logit(Thr)+1.96*pointwise_se)
    lower_limit = invlogit(logit(Thr)-1.96*pointwise_se)
    # Convert these into loadunits of X
    CIup = (np.log(upper_limit/(1-upper_limit)) - b0)/b1
    CIlow = (np.log(lower_limit/(1-lower_limit)) - b0)/b1
    return CC, CIup, CIlow


def logit(p):
    return np.log(p/(1-p))

def invlogit(x):
    # inverse function of logit
    return 1/(1+np.exp(-x))