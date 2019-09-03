

import os
import StringIO
import numpy as np

NUM_READINGS = 28
DATA_FOLDER = "C:\\Users\\Andrew\\Documents\\Balloon\\2017_0803\\payload_data"


def main():
    """


    """
    
    allFiles = os.listdir(DATA_FOLDER)

    data = np.zeros((1, 2*NUM_READINGS))
    for f in allFiles:
        f = f.lower()
        if f.endswith('.csv'):

            print f

            filePath = os.path.join(DATA_FOLDER, f)

            fileHandle = open(filePath, 'r')
            dataText = fileHandle.read()
            fileHandle.close()

            header = dataText[0:dataText.find('\n')-1]
            cleanText = dataText[0:dataText.rfind('\n')-1]
            cleanText = dataText[0:cleanText.rfind('\n')]
            cleanDataFile = StringIO.StringIO(cleanText)

            fileData = np.loadtxt(cleanDataFile, delimiter=',', skiprows=1)
            numCols = fileData.shape[1]

            for i in xrange(0, numCols, 2):
                fileData[:, i] += data[-1, i]

            data = np.append(data, fileData, axis=0)

    np.savetxt('test.csv', data, delimiter=',', header=header)






if __name__ == '__main__':
    main()