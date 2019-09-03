"""
Written by Andrew Donelick

"""


import datetime
import os

from KML import *


DATA_DIRECTORY = "../Data"


def build_data_filepath():
    """
    Builds the filepath for the data file.

    :return: (string) Path of the data file
    """
    d = datetime.datetime.now()

    # Create the CSV file in which we will log the packet data
    fileIndex = 0
    dataFilename = d.strftime("balloon_data_20%y_%m%d_")
    dataFilename += str(fileIndex).zfill(2) + '.csv'
    dataPath = os.path.join(DATA_DIRECTORY, dataFilename)

    while os.path.exists(dataPath):
        fileIndex += 1
        dataFilename = d.strftime("balloon_data_20%y_%m%d_")
        dataFilename += str(fileIndex).zfill(2) + '.csv'
        dataPath = os.path.join(DATA_DIRECTORY, dataFilename)

    return dataPath


def getKMLpath(name, altitudeMode, indexString):
    """
    Gets the path for a new KML file.

    :param name: (string) Name of the new file
    :param indexString: (string) Index number for the new file

    :return: (string)
    """

    kmlTemplateFile = open('KML Template.txt', 'r')
    defaultKML = kmlTemplateFile.read()
    kmlFilename = name + "_" + indexString + '.kml'
    defaultKML = addName(defaultKML, kmlFilename)
    defaultKML = addAltitudeMode(defaultKML, altitudeMode)

    kmlPath = os.path.join(DATA_DIRECTORY, kmlFilename)
    with open(kmlPath, 'w') as kmlFile:
        kmlFile.write(defaultKML)

    return kmlPath


def saveDataPacket(packet, filename):
    """
    Saves a data packet to a CSV file. The filename is given.

    :param packet: (DataPacket) Packet to save to the file
    :param filename: (string) Name of the file to save the data to

    :return: (None)
    """

    fileHandle = open(filename, 'a')
    fileSize = os.path.getsize(filename)
    fileEmpty = (fileSize == 0)

    if fileEmpty:

        fileHandle.write("Interior Temperature 1, ")
        fileHandle.write("Interior Temperature 2, ")
        fileHandle.write("Interior Temperature 3, ")
        fileHandle.write("Exterior Temperature, ")

        fileHandle.write("Pressure, ")
        fileHandle.write("Humidity, ")

        fileHandle.write("GPS Time 1, ")
        fileHandle.write("Latitude 1, ")
        fileHandle.write("Longitude 1, ")
        fileHandle.write("Altitude 1, ")
        fileHandle.write("Number of GPS Satellites 1, ")

        fileHandle.write("GPS Time 2, ")
        fileHandle.write("Latitude 2, ")
        fileHandle.write("Longitude 2, ")
        fileHandle.write("Altitude 2, ")

        fileHandle.write("Acceleration (x), ")
        fileHandle.write("Acceleration (y), ")
        fileHandle.write("Acceleration (z), ")

        fileHandle.write("Rotation Rate (x), ")
        fileHandle.write("Rotation Rate (y), ")
        fileHandle.write("Rotation Rate (z), ")

        fileHandle.write("Magnetic Field (x), ")
        fileHandle.write("Magnetic Field (y), ")
        fileHandle.write("Magnetic Field (z), ")

        fileHandle.write("Pitch, ")
        fileHandle.write("Roll, ")
        fileHandle.write("Yaw, ")

        fileHandle.write("Time Since Reset, ")
        fileHandle.write("Data Logging Status, ")
        fileHandle.write("Data Filename, ")
        fileHandle.write("Data Age, ")
        fileHandle.write("Relay States")
        fileHandle.write('\n')


    fileHandle.write(str(packet.getInteriorTemperature1()) + ', ')
    fileHandle.write(str(packet.getInteriorTemperature2()) + ', ')
    fileHandle.write(str(packet.getInteriorTemperature3()) + ', ')
    fileHandle.write(str(packet.getExteriorTemperature()) + ', ')

    fileHandle.write(str(packet.getPressure()) + ', ')
    fileHandle.write(str(packet.getHumidity()) + ', ')

    # Writes the GPS information for the sensor computer
    fileHandle.write(str(packet.getGpsTime1()) + ', ')
    fileHandle.write(str(packet.getLatitude1()) + ', ')
    fileHandle.write(str(packet.getLongitude1()) + ', ')
    fileHandle.write(str(packet.getAltitude1()) + ', ')
    fileHandle.write(str(packet.getNumSatellites1()) + ', ')

    # Writes the GPS information for the communications computer
    fileHandle.write(str(packet.getGpsTime2()) + ', ')
    fileHandle.write(str(packet.getLatitude2()) + ', ')
    fileHandle.write(str(packet.getLongitude2()) + ', ')
    fileHandle.write(str(packet.getAltitude2()) + ', ')

    ax, ay, az = packet.getAcceleration()
    gx, gy, gz = packet.getRates()
    mx, my, mz = packet.getMagneticReading()

    fileHandle.write(str(ax) +', ' + str(ay) + ', ' + str(az) + ', ')
    fileHandle.write(str(gx) +', ' + str(gy) + ', ' + str(gz) + ', ')
    fileHandle.write(str(mx) +', ' + str(my) + ', ' + str(mz) + ', ')

    pitch, roll, yaw = packet.getAttitude()
    fileHandle.write(str(pitch) + ', ')
    fileHandle.write(str(roll) + ', ')
    fileHandle.write(str(yaw) + ', ')

    fileHandle.write(str(packet.getResetTime()) + ', ')
    fileHandle.write(str(packet.getDataLoggingStatus()) + ', ')
    fileHandle.write(str(packet.getFilename()) + ', ')
    fileHandle.write(str(packet.getDataAge()) + ', ')
    fileHandle.write(str(packet.getRelayStates()))
    fileHandle.write('\n')

    fileHandle.close()