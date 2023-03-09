# This file was made to handle coap protocol. I don't like this shit.
import logging
import struct

# Author: Kacper Kuczmarski 09.02.2022
# Molex Connected Enterprise Solutions Sp. z o.o.

from coapthon.client.helperclient import HelperClient
import os
from serialHandle import *
import socket
import cbor2


# This function for Drivers and Sensors return not only the model of tested device,
# but also serial number

def getModel(ipAdd, testedDevice):
    model = ''
    serialNum = ''
    res = 'No connection'

    try:
        name = cbor2.loads(getCoap(ipAdd, 'molex/actuators/', 'Str'))['e'][0]['n']
    except (TypeError, cbor2.CBORDecodeEOF):
        return 'not Found', 'not Found'

    match testedDevice:
        case 'Drivers':
            try:
                res = cbor2.loads(getCoap(ipAdd, 'molex/actuators/' + name + '/inventory', 'Str'))['e']
                model = res['model']
                serialNum = res['snum']
                print(res['snum'])
            except:
                return 'not Found', 'not Found'
        case _:
            model = 'not Driv'
            serialNum = 'not Driv'

    return model, serialNum


def getCoap(ipAdd, path, argType=''):
    # Connect to given ip address and path then return response
    port = 5683
    client = HelperClient(server=(ipAdd, port))
    response = client.get(path, timeout=3)
    client.stop()
    try:
        # Change it later (or dont)
        if argType == 'Str':
            # print("String mode")
            exitval = response.payload
        else:
            exitval = response
    except:
        exitval = '-1'
    return exitval


def ComTest(ipAdd, testedDevice, i=0):
    sensor = ''
    j = i
    print("ComTest: Start - " + ipAdd + testedDevice + str(i))
    try:
        names = cbor2.loads(getCoap(ipAdd, 'molex/sensors/', 'Str'))['e']
        for name in names:
            if 'PIR' in name['n']:
                sensor = name['n']
    except (TypeError, cbor2.CBORDecodeEOF):
        if j < 3:
            j += 1
            print("ComTest: Retrying (TypeError)" + str(i))
            r = ComTest(ipAdd, testedDevice, i)
            return r
        else:
            return 'Fail'
    match testedDevice:
        case 'Drivers':
            try:
                res = cbor2.loads(getCoap(ipAdd, 'molex/sensors/' + sensor + '/inventory', 'Str'))['e']
                if 'Sensor O/L' in res['model'] or 'AdvLIG' in res['model']:
                    return 'Pass'
            except (TypeError, cbor2.CBORDecodeEOF, KeyError):
                pass
        case _:
            return 'not Driver'
    if j < 3:
        j += 1
        print("ComTest: Retrying (other Error)" + str(j))
        ComTest(ipAdd, testedDevice, j)
    else:
        return 'Fail'


def getMac(ipAdd):
    try:
        return cbor2.loads(getCoap(ipAdd, 'molex/network/', 'Str'))['e']['mmac']
    except TypeError:
        return 'TypeError'


def putCoap(ipAdd, turnon):
    # ==== CoAP part ====
    port = 5683
    path = "molex/actuators"

    client = HelperClient(server=(ipAdd, port))
    response = client.get(path)
    print(response.pretty_print())

    # ct = {'content_type': defines.Content_types["application/link-format"]}
    # main payload 0%
    payload0proc = '\xa1ae\xaaduuidt2001-17-801f120cd7b3anod0.1_ColorLightauarbclecoloram\x00aa\x18dbca\nbpi\x00bvi\x19\x16Dbat\x00'
    # fifty %
    payload50proc = '\xa1ae\xaaduuidt2001-17-801f120cd7b3anod0.1_ColorLightauaKbclecoloram\x00aa\x18dbca\nbpi\x182bvi\x19\x16Dbat\x00'
    # eighty %
    payload80proc = '\xa1ae\xaaduuidt2001-17-801f120cd7b3anod0.1_ColorLightauaKbclecoloram\x00aa\x18dbca\nbpi\x18Pbvi\x19\x16Dbat\x00'
    # new
    payload80proc = '\xa1ae\xaaduuidt2001-17-fc0fe7668c65anod0.1_ColorLightauaKbclecoloram\x00aa\x18dbca\nbpi\x18dbvi\x19\n\x8cbat\x00'
    # another driver conflict
    payload80proc = '\xa1ae\x81\xa9duuidt2003-17-fc0fe7668c6aannd0.3_MonoLightaubNAbclecoloram\x00aa\x18dbca\nbpi\x18dbbat\x19\x0b\xb8'

    if turnon == True:
        response = client.put(path, payload80proc, timeout=1)
    else:
        response = client.put(path, payload0proc, timeout=1)
    response = client.discover()
    location_path = response.location_path
    print(response.pretty_print())

    client.stop()


