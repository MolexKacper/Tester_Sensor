import csv
from os.path import exists
import serial


def serverSave(filepath, filename, data, macOrSerialNum_RowName_STR):
    filepath = filepath.replace('\n', '')
    filename = filename.replace('\n', '')
    if not (filepath.endswith("/") or filepath.endswith("\\")):
        filepath = "".join([filepath, "/"])
    print("csvHandle: trying to save to: " + filepath + filename)
    file_exists = exists(filepath + filename)
    if not file_exists:
        try:
            with open(filepath + filename, 'w+', newline='') as file:
                fieldnames = [macOrSerialNum_RowName_STR, 'Time', 'Date', 'Model', 'Worker ID', 'Current', 'Voltage',
                              'Power', 'COM Test']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(
                    {macOrSerialNum_RowName_STR: data[0], 'Time': data[1], 'Date': data[2], 'Model': data[3],
                     'Worker ID': data[4], 'Current': data[5], 'Voltage': data[6], 'Power': data[7],
                     'COM Test': data[8]})
            return 0
        except Exception as e:
            print("csvHandle: create new file unexpected error: " + e.__class__.__name__ + ": " + e.strerror)
            return -1
    else:
        try:
            with open(filepath + filename, 'a') as file:
                fieldnames = [macOrSerialNum_RowName_STR, 'Time', 'Date', 'Model', 'Worker ID', 'Current', 'Voltage',
                              'Power', 'COM Test']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(
                    {macOrSerialNum_RowName_STR: data[0], 'Time': data[1], 'Date': data[2], 'Model': data[3],
                     'Worker ID': data[4], 'Current': data[5], 'Voltage': data[6], 'Power': data[7],
                     'COM Test': data[8]})
            return 1
        except serial.SerialException:
            print("csvHandle: serial error")
            return -1
        except PermissionError:
            print("csvHandle: permission denied, close all Excel workbooks!")
            return -1

# dat = ['Test', 'czy', 'to', 'dzielo', 'dziala', 'hello', '1', '2', '3']
# errorserv = serverSave('W:\\MAC address test\\test\n', "test2.csv", dat, macOrSerialNum_RowName_STR='MAC Address')
# print(errorserv)
