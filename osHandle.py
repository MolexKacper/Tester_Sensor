# This file was made to handle the os operations. It contains 3 functions:
# getWorkerID, getDate and getTime, which are self-explanatory.

# Author: Kacper Kuczmarski 09.02.2022
# Molex Connected Enterprise Solutions Sp. z o.o.

import os
from datetime import date
from datetime import datetime


# Get workerID from whoami command and return it
def getOperatorDateTime():
    worker = os.popen("whoami").read()
    today = date.today()
    d = today.strftime("%d-%m-%Y")
    now = datetime.now()
    dt = now.strftime("%H:%M:%S")
    return [worker, d, dt]

