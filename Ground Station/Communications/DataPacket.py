"""
DataPacket.py 

Class that defines the data packet received from the balloon payload.
"""

from Packet import *

PACKET_TYPE = 0
BATTERY_VOLTAGE = 1

INTERIOR_TEMPERATURE_1 = 2
INTERIOR_TEMPERATURE_2 = 3
INTERIOR_TEMPERATURE_3 = 4
EXTERIOR_TEMPERATURE = 5
BAROMETRIC_PRESSURE = 6
HUMIDITY = 7

YEAR_1 = 8
MONTH_1 = 9
DATE_1 = 10
HOUR_1 = 11
MINUTE_1 = 12
SECOND_1 = 13
LATITUDE_1 = 14
LONGITUDE_1 = 15
ALTITUDE_1 = 16
SPEED_1 = 17
HEADING_1 = 18
NUM_SATELLITES_1 = 19

AX = 20
AY = 21
AZ = 22

GX = 23
GY = 24
GZ = 25

MX = 26
MY = 27
MZ = 28

PITCH = 29
ROLL = 30
YAW = 31

RESET_TIME = 32
DATA_LOGGING = 33
FILENAME_INDEX = 34

DATA_AGE = 35
RELAY_STATES = 36

YEAR_2 = 37
MONTH_2 = 38
DATE_2 = 39
HOUR_2 = 40
MINUTE_2 = 41
SECOND_2 = 42

LATITUDE_2 = 43
LONGITUDE_2 = 44
ALTITUDE_2 = 45


