import tkinter as tk
import threading
from tkinter import font
from pynput import keyboard
import queue
import time
import random
import os

root = tk.Tk() # tworzenie okna głównego programu
root.title("Test Szybkiego Pisania")
accuracyNEW = tk.StringVar()
accuracyNEW.set(0)
newword=tk.StringVar()
newword.set("start")
trackedword=tk.StringVar()
trackedword.set("")
trackword=""
que = queue.Queue()
result = 0
word=""
end=0
c = 0
tab=[]
getstartedonce = 0
indexword=0
Height = 600
Width = 800
fonts=font.families()
words = open("slownik.txt")
data = words.readlines()
data = [data[x][:-1] for x in range(len(data))]

class Losowanie(threading.Thread):
    def __init__(self, time_left, words, accuracy, numberOfLetters):
        threading.Thread.__init__(self)
        self.time_left = time_left
        self.words = words
        self.accuracy = accuracy
        self.numberOfLetters = numberOfLetters
        self.listOfWords = []
        self.one_second = 0
        self.seconds = 1
        self.wordsPerSecond = 0
        self.wordsPerMinute = 0
        self.value = 0

    def accuracyCalc(self, letter):
        #calculating accuracy
        if letter:
            self.accuracy += 1
            self.numberOfLetters += 1
        else:
            self.numberOfLetters += 1
        return round(self.accuracy / self.numberOfLetters * 100)

    def wordCount(self):
        #adding words per second
        self.wordsPerSecond += 1

    def wordCalc(self):
        #calculating words per minute
        self.wordsPerMinute += self.wordsPerSecond
        self.wordsPerSecond = 0
        self.value =  round((self.wordsPerMinute / self.seconds) * 60)

    def timer(self):
        #calculate time left
        while self.time_left != 0:
            time.sleep(1)
            self.time_left -= 1
            self.seconds += 1

    def randomWords(self):
        #Choose random word from list of words
        #at the same time checking if word has repeated
        while True:
            newWord = self.words[random.randint(0, 999)]
            if newWord in self.listOfWords:
                pass
            else:
                self.listOfWords.append(newWord)
                break
        return newWord

class Widgets():#class for creating a objects like timer ect.
    def __init__(self,window,relw,relh,relx,rely):
        self.the_frame = tk.Frame(window)
        self.the_frame.place(relwidth=relw,relheight=relh,relx=relx,rely=rely)

    def labelTimer(self):   #printing Timer
        global end, accuracyNEW
        self.labelt = tk.Label(root, text=str(test.time_left)+" s",font=(fonts[90],36))
        self.labelt.place(relwidth=0.15, relheight=0.1, relx=0.2, rely=0.05)
        if(test.time_left<=10):
            self.lesstime()
            if(test.time_left==0):
                if(end==0):
                    framewords.endGame()
                    end=1
        self.labelt.after(1000, self.labelTimer)

    def labelAccuracy(self): #printing Accuracy
        global accuracyNEW
        self.label = tk.Label(root, textvariable=str(accuracyNEW),font=(fonts[90],36))
        self.label.place(relwidth=0.15, relheight=0.1, relx=0.42, rely=0.05)

    def labelCountWords(self):  #printing CountWords
        if test.time_left != 0:
            test.wordCalc()
            self.label = tk.Label(root, text=str(test.value)+" wpm",font=(fonts[90],30))
            self.label.place(relwidth=0.25, relheight=0.1, relx=0.65, rely=0.05)
            self.label.after(1000, self.labelCountWords)

    def printWord(self): #printing introduce word
        global trackedword
        self.labelw = tk.Label(root, textvariable=trackedword,font=(fonts[90],36))
        self.labelw.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.7)

    def wordToGreen(self):
        self.labelw.configure(fg="green")   #change introduce word to green

    def reverse(self):
        self.labelw.configure(fg="black")   #change introduce word to black

    def lesstime(self):
        self.labelt.configure(fg="red")     #change timer color to red

    def resetButton(self):
        
        self.reset = tk.Button(root, text="Restart", fg="black", activeforeground="#33ccff",command=self.Restart ,bd=0,font=(fonts[90],24))
        self.reset.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.37)
    
    def Restart(self):
        global accuracyNEW,c,word,trackedword,tab,end,indexword
        end=0
        trackedword.set("")
        accuracyNEW.set(0)
        test.value=0
        test.seconds = 1
        test.wordsPerSecond = 0
        test.wordsPerMinute = 0
        test.accuracy = 0
        test.numberOfLetters = 0
        c=0
        tab=[]
        indexword=0
        test.time_left=60
        test.listOfWords=[]
        word="start"
        self.labelCountWords()
        t.change()
        self.reset.destroy()
        self.labelAc.destroy()
        self.labelCw.destroy()
        self.labelAcr.destroy()
        self.labelCwr.destroy()

    def on_closing(self):   #close the root window
        test.time_left=0
        test.var = False
        root.destroy()
        os._exit(0)

    def endGame(self):
        self.resetButton()
        global accuracyNEW
        self.maxAccuracy=0
        self.maxCountWord=0
        self.avgAccuracy=0
        self.avgCountWords=0
        self.res=open("results.txt", "a+")#reading saved results in file
        self.res.seek(0)
        self.Results=self.res.readlines()
        for i in range(len(self.Results)):
            self.Results[i]=self.Results[i][:-1].split()
        for i in range(len(self.Results)):
            self.avgAccuracy=self.avgAccuracy+int(self.Results[i][0])#Adding Accuracy scores
            if(int(self.Results[i][0])>self.maxAccuracy):#Looking for max in Accuracy
                self.maxAccuracy=int(self.Results[i][0])
            self.avgCountWords=self.avgCountWords+int(self.Results[i][1])#Adding CountWords scores
            if(int(self.Results[i][1])>self.maxCountWord):#Looking for max in CountWords
                self.maxCountWord=int(self.Results[i][1])
        if((len(self.Results)>1)):
            self.avgAccuracy=round(self.avgAccuracy/(len(self.Results)-1))#Calculating round average Accuracy
            self.avgCountWords=round(self.avgCountWords/(len(self.Results)-1))#Calculating round average Count Words
        self.res.close()
        self.labelAc = tk.Label(root, text="Average Accuracy: "+str(self.avgAccuracy)+" %",font=(fonts[90],12)) #Creating label for average Accuracy
        self.labelAc.place(relwidth=0.25, relheight=0.1, relx=0.37, rely=0.15)  #show average Accuracy label
        self.labelCw = tk.Label(root, text="Average WPM: "+str(self.avgCountWords),font=(fonts[90],12)) #Creating label for average CountWords
        self.labelCw.place(relwidth=0.3, relheight=0.1, relx=0.63, rely=0.15)   #show average CountWords label
        if(self.maxAccuracy<int(accuracyNEW.get())):    #Checking is it new results of Accuracy highest than max in file
            self.labelAcr = tk.Label(root, text="New Record!",font=(fonts[90],12),fg="green")   #Creating label for information of record Accuracy
            self.labelAcr.place(relwidth=0.25, relheight=0.03, relx=0.37, rely=0.25)    #show label with information about record
        if(self.maxCountWord<test.value):   #Checking is it new results of CountWords highest than max in file
            self.labelCwr = tk.Label(root, text="New Record!",font=(fonts[90],12),fg="green")   #Creating label for information of record CountWords
            self.labelCwr.place(relwidth=0.25, relheight=0.03, relx=0.66, rely=0.25)    #show label with information about record
        self.avgResults()

    def avgResults(self):
        global accuracyNEW
        newword.set("End")  #Print  end when time expire
        trackedword.set("")
        self.res=open("results.txt", "a")
        self.accuracyRes=accuracyNEW.get()
        self.res.write(str(self.accuracyRes)+" "+str(test.value)+"\n")  #saveing new scores
        self.res.close()

