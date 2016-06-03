"""
Written by Andrew Donelick
adonelick@hmc.edu

Usage:
    python processData.py filename

    filename: (string) Path for the file to process

"""

import os
import argparse
import numpy as np 

NUM_ENTRIES = 15

def main(directory):
    """
    Converts the data saved by the SPARKY flight computer into a form
    which can be read and plotted.

    :param directory: (string) Path for the files to process

    :return: (None)
    """

    combinedData = None
    files = os.listdir(directory)
    files.sort()
    lastTime = 0

    for filename in files:

        # Skip any non CSV files
        if not filename.endswith(".csv"):
            continue

        rawData = np.loadtxt(filename, delimiter=',', skiprows=1)
        data = np.zeros(rawData.shape, np.float32)

        # Convert the time entries from milliseconds to seconds
        # Add on the last recorded time from the last data file
        for i in xrange(NUM_ENTRIES):
            data[:,2*i] = (rawData[:,2*i] / 1000.0) + lastTime

        # Convert the temperature readings to degrees C
        data[:,1] = (rawData[:,1]).astype(np.int16) / 100.0
        data[:,3] = (rawData[:,3]).astype(np.int16) / 100.0
        data[:,5] = (rawData[:,5]).astype(np.int16) / 100.0
        data[:,7] = (rawData[:,7]).astype(np.int16) / 100.0

        # Convert the pressure reading to PSI
        data[:,9] = (rawData[:,9]).astype(np.int16) / 1000.0

        # Convert humidity readings to %
        data[:,11] = (rawData[:,11]).astype(np.int16) / 100.0

        # Convert altitude readings to meters
        data[:,13] = (rawData[:,13]).astype(np.int32) / 100.0

        # Convert pitch, roll, yaw maeasurements to degrees
        data[:,15] = (rawData[:,15]).astype(np.int16) / 100.0
        data[:,17] = (rawData[:,17]).astype(np.int16) / 100.0
        data[:,19] = (rawData[:,19]).astype(np.int16) / 100.0

        # No conversion necessary for heater status or relay states
        data[:,21] = rawData[:,21]
        data[:,23] = rawData[:,23]

        # Convert the GPS time to seconds
        data[:,25] = ((rawData[:,25]).astype(np.uint32) / 1000000) * 3600
        data[:,25] += ((rawData[:,25]).astype(np.uint32) / 10000) * 60
        data[:,25] += ((rawData[:,25]).astype(np.uint32) / 100)
        data[:,25] += (rawData[:,25]).astype(np.uint32) / 100.0

        # No conversion necessary for latitude and longitude
        data[:,27] = rawData[:,27]
        data[:,29] = rawData[:,29]

        if combinedData == None:
            combinedData = data
        else:
            combinedData = np.append(combinedData, data, axis=0)

        lastTime = combinedData[-1, 2*(NUM_ENTRIES - 1)]

    newFilename = "ProcessedData.csv"
    np.savetxt(newFilename, combinedData, delimiter=',')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process balloon data file')
    parser.add_argument('directory', type=str, nargs=1,
                        help='Directory of the files to process')

    args = parser.parse_args()
    main(args.filename[0])
