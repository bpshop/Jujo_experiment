# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 22:55:30 2022

@author: Daniel
"""

import call_rest
import sys
sys.path.insert(1, 'C:/Users/Daniel/Documents/6_Code/geolib')
import swiss_projection
import geodetic_tools
import numpy as np
import prepare_measurements


cc2deg = 1e-2*1e-2*360.0/400.0
rad2deg = 180.0/np.pi
cc2rad = cc2deg/rad2deg

coords_shpinx = [2641904.990, 1155278.120, 3578.310]
coords_chasseral = [2571223.123, 1220294.937, 1606.200]

dov_shpinx = cc2rad*np.array([-46.56, 50.64])  # cc; Eta, Xi
dov_chasseral = cc2rad*np.array([11.31, -31.93])  # cc; Eta, Xi
print('Lotabweichungen berücksichtigt')

# dov_shpinx = cc2rad*np.array([0, 0])  # cc; Eta, Xi
# dov_chasseral = cc2rad*np.array([0, 0])  # cc; Eta, Xi
# print('Lotabweichungen nicht berücksichtigt')

# East, North, h (Bessel)
coords_shpinx_bessel = call_rest.call_geod_rest(coords_shpinx, 'ln02tobessel')
coords_chasseral_bessel = call_rest.call_geod_rest(coords_chasseral,
                                                   'ln02tobessel')

# Geographic coordinates (on Bessel)
coords_shpinx_llh = swiss_projection.inverse_lv95_projection(coords_shpinx_bessel)
coords_chasseral_llh = swiss_projection.inverse_lv95_projection(coords_chasseral_bessel)

# XYZ Geocentric (CH1903+)
coords_shpinx_xyz = swiss_projection.llh2xyz(coords_shpinx_llh, "Bessel1841")
coords_chasseral_xyz = swiss_projection.llh2xyz(coords_chasseral_llh, "Bessel1841")

# astronomic coordinates
Lambda_sphinx = coords_shpinx_llh[0]+dov_shpinx[0]/np.cos(coords_shpinx_llh[1])
Theta_sphinx = coords_shpinx_llh[1]+dov_shpinx[1]

Lambda_chasseral = coords_chasseral_llh[0]+dov_chasseral[0]/np.cos(coords_chasseral_llh[1])
Theta_chasseral = coords_chasseral_llh[1]+dov_chasseral[1]

# Astronomical topocentric system at chasserl
LOS = np.array(coords_shpinx_xyz) - np.array(coords_chasseral_xyz)
d = np.linalg.norm(LOS)
LOS_topo_chasseral = np.matmul(swiss_projection.topocentric(Lambda_chasseral, Theta_chasseral), LOS)
# np.linalg.norm(LOS_topo_chasseral)
zenith_angle_1 = geodetic_tools.angle_between_vectors(LOS_topo_chasseral, [0, 0, 1])
zenith_angle_1 = zenith_angle_1*200.0/np.pi

# Astronomical topocentric system at sphinx
LOS = np.array(coords_chasseral_xyz) - np.array(coords_shpinx_xyz)
LOS_topo_sphinx = np.matmul(swiss_projection.topocentric(Lambda_sphinx, Theta_sphinx), LOS)
# np.linalg.norm(LOS_topo_sphinx)
zenith_angle_2 = geodetic_tools.angle_between_vectors(LOS_topo_sphinx, [0, 0, 1])
zenith_angle_2 = zenith_angle_2*200.0/np.pi

zenith_angle_1 + zenith_angle_2

mean_s2c, mean_c2s = prepare_measurements.get_meas()

eps1 = zenith_angle_1 - mean_c2s  # gon
eps2 = zenith_angle_2 - mean_s2c  # gon

gamma = geodetic_tools.angle_between_vectors(coords_shpinx_xyz, coords_chasseral_xyz)

k = np.pi/200*(eps1 + eps2) / gamma
print('k = {:.3f}'.format(k))

# Fehler bei nicht berücksichtigter Refraktion
standard_ref = 0.13*gamma/2.0

c2s_corr = np.pi/200*mean_c2s + standard_ref  # rad
s2c_corr = np.pi/200*mean_s2c + standard_ref  # rad

# daraus entstehender Fehler
eps3 = np.pi/200*zenith_angle_1 - c2s_corr  # rad
eps4 = np.pi/200*zenith_angle_2 - s2c_corr  # rad

# Höhenfehler
print('Höhenfehler Chasseral2Sphinx = {:.3f} m'.format(d*eps3))
print('Höhenfehler Sphinx2Chasseral = {:.3f} m'.format(d*eps4))