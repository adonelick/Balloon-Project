"""
Written by Andrew Donelick
adonelick@hmc.edu

Plots a specified measurement against time. The data file
from which this script reads should have been processed to
remove the file header and converted unsigned values to signed values.

"""

import os
import argparse
import numpy as np 
from matplotlib import pyplot as plt


KML_FILE_LOCATION = "C:\Users\Andrew\Documents\Balloon\KML Logs"
POSITION = "position"
INTERIOR_TEMP = "interiorTemp"
MEASUREMENTS = {
    "interiorTemp" : ("Interior Temperature", "Degrees C", 1),
    "heaterTemp" : ("Heater Temperature", "Degrees C", 5),
    "exteriorTemp" : ("Exterior Temperature", "Degrees C", 7),
    "pressure" : ("Atmospheric Pressure", "PSI", 9),
    "humidity" : ("Relative Humidity", "%", 11),
    "altitude" : ("Altitude", "m", 13),
    "pitch" : ("Pitch", "Degrees", 15),
    "roll" : ("Roll", "Degrees", 17),
    "yaw" : ("Yaw", "Degrees", 19),
    "latitude" : ("Latitude", "Degrees", 27),
    "longitude" : ("Longitude", "Degrees", 29)
}


def main(filename, measurement):
    """

    For the "position" argument, the program generates a KML file which 
    can be viewed in Google Earth.

    :param filename: (string) Path of the file to be used for plotting
    :param measurement: (string) Key of the measurement to be plotted

    :return: (None)
    """
    
    data = np.loadtxt(filename, delimiter=',')

    if measurement == POSITION:
        latitudeIndex = MEASUREMENTS["latitude"][2]
        longitudeIndex = MEASUREMENTS["longitude"][2]
        altitudeIndex = MEASUREMENTS["altitude"][2]

        latitude = data[:, latitudeIndex]
        longitude = data[:, longitudeIndex]
        altitude = data[:, altitudeIndex]

        name = raw_input("Please type a name for the new KML file: ")
        generateKML(latitude, longitude, altitude, name)
    else:

        if not (MEASUREMENTS.has_key(measurement)):
            print "Invalid measurement!", measurement
            return

        if measurement == INTERIOR_TEMP:

            measurementTitle = MEASUREMENTS[measurement][0]
            measurementUnit = MEASUREMENTS[measurement][1]
            measurementIndex = MEASUREMENTS[measurement][2]
            
            x1 = data[:, measurementIndex - 1]
            y1 = data[:, measurementIndex]

            x2 = data[:, measurementIndex + 1]
            y2 = data[:, measurementIndex + 2]

            plt.plot(x1, y1, label="Interior Temperature 1")
            plt.plot(x2, y2, label="Interior Temperature 2")
            plt.legend()

        else:
            measurementTitle = MEASUREMENTS[measurement][0]
            measurementUnit = MEASUREMENTS[measurement][1]
            measurementIndex = MEASUREMENTS[measurement][2]

            x = data[:, measurementIndex - 1]
            y = data[:, measurementIndex]
            plt.plot(x, y)

        plt.xlabel("Time (s)")
        plt.ylabel(measurementUnit)
        plt.title(measurementTitle)
        plt.show()


def generateKML(latitude, longitude, altitude, name):
    """
    Generates and saves a KML file based on the given latitude, 
    longitude, and altitude vectors. 

    :param latitude: (numpy array) Array of latitudes for the points
    :param longitude: (numpy array) Array of longitudes for the points
    :param altitude: (numpy array) Array of altitudes for the points
    :param name: (string) Name of the KML File

    :return: (None)
    """

    assert(len(latitude) == len(longitude))
    assert(len(latitude) == len(longitude))
    numPoints = len(latitude)

    # Build up the string of points for the KML file
    pointsString = ""
    for i in xrange(numPoints):
        pointsString += (latitude[i] + ',')
        pointsString += (longitude[i] + ',')
        pointsString += (altitude[i] + ' ')

    lastPointString = latitude[-1] + ',' + longitude[-1] + ',' + altitude[-1]

    templateFile = open('KML Template.txt', 'rb')
    kmlTemplate = templateFile.read()
    templateFile.close()

    # Put the points into a previously formatted KML file
    kmlTemplate = kmlTemplate[0:1239] + pointsString + kmlTemplate[1239:]
    kmlTemplate = kmlTemplate[0:1015] + lastPointString + kmlTemplate[1015:]
    kmlTemplate = kmlTemplate[0:234] + name + kmlTemplate[234:]

    kmlFile = open(os.path.join(KML_FILE_LOCATION, name + ".kml"), 'wb')
    kmlFile.write(kmlTemplate)
    kmlFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process balloon data file')
    parser.add_argument('filename', type=str, nargs=1,
                        help='Filename for the file to plot')
    parser.add_argument('measurement', type=str, nargs=1,
                         help='Name of the measurement to plot')

    args = parser.parse_args()
    main(args.filename[0], args.measurement[0])
    main()
