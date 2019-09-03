"""
main.py 

Receives, displays, and saves the data being transmitted from the 
balloon payload and a GPS unit mounted inside the tracking vehicle.
"""

import os
import sys
import time
import serial
import datetime
import pynmea2

from BalloonCommands import *
from DataPacket import *
from CommandPacket import *
from KML import *

GPS_COM_PORT = "COM10"
RADIO_COM_PORT = "COM9"

DATA_DIRECTORY = "../Data"

def main():
    """
    Runs the main program to receive data and GPS packets.

    :return: (None)
    """

    # Set up the serial port connected to the GPS
    gps = serial.Serial(GPS_COM_PORT, 4800, timeout=0.1)

    # Set up the serial port connected to the radio
    radio = serial.Serial(RADIO_COM_PORT, 1200, timeout=0.1)
    d = datetime.now()

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

    # Set up the KML file for tracking the payload
    kmlPath = getKMLpath("balloon_position", ABSOLUTE, dataFilename[13:25])

    # Set up the KML file for tracking the car
    carKMLpath = getKMLpath("car_position", CLAMPED_TO_GROUND, dataFilename[13:25])

    # Get the most recent modification time of the command file
    commandModificationTime = os.path.getmtime(COMMAND_LOG_PATH)

    while True:

        # Check if we want to send a command to the balloon module
        if os.path.getmtime(COMMAND_LOG_PATH) > commandModificationTime:
            commandModificationTime = os.path.getmtime(COMMAND_LOG_PATH)

            fileHandle = open(COMMAND_LOG_PATH, 'r')
            allCommands = fileHandle.readlines()
            newCommand = allCommands[-1][0:-1]

            if newCommand != ' ':
                tokens = newCommand.split(' ')
                commandString = tokens[0]

                if len(tokens) == 2:
                    commandValue = int(tokens[1])
                else:
                    commandValue = 0
                commandPacket = CommandPacket(commandString, commandValue)
                radio.write(commandPacket.getKISS())
                time.sleep(1)

        # Read the current sring from the GPS to get the car's location
        gpsSentence = ''
        gpsBytes = gps.read(1000)
        while gpsBytes:

            gpsSentence += gpsBytes
            gpsBytes = gps.read(1000)
            time.sleep(0.01)

        if gpsSentence[0:6] == "$GPGGA":
            sentences = gpsSentence.split('\r\n')
            msg = pynmea2.parse(sentences[0])
            updateKMLFile(carKMLpath, msg.latitude, msg.longitude, msg.altitude)

        # Check is any new data is available at the serial port for the radio
        kissString = b''
        radioBytes = radio.read(1000)
        while radioBytes:

            kissString += radioBytes
            radioBytes = radio.read(1000)
            time.sleep(0.01)

        if len(kissString) < 3:
            continue

        if kissString:
            if isDataPacket(kissString):
                dataPacket = DataPacket()
                dataPacket.decode(kissString)
                print(dataPacket)

                saveDataPacket(dataPacket, dataPath)
                latitude = dataPacket.getLatitude()
                longitude = dataPacket.getLongitude()
                altitude = dataPacket.getAltitude() / 3.28084
                updateKMLFile(kmlPath, latitude, longitude, altitude)

            
            elif isAckPacket(kissString):
                commandPacket = CommandPacket()
                properDecoding = commandPacket.decode(kissString)

                if properDecoding:
                    print("Command Received!")
                else:
                    print("Improper response to command")
            else:
                pass

        time.sleep(0.5)


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


def isDataPacket(kissString):
    """
    Check if the given string is an encoded DATA packet.

    :param kissString: (string) String received from the radio

    :return: (boolean)
    """
    
    packetType = struct.unpack('B', kissString[2])[0]
    return kissString and (packetType == DATA)


def isAckPacket(kissString):
    """
    Check if the given string is an encoded ACK packet.

    :param kissString: (string) String received from the radio

    :return: (boolean)
    """

    packetType = struct.unpack('B', kissString[2])[0]
    return kissString and (packetType == ACK)


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

        fileHandle.write("GPS Time, ")
        fileHandle.write("Altitude, ")

        fileHandle.write("Latitude, ")
        fileHandle.write("Longitude, ")

        fileHandle.write("Number of GPS Satellites, ")

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

    fileHandle.write(str(packet.getGpsTime()) + ', ')
    fileHandle.write(str(packet.getAltitude()) + ', ')

    fileHandle.write(str(packet.getLatitude()) + ', ')
    fileHandle.write(str(packet.getLongitude()) + ', ')
    fileHandle.write(str(packet.getNumSatellites()) + ', ')

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



if __name__ == '__main__':
    main()
