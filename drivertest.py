import tkinter
import serial
import autosearch
import osHandle
import searchMolex
import serialHandle
import settings
import threading
import coap
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from csvHandle import serverSave
from printerHandle import printZebra
from functools import partial
from PIL import Image, ImageTk
import time as t

root = Tk()


class AppWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.startVarApp = False
        self.master = master

        # Style configuration of the window
        buttonStyle = ttk.Style()
        buttonStyle.theme_use("clam")
        buttonStyle.configure('W.TButton', font=("Malgun Gothic", 16), background='#9B9797', foreground='#1F1E1F')

        # Create settings window object
        self.settingsWindow = settings.AppSettings()
        # Get settings data from settings files
        self.settingsWindow.settingsVarSet()

        self.progindexNum = 0

        # Menu configuration
        self.menu = Menu(self.master)
        root.config(menu=self.menu)

        fileMenu = Menu(self.menu, tearoff=False)
        fileMenu.add_command(label="Settings", command=self.settingsWindow.run)
        fileMenu.add_separator()
        fileMenu.add_command(label="Print test label", command=partial(printZebra, b'01:02:03:04:05:06'))
        fileMenu.add_separator()
        # fileMenu.add_command(label="Exit", command=self.exitProgram)
        self.menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(self.menu, tearoff=False)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        # editMenu.add_command(label="Don't press me", command=mine)
        self.menu.add_cascade(label="Edit", menu=editMenu)

        searchMenu = Menu(self.menu, tearoff=False)
        searchMenu.add_command(label="Search", command=self.runSearchEngine)
        searchMenu.add_command(label="PlaceHolder")
        self.menu.add_cascade(label="Search", menu=searchMenu)

        helpMenu = Menu(self.menu, tearoff=False)
        helpMenu.add_command(label="About", command=self.helpPopup)
        self.menu.add_cascade(label="Help", menu=helpMenu)

        # ====== DYNAMIC Labels ======
        self.devLabel = StringVar()
        self.comLabel = StringVar()
        self.countLabel = StringVar()
        self.flashLabelString = StringVar()
        self.flashLabelString.set("Press 'Flash' button to start programming")
        self.countProgLabel = StringVar()
        self.countProgLabel.set("Flash counter: " + str(self.progindexNum))
        self.passLabelString = StringVar()
        self.passLabelString.set("Please insert first device!")

        self.passLabel = Label(root, textvariable=self.passLabelString, font=("Malgun Gothic Semilight", 25),
                               background='#3D3B3C', foreground='#E3E2DD')
        self.passLabel.place(x=225, y=158)
        # TESTED DEV
        ttk.Label(root, textvariable=self.devLabel, font=("Malgun Gothic Semilight", 17),
                  background='#3D3B3C', foreground='#E3E2DD').place(x=40, y=30)
        # COM
        ttk.Label(root, textvariable=self.comLabel, font=("Malgun Gothic Semilight", 17),
                  background='#3D3B3C', foreground='#E3E2DD').place(x=335, y=30)
        # COUNT TEST
        ttk.Label(root, textvariable=self.countLabel, font=("Malgun Gothic Semilight", 17),
                  background='#3D3B3C', foreground='#E3E2DD').place(x=40, y=90)

        # FLASH STATUS
        self.flashLabel = ttk.Label(root, textvariable=self.flashLabelString, font=("Malgun Gothic Semilight", 20),
                                    background='#3D3B3C', foreground='#E3E2DD')
        self.flashLabel.place(x=950, y=120)
        # COUNT PROG
        ttk.Label(root, textvariable=self.countProgLabel, font=("Malgun Gothic Semilight", 17),
                  background='#3D3B3C', foreground='#E3E2DD').place(x=950, y=240)

        # ====== STATIC Labels ======
        ttk.Label(root, text="Programming status:",
                  font=("Malgun Gothic Semilight", 25), background='#3D3B3C', foreground='#E3E2DD').place(x=950, y=30)
        space = ' '
        ttk.Separator(root).place(x=880, y=0, height=880, width=5, )
        self.footerLabel = ttk.Label(root,
                                     text=space * 40 + "Molex Connected Enterprise Solutions Sp. z o.o. ©"
                                                       " all rights reserved"
                                     , font=("Malgun Gothic Semilight", 12), background='#9B9797',
                                     foreground='#1F1E1F', width=200)
        self.footerLabel.place(relx=0, rely=0.92)

        # ====== Buttons ======
        butt1 = ttk.Button(root, text="Test", command=self.startTest, style='W.TButton')
        butt1.place(x=40, y=170)

        # Molex img
        self.img = Image.open("molexlogo.png")
        self.zoom = 0.2
        pixels_x, pixels_y = tuple([int(self.zoom * x) for x in self.img.size])
        self.img = ImageTk.PhotoImage(self.img.resize((pixels_x, pixels_y)))
        try:
            imgLabel = Label(root, image=self.img)
            imgLabel.photo = self.img
            imgLabel.place(x=630, y=30)
        except:
            print("Image file doesn't exist!")

        # ==== Table configuration ====
        # Another frame for table (is it really needed?)
        frame = Frame(root, width=500, height=0)
        frame.place(x=40, y=250)

        # Style configuration of the table
        style = ttk.Style(frame)
        style.theme_use("clam")
        style.configure("Treeview", background="#7F7979",
                        fieldbackground="#7F7979", foreground="white")

        self.listTab = ttk.Treeview(frame, height=8)
        self.listTab.pack()

        # Scrollbar for table
        vsb = ttk.Scrollbar(root, orient="vertical", command=self.listTab.yview)
        vsb.place(x=802, y=250, height=190)

        self.listTab.configure(yscrollcommand=vsb.set)

        self.listTab['columns'] = (
            'MAC/SNUM', 'Time Stamp', 'Date', 'Model', 'Worker ID', 'Current Test', 'Voltage Test', 'Power Test',
            'Com Test')

        self.listTab.column("#0", width=0, stretch=NO)
        self.listTab.column("MAC/SNUM", anchor=CENTER, width=120)
        self.listTab.column("Time Stamp", anchor=CENTER, width=80)
        self.listTab.column("Date", anchor=CENTER, width=80)
        self.listTab.column("Model", anchor=CENTER, width=80)
        self.listTab.column("Worker ID", anchor=CENTER, width=80)
        self.listTab.column("Current Test", anchor=CENTER, width=80)
        self.listTab.column("Voltage Test", anchor=CENTER, width=80)
        self.listTab.column("Power Test", anchor=CENTER, width=80)
        self.listTab.column("Com Test", anchor=CENTER, width=80)

        self.listTab.heading("#0", text="", anchor=CENTER)
        self.listTab.heading("MAC/SNUM", text="MAC/SNUM", anchor=CENTER)
        self.listTab.heading("Time Stamp", text="Time Stamp", anchor=CENTER)
        self.listTab.heading("Date", text='Date', anchor=CENTER)
        self.listTab.heading("Model", text='Model', anchor=CENTER)
        self.listTab.heading("Worker ID", text="Operator ID", anchor=CENTER)
        self.listTab.heading("Current Test", text="Current Test", anchor=CENTER)
        self.listTab.heading("Voltage Test", text="Voltage Test", anchor=CENTER)
        self.listTab.heading("Power Test", text="Power Test", anchor=CENTER)
        self.listTab.heading("Com Test", text="Com Test", anchor=CENTER)

    # def exitProgram(self):
    #    on_closing()

    def addToList(self, data, indexNum):
        self.listTab.insert(parent='', index='end', iid=indexNum, text='',
                            values=data)

    # def getTestedDev(self):
    #    return self.Combo.get()

    def runSearchEngine(self):
        searchMolex.searchCoreSync()

    def helpPopup(self):
        tkinter.messagebox.showinfo(title="Help", message="Molex CoreSync tester software version 1.0. "
                                                          "\nWritten and developed by Kacper Kuczmarski in Python. "
                                                          "\nAll rights reserved. "
                                                          "Only for internal use.\n\nAnno Domini 2022")

    def startTest(self):
        self.startVarApp = True


