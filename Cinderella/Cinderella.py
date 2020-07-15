import subprocess
import sys
from datetime import datetime, date
from reportlab.lib.colors import red, blue, black
from reportlab.pdfgen import canvas
from kivy.app import App
from kivy.lang import Builder  # Builder for kv file(s)
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from reportlab.lib.pagesizes import letter, A4

Window.maximize()

kv = Builder.load_file('windows.kv')  # Reads my kv file


class RoomsListSpinner(Spinner):
    pass


# class LoginWindow(Screen):
#     userName = ObjectProperty(None)
#     password = ObjectProperty(None)
#
#     def loginButton(self):
#         if self.userName.text.lower() == "" and self.password.text == "":
#             self.reset()
#             sm.current = "main"
#         else:
#             loginError()
#             self.reset()
#
#     def reset(self):
#         self.userName.text = ""
#         self.password.text = ""


class MainWindow(Screen):
    pass


stays = []
checkouts = []


class roomsListWindow(Screen):

    def addBlank(self, text):
        if checkouts.__contains__(text):
            checkouts.remove(text)
        if stays.__contains__(text):
            stays.remove(text)

    def addToStays(self, text):
        for checkout in checkouts:
            if checkout == text:
                checkouts.remove(text)
        stays.append(text)

    def addToCheckouts(self, text):
        for stay in stays:
            if stay == text:
                stays.remove(text)
        checkouts.append(text)

    def getStays(self):
        stays.sort()

    def getCheckouts(self):
        checkouts.sort()

    def printHKNumber(self, text):
        now = datetime.now()
        now = now.strftime("%m_%d_%Y-%H_%M_%S")
        # print(str(now))
        outputDoc = canvas.Canvas("Cinderella_" + str(now) + ".pdf", pagesize=letter)
        outputDoc.setAuthor("Edsandro de Oliveira")
        outputDoc.setTitle("Housekeeping Report - Cinderella")
        outputDoc.setFont("Times-Roman", 12)
        outputDoc.setSubject("Alternative Solution's Project")
        staysFinal = []
        checkoutsFinal = []
        hkVar = str
        i = int
        i = 0
        j = int
        j = 0
        k = int
        k = 0
        housekeepers = int(text)
        a = (len(stays))
        b = (len(checkouts))
        x = a + b
        n = housekeepers
        z = stays + checkouts
        z.sort()
        result = self.split(x, n)
        removeList = [0]
        # print("Stays: ", end=" ")
        # print(stays)
        # print("Checkouts:: ", end=" ")
        # print(checkouts)
        # print(housekeepers)
        # print(result)
        # print(z)
        if result == [-1] and len(z) != 0:
            msg = "You have more housekeepers than rooms. Please consider one housekeeper per room and dismiss the surplus for the day."
            print(msg)
            popup = Popup(title='FILE IS OPEN',
                          content=Label(text=msg),
                          size_hint=(None, None), size=(900, 400))
            popup.open()
        elif len(z) != 0:
            final = [[0 for x in range(len(z))] for y in range(housekeepers)]
            while i < housekeepers:
                # print("Housekeeper " + str(i + 1) + ":")
                hkVar = "Housekeeper " + str(i + 1) + ":"
                j = 0
                while j < result[i]:
                    if z[k] != 0:
                        final[i][j] = z[k]
                    # print(z[k])
                    k += 1
                    j += 1
                i += 1
            for subList in final:
                for delVar in (0, -1):
                    while subList and subList[delVar] == 0:
                        subList.pop(delVar)
            # print(final)
            try:
                opX = 30
                opY = 750
                i = 0
                for subList in final:
                    if len(subList)>22:
                        popup = Popup(title='TOO MUCH',
                                      content=Label(text='Under Specifications: No housekeeper can handle more than 22 rooms'),
                                      size_hint=(None, None), size=(800, 400))
                        popup.open()
                    rsX = 80
                    outputDoc.setFillColor(black)
                    outputDoc.drawString(opX, opY, "HK # " + str(i + 1) + ": | ")
                    for element in range(len(subList)):
                        if stays.__contains__(subList[element]):
                            print(str(element))
                            outputDoc.setFillColor(blue)
                            outputDoc.drawString(rsX, opY, subList[element] + " | ")
                        else:
                            outputDoc.setFillColor(red)
                            outputDoc.drawString(rsX, opY, subList[element] + " | ")
                        rsX += 24.5
                    i += 1
                    opY -= 30
                opY -= 15
                rsX = 30
                outputDoc.setFillColor(blue)
                outputDoc.drawString(rsX, opY, "STAYING")
                rsX += 60
                outputDoc.setFillColor(red)
                outputDoc.drawString(rsX, opY, "CHECKING OUT TODAY")
                outputDoc.showPage()
                outputDoc.save()
                subprocess.Popen(["Cinderella_" + str(now) + ".pdf"], shell=True)
            except IOError:
                popup = Popup(title='FILE IS OPEN',
                              content=Label(text='Please close the file before save a new report'),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
        else:
            msg = "Please select room(s) to be cleaned."
            # print(msg)
            popup = Popup(title='NO ROOMS SELECTED',
                          content=Label(text=msg),
                          size_hint=(None, None), size=(400, 400))
            popup.open()

    def close_window(self):
        sys.exit()

    def split(self, x, n):
        result = []
        if x < n:
            result.append(-1)
            # print(-1)
        elif x % n == 0:
            for i in range(n):
                result.append(x // n)
                # print(x // n, end=" ")
        else:
            zp = n - (x % n)
            pp = x // n
            for i in range(n):
                if i >= zp:
                    result.append(pp + 1)
                    # print(pp + 1, end=" ")
                else:
                    result.append(pp)
                    # print(pp, end=" ")
        return result


class HousekeepingReportWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# def loginError():
#     loginErrorPopup = Popup(title='Login Error', content=Label(text='Invalid username or password. Please try again.'),
#                             size_hint=(None, None), size=(400, 400))
#     loginErrorPopup.open()
#

sm = WindowManager()  # Creating the window manager #my Screen Manager

# screens = [LoginWindow(name="login"), MainWindow(name="main"), roomsListWindow(name='roomsList'),
#            HousekeepingReportWindow(name='hkReport')]  # Adding each screen to the WM

screens = [roomsListWindow(name='roomsList'),HousekeepingReportWindow(name='hkReport')]  # Adding each screen to the WM

for screen in screens:
    sm.add_widget(screen)

sm.current = "roomsList"  # Setting the initial screen to be shown


class Cinderella(App):
    def build(self):
        return sm


Cinderella().run()