class DataPacket(Packet):

    def __init__(self):
        """
        Creates a new data packet. Overrides the Packet constructor.

        :return: (DataPacket) New data packet
        """
        
        self.packetType = DATA
        self.types = [BYTE,                         # Packet type
                      FLOAT,                        # Battery voltage
                      FLOAT, FLOAT, FLOAT, FLOAT,   # Temperature readings
                      FLOAT, FLOAT,                 # Pressure and humidity readings
                      BYTE, BYTE, BYTE,             # GPS Year, month, date (sensor computer)
                      BYTE, BYTE, BYTE,             # GPS Hour, minute, second (sensor computer)
                      LONG, LONG, LONG,             # GPS latitude, longitude, altitude (sensor computer)
                      ULONG, UINT, BYTE,            # GPS speed, heading, num satellites (sensor computer)
                      FLOAT, FLOAT, FLOAT,          # IMU data (accelerometer)
                      FLOAT, FLOAT, FLOAT,          # IMU data (gyroscope)
                      FLOAT, FLOAT, FLOAT,          # IMU data (magnetometer)
                      FLOAT, FLOAT, FLOAT,          # Attitude data
                      ULONG,                        # Time since reset
                      BOOL, UINT,                   # Data logging
                      ULONG,                        # Time since last data arrival
                      ULONG,                        # Relay states
                      BYTE, BYTE, BYTE,             # GPS Year, month, date (comm computer)
                      BYTE, BYTE, BYTE,             # GPS Hour, minute, second (comm computer)
                      LONG, LONG, LONG              # GPS latitude, longitude, altitude (comm computer)
                     ] 

        self.values = [0]*len(self.types)
        self.values[0] = DATA


    def getBatteryVoltage(self):
        """
        Gets the battery voltage of the payload.

        :return: (float) Battery voltage
        """
        return self.values[BATTERY_VOLTAGE]


    def getInteriorTemperature1(self):
        return self.values[INTERIOR_TEMPERATURE_1]


    def getInteriorTemperature2(self):
        return self.values[INTERIOR_TEMPERATURE_2]


    def getInteriorTemperature3(self):
        return self.values[INTERIOR_TEMPERATURE_3]


    def getExteriorTemperature(self):
        return self.values[EXTERIOR_TEMPERATURE]


    def getPressure(self):
        return 0.000145038*self.values[BAROMETRIC_PRESSURE]


    def getHumidity(self):
        return self.values[HUMIDITY]


    def getGpsTime1(self):
        year = 2000 + self.values[YEAR_1]
        month = self.values[MONTH_1]
        day = self.values[DATE_1]
        hour = self.values[HOUR_1]
        minute = self.values[MINUTE_1]
        second = self.values[SECOND_1]

        if month <= 0: month = 1
        if month > 12: month = 1

        if day <= 0: day = 1
        if day > 31: day = 1

        timezoneDifference = 7
        pacificTime = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        pacificTime = pacificTime + timedelta(hours=-timezoneDifference)

        return pacificTime


    def getAltitude1(self):
        rawAltitude = self.values[ALTITUDE_1]
        return 0.0328084 * rawAltitude


    def getLongitude1(self):
        return self.values[LONGITUDE_1] / 10000000.0


    def getLatitude1(self):
        return self.values[LATITUDE_1] / 10000000.0


    def getNumSatellites1(self):
        return self.values[NUM_SATELLITES_1]


    def getSpeed(self):
        return 0.000621371 * self.values[SPEED_1]


    def getGpsTime2(self):
        year = 2000 + self.values[YEAR_2]
        month = self.values[MONTH_2]
        day = self.values[DATE_2]
        hour = self.values[HOUR_2]
        minute = self.values[MINUTE_2]
        second = self.values[SECOND_2]

        if month <= 0: month = 1
        if month > 12: month = 1

        if day <= 0: day = 1
        if day > 31: day = 1

        timezoneDifference = 7
        pacificTime = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        pacificTime = pacificTime + timedelta(hours=-timezoneDifference)

        return pacificTime

    def getAltitude2(self):
        rawAltitude = self.values[ALTITUDE_2]
        return 0.0328084 * rawAltitude


    def getLongitude2(self):
        return self.values[LONGITUDE_2] / 10000000.0


    def getLatitude2(self):
        return self.values[LATITUDE_2] / 10000000.0


    def getAcceleration(self):
        ax = self.values[AX]
        ay = self.values[AY]
        az = self.values[AZ]

        return ax, ay, az


    def getRates(self):
        gx = self.values[GX]
        gy = self.values[GY]
        gz = self.values[GZ]

        return gx, gy, gz


    def getMagneticReading(self):
        mx = self.values[MX]
        my = self.values[MY]
        mz = self.values[MZ]

        return mx, my, mz


    def getAttitude(self):
        pitch = self.values[PITCH]
        roll = self.values[ROLL]
        yaw = self.values[YAW]

        return pitch, roll, yaw


    def getResetTime(self):
        return self.values[RESET_TIME] / 1000.0


    def getDataLoggingStatus(self):
        return self.values[DATA_LOGGING]


    def getFilename(self):
        filenameIndex = self.values[FILENAME_INDEX]
        return "DATA" + str(filenameIndex).zfill(3) + '.CSV'


    def getDataAge(self):
        return self.values[DATA_AGE] / 1000.0


    def getRelayStates(self):
        """
        Gets the current states of all four relays.

        :return: (4-tuple) Boolean states of all relays
        """ 
        relayStates = self.values[RELAY_STATES]

        relay1 = bool(relayStates & 0b0001)
        relay2 = bool(relayStates & 0b0010)
        relay3 = bool(relayStates & 0b0100)
        relay4 = bool(relayStates & 0b1000)

        return relay1, relay2, relay3, relay4


    def __str__(self):
        """
        Gets the string representation of the object.

        :return: (string) String representation
        """

        string = ''
        string += "Battery Voltage:                 " + "{0:.2f}".format(self.getBatteryVoltage()) + '\n'
        string += "Data Logging:                    " + str(self.getDataLoggingStatus()) + '\n'
        string += "Data Filename:                   " + self.getFilename() +'\n'

        string += "Time Since Instrument Reset (s): " + "{0:.2f}".format(self.getResetTime())  + '\n'
        string += "Data Age (s):                    " + "{0:.2f}".format(self.getDataAge()) + '\n'
        string += '\n'
        string += "Interior Temperature 1 (F):      " + "{0:.2f}".format(self.getInteriorTemperature1()) + '\n'
        string += "Interior Temperature 2 (F):      " + "{0:.2f}".format(self.getInteriorTemperature2()) + '\n'
        string += "Interior Temperature 3 (F):      " + "{0:.2f}".format(self.getInteriorTemperature3()) + '\n'
        string += "Exterior Temperature (F):        " + "{0:.2f}".format(self.getExteriorTemperature()) + '\n'
        string += "Pressure (PSI):                  " + "{0:.2f}".format(self.getPressure()) + '\n'
        string += "Humidity (%):                    " + "{0:.2f}".format(self.getHumidity()) + '\n'
        string += '\n'

        string += "GPS Time:                        " + str(self.getGpsTime1()) + '\n'
        string += "Latitude:                        " + "{0:.9f}".format(self.getLatitude1()) + '\n'
        string += "Longitude:                       " + "{0:.9f}".format(self.getLongitude1()) + '\n'
        string += "Altitude (ft):                   " + "{0:.2f}".format(self.getAltitude1()) + '\n'
        string += "Speed (MPH):                     " + "{0:.2f}".format(self.getSpeed()) + '\n'
        string += '\n'

        string += "GPS Time:                        " + str(self.getGpsTime2()) + '\n'
        string += "Latitude:                        " + "{0:.9f}".format(self.getLatitude2()) + '\n'
        string += "Longitude:                       " + "{0:.9f}".format(self.getLongitude2()) + '\n'
        string += "Altitude (ft):                   " + "{0:.2f}".format(self.getAltitude2()) + '\n'
        string += '\n'

        ax, ay, az = self.getAcceleration()
        string += "Acceleration (x, y, z):          "
        string += "{0:.2f}".format(ax) + ", "
        string += "{0:.2f}".format(ay) + ", "
        string += "{0:.2f}".format(az) + '\n'

        gx, gy, gz = self.getRates()
        string += "Rates (x, y, z):                 "
        string += "{0:.2f}".format(gx) + ", "
        string += "{0:.2f}".format(gy) + ", "
        string += "{0:.2f}".format(gz) + '\n'

        mx, my, mz = self.getMagneticReading()
        string += "Magnetic Field (x, y, z):        "
        string += "{0:.2f}".format(mx) + ", "
        string += "{0:.2f}".format(my) + ", "
        string += "{0:.2f}".format(mz) + '\n'

        roll, pitch, yaw = self.getAttitude()
        string += "Roll (deg):                      " + "{0:.2f}".format(roll) + '\n'
        string += "Pitch (deg):                     " + "{0:.2f}".format(pitch) + '\n'
        string += "Yaw (deg):                       " + "{0:.2f}".format(yaw) + '\n'
        string += '\n'
        relayStates = self.getRelayStates()
        

        string += "Relay States:                    " 
        string += (( "ON  ") if relayStates[0] else ( "OFF  ")) 
        string += (( "ON  ") if relayStates[1] else ( "OFF  "))
        string += (( "ON  ") if relayStates[2] else ( "OFF  "))
        string += (( "ON  ") if relayStates[3] else ( "OFF  "))
        string += '\n'


        return string

    def __repr__(self):
        return str(self)
