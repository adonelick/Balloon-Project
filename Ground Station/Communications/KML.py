
NAME_START = "<name>"
NAME_END = "</name>"
ALTITUDE_MODE_START = "<altitudeMode>"
ALTITUDE_MODE_END = "</altitudeMode>"
COORDINATE_START = "<coordinates>"
POINT_COORDINATE_END = "</coordinates>\n            </Point>"
LINE_COORDINATE_END = "</coordinates>\n            </LineString>"


ABSOLUTE = "absolute"
CLAMPED_TO_GROUND = "clampToGround"

def updateKMLFile(kmlPath, latitude, longitude, altitude):
    """
    Updates a kml file with a new location coordinate.

    :param kmlPath: (string) Path of the KML file to update
    :param latitude: (float) Current latitude of the payload
    :param longitude: (float) Current longitude of the payload
    :param altitude: (float) Current altitude of the payload (MSL, in meters)

    :return: (None)
    """
    
    kmlFile = open(kmlPath, 'r')
    kml = kmlFile.read()
    kmlFile.close()

    kml = addCoordinate(kml, latitude, longitude, altitude)
    with open(kmlPath, 'w') as kmlFile:
        kmlFile.write(kml)


def addName(kml, name):
    """
    Adds a name to the KML file data.

    :param kml: (string) Current kml file text
    :param namae: (string) Name of the kml file data

    :return: (string) Updated kml file text
    """

    nameStart = kml.find(NAME_START) + len(NAME_START)
    nameEnd = kml.find(NAME_END)
    kml = kml[0:nameStart] + name + kml[nameEnd:]

    return kml


def addAltitudeMode(kml, altitudeMode):
    """
    Adds the altitude mode to the KML file data.

    :param kml: (string) Current kml file text
    :param altitudeMode: (string) Mode of displaying altitude

    :return: (string) Updated kml file text

    """

    altitudeModeStart = kml.find(ALTITUDE_MODE_START) + len(ALTITUDE_MODE_START)
    altitudeModeEnd = kml.find(ALTITUDE_MODE_END)
    kml = kml[0:altitudeModeStart] + altitudeMode + kml[altitudeModeEnd:]

    altitudeModeStart = kml.find(ALTITUDE_MODE_START, altitudeModeEnd) + len(ALTITUDE_MODE_START)
    altitudeModeEnd = kml.find(ALTITUDE_MODE_END, altitudeModeStart)
    kml = kml[0:altitudeModeStart] + altitudeMode + kml[altitudeModeEnd:]

    return kml
 

def addCoordinate(kml, latitude, longitude, altitude):
    """
    Adds a coordinate to a balloon tracking KML file.

    :param kml: (string) Current kml file text
    :param latitude: (float) Current latitude of the payload
    :param longitude: (float) Current longitude of the payload
    :param altitude: (float) Current altitude of the payload (MSL, in meters)

    :return: (string) New kml file text with the new coordinate added
    """

    # Build the coordinate string to add to the file
    coordinateString = str(longitude)
    coordinateString += ',' + str(latitude)
    coordinateString += ',' + str(altitude)

    # Add the coordinate as the last known point
    lastCoordinateStart = kml.find(COORDINATE_START) + len(COORDINATE_START)
    lastCoordinateEnd = kml.find(POINT_COORDINATE_END)
    kml = kml[0:lastCoordinateStart] + coordinateString + kml[lastCoordinateEnd:]

    # Add the coordinate to the coordinate history list
    lineCoordinateEnd = kml.find(LINE_COORDINATE_END)
    kml = kml[0:lineCoordinateEnd] + "    " + coordinateString + '\n' + "                " + kml[lineCoordinateEnd:]

    return kml
    