"""
Packet.py 


"""

import logging as log
import struct
import binascii
import numpy as np
from datetime import datetime, timedelta
from ColorEscapeCodes import *


UNKNOWN = -1
DATA = 0
COMMAND = 1
ACK = 2

BOOL = '<?'
BYTE = '<B'
INT = '<h'
UINT = '<H'
LONG = '<l'
ULONG = '<L'
FLOAT = '<f'

FEND = b'\xC0'
FESC = b'\xDB'
TFEND = b'\xDC'
TFESC = b'\xDD'

WIDTHS = {
    BOOL : 1,
    BYTE : 1,
    INT : 2,
    UINT : 2,
    LONG : 4,
    ULONG : 4,
    FLOAT : 4
}


class Packet(object):

    def __init__(self):
        """
        Create a new Packet object.

        :return: (Packet) New packet object
        """
        self.packetType = UNKNOWN
        self.values = []
        self.types = []


    def getNumBytes(self):
        """
        Returns the number of bytes in each packet for radio transmission.
        This value excludes the bytes needed for formatting the KISS packet
        (three extra bytes).

        :return: (int) Number of bytes in each packet
        """

        numBytes = 0
        for t in self.types:
            numBytes += WIDTHS[t]

        return numBytes


    def getBytes(self):
        """
        Returns the byte string associated with the values of a packet. 
        This string is not formatted for nice display; for that, see
        the getHexString method.

        :return: (string) Byte string of the packet's values
        """
        assert(len(self.values) == len(self.types))
        bytes = b''

        # Add the values 
        for i, value in enumerate(self.values):
            valueType = self.types[i]
            bytes += struct.pack(valueType, value)

        return bytes


    def getHexString(self):
        """
        Returns a nice hex string representation of a packet's values.
        This shows the hex data as alphanumeric characters (0-9, A-F),
        rather than as ASCII interpretations of the byte data.

        :return: (string) Hex string representation of the packet's values
        """
        return binascii.hexlify(self.getBytes())


    def getKISS(self):
        """
        Get the KISS packet to send over the radio to the receiving computer.
        The KISS packet includes the bytes that start and end a packet, and
        escaped FESC and FEND bytes. 

        :return: (string) KISS packet to send over the radio
        """
        checksum = self.computeChecksum()

        kissPacket =  FEND + '\x00'
        kissPacket += escapeValues(self.getBytes())
        kissPacket += escapeValues(struct.pack(UINT, checksum))
        kissPacket += FEND

        return kissPacket


    def computeChecksum(self):
        """
        Computes the checksum of all data values within the packet. This 
        checksum computation does not account for the KISS packet parts;
        it's just computed on the data values.

        :return: (int) checksum of data values 
        """

        dataBytes = self.getBytes()
        numBytes = len(dataBytes)

        valueSum = np.uint16(0)
        for i in range(0, numBytes, 2):

            if i == numBytes - 1:
                chunk = struct.unpack(UINT, b'\x00' + dataBytes[i:])
            else:
                chunk = struct.unpack(UINT, dataBytes[i:i+2])
            valueSum = np.uint16(valueSum + chunk)

        checksum = np.uint16(-1) - valueSum
        return checksum

        
    def decode(self, dataString):
        """
        Gets the current values within a byte string.

        :return: (boolean) Whether or not we were able to decode the packet
        """

        if (dataString[0] != ord(FEND)) or (dataString[-1] != ord(FEND)):
            return False

        # Chop off the KISS packet parts of the data string,
        # descape the FESC and FEND characters
        dataString = dataString[2:-1]
        dataBytes = descapeValues(dataString)


        # Check if we have the same number of bytes as we should have
        if len(dataBytes) != (self.getNumBytes() + 2):
            log.error("Error with number of bytes: " + str((len(dataBytes), self.getNumBytes() + 2)))
            return False

        # Decode each of the values from the raw bytes
        byteIndex = 0
        self.values = []
        for t in self.types:

            valueBytes = dataBytes[byteIndex:byteIndex + WIDTHS[t]]
            value = struct.unpack(t, valueBytes)[0]
            self.values.append(value)

            byteIndex += WIDTHS[t]

        # Check the checksum of the bytes to see if we decoded correctly
        checksumBytes = dataBytes[-2:]
        packetChecksum = np.uint16(struct.unpack(UINT, checksumBytes))[0]
        computedChecksum = self.computeChecksum()

        if packetChecksum != computedChecksum:
            log.error("Checksum error")
            return False

        return True


def escapeValues(data):
    """
    Escpaes the FEND and FESC values within a packet according
    to the KISS protocol. 

    :param bytes: (string) Original byte string 

    :return: (string) packet string with escpaed values
    """

    newBytes = bytes()
    for b in data:
        if b == ord(FEND):
            newBytes += (FESC + TFEND)
        elif b == ord(FESC):
            newBytes += (FESC + TFESC)
        else:
            newBytes += bytes([b])

    return newBytes


def descapeValues(data):
    """
    De-escpaes the FEND and FESC values within a packet according
    to the KISS protocol. 

    :param bytes: (string) Byte string with escaped values

    :return: (string) packet string with de-escpaed values
    """

    numBytes = len(data)
    newBytes = bytes()
    i = 0
    while (i < numBytes):

        b = data[i]
        if (b == ord(FESC)) and (i != numBytes - 1):
            if data[i+1] == ord(TFEND):
                newBytes += FEND
                i += 1

            elif data[i+1] == ord(TFESC):
                newBytes += FESC
                i += 1

            else:
                newBytes += bytes([b])
        else:
            newBytes += bytes([b])

        i += 1

    return newBytes
