"""
Written by Andrew Donelick

"""

# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout

# General Python imports
import datetime
import pynmea2
import serial
import threading
import time

# Custom imports
import FileUtilities
from BalloonCommands import *
from CommandPacket import *
from DataPacket import *
from KML import *

from functools import partial


class GroundStation(GridLayout):

    _GPS_port = None
    _radio_port = None
    _radio_port_lock = threading.Lock()
    _communication_stop = threading.Event()

    # Variables for saving the data recorded with this application
    _balloon_position_1_filepath = ""
    _balloon_position_2_filepath = ""
    _vehicle_position_filepath = ""
    _data_filepath = ""

    kv_GPS1_latitude = StringProperty()
    kv_GPS1_longitude = StringProperty()
    kv_GPS1_altitude = StringProperty()
    kv_GPS1_time = StringProperty()

    kv_GPS2_latitude = StringProperty()
    kv_GPS2_longitude = StringProperty()
    kv_GPS2_altitude = StringProperty()
    kv_GPS2_time = StringProperty()

    kv_GPS3_latitude = StringProperty()
    kv_GPS3_longitude = StringProperty()
    kv_GPS3_altitude = StringProperty()
    kv_GPS3_time = StringProperty()

    kv_interior_temp_1 = StringProperty()
    kv_interior_temp_2 = StringProperty()
    kv_interior_temp_3 = StringProperty()
    kv_exterior_temp = StringProperty()
    kv_pressure = StringProperty()
    kv_humidity = StringProperty()


    def __init__(self, **kwargs):
        """
        Creates a new GroundStation object.

        :kwargs: (dictionary) Keyword arguments

        :return: (GroundStation) New GroundStation object
        """
        super(GroundStation, self).__init__(**kwargs)
        self.build()


    def build(self):
        """
        Function to help setup the GroundStation object

        :return: (None)
        """

        # Create the file paths for the various data logging files
        self._data_filepath = FileUtilities.build_data_filepath()
        self._balloon_position_1_filepath = FileUtilities.getKMLpath("balloon_position_1", ABSOLUTE, self._data_filepath[-16:-4])
        self._balloon_position_2_filepath = FileUtilities.getKMLpath("balloon_position_2", ABSOLUTE, self._data_filepath[-16:-4])
        self._vehicle_position_filepath = FileUtilities.getKMLpath("vehicle_position", ABSOLUTE, self._data_filepath[-16:-4])


    def connect_to_radio(self):
        """
        Connects to the radio used to communicate with the payload while
        in flight. This function also starts the thread to receive and process
        balloon telemetry.

        :return: (None)
        """
        if self._radio_port is None:
            com_port = self.ids.radio_COM_port.text
            self._radio_port = serial.Serial(com_port, 1200, timeout=0.1)

            telemetry_thread = threading.Thread(target=self.telemetry_receiving_thread)
            telemetry_thread.start()


    def telemetry_receiving_thread(self):
        """
        This thread is responsible for receiving and processing all of the 
        telemetry that comes down from the balloon payload.

        :return: (None)
        """
        while True:
            if self._communication_stop.is_set():
                break

            # Check is any new data is available at the serial port for the radio
            kissString = bytes()
            self._radio_port_lock.acquire()
            radioBytes = self._radio_port.read(1000)
            self._radio_port_lock.release()
            while radioBytes:

                kissString += radioBytes
                self._radio_port_lock.acquire()
                radioBytes = self._radio_port.read(1000)
                self._radio_port_lock.release()
                time.sleep(0.01)

            if len(kissString) > 0:
                print("Length of received packet: " + str(len(kissString)))
                print(kissString.hex())

            if len(kissString) < 3:
                continue

            if kissString:
                if isDataPacket(kissString):
                    dataPacket = DataPacket()
                    packetDecoded = dataPacket.decode(kissString)
                    if packetDecoded:
                        print(dataPacket)

                        Clock.schedule_once(partial(self.update_balloon_telemetry, dataPacket))
                        FileUtilities.saveDataPacket(dataPacket, self._data_filepath)

                        # Save the position data for the sensor computer to the KML file
                        latitude = dataPacket.getLatitude1()
                        longitude = dataPacket.getLongitude1()
                        altitude = dataPacket.getAltitude1() / 3.28084
                        updateKMLFile(self._balloon_position_1_filepath, latitude, longitude, altitude)

                        # Save the position data for the communication computer to the KML file 
                        latitude = dataPacket.getLatitude2()
                        longitude = dataPacket.getLongitude2()
                        altitude = dataPacket.getAltitude2() / 3.28084
                        updateKMLFile(self._balloon_position_2_filepath, latitude, longitude, altitude)
                

            #     elif isAckPacket(kissString):
            #         commandPacket = CommandPacket()
            #         properDecoding = commandPacket.decode(kissString)

            #         if properDecoding:
            #             print("Command Received!")
            #         else:
            #             print("Improper response to command")
            #     else:
            #         pass


    def connect_to_GPS(self):
        """
        Connects to the vehicle tracking GPS and starts the vehicle tracking thread.

        :return: (None)
        """
        if self._GPS_port is None:
            com_port = self.ids.GPS_COM_port.text
            self._GPS_port = serial.Serial(com_port, 4800, timeout=0.1)

            tracking_thread = threading.Thread(target=self.vehicle_tracking_thread)
            tracking_thread.start()


    def vehicle_tracking_thread(self):
        """
        Runs the vehicle tracking communication with the local GPS.

        :return: (None)
        """

        while True:
            if self._communication_stop.is_set():
                break

            # Read the current sring from the GPS to get the car's location
            gpsSentence = ''
            gpsBytes = self._GPS_port.read(1000)
            while gpsBytes:

                gpsSentence += gpsBytes.decode("utf-8")
                gpsBytes = self._GPS_port.read(1000)
                time.sleep(0.01)

            if gpsSentence[0:6] == "$GPGGA":
                sentences = gpsSentence.split('\r\n')
                msg = pynmea2.parse(sentences[0])

                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
                timestamp = datetime.now()
                Clock.schedule_once(partial(self.update_tracking_vehicle_GPS, latitude, longitude, altitude, timestamp))
                updateKMLFile(self._vehicle_position_filepath, msg.latitude, msg.longitude, msg.altitude)


    def update_balloon_telemetry(self, packet, dt=0):
        """
        Updates the displays on the user interface with the latest 
        telemetry data from the balloon payload.

        :param packet: (DataPacket) Packet of received data

        :return: (None)
        """
        self.kv_GPS2_latitude = '{:.6f}'.format(packet.getLatitude2())
        self.kv_GPS2_longitude = '{:.6f}'.format(packet.getLongitude2())
        self.kv_GPS2_altitude = '{:.1f}'.format(packet.getAltitude2())


    def update_tracking_vehicle_GPS(self, latitude, longitude, altitude, timestamp, dt=0):
        """
        Updates the vehicle tracking information on the user interface.

        :param latitude: (float) Current latitude
        :param longitude: (float) Current longitude
        :param altitude: (float) Current altitude

        :return: (None)
        """
        self.kv_GPS3_latitude = '{:.6f}'.format(latitude)
        self.kv_GPS3_longitude = '{:.6f}'.format(longitude)
        self.kv_GPS3_altitude = '{:.1f}'.format(altitude * 3.28084)
        self.kv_GPS3_time = timestamp.strftime("%H:%M:%S")


    def on_stop(self):
        """
        Handles the closing event for the application.

        :return: (None)
        """
        self._communication_stop.set()

        if not self._GPS_port is None:
            self._GPS_port.close()

        if not self._radio_port is None:
            self._radio_port.close()



class GroundStationApp(App):

    title = "Balloon Ground Station"


    def build(self):

        self.root_widget = GroundStation()
        return self.root_widget



    def on_stop(self):
        """
        Catch the closing event, and notify the root_widget in case
        anything needs to be cleaned up prior to closing.

        :return: (None)
        """
        self.root_widget.on_stop()



def isDataPacket(kissString):
    """
    Check if the given string is an encoded DATA packet.

    :param kissString: (string) String received from the radio

    :return: (boolean)
    """
    return kissString and (kissString[2] == DATA)


def isAckPacket(kissString):
    """
    Check if the given string is an encoded ACK packet.

    :param kissString: (string) String received from the radio

    :return: (boolean)
    """

    packetType = struct.unpack('B', kissString[2])[0]
    return kissString and (packetType == ACK)



if __name__ == '__main__':
    GroundStationApp().run()


