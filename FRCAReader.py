# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:17:33 2015

@author: RLSR
"""

from Tkinter import Tk, Label, Checkbutton, W, S, BooleanVar, Button
from Tkinter import StringVar, DISABLED, NORMAL
import tkFont
import os
from random import randint


class Logic:
    def __init__(self):
        self.quest_dir = os.path.join(os.path.dirname(__file__), 'resource')
        self.filenames = [f for f in os.listdir(self.quest_dir) 
            if os.path.isfile(os.path.join(self.quest_dir,f))]
    
    def chooseQuestion(self):
        f = self.filenames[randint(0, 1666)]
        return open(os.path.join(self.quest_dir, f), 'r')
        
    def parseQuestion(self, question):
        q = question.readlines()
        for l in q:
            if l == '':
                del q[l]
                print 'Line '+str(l)+'was empty and deleted from the question'
        answers = []
        for i in range(1, 6):
            answers.append(self.str2bool(q[i].split(',', 1)[0]))
            q[i] = q[i].split(',', 1)[1]
        return {'answers': answers, 'question': q}

    def prepareQuestion(self):
        q = self.chooseQuestion()
        d = self.parseQuestion(q)
#        for keys, values in d.items():
#            print str(keys)+': \n'+str(values)
        return d

    def str2bool(self, v):
        if str(v).lower() in ('true', 'True', '1'):
            return True
        else:
            return False
        

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.logic = Logic()
        self.text = self.logic.prepareQuestion()
        self.font = tkFont.Font(size=24)
        self.stmtvar = StringVar()
        self.stmtvar.set(self.text['question'][0])
        self.statement = Label(self, textvariable = self.stmtvar)
        self.statement.pack(anchor = W)
        self.checkbuttons = {}
        self.checkbtntext = {}
        self.checkbuttonvar = {}        
        for i in range(1, 6):
            self.checkbuttonvar[str(i)] = BooleanVar()
            self.checkbtntext[str(i)] = StringVar()
            self.checkbtntext[str(i)].set(self.text['question'][i])
            self.checkbuttons['question '+str(i)] = Checkbutton(self,
                              textvariable = self.checkbtntext[str(i)],
                              variable = self.checkbuttonvar[str(i)])
            self.checkbuttons['question '+str(i)].pack(anchor = W)
        self.buttonNext = Button(self, text = 'Next question',
                                 command = self.nextQuestion)
        self.buttonNext.pack(anchor = S)
        self.buttonAnswer = Button(self, text = 'Show answers',
                                 command = self.showAnswer)
        self.buttonAnswer.pack(anchor = S)

    def nextQuestion(self):
        self.text = self.logic.prepareQuestion()
        self.stmtvar.set(self.text['question'][0])        
        for i in range(1, 6):
            self.checkbuttons['question '+str(i)].configure(fg='black')
            self.checkbuttonvar[str(i)].set(False)
            self.checkbtntext[str(i)].set(self.text['question'][i])

    def showAnswer(self):
        self.givenAnswers = []
        for i in range(1, 6):
            self.givenAnswers.append(self.logic.str2bool(
                self.checkbuttonvar[str(i)].get()))
        
        for i in range(0, 5):
            if self.givenAnswers[i] == self.text['answers'][i]:
                self.checkbuttons['question '+str(i+1)].configure(fg='#009E18')
            else:
                self.checkbuttons['question '+str(i+1)].configure(fg='red')
        
            # self.checkbuttons['question '+str(i)].configure(font = self.font)


def main():
    root = MainWindow()
    root.mainloop()
    
if __name__ == '__main__':
    main()
