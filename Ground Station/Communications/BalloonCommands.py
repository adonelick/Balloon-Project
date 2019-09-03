"""
BalloonCommands.py 

This file contains all of the commands that can be sent to the 
balloon module from the ground station software.

"""

from datetime import datetime

NOTHING = ''
RADIO_TEST = "RADIO_TEST"
CHANGE_TRANSMISSION_RATE = "CHANGE_TRANSMISSION_RATE"
SWITCH_RELAYS = "SWITCH_RELAYS"
CUTDOWN = "CUTDOWN"
RESET = "RESET"

ALL_COMMANDS = [
    RADIO_TEST,
    CHANGE_TRANSMISSION_RATE,
    SWITCH_RELAYS,
    CUTDOWN,
    RESET
]

COMMAND_INDICES = {
    NOTHING : 0, 
    RADIO_TEST : 1,
    CHANGE_TRANSMISSION_RATE : 7,
    SWITCH_RELAYS : 3,
    CUTDOWN : 9,
    RESET : 5
}

YES = "YES"
ON = "ON"
OFF = "OFF"

COMMAND_LOG_PATH = "balloon_commands.txt"

def getCommands():
    """
    Get the command we wish to send to the balloon payload from the user.
    Once a command is received, it is logged into a file for retrieval
    by the program operating the radio.

    :return: (None)
    """

    fileHandle = open(COMMAND_LOG_PATH, 'a')
    fileHandle.write("\nNew command session: " + str(datetime.now()) + '\n')
    fileHandle.write(" \n")
    fileHandle.close()

    print("Type a command to send to the balloon module\n")

    while True:

        command = raw_input(">>> ")
        commandParts = command.split()

        # Check if we want to quit the program
        if command == "QUIT":
            break

        # Check if we just pressed enter
        if command == "":
            continue

        # The command is not in our list 
        if not (commandParts[0] in ALL_COMMANDS):
            print("Unrecognized command")
            continue

        # Check if the given command meets its own requirements
        if not parseCommand(command):
            continue

        # Save the command to the command log file, if really desired
        sendCommand = raw_input("Send Command \"" + command + "\"? ")
        if sendCommand == YES:
            fileHandle = open(COMMAND_LOG_PATH, 'a')
            fileHandle.write(command)
            fileHandle.write('\n')
            fileHandle.close()


def parseCommand(command):
    """
    Determines if a command string is a valid command. This function
    checks if the command is a really a command, and whether or
    not the command has the proper structure. 

    :return: (boolean) Whether or not the command is valid
    """
    commandParts = command.split()

    if commandParts[0] in [RADIO_TEST, CUTDOWN, RESET]:
        return True
    elif commandParts[0] == CHANGE_TRANSMISSION_RATE:

        try:
            newRate = int(commandParts[1])
            return True
        except:
            print("Invalid transmission rate")
            return False

    elif commandParts[0] == SWITCH_RELAYS:

        try:
            relay = int(commandParts[1])
            return True
        except:
            print("Invalid relay index")
            return False

    else:
        return False



if __name__ == '__main__':
    getCommands()