def send_multicast():
    host_ip = socket.gethostbyname(socket.gethostname()).strip()
    print(host_ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host_ip, 9761))

    msg = f'server/address/{host_ip}'
    sock.sendto(str.encode(msg), ('224.0.0.22', 55234))
    sock.sendto(str.encode(msg), ('239.0.0.255', 55234))


def send_gateway_reset(ipAdd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = 'fw/reset'
    #msg ='/fw/lcr/set/control/0'
    msg = str.encode(msg)
    try:
        response = sock.sendto(msg, (ipAdd, 9760))  # Send message to each of the switch's ports
        print(response)
    except:
        print("Failed to reset " + ipAdd)
    sock.close()


def set_dimming_level(ipAdd, dimValue):
    print(f"Setting Dim Level {dimValue} for ip Address: " + ipAdd)
    ipAdd = ipAdd.strip()
    # ==== CoAP part ====
    port = 5683
    path = "molex/actuators"

    client = HelperClient(server=(ipAdd, port))

    # Set the dimming Level
    dim_set = cbor2.dumps(
        {u'e':
            {
                u'pi': dimValue,
               # u'vi': 30000,
                u'at': 1}}
    )
    try:
        client.put(path, dim_set, timeout=2)
    except Exception as e:
        print("Error put coap: " + e.__str__())
    # Set the dimming Level for dual
    # dim_set = cbor2.dumps(
    #    {u'e':
    #        {
    #            u'vi': 2700}}
    # )

    # client.put(path, dim_set, timeout=5)
    try:
        client.stop()
    except Exception as e:
        print("Error put coap: " + e.__class__.__name__)

def set_sensor_color(ipAdd, color):
    """

    :param ipAdd: IP Address of CoreSync Gateway
    :param color: String - "R", "G", "B", "W" to choose or hex can be input
    :return:
    """
    print(f"Setting color {color} for ip Address: " + ipAdd)
    ipAdd = ipAdd.strip()
    # ==== CoAP part ====
    port = 5683
    path = "molex/actuators/d0.2_RGB"

    client = HelperClient(server=(ipAdd, port))
    try:
        color = color.lower()
    except AttributeError:
        pass
    match color:
        case "r":
            colorHex = 0xFF000000
        case "g":
            colorHex = 0x00FF0000
        case "b":
            colorHex = 0x0000FF00
        case "w":
            colorHex = 0xFFFFFF00
        case _:
            colorHex = color

    # Set the dimming Level
    dim_set = cbor2.dumps(
        {u'e':
            {
                u'pi': 100,
                u'vi': colorHex,
                u'at': 1}}
    )
    try:
        client.put(path, dim_set, timeout=2)
    except Exception as e:
        print("Error put coap: " + e.__str__())


# ============================================
# ============== Testing module ==============
# ============================================

#send_gateway_reset('192.168.0.188')
send_multicast()
#[s,m] = getModel('192.168.0.188', 'Drivers')
#set_dimming_level('192.168.0.188', 100)
"""
prevres = ""
while True:
    #send_multicast()
    try:
        name = cbor2.loads(getCoap('192.168.0.188', 'molex/actuators/', 'Str'))['e'][0]['n']
        #print(name)
        res = cbor2.loads(getCoap('192.168.0.188', 'molex/actuators/' + name + '/inventory', 'Str'))['e']['snum']
    except cbor2.CBORDecodeEOF:
        pass
    #print(res)
    if not res == prevres:
        print("Device Changed from: " + prevres + "to: " + res)
    prevres = res
"""
#print(s)
#print(m)
#himom = comTest('192.168.0.199', 'Drivers')
#print(himom)
#print(getCoap('192.168.0.195', 'molex/network/', 'Str'))
#set_dimming_level('192.168.0.199', 0)
#model = cbor2.loads(getCoap('192.168.0.195', 'molex/sensors/', 'Str'))['e'][3]['n']
#print(model) # Dual values
#while True:
#    move = cbor2.loads(getCoap('192.168.0.195', 'molex/sensors/d0.5_PIR/', 'Str'))['e']['bv']
#    if move == 0:
#        print("no motion") # Dual values
#    else:
#        print("movement detected")

#set_sensor_color('192.168.0.195', 0xffffff00)
#model = cbor2.loads(getCoap('192.168.0.195', 'molex/actuators/d0.2_RGB', 'Str'))['e']
#print(model)
#send_gateway_reset('192.168.0.196')
#putCoap('192.168.0.196', True)
#print(getCoap('192.168.0.196', "molex/actuators/d0.1_ColorLight", 'Str'))
#[mod, ser] = getModel('192.168.0.102', 'Drivers')
#print(mod + "  " + ser)
#print(cbor2.loads(getCoap('192.168.0.196', "molex/actuators")))
# print(getCoap('192.168.0.196', "molex/actuators/"))
# dim_level = resource_CV_DIM.payload
# power_temp = cbor2.loads(resource_CV_power.payload)["e"]["vi"]
