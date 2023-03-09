# This file was created to handle autosearch timer and search in treeview (Tkinter table)


from threading import Timer
from tkinter import messagebox


def isDUTinTable(treeview, testedDevice, macOrSerial, gtfoiter):
    print("DUT:" + macOrSerial + ' iter ' + str(gtfoiter))
    # Sth wrong then reset this shit - it shouldn't be that high
    if gtfoiter > 15:
        return 'EOT'
    if macOrSerial == "" or macOrSerial =="TypeError":
        return 'yes'
    # look if there is already test for the device
    if search(treeview, macOrSerial) and testedDevice == 'Drivers':
        print('gtfo')
        if gtfoiter > 5:
            print("DUT already tested!")
            DUTHandle = messagebox.askquestion("DUT already tested!",
                                               "DUT already tested!\n\nDo you want to do the test anwyway?\nSerial Num:" + macOrSerial)
            print(DUTHandle)
            if DUTHandle == 'yes':
                return 'No'
            else:
                # end of test
                return 'EOT'
        else:
            return 'yes'
    return 'No'


# search in treeview, if item exists return true, otherwise false
def search(treeview, comparevalue):
    children = treeview.get_children('')
    for child in children:
        values = treeview.item(child, 'values')
        if comparevalue in values:
            return True
    return False


# This class can produce objects - threading timers
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)