from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter import ttk  # Carga ttk (para widgets nuevos 8.5+)

from checker import Checker
from controller import Controller
from contest import Contest
from contest_frame import Contest_Frame
from math import ceil, floor, sqrt
import webbrowser

class checkerUi:
    def __init__(self, root, controller, checker):
        root = root
        self.controller = controller
        self.controller.setView(self)
        self.checker = checker

        root.title("iRacing Contest Checker")

        login_frame = ttk.Frame(root, relief='sunken', padding="12 12 12 12")
        login_frame.grid(column=0, row=0, sticky=(N,W))

        footer_frame = ttk.Frame(root, padding="3 3 3 3")
        footer_frame.grid(column=0, row=1, rowspan=2, sticky=(N,W))

        self.results_frame = ttk.Frame(root, relief='sunken', width=400, height=400, padding="12 12 12 12")
        self.results_frame.grid(column=1, row=0, rowspan=2, sticky=(E,W))



        label_userName = ttk.Label(login_frame, text="iRacing Username")
        self.userName = StringVar()
        userName_entry = ttk.Entry(login_frame, width=35, textvariable = self.userName)

        label_password = ttk.Label(login_frame, text="iRacing Password")
        self.password = StringVar()
        password_entry = ttk.Entry(login_frame, width=35, textvariable = self.password, show = "*")

        self.saveCredentials = StringVar()
        saveCredentials_checkbox = ttk.Checkbutton(login_frame, text="Stay logged in", variable=self.saveCredentials)

        self.status = StringVar()
        self.status_label = ttk.Label(login_frame, textvariable= self.status)

        checkButton = ttk.Button(login_frame, text="Check Participation", command=self.checkContests)
        self.results = StringVar()
        self.results_label = ttk.Label(login_frame,textvariable = self.results)

        label_version = ttk.Label(footer_frame, text="Ver 0.1")
        label_disclaimer = ttk.Label(footer_frame, wraplength=340, justify="left", text="Participation data and contest draws might not be accurate. Not official in any way")
        #text_disclaimer = Text(footer_frame, wrap="word", width=60, height=2, state=DISABLED)
        #text_disclaimer.insert(INSERT, " Participation data and contest draws could not be accurate. Not official in any way")
        label_forums = ttk.Label(footer_frame, text="forums.iracing.com", foreground="blue", cursor="hand2")
        label_forums.bind("<Button-1>", lambda e: self.callback("http://forums.iracing.com/discussion/33370/season-1-2023-contests"))

        #login_frame grid----------------------------------------------------------------------------------
        label_userName.grid(            column=0, row=0, sticky=(N,W), pady=5)
        userName_entry.grid(            column=1, row=0, columnspan=2, sticky=(N,W), pady=5, padx=5)
        label_password.grid(            column=0, row=1, sticky=(N,W), pady=5)
        password_entry.grid(            column=1, row=1, columnspan=2, sticky=(N,W), pady=5, padx=5)
        saveCredentials_checkbox.grid(  column=2, row=2, sticky=(N,W))
        checkButton.grid(               column=1, row=3, sticky=(N,W), pady=10)
        self.status_label.grid(         column=0, row=4, columnspan=3, sticky=(N,W), pady=5)

        #footer_frame grid----------------------------------------------------------------------------------
        label_disclaimer.grid(          column=0, row=0, columnspan=2, pady=5)
        #text_disclaimer.grid(           column=0, row=0, columnspan=2)
        label_version.grid(             column=0, row=1, sticky=(S,W))
        label_forums.grid(              column=1, row=1, sticky=(S,E))


        self.retrieveSavedUser()
        userName_entry.focus()

    def retrieveSavedUser(self):
        savedUser = self.controller.retrieveSavedUser()
        if len(savedUser) > 1 :
            self.userName.set(savedUser)
            self.password.set("********")
            self.saveCredentials.set('1')

    def checkContests(self):
        self.controller.checkContests(self.userName, self.password, self.saveCredentials)

    #function called by event from checker thread
    def update(self, data):
        #status message for user
        self.status.set(self.checker.getStatus())

        #contest data
        contests =  self.checker.getContestList()
        if(contests):
            index = 0
            for  c in contests:
                #figure out row and column position based on the length of contest list
                column = self.squareGridCol(len(contests), index)
                row = self.squareGridRow(len(contests),index)

                cf = Contest_Frame(self.results_frame, c.name, 0, c.eligibleRaces, c.draws)
                cf.grid(column=column, row=row, padx=3, pady=3)              

                index = index +1



    def squareGridCol(self, length, index):
        columns= length/ceil(sqrt(length))     #make it square-ish
        column = index/(length/columns)         #find column this index goes in
        column = floor(column)
        return column

    def squareGridRow(self, length, index):
        columnSize = ceil(sqrt(length))
        return int(index-(columnSize*floor(index/columnSize)))


    def showAuthError(self):
        root.title("Authentication Error")
        message = "Authentication error, check username or password \n" + self.status.get()
        self.status.set(message)

    def callback(self, url):
        webbrowser.open_new(url)



#Main Loop

#Create UI
root = Tk()

#bind to event that will be called by checker thread
root.bind("<<Update>>", lambda event: ui.update(event,))
contestChecker = Checker(root)
myController = Controller(contestChecker)
ui = checkerUi(root, myController, contestChecker)

root.mainloop()