import checker
import os
from os.path import exists
import pickle

class Controller:
    def __init__(self, checkerThread):
        self.checker = checkerThread
      

    def setView(self, view):
        self.myView = view

    def checkContests(self, username, login, savelogin):
        #check if session file exists and save login checkmark is set
        authSuccess = False
        saveCredentials = True if savelogin.get() == '1' else False

        if saveCredentials and exists('cookies') and self.userMatch(username.get(), self.retrieveSavedUser()):
            #conditions to load session matched - current username matches saved one
            authSuccess = self.loadSession()
        else:
            #auth from scratch
            authSuccess = self.auth(username.get(), login.get())            

        if not authSuccess:
            self.myView.showAuthError()
            return
            
        #save creds for future if user wants it
        self.manageCredentials(username.get(), saveCredentials)
        try:
            self.checker.start()
        except:
             self.myView.showAuthError()
        #thread can only be started once, need to change this?

    def loadSession(self):        
        print("previous cookie file found")
        try:
            with open('cookies', 'rb') as f:
                self.checker.setCookies(pickle.load(f))                
        except:
            return False
        return True
    
    def auth(self, username, password):
        return  self.checker.auth(username, password) #tkinter stringVar() to string.
     

    def manageCredentials(self,username, saveCredentials):  
        #save credentials or delte them based on user input      
        if saveCredentials:
            #save cookies 
            with open('cookies','wb') as f:
                pickle.dump(self.checker.getCookies(), f)
            with open('user','w') as f:
                f.write(username)

        try:
            os.remove('cookies')
            os.remove('user')
        except:
            pass
    
    def userMatch(user1, user2):
        if user1.__eq__(user2):
            return True
        return False

    def retrieveSavedUser(self):
        username = ''
        if exists('user'):
            file = open('user', 'r')
            username =  file.readline()

        return username
