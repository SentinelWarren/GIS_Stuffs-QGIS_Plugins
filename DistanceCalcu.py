## Copyright (c) 2017 Warren Alex cc PowerCorner
## Distributed under the MIT software license, see the accompanying
## file COPYING or http://www.opensource.org/licenses/mit-license.php.

from math import sin, cos, sqrt, asin, radians
from Tkinter import Tk
from tkFileDialog import askopenfilename
import csv
import fiona
from shapely.geometry import Point, mapping

def haversine(firLon, firLat, secLon, secLat):
        
        earthR = 6371
        # convert to radians 
        firLon, firLat, secLon, secLat = map(radians, [firLon, firLat, secLon, secLat])
        # formula 
        disLon = secLon - firLon 
        disLat = secLat - firLat 
        a = sin(disLat/2)**2 + cos(firLat) * cos(secLat) * sin(disLon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = earthR * c

        return km

def prevread(rep):
        prev = None
        for d in rep:
            yield prev, d
            prev = d


Tk().withdraw()
csvDatabase = askopenfilename()

with open(csvDatabase, 'rb') as f:
   reader = csv.DictReader(f)
   for st in prevread(reader):
       print st


# shapefile schema
schema = { 'geometry': 'Point', 'properties':{'Distance' : 'float', 'Village_NM': 'str', 'Region': 'str', 'Lat':'float', 'Lon':'float', }}

# shapefile creation
with fiona.collection("Output/Distance.shp", "w", "ESRI Shapefile", schema) as output:
    with open(csvDatabase, 'rb') as f:
       reader = csv.DictReader(f)


       # we need here to eliminate the first pair of point with None
       for i, st in enumerate(prevread(reader)):
            try:
                if i == 0: #(pair with None)
                    # writing of the point geometry and the attributes
                    point = Point(float(st[1]['Lon']), float(st[1]['Lat']))
                    dist = 0 # None
                    output.write({'properties': { 'Distance': dist, 'Village_NM':st[1]['Village_NM'], 'Region':st[1]['Region'], 'Lat':float(st[1]['Lat']), 'Lon':float(st[1]['Lon'])},'geometry': mapping(point)})
                else:
                    # writing of the point geometry and the attributes
                    point = Point(float(st[1]['Lon']), float(st[1]['Lat']))
                    # Haversine distance between pairs of points
                    dist = haversine(float(st[0]['Lon']), float(st[0]['Lat']), float(st[1]['Lon']),float(st[1]['Lat']))
                    output.write({'properties': { 'Distance': dist, 'Village_NM':st[1]['Village_NM'], 'Region':st[1]['Region'], 'Lat':float(st[1]['Lat']), 'Lon':float(st[1]['Lon'])},'geometry': mapping(point)})
            except ValueError:
                pass
