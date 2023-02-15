from checker import Checker
import os
from os.path import exists
import pickle
import threading

class Controller:
    def __init__(self, checkerThread):
        self.checker = checkerThread
        self.startNewThread = False
      

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
        custId = self.checker.getCustomerId()
        self.manageCredentials(username.get(), custId, saveCredentials)
        try:
            #Start the checker thread here
            if not self.startNewThread:
                self.checker.start()
            else:
                #create new thread and update references 
                self.checker = Checker(self.myView.getRoot())
                self.myView.setContestChecker(self.checker)
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

    
    def manageCredentials(self,username, custId, saveCredentials):  
    #save credentials or delte them based on user input 
    # not working in controller - maybe works only in non ui-thread     
        if saveCredentials:
            #save cookies 
            try:
                
                with open('cookies','wb') as f:
                    print("saving cookies ")
                    pickle.dump(self.checker.getCookies(), f)
                
                with open('user','w+') as f:
                    print("saving user file")
                    f.writelines([username+'\n', str(custId)])                    
                return 

            except Exception as e:
                print("exception writing files",e )                
                #shoud continue and remove cookie file if exception
        
        try:
            os.remove('cookies')
            os.remove('user')
        except:
            pass


    def userMatch(self, user1, user2):
        if user1.__eq__(user2):
            return True
        return False


    def retrieveSavedUser(self):
        username = ''
        if exists('user'):
            file = open('user', 'r')
            lines =  file.read().splitlines()
            username = lines[0]
            custId = lines[1]
            Checker.setCustomerId(custId) #not elegant
        return username


    def flagNewThread(self, flag):
        #start a new thread when button pressed
        self.startNewThread = flag
