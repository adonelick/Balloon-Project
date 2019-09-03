

from DataPacket import *

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def main():

    packet = DataPacket()

    packet.values[BATTERY_VOLTAGE] = 11.38

    packet.values[INTERIOR_TEMPERATURE_1] = 10
    packet.values[INTERIOR_TEMPERATURE_2] = 12.345
    packet.values[EXTERIOR_TEMPERATURE] = -123.5

    packet.values[BAROMETRIC_PRESSURE] = 1000
    packet.values[HUMIDITY] = 23.24

    packet.values[GPS_TIME] = 17534900
    packet.values[GPS_DATE] = 100717
    packet.values[RAW_ALTITUDE] = 100000
    packet.values[ASCENT_RATE] = 1.0

    packet.values[RAW_LATITUDE_DEGREES] = 46
    packet.values[RAW_LATITUDE_BILLIONTHS] = 123456789
    packet.values[RAW_LATITUDE_SIGN] = 1

    packet.values[RAW_LONGITUDE_DEGREES] = 118
    packet.values[RAW_LONGITUDE_BILLIONTHS] = 123456789
    packet.values[RAW_LONGITUDE_SIGN] = 0xFF

    packet.values[GPS_VALIDITY] = False
    packet.values[GPS_SENTENCES] = 1000
    packet.values[FAILED_SENTENCES] = 10
    packet.values[NUM_SATELLITES] = 7

    packet.values[AX] = 1.01
    packet.values[AY] = 0.01
    packet.values[AZ] = -0.05

    packet.values[GX] = 10.23
    packet.values[GY] = -1.23
    packet.values[GZ] = 0.001

    packet.values[MX] = 23
    packet.values[MY] = 24
    packet.values[MZ] = 25

    packet.values[PITCH] = -5
    packet.values[ROLL] = 1
    packet.values[YAW] = 179

    packet.values[RESET_TIME] = 3600000
    packet.values[DATA_LOGGING] = False

    packet.values[DATA_AGE] = 12345
    packet.values[RELAY_STATES] = 0b0101

    kissPacket = packet.getKISS()
    print binascii.hexlify(kissPacket[2:-1])

    newPacket = DataPacket()
    newPacket.decode(kissPacket)

    print ""
    print newPacket


    """
    print HEADER + "This is a test" + ENDC
    print OKBLUE + "THis is a test" + ENDC
    print OKGREEN + "This is a test" + ENDC
    print WARNING + "This is a test" + ENDC
    print FAIL + "This is a test" + ENDC
    print BOLD + "This is a test" + ENDC
    print UNDERLINE + "This is a test" + ENDC
    """


if __name__ == '__main__':
    main()