#Class for changeing and printing words
class Wordchange():
    def __init__(self, window): #creating label for writting word
        global word, newword
        self.window=window
        self.label = tk.Label(window, textvariable=newword,font=(fonts[90],36),fg="red")
        self.label.place(relwidth= 0.5, relheight=0.11, relx=0.25,rely=0.55)

    def equalword(self):    #Check if words are the same and rand new word
        global indexword,framewords,tab,trackword,word
        if(trackword==word):
            threading.Thread(target=test.wordCount).start() #rand new word
            word=test.randomWords()
            indexword=0
            tab=[]  #clearing list
            self.change()   #change required word
            framewords.wordToGreen()    #change color of word on green
    def skipword(self): #Skipping word to new
        global indexword,tab,word
        word=test.randomWords()
        indexword=0
        tab=[]
        trackedword.set("")
        self.change()
    def change(self):#function to required word
        global word,newword
        newword.set(word)

#main program
def on_press(key):
        if test.time_left == 0:#End of running
            pass
        else:
            global c, indexword, trackword, word, tab
            if c == 0:
                threading.Thread(target=test.timer).start()
                threading.Thread(target=test.wordCalc).start()
                c += 1
            try:
                framewords.reverse()
                if(indexword<=(len(word)-1)): #checking if index is less than word lenght
                    if(type(key.char) == str):
                        tab.append(key.char)# adding leeter to list
                        trackword="".join(tab)
                        trackedword.set(trackword)
                        if(tab[indexword]==word[indexword]): # chcecking if letter in tab is same like in word 
                            threading.Thread(target=lambda q, arg1: q.put(test.accuracyCalc(arg1)), args=(que, 1,)).start()
                            result = que.get()
                            accuracyNEW.set(result)
                            frameproc.labelAccuracy()
                            indexword=indexword+1
                        else:
                            threading.Thread(target=lambda q, arg1: q.put(test.accuracyCalc(arg1)), args=(que, 0,)).start()
                            result = que.get()
                            accuracyNEW.set(result)
                            frameproc.labelAccuracy()
            except AttributeError:
                if(len(tab)>=1): #checking is len word longest than 0
                    if(key == keyboard.Key.backspace):
                        tab.pop()#deleting last letter in list
                        trackword="".join(tab)
                        trackedword.set(trackword)
                        if(indexword>0):
                            indexword=indexword-1
                if(key == keyboard.Key.space or key == keyboard.Key.enter):
                    t.skipword()
            t.equalword()

def on_release(key): #waiting for esc to stop listener
    if key == keyboard.Key.esc:
        test.time_left = 0
        # Stop listener
        return False

def getstarted(): #Start listen a keyboard
    global word
    word="start"
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()
#Gui code
test = Losowanie(60, data, 0, 0)
t=Wordchange(root)
canvas = tk.Canvas(root, height=Height, width=Width )
canvas.pack()
framespeed=Widgets(root,relw=0.3,relh=0.2,relx=0.05,rely=0.075)#Creating a gui frame
frametime=Widgets(root,relw=0.3,relh=0.2,relx=0.35,rely=0.075)
frameproc=Widgets(root,relw=0.3,relh=0.2,relx=0.65,rely=0.075)
framewords=Widgets(root,relw=0.8,relh=0.11,relx=0.1,rely=0.55)
gui=Wordchange(root)
frametime.labelTimer()
frameproc.labelAccuracy()
framespeed.labelCountWords()
framewords.printWord()
root.protocol("WM_DELETE_WINDOW", framewords.on_closing)
threading.Thread(target=getstarted).start()

root.mainloop()