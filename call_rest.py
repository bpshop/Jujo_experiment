# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 14:21:56 2022

@author: Daniel
"""
import requests
import json
import numpy as np
# see https://www.swisstopo.admin.ch/content/swisstopo-internet/fr/online/calculation-services/m2m/_jcr_content/contentPar/tabs/items/dokumente_und_publik/tabPar/downloadlist/downloadItems/55_1489059323854.download/Report16-03.pdf


def call_geod_rest(coords, direction):
    
    base_url = 'http://geodesy.geo.admin.ch/reframe/'
    
    url = base_url + direction + '?easting='
    url = url + str(coords[0]) + '&northing='
    url = url + str(coords[1]) + '&altitude='
    url = url + str(coords[2]) + '&format=json'
    
    # uncomment to see the formed url
    # print(url)
    
    r = requests.get(url)
    
    # if you rather use a proxy, call this:
    # proxies = {
    #  "http": "http://my_proxy.com:my_port",
    #  "https": "http://my_proxy.com:my_port",
    # }
    # 
    # r = requests.get(url, proxies=proxies)
    
    coords_out = [np.nan, np.nan, np.nan]
    if(r.ok):
        jData = json.loads(r.content)
        x_out = float(jData["easting"])
        y_out = float(jData["northing"])
        z_out = float(jData["altitude"])
        
        coords_out = [x_out, y_out, z_out]
       
    return coords_out