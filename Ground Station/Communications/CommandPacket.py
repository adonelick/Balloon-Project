"""
CommandPacket.py 

Class that defines the command packet to be sent to the balloon payload.
"""

from Packet import *
from BalloonCommands import COMMAND_INDICES

class CommandPacket(Packet):

    def __init__(self, commandString='', commandValue=0):
        """
        Creates a new command packet. Overrides the Packet constructor.

        :return: (CommandPacket) New command packet
        """

        self.packetType = COMMAND
        self.types = [BYTE, BYTE, ULONG,
                      ULONG, ULONG, ULONG, ULONG, ULONG]

        commandIndex = COMMAND_INDICES[commandString]
        self.values = [COMMAND, commandIndex, commandValue,
                       0x12345678, 0x12345678, 0x12345678,
                       0x12345678, 0x12345678]