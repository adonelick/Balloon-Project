
from KML import *


def main():
    
    kmlTemplateFile = open('KML Template.txt', 'r')
    kmlTemplate = kmlTemplateFile.read()
    endName = kmlTemplate.find(NAME_END)

    filename = "BalloonTest.kml"
    kml = addName(kmlTemplate, filename)
    kml = addCoordinate(kml, 47.031635, -117.2965017, 1000.0)
    kml = addCoordinate(kml, 47.131635, -117.2965017, 2000.0)
    kml = addCoordinate(kml, 47.231635, -117.2965017, 3000.0)
    kml = addCoordinate(kml, 47.331635, -117.2965017, 4000.0)
    kml = addCoordinate(kml, 47.431635, -117.2965017, 5000.0)
    print kml










if __name__ == '__main__':
    main()