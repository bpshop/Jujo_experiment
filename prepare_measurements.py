# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 09:50:02 2022

@author: Daniel
"""

import numpy as np

def get_meas():
    chasseral_2_sphinx = np.array([[99.0930, 99.0943, 99.0932, 99.0919, 99.0907, 99.0917, 99.0917, 99.0927],
    [300.9066, 300.9099, 300.9073, 300.9083, 300.9083, 300.9064, 300.9064, 300.9061]])
    
    sphinx_2_chasseral = np.array([[101.7104, 101.7109], [298.2897, 298.2902]])
    
    chasseral_2_sphinx_final = np.zeros((chasseral_2_sphinx.shape[1], 1))
    for i in range(chasseral_2_sphinx.shape[1]):
        chasseral_2_sphinx_final[i, 0] = 0.5*(chasseral_2_sphinx[0, i] + 400 - chasseral_2_sphinx[1, i])
    
    sphinx_2_chasseral_final = np.zeros((sphinx_2_chasseral.shape[1], 1))
    for i in range(sphinx_2_chasseral.shape[1]):
        sphinx_2_chasseral_final[i, 0] = 0.5*(sphinx_2_chasseral[0, i] + 400 - sphinx_2_chasseral[1, i])
        
    mean_s2c = np.mean(sphinx_2_chasseral_final)
    mean_c2s = np.mean(chasseral_2_sphinx_final)
    
    return mean_s2c, mean_c2s
