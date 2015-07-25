# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:17:33 2015

@author: RLSR
"""

from Tkinter import Tk, Label, Checkbutton, W, BooleanVar
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

    def nextQuestion(self):
        q = self.chooseQuestion()
        d = self.parseQuestion(q)
        for keys, values in d.items():
            print str(keys)+': \n'+str(values)
        return d

    def str2bool(self, v):
        return str(v).lower() in ('true', 'True')
        

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.logic = Logic()
        self.text = self.logic.nextQuestion()
        self.font = tkFont.Font(size=24)
        self.statement = Label(self, text = self.text['question'][0])
        self.statement.pack(anchor = W)
        self.checkbuttons = {}
        self.checkbuttonvar = {}        
        for i in range(1,6):
            self.checkbuttonvar[str(i)] = BooleanVar()
            self.checkbuttons['question '+str(i)] = Checkbutton(self,
                              text=self.text['question'][i],
                              variable=self.checkbuttonvar[str(i)])
            self.checkbuttons['question '+str(i)].pack(anchor = W)
            # self.checkbuttons['question '+str(i)].configure(font = self.font)


def main():
    root = MainWindow()
    root.mainloop()
    
if __name__ == '__main__':
    main()