class TestDriver:
    """

    """

    # ============================
    # ======== Class init ========
    # ============================
    def __init__(self):
        # ===========================
        # ======== Variables ========
        # ===========================

        # Initialization of the window and main frame
        # Index number of Table
        self.isrunning = True
        self.app = AppWindow(root)
        self.settingsVar = self.app.settingsWindow
        self.indexNum = 0
        # Initial value of folder path
        self.folder_path = 'W:\\MAC address test\\python'
        # how many times dut was rejected
        self.gtfoiter = 0
        # how many times tester was restarted (for main timer)
        self.restartiter = 0
        # how many times test was performed (mainly for errors with serial connection)
        self.testiter = 0
        # the list of all tested serial numbers
        self.alltesteddevices = []
        # Variables for autotest
        self.autoDiscoveryIP = ''
        self.previousstate_nocon = True
        self.testStarted = False
        self.testpass = False
        # only for Drivers
        # For Driver's tester we have fixed ip add
        self.ipAdd = '192.168.0.188'
        self.DUTnames = {"ExtDrv1x350": 0.25,
                         "ExtDrv1x500": 0.4,
                         "ExtDrv1x700": 0.6,
                         "ExtDrv1x880": 0.7,
                         "ExtDrv1x1050": 0.9,
                         "ExtDrv1x1200": 1.1,
                         "ExtDrv1x1400": 1.25}
        print("Static ip Address of Gateway: " + self.ipAdd)

        # ====== TIMERS =======
        # this timer counts how much time does the test takes
        self.mainRestartTimer = threading.Timer
        self.arduinoTimer = threading.Thread(target=self.arduinoHandle)
        self.arduinoTimer.start()
        self.labelTimer = autosearch.RepeatTimer(1, self.LabelsUpdate)
        self.labelTimer.start()
        self.multicasttimer = autosearch.RepeatTimer(8, coap.send_multicast)
        self.multicasttimer.start()
        # self.timer2 = []
        # Run 255 threads to look for the ip at the same time
        # for i in range(100, 255):
        #    self.timer2.append(autosearch.RepeatTimer(0.5, self.auto_getIP, args=(i,)))
        #    self.timer2[i - 100].start()
        print("All timers initialized")

    # ========================================
    # ======== Main test for Drivers ========
    # ========================================
    def performTest(self):
        event = threading.Event()
        try:
            # Stop the timer
            self.mainRestartTimer.cancel()
            print("performTest: Timer has been stopped")
        except Exception as e:
            print("performTest: Timer was not defined. Error: " + e.__class__.__name__)

        #                 ====== Start test ======
        # ===================  Get init values ===================
        serialHandle.sendData('71')  # power on
        print("\n=========================\n====== POWER IS ON ======\n=========================\n")
        self.testStarted = True
        # Get current device name (from settings)
        testedDevice = self.settingsVar.currentDevice
        # init
        [current, voltage, power] = ['Fail', 'Fail', 'Fail']
        [model, serialNum] = ['not Found', 'not Found']
        i_mod = 0

        while [model, serialNum] == ['not Found', 'not Found']:
            # get model, returs 2 params (model and serial number), in gateways only one is used
            [model, serialNum] = coap.getModel(self.ipAdd, testedDevice)
            if i_mod > 5:
                break
            i_mod += 1
            event.wait(1)

        self.testpass = False

        # =================== Get init values ===================

        # look if there is already test for the device
        for s in self.alltesteddevices:
            if serialNum in s:
                self.gtfoiter += 1
                print("gtfo: " + str(self.gtfoiter))
                self.testStarted = False
                if self.gtfoiter > 3:
                    self.gtfoiter = 0
                    print("DUT already tested!")
                    DUTHandle = messagebox.askquestion("DUT already tested!",
                                                       "DUT already tested!\n\nDo you want to do the test anwyway?\nSerial Number:" + serialNum)
                    print(DUTHandle)
                    if DUTHandle == 'no':
                        self.changeStatusLabel('Please insert a new device')
                        self.testStarted = False
                        self.endoftest()
                        return
                    else:
                        break
                else:
                    self.performTest()
                    return

        self.alltesteddevices.append(serialNum)

        # get workerID, date and time from osHandle.py
        [operatorID, currDate, currTime] = osHandle.getOperatorDateTime()
        # try to reach device that is specified for communication test
        # comRes = coap.comTest(self.ipAdd, testedDevice)

        # main switch case
        match testedDevice:
            # Gateway option selected
            case 'Gateways':
                print("It is tester for Drivers")

            # Driver option selected
            case 'Drivers':
                print("Driver's tester start, Gateway's IP Address: " + self.ipAdd)

                current_correction = self.mos_test()
                print("current_correction: " + str(current_correction))
                if current_correction > 0.12:
                    print("MOS probably broken :( ")

                # No gateway found
                if self.ipAdd == '-1' or self.ipAdd == '' or \
                        coap.getCoap(self.ipAdd, 'molex/network', 'Str') == '-1':
                    tkinter.messagebox.showinfo(title="Testing Gateway", message='Gateway not found!')
                    self.testStarted = False
                    serialHandle.restartArdandGoBack()
                    self.endoftest()
                    return 0

                # Gateway found
                print("Gateway found, start")

                # Give it some time to stable
                #t.sleep(3)
                # Get data from arduino and save it to these variables
                # If it is a fail try to do it again (not the best solution)
                # After 3 trials return fail
                while [current, voltage, power] == ['Fail', 'Fail', 'Fail'] or current < 0.30:
                    threading.Thread(coap.set_dimming_level(self.ipAdd, 100)).run()
                    event.wait(0.3)
                    current = serialHandle.getOneSample() - current_correction
                    if current < 0:
                        current = -current
                    self.testiter += 1
                    print(self.testiter + current)
                    if self.testiter > 10:
                        self.testiter = 0
                        break
                self.testiter = 0

                dataTest = self.test(model, serialNum, current_correction)
                # Get the information if its fail or pass
                testResult = dataTest[0]
                # mos fail
                if dataTest[3] < 0:
                    dataTest[3] = "mos fail " + str(dataTest[3] + current_correction)
                # Set all data to one variable
                data = [dataTest[1], currTime, currDate, dataTest[2], operatorID,
                        dataTest[3], dataTest[4], dataTest[5], dataTest[6]]

                # If all these variables are fail it means we have no communication with arduino,
                # or something is wrong with it
                if not testResult == 'COMFail':
                    # Save the results to server
                    errorserv = serverSave(filepath=self.settingsVar.folder_path + '/',
                                           filename=currDate + 'Driver.csv',
                                           data=data, macOrSerialNum_RowName_STR='SeriaNum')
                    # No server communication - permission denied
                    if errorserv == -1:
                        tkinter.messagebox.showwarning(title="Testing Driver",
                                                       message="Test ended, file permission denied!"
                                                               "\nNo data stored on the server")
                    # Check test condition
                    if testResult == 'Fail':
                        print("Fail!")
                        self.testpass = False
                    else:
                        print("Test ended successfully")
                        self.testpass = True

                # restart this badass and return to base position
                try:
                    serialHandle.restartArdandGoBack()
                    print("Go back to the shadow!")
                except AttributeError:
                    tkinter.messagebox.showwarning(title="CoreSync Tester",
                                                   message="No communication with mainboard, can't return to base position!")

                # Print MAC Add (uncomment it later) - Zebra handle
                # printZebra(macAdd.encode())
                # printZebra(macAdd.encode())
                # Inserting data to the table
                self.app.addToList(data=data, indexNum=self.indexNum)
                # Increase the index of table
                self.indexNum += 1

            # Sensor option selected
            case 'Sensors':
                print("Tester only for Gateways")

            # ByPass option selected
            case 'ByPasses':
                tkinter.messagebox.showinfo(title="Testing ByPass", message="Placeholder for ByPasses")
            case 'Agatka':
                tkinter.messagebox.showinfo(title="Testing Mati", message="A Wild Golum Appears!")
                img2 = tkinter.PhotoImage(file="molex4.png")
                imgLabel = tkinter.Label(self.app, image=img2)
                imgLabel.img = img2
                imgLabel.place(relx=0.8, rely=0.2, anchor='center')

            # Default case (no device selected)
            case _:
                tkinter.messagebox.showinfo(title="No device selected!", message="Please select a device to test!")

        Tk.update(self=self.app)
        if self.testpass:
            self.changeStatusLabel('Pass', '#3b7', 60, True)
        else:
            self.changeStatusLabel('Fail', '#f00', 60, True)

        self.endoftest()
        self.testStarted = False

        # AUTO DISCOVER!!!!!!!!!!!!!!!!!!!!!!!!!!
        # It creates threads that are trying to reach addresses
        # One thread is responsible for one address, when CoreSync device respond test is started

    def mos_test(self, samples=10):
        current_correction = 0
        event = threading.Event()
        for x in range(samples-4):
            threadDim = threading.Thread(coap.set_dimming_level(self.ipAdd, 0))
            threadDim.run()
            current = serialHandle.getOneSample()
            if current < 0.2:
                break
            event.wait(0.3)
        for x in range(samples):
            current = serialHandle.getOneSample()
            current_correction += current
        current_correction /= samples
        return current_correction

    # ======================================
    # ======== Sub test for Drivers ========
    # ======================================
    def test(self, model, serialNum, current_correction):
        """

        :return: 1st - test result, others are for data of the test
        """
        # Get all data
        #[model, s] = coap.getModel(self.ipAdd, 'Drivers')
        [current, voltage, power] = serialHandle.getData()
        comRes = coap.ComTest(self.ipAdd, 'Drivers')
        current = round(current - current_correction, 2)
        if current < 0:
            current = -current
        print("=== CURR RESULT: " + str(current) + " ===")
        # If current is fail it means we have no communication with arduino,
        if current == 'Fail':
            print("Test ended, no COM communication!\nNo data stored on the server")
            return ['COMFail', serialNum, model, current, voltage, power, comRes]

        # Depending on model set current limits, if we can't find model set high limit
        try:
            currentLim = self.DUTnames[model]
        except KeyError:
            currentLim = 1000

        if current >= currentLim and comRes == 'Pass':
            print("drivertest: Pass")
            return ['Pass', serialNum, model, current, voltage, power, comRes]
        else:
            print("drivertest: Fail")
            return ['Fail', serialNum, model, current, voltage, power, comRes]

    # =======================================
    # ======== Function for IP timer ========
    # =======================================
    def auto_getIP(self, arg):
        try:
            # This is like multicast, so last digit is crucial
            # For now it is hardcoded
            resp = coap.getCoap('192.168.0.' + str(arg), '.well-known/core', 'Str')
            self.autoDiscoveryIP = '192.168.0.' + str(arg)
            if resp == '-1':
                self.autoDiscoveryIP = ''
        except:
            pass
        if not (self.autoDiscoveryIP == ''):
            print("Let's run test!: " + self.autoDiscoveryIP)
            self.performTest()

    # ===================================
    # ======== Test ending point ========
    # ===================================
    def endoftest(self):
        # END OF THE TEST
        event = threading.Event()
        self.gtfoiter = 0
        serialHandle.sendData('70')
        print("\n==========================\n====== POWER IS OFF ======\n==========================\n")
        try:
            # restart this badass and return to base position
            serialHandle.restartArdandGoBack()
            try:
                self.mainRestartTimer.cancel()
            except:
                print('endoftest: maintimer not defined')
                pass
            print("Go back to the shadow!")
            event.wait(7)
            self.changeStatusLabel("Please, insert a new device")
        except AttributeError:
            tkinter.messagebox.showwarning(title="CoreSync Tester",
                                           message="No communication with mainboard, can't return to base position!")

    # =======================================
    # ======== No connection handler ========
    # =======================================
    def noActLinkHandle(self):
        self.mainRestartTimer.cancel()

        print("time passed")
        self.restartiter += 1
        if self.restartiter > 2:
            print("Damaged DUT")

            self.restartiter = 0
            self.changeStatusLabel('Fail', '#f00', 60, True)
            self.endoftest()
        else:
            self.changeStatusLabel("Testing Device, reconnect (" + str(self.restartiter) + ")!")
            t.sleep(0.15)
            settings.backw()
            t.sleep(1.15)
            serialHandle.restartArd()

    # =================================
    # ======== Updating labels ========
    # =================================
    def LabelsUpdate(self):
        # Update all dynamic labels
        self.app.comLabel.set("COM port: " + self.settingsVar.currentComport)
        self.app.devLabel.set("Tested device: " + self.settingsVar.currentDevice)
        self.app.countLabel.set("Test counter: " + str(self.indexNum))
        self.app.countProgLabel.set("Flash counter: " + str(self.app.progindexNum))
        Tk.update(self=root)

    # ============================================
    # ======== communication with Arduino ========
    # ============================================
    def arduinoHandle(self):
        while self.isrunning:
            if self.app.startVarApp:
                self.performTest()
                self.app.startVarApp = False
            # Update "Testing device" label after arduino's command
            if not self.testStarted:
                try:
                    self.s = serialHandle.getArdState()
                    if not self.s == b'':
                        print(self.s)
                    if b'Stop!' in self.s:
                        self.noActLinkHandle()
                    if b'Start!' in self.s:
                        self.changeStatusLabel("Testing Device, please wait")
                        # Force update
                        Tk.update(self=root)
                        # TIMER if no communication after 60 seconds go back and restart arduino!
                        self.mainRestartTimer = threading.Timer(65, self.noActLinkHandle)
                        self.mainRestartTimer.start()
                        print("Main Timer is running!")
                        self.performTest()
                except serial.SerialException:
                    # if no communication try to restart
                    serialHandle.closeArd()
                    self.autocomconnection()
                    continue
                except AttributeError:
                    self.autocomconnection()
                    continue
                except Exception as e:
                    print("Unexpected error occurred: " + e.__class__.__name__ + e.__str__())
                    continue

    def autocomconnection(self):
        [l1, l2] = self.settingsVar.comRefresh()
        idports = None
        for idports, ports in enumerate(l1):
            if 'USB Serial Device' in ports or 'szeregowe USB' in ports:
                serialHandle.connectToComPort(l2[idports])
                self.settingsVar.currentComport = l2[idports]

    # ==========================================
    # ======== Main status label change ========
    # ==========================================
    def changeStatusLabel(self, text, textcolor='#3D3B3C', fontsize=30, ispassLabel=False):
        self.app.passLabelString.set(text)
        if ispassLabel:
            self.app.passLabel.configure(font=("Malgun Gothic Semilight", fontsize),
                                         background=textcolor, foreground='#E3E2DD')
            self.app.passLabel.place(x=330, y=110)
        else:
            self.app.passLabel.configure(font=("Malgun Gothic Semilight", fontsize),
                                         background=textcolor, foreground='#E3E2DD')
            self.app.passLabel.place(x=225, y=158)
        # Force update
        Tk.update(self=root)

    # ======================================
    # ======== App closing function ========
    # ======================================
    def on_closing(self):
        print('In the name of all Gods, close this application!')
        self.labelTimer.cancel()
        self.multicasttimer.cancel()
        self.isrunning = False
        try:
            self.mainRestartTimer.cancel()
        except TypeError:
            pass
        try:
            serialHandle.arduino.close()
        except AttributeError:
            pass
        print("All timers and connections are closed")
        self.app.destroy()
