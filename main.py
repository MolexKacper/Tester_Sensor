"""

 This program was made to test CoreSync Sensor
 The application has simple GUI. Results are presented in tabular and saved to the selected by user path.
 To see the results of the test, user needs to select proper device,
 then select correct COM port (with Arduino) - done automatically.


 Author: Kacper Kuczmarski 16.08.2022
 Consul: Mati
 Molex Connected Enterprise Solutions Sp. z o.o.

 ========= Dla nowego pracownika =========

 Jeżeli to czytasz znaczy że już tu nie pracuje. To jest okej - jestem w lepszym miejscu.
 Pozdrów prosze (jeżeli jeszcze pracują) Agatę, Stefana i Matiego ode mnie, będę bardzo wdzięczny.
 Kod, na który patrzysz zawiera sporo błędów oraz nie jest pisany zgodnie z ogólnie obowiązującymi normami.
 Wynika to z faktu, iż zaczynając pracę musiałem działać bez jakiejkolwiek pomocy, czy dokumentacji, natomiast
 kod w Pythonie z początku nie miał być główną częścią testera, a jedynie dodatkiem. Mam nadzieję, iż rozgryzanie
 tego co napisałem nie przyniesie Ci aż tak wielko bólu. Projekt dla gatewaya nazywa się 'pythonProject'.

 Powodzenia i owocnej pracy!

 ========= Dla nowego pracownika =========

"""

import tkinter
from tkinter.simpledialog import askstring
import sensortest

def main():
    operatorID = "test"
    while len(operatorID) < 4:
        operatorID = askstring('Logowanie', '\nPodaj proszę swoje imię i nazwisko\n\n').strip()
    mainAppTester = sensortest.TestDriver()
    sensortest.root.geometry("880x540")
    sensortest.root.title("CoreSync Tester")
    sensortest.root['background'] = '#3D3B3C'

    sensortest.root.mainloop()

    try:
        sensortest.root.protocol("WM_DELETE_WINDOW", mainAppTester.on_closing())
    except tkinter.TclError:
        pass

if __name__ == "__main__":
    main()

