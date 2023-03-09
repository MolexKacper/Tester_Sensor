#

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pickle

import osHandle
import serialHandle
import os

class AppSettings:
    def __init__(self):
        # Entry point for drop down list of options for com ports (ComboBox)
        # Get the list of com ports at the start point of the program
        self.indexNum = 0
        self.c1state = ""
        self.c2state = ""
        self.dataToSave = None
        self.vlistCom = []
        self.portlist = []
        self.mapping = {}
        self.currentComport = "COM4"
        self.previousComport = ""
        self.currentDevice = "Drivers"
        self.folder_path = "W:/MAC address test/def"
        self.mplab_path = "C:/Program Files/Microchip/MPLABX/v6.05/mplab_platform/mplab_ipe"
        self.hex_path = "C:/Users/kacpek1/TG2_T2.6.3.16.35.hex"
        self.printerIP = "192.168.0.100"
        self.projectpath = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        # Style configuration of the window
        buttonStyle2 = ttk.Style()
        buttonStyle2.configure('W.TButton', font=("Malgun Gothic", 16), background='#9B9797', foreground='#1F1E1F')

        # Initialization of the window and settings frame
        self.settingsRoot = Tk()
        self.settingsRoot.geometry("880x440")
        self.settingsRoot.title("CoreSync Tester - settings")
        self.settingsRoot.configure(background='#9B9797')

        # ====== Labels ======
        ttk.Label(self.settingsRoot, text="Tested device: ", font=("Malgun Gothic Semilight", 18), background='#9B9797',
                  foreground='#1F1E1F').place(x=40, y=30)
        ttk.Label(self.settingsRoot, text="COM port: ", font=("Malgun Gothic Semilight", 18), background='#9B9797',
                  foreground='#1F1E1F').place(x=40, y=90)
        ttk.Label(self.settingsRoot, text="Save file path: ", font=("Malgun Gothic Semilight", 18), background='#9B9797',
                  foreground='#1F1E1F').place(x=40, y=150)
        ttk.Label(self.settingsRoot, text="Manual steering: ", font=("Malgun Gothic Semilight", 18), background='#9B9797',
                  foreground='#1F1E1F').place(x=40, y=220)
        ttk.Label(self.settingsRoot, text="Printer's IP Address: ", font=("Malgun Gothic Semilight", 18),
                  background='#9B9797', foreground='#1F1E1F').place(x=40, y=330)

        seperatorwidth = 4
        ttk.Separator(self.settingsRoot).place(x=438, y=10, height=420, width=seperatorwidth + 2)
        ttk.Separator(self.settingsRoot).place(x=10, y=10, height=seperatorwidth, width=832)  # up
        ttk.Separator(self.settingsRoot).place(x=10, y=10, height=420, width=seperatorwidth)  # left
        ttk.Separator(self.settingsRoot).place(x=838, y=10, height=420, width=seperatorwidth)  # right
        ttk.Separator(self.settingsRoot).place(x=10, y=430, height=seperatorwidth, width=832)  # down

        # ====== Labels for programming ======
        ttk.Label(self.settingsRoot, text="Programming settings:", font=("Malgun Gothic Semilight", 18), background='#9B9797',
                  foreground='#1F1E1F').place(x=480, y=30)
        ttk.Label(self.settingsRoot, text="MPLAB IPE path: ", font=("Malgun Gothic Semilight", 18),
                  background='#9B9797', foreground='#1F1E1F').place(x=480, y=90)
        ttk.Label(self.settingsRoot, text="Hex file path: ", font=("Malgun Gothic Semilight", 18),
                  background='#9B9797', foreground='#1F1E1F').place(x=480, y=150)


        # ===== Check box =====
        self.c1 = ttk.Checkbutton(self.settingsRoot, text='Flash DUT')
        self.c1.state(['!alternate'])
        self.c1.state([self.c1state])
        self.c1.place(x=480, y=70)

        self.c2 = ttk.Checkbutton(self.settingsRoot, text='Print')
        self.c2.state(['!alternate'])
        self.c2.state([self.c2state])
        self.c2.place(x=40, y=400)

        # ==== ComboBox for Com ports ====
        self.ComCombo = ttk.Combobox(self.settingsRoot, state='readonly', font=("Malgun Gothic Semilight", 13),
                                background='#9B9797', foreground='#1F1E1F')
        if self.currentComport == '':
            self.ComCombo.set("COM9")
        else:
            self.ComCombo.set(self.currentComport)
        self.ComCombo.place(x=200, y=98)
        [self.vlistCom, self.portlist] = self.comRefresh()
        self.ComCombo['values'] = self.vlistCom

        #for i in range(len(self.portlist)):
        #    mapping[self.vlistCom[i]] = self.portlist[i]

        # Entry point for drop down list of options for device (ComboBox)
        self.vlist = ["Gateway", "Drivers", "Sensors", "Print"]
        self.Combo = ttk.Combobox(self.settingsRoot, values=self.vlist, font=("Malgun Gothic Semilight", 13), background='#9B9797',
                             foreground='#1F1E1F')
        self.Combo.set("Gateway")
        self.Combo.place(x=200, y=35)

        # ==== TextBoxes ====
        # Text for access path
        self.textPath = ttk.Entry(self.settingsRoot, width=40)
        self.textPath.insert(0, self.folder_path)
        self.textPath.place(x=42, y=192)
        # Text for printers ip
        self.textPrinterIP = ttk.Entry(self.settingsRoot, width=40)
        self.textPrinterIP.insert(0, self.printerIP)
        self.textPrinterIP.place(x=42, y=370)
        # Text for MPLAB IPE path
        self.textMplab = ttk.Entry(self.settingsRoot, width=40)
        self.textMplab.insert(0, self.mplab_path)
        self.textMplab.place(x=482, y=132)
        # Text for .hex file path
        self.textHex = ttk.Entry(self.settingsRoot, width=40)
        self.textHex.insert(0, self.hex_path)
        self.textHex.place(x=482, y=192)

        # ===== Buttons ======
        self.butt1 = ttk.Button(self.settingsRoot, text="Save and close", command=self.onClosing)
        self.butt1.place(x=480, y=368)
        # butt1.configure(bg='#9B9797')
        self.butt2 = ttk.Button(self.settingsRoot, text="...", width=4, command=lambda: self.browse_button('csv'), style='W.TButton')
        self.butt2.place(x=300, y=190)

        self.butt3 = ttk.Button(self.settingsRoot, text="Forward", command=lambda: serialHandle.sendData('1'), style='W.TButton')
        self.butt3.place(x=40, y=260)

        self.butt4 = ttk.Button(self.settingsRoot, text="Backward", command=lambda: serialHandle.sendData('2'), style='W.TButton')
        self.butt4.place(x=140, y=260)

        self.butt5 = ttk.Button(self.settingsRoot, text="Reset", command=lambda: serialHandle.restartArd(self.currentComport), style='W.TButton')
        self.butt5.place(x=40, y=300)

        self.butt6 = ttk.Button(self.settingsRoot, text="Start position", command=lambda: serialHandle.restartArdandGoBack(self.currentComport),
                           style='W.TButton')
        self.butt6.place(x=140, y=300)

        self.butt7 = ttk.Button(self.settingsRoot, text="Get Data", command=lambda: serialHandle.sendData('4'), style='W.TButton')
        self.butt7.place(x=240, y=260)

        self.butt8 = ttk.Button(self.settingsRoot, text="...", width=4, command=lambda: self.browse_button('mplab'), style='W.TButton')
        self.butt8.place(x=740, y=130)

        self.butt9 = ttk.Button(self.settingsRoot, text="...", width=4, command=lambda: self.browse_button('hex'), style='W.TButton')
        self.butt9.place(x=740, y=190)

        self.butt10 = ttk.Button(self.settingsRoot, text="Manual program", command=lambda: osHandle.programDUT(self.mplab_path, self.hex_path), style='W.TButton')
        self.butt10.place(x=480, y=230)

        self.butt11 = ttk.Button(self.settingsRoot, text="Lock/Unlock", command=lambda: serialHandle.sendData('6'), style='W.TButton')
        self.butt11.place(x=240, y=300)

        self.settingsRoot.mainloop()

    # This function is called when settings window is closing
    def onClosing(self):
            self.printerIP = self.textPrinterIP.get()
            self.folder_path = self.textPath.get()
            # Get current device name from combobox
            print(self.Combo.get())
            self.currentDevice = self.Combo.get()
            self.previousComport = self.currentComport
            # if some shit is inside get whatever is in (secure for initial value)
            #try:
            #    print("")
                # self.currentComport = mapping[self.ComCombo.get()]
            #except KeyError:
            #    self.currentComport = self.ComCombo.get()
            # if previous com port and current one are not equal, or it is initial val try to connect to new com port
            if not self.previousComport == self.currentComport or self.currentComport == "COM5":
                serialHandle.connectToComPort(self.currentComport)

            self.dataToSave = [self.printerIP, self.folder_path, self.c1.state(), self.hex_path, self.mplab_path, self.c2.state()]
            self.settingsVarSave()
            self.settingsVarSet()

            # kill window
            self.settingsRoot.destroy()

    def browse_button(self, buttonType):
        match buttonType:
            case "csv":
                print("CSV")
                self.folder_path = filedialog.askdirectory()
                # update text
                self.textPath.delete(0, END)
                self.textPath.insert(0, self.folder_path)
            case "hex":
                print("HEX")
                self.hex_path = filedialog.askopenfilename()
                print(self.hex_path)
                # update text
                self.textHex.delete(0, END)
                self.textHex.insert(0, self.hex_path)
            case "mplab":
                print("MPLAB")
                self.mplab_path = filedialog.askdirectory()
                # update text
                self.textMplab.delete(0, END)
                self.textMplab.insert(0, self.mplab_path)
            case _:
                print("browse handle: unknown argument!")


        self.settingsRoot.focus_force()

    # This function is used to refresh the list of com ports
    def comRefresh(self):
        [vlistCom, portlist] = serialHandle.list_serial_ports()
        return vlistCom, portlist

    # Open settings file where all data are stored and save it to the program variables
    def settingsVarSet(self):
        try:
            with open(self.projectpath + '\\' + "config.pickle", "rb") as file:
                print('opening')
                dataArr = pickle.load(file)
                dataArr = list(dataArr)
            if len(dataArr) <= 1:
                print("File is empty")
            else:
                [self.printerIP, self.folder_path, self.c1state, self.hex_path, self.mplab_path, self.c2state] = dataArr
        except FileNotFoundError:
            with open(self.projectpath + '\\' + "config.pickle", "xb") as file:
                print("Settings: File does not exist - creating one")
                pickle.dump([self.printerIP, self.folder_path, self.c1state, self.hex_path, self.mplab_path, self.c2state], file)  # Creating file with default array
        except pickle.UnpicklingError:
            with open(self.projectpath + '\\' + "config.pickle", "wb") as file:
                print("Settings: Unpickling error - creating new file")
                pickle.dump({}, file)  # Creating file with empty array
        except Exception as e:
            print("Settings: Unknown error occured: " + e.__class__.__name__ + ": " + e.__str__())

    def settingsVarSave(self, datatosave=[]):
        # we're saving from
        if self.dataToSave is None:
            self.dataToSave = datatosave
        for dataindex, data in enumerate(self.dataToSave):
            try:
                self.dataToSave[dataindex].strip()
            except AttributeError:
                self.dataToSave[dataindex] = ''.join(data)
        try:
            with open(self.projectpath + '\\' + "config.pickle", "wb") as file:
                print(self.dataToSave)
                pickle.dump(self.dataToSave, file)
                print("Settings: Config file saved")
        except PermissionError:
            print("Save Error: Permission denied")







