# This file was made to handle the serial port and grab the data
# from Arduino board. File contains 2 functions: list_serial_ports and getData.
# First one lists all connected serial ports and second one is to grab the data
# from Arduino board.
import time as t

# Author: Kacper Kuczmarski 02.09.2022
# Molex Connected Enterprise Solutions Sp. z o.o.

import serial
import serial.tools.list_ports
import time

import settings

# Initial arduino
arduino = serial


# Get the list of serial ports (COM)
# This function returns 2 param
# one for the COM list with detail and one with COM name only
def list_serial_ports():
    ports = list(serial.tools.list_ports.comports())
    forlist = []
    comports = []
    for port in ports:
        try:
            forlist.append(str(port))
            comports.append(port.device)
        except AttributeError:
            print("\nThis utility requires that pyserial version 3.4 or greater is installed.")
    return forlist, comports


# Get the list of serial ports (COM) old unused one

# def getSerialports():
#    ports = ['COM%s' % (i + 1) for i in range(15)]
#    result = []
#    for port in ports:
#        try:
#            s = serial.Serial(port)
#            s.close()
#            result.append(port)
#        except (OSError, serial.SerialException):
#            pass
#    return result

# Get the data from data stream [ not my best code :( ]

#  ===================== OLD VERSION =====================
"""
# This function returns the data from arduino board
# It does not require any argument, because it connects to global variable, defined in main and this file
def getData(dataBytes=100, ardCommand='4\n'):
    global arduino

    # Data straight from read command
    s = []
    # Formatted data
    x = []
    # If this fails we have no communication
    try:
        # Read 1000 chars from serial, decode it and split
        print("Send command")
        arduino.write(ardCommand.encode())
        t.sleep(0.15)
        print("Try to read data")
        s = arduino.read(dataBytes)
        print(s)
        try:
            # Do we need that?
            s = s[2:]
        except:
            print("Serial Handle: Unable to cut readings (no data)")
            return 'Fail', 'Fail', 'Fail'
    except:
        print("Serial Handle: Unable to read the data")
        return 'Fail', 'Fail', 'Fail'

    print("Decode data")
    s = s.decode('UTF-8')
    print("Split data")
    x = s.split('\r\n')

    print(x)
    # Delete first and last element (perhaps corrupted)
    # If cannot delete the data return fails (something wrong with connection)
    try:
        del x[0]
        del x[len(x) - 1]
    except:
        print("Serial Handle: Unable to cut the data (no data)")
        return 'Fail', 'Fail', 'Fail'

    # Average data
    current = 0

    for i in range(0, len(x)):
        current = current + float(x[i])
    # Calculate the average
    try:
        current /= len(x)
        voltage = current * 50
        power = current * voltage
    except ZeroDivisionError:
        return 'Fail', 'Fail', 'Fail'

    # return data rounded to 2 decimal points
    return round(current, 2), round(voltage, 2), round(power, 2)
"""
def getData(samples=25, ardCommand='4\n'):
    global arduino
    c = 0
    try:
        # Read 1000 chars from serial, decode it and split
        print("Send command")
        arduino.write(ardCommand.encode())
        t.sleep(0.15)
        print("Try to read data")
        for i in range(samples):
            c = c + getOneSample()
        c = c/samples
        voltage = c * 50
        power = c * voltage
        return round(c, 2), round(voltage, 2), round(power, 2)
    except:
        print("Serial Handle: Unable to read the data")
        return 'Fail', 'Fail', 'Fail'


def sendData(message):
    global arduino

    message = message + '\n'
    try:
        arduino.write(message.encode())
    except AttributeError:
        print("SendData: Arduino not initialized")
    except:
        print("SendData: Arduino not connnected")
    # time.sleep(0.15)


# Connect to selected com port, arduino variable is global and used in main.py
def connectToComPort(comport):
    global arduino
    try:
        # init Serial communication with arduino
        arduino = serial.Serial(port=comport, baudrate=115200, timeout=0.7)
        print("connectToComPort: Connected to: " + comport)
    except serial.SerialException:
        print('connectToComPort: No COM communication! Select proper COM port!')


def getArdState():
    global arduino
    if arduino.in_waiting > 0:
        return arduino.readline()
    return b''


# close Arduino connection
def closeArd():
    global arduino
    arduino.close()


# Restart Arduino and write command '3' to Arduino - go to start position
def restartArdandGoBack():
    global arduino
    # previous com port is unused in this case
    # restartArd()
    # time.sleep(1)
    sendData('3')
    # t.sleep(0.15)


# Get currently used COM port and reconnect Arduino
def restartArd(COMport):
    global arduino
    # previous com port is unused in this case
    try:
        arduino.close()
        arduino = serial.Serial(port=COMport, baudrate=115200, timeout=0.7)
        t.sleep(0.15)
    except serial.SerialException:
        print("restartArd: Unable to restart, no COM communication!")
    except AttributeError:
        print("restartArd: Unable to restart, no initial communication!")


def getOneSample():
    sendData('8')
    while True:
        start = time.time()
        res = arduino.readline()
        end = time.time()
        if end-start > 1:
            return 99
        if not res == b'':
            break
        else:
            continue
    return float(res.removesuffix(b'\r\n'))

