#! /usr/bin/python3
"""
geolocate.py - calculate the latitude and longitude of an unknown targeted
location by using three known points (latitudes and longitudes) and for each
point a distance in kilometers to the target location.
"""


import math
import numpy as np


def main():
    latA = 35.711536
    longA = 139.766667
    latB = 35.710251
    longB = 139.755461

    latC = 35.730429
    longC = 139.747774

    print_header()

    P1 = convert_geo_to_xyz(latA, longA)
    P2 = convert_geo_to_xyz(latB, longB)
    P3 = convert_geo_to_xyz(latC, longC)

    distA, distB, distC = get_distance()
    lat_unknown, lon_unknown = calculate_coordition(P1, P2, P3, distA, distB, distC)
    message = "The targeted location is {}, {}".format(lat_unknown, lon_unknown)
    print(message)
    print(P1, P2, P3)

def print_header():
    print("------------------------------------------------------------")
    print("-------------------Location Calculator----------------------")
    print("------------------------------------------------------------")


def get_distance():
    distA = float(input('Please input distance A in km: '))
    distB = float(input('Please input distance B in km: '))
    distC = float(input('Please input distance C in km: '))
    return distA, distB, distC


def convert_geo_to_xyz(lat, longi, earthR=6371):
    """
    Convert geodetic lat/long to ECEF xyz.

    Parameters
    ----------
    lat : float
        Latitude of a location.
    longi : float
        Longitutde of a location.

    Returns
    -------
    2D numpy array.
        The Cartesian coordinate of a location.
    """

    x = earthR * (math.cos(math.radians(lat)) * math.cos(math.radians(longi)))
    y = earthR * (math.cos(math.radians(lat)) * math.sin(math.radians(longi)))
    z = earthR * (math.sin(math.radians(lat)))
    coordinate = np.array([x, y, z])

    return coordinate


# def transform_circle(p1, p2, p3):
#     """
#     none
#     """
#     unit_vector_x = ((p2 - p1) / (np.linalg.norm(p2 - p1))).transpose()
#     i = unit_vector_x.dot(p3 - p1)
#     unit_vector_y = (p3 - p1 - i * unit_vector_x) / (np.linalg.norm(p3 - p1 - i * unit_vector_x))
#     unit_vector_z = np.cross(unit_vector_x, unit_vector_y)
#     d = np.linalg.norm(p2 - p1)
#     j = np.dot(unit_vector_y, p3 - p1)
#     return unit_vector_x, unit_vector_y, unit_vector_z, i, d, j


def calculate_coordition(P1, P2, P3, DistA, DistB, DistC, earthR=6371):
    ex = (P2 - P1)/(np.linalg.norm(P2 - P1))
    i = np.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(np.linalg.norm(P3 - P1 - i*ex))
    ez = np.cross(ex,ey)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(ey, P3 - P1)

    #from wikipedia
    #plug and chug using above values
    x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
    y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    z = np.sqrt(pow(DistA,2) - pow(x,2) - pow(y,2))

    #triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + z*ez

    #convert back to lat/long from ECEF
    #convert to degrees
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))

    return lat, lon



if __name__ == '__main__':
    main()
