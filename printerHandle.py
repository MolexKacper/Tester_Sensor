# This file was created to print given in argument BINARY MAC address
# on 3 peel-able labels. It has hardcoded ip address and port, so printer
# has to have static IP address.

import socket
import settings

def printZebra(macAdd=b""):
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.settimeout(2)
    # printer's ip (from setting.py)
    host = settings.getPrinterIP()
    print("Printer host IP: " + host)
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        # Byte Zebra code representation sent directly to printer
        #mysocket.send(b"^XA "
        #              b"^FO50,40^A0,40^FDMAC address^FS"
        #              b"^FO25,85^A0,40^FD" + macAdd + b"^FS"
        #              b"^FO390,40^A0,40^FDMAC address^FS"
        #              b"^FO360,85^A0,40^FD" + macAdd + b"^FS"
        #              b"^FO710,40^A0,40^FDMAC address^FS"
        #              b"^FO690,85^A0,40^FD" + macAdd + b"^FS"
        #              b"^XZ")  # using bytes
        # QR code variation - imo best one!
        #mysocket.send(b"^XA "  # starting point
        #              b'^MUd,600,600'
        #              b'^PR1,2,2'  # speed
                      #b'^MD3'  # media darkness (doesnt help)
        #              b'^FO155,40^A0,35^FDMAC Address^FS'
        #              b'^FO140,80^A0,35^FD'+macAdd+b'^FS'  # label
        #              b'^FO30,13^BQN,2,4^FD   '+macAdd+b'^FS'  # qr code
        #              b"^XZ")  # using bytes
        # new QR
        mysocket.send(b"^XA "  # starting point
                      b'^MUd,600,600'
                      b'^PR1,2,2'  # speed
                      # b'^MD3'  # media darkness (doesnt help)
                      b'^FO160,50^A0,25^FDMAC Address^FS'
                      b'^FO115,85^A0,32^FD' + macAdd + b'^FS'  # label
                      b'^FO40,35^BQN,2,3^FD   ' + macAdd + b'^FS'  # qr code
                      b"^XZ")  # using bytes
        # Anthony's example
        #mysocket.send(b"^XA "  # starting point
        #              b'^MUd,300,600'
        #              b'^PR1,2,2'  # speed
        #              #b'^MD3'  # media darkness (doesnt help)
        #              b'^BY1^FO70,30^BC,70,N,N,N,N'   # bar code settings
        #              b'^FDXX:XX:XX:XX:XX:XX^FS'  # label
        #              b'^CF0,20^FO75,105^FDMAC: XX:XX:XX:XX:XX:XX^FS'  # barcode
        #              b"^XZ")  # using bytes

        mysocket.close()  # closing connection
    except:
        print("Error with the printer's connection")


#printZebra(b'1A:2B:3C:4D:5E:6F')