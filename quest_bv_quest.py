# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:17:33 2015

@author: RLSR
"""

from Tkinter import Tk, Label, Checkbutton, W, S, BooleanVar, Button, LEFT
from Tkinter import StringVar
import tkFont
import os
from random import randint


class Logic:
    def __init__(self):
        self.quest_dir = os.path.join(os.path.dirname(__file__), 'resource')
        self.filenames = [f for f in os.listdir(self.quest_dir) 
            if os.path.isfile(os.path.join(self.quest_dir,f))]
    
    def chooseQuestion(self):
        self.f = self.filenames[randint(0, 1666)]
        return open(os.path.join(self.quest_dir, self.f), 'r')
        
    def parseQuestion(self, question):
        q = question.readlines()
        to_delete = []
        for l in range(len(q)):
            if (q[l] == '' or q[l] == '\r\n' or q[l] == '\n'):
                to_delete.append(l)
        for i in list(reversed(to_delete)):
#            s = 'Empty line '+ str(i) +' was deleted from {}'.format(self.f)
            del q[i]
#            print s
        answers = []
        try:
            for i in range(1, 6):
                answers.append(self.str2bool(q[i].split(',', 1)[0]))
                q[i] = q[i].split(',', 1)[1]
            return {'answers': answers, 'question': q}
        except IndexError:
            raise Exception(
                'There was a mistake in {0} formatting: \n\n'.format(self.f)
                + 'QUESTION: \n'                
                + '{}\n\n'.format(q)
                + 'ANSWERS: \n'
                + '{}\n'.format(answers))

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
        self.bind("<Key-KP_Subtract>", self.OnSmaller)
        self.bind("<Key-KP_Add>", self.OnBigger)
        self.bind("<Right>", self.nextQuestion)
        self.bind("<Return>", self.showAnswer)
        self.logic = Logic()
        self.widgetwraplist = []
        self.text = self.logic.prepareQuestion()
        self.font = tkFont.Font(size=24)
        self.stmtvar = StringVar()
        self.stmtvar.set(self.text['question'][0])
        self.statement = Label(self, textvariable=self.stmtvar, font=self.font)
        self.statement.pack(anchor = W)
        self.widgetwraplist.append(self.statement)
        self.checkbuttons = {}
        self.checkbtntext = {}
        self.checkbuttonvar = {}        
        for i in range(1, 6):
            self.checkbuttonvar[str(i)] = BooleanVar()
            self.checkbtntext[str(i)] = StringVar()
            self.checkbtntext[str(i)].set(self.text['question'][i])
            self.checkbuttons['question '+str(i)] = Checkbutton(self,
                              textvariable = self.checkbtntext[str(i)],
                              variable = self.checkbuttonvar[str(i)],
                              font=self.font)
            self.checkbuttons['question '+str(i)].pack(anchor = W)
            self.widgetwraplist.append(self.checkbuttons['question '+str(i)])
        self.explvar = StringVar()
        self.explvar.set(' '.join(self.text['question'][6:]))
        self.explanation = Label(self, textvariable=self.explvar,
                                 font=self.font, justify=LEFT)
        self.widgetwraplist.append(self.explanation)
        self.buttonNext = Button(self, text = 'Next question',
                                 command = lambda: self.nextQuestion(1),
                                 font=self.font)
        self.buttonNext.pack(anchor = S)
        self.buttonAnswer = Button(self, text = 'Show answers',
                                 command = lambda: self.showAnswer(1),
                                 font=self.font)
        self.buttonAnswer.pack(anchor = S)

    def nextQuestion(self, event):
        self.text = self.logic.prepareQuestion()
        self.stmtvar.set(self.text['question'][0])
        self.explvar.set(' '.join(self.text['question'][6:]))
        self.explanation.pack_forget()
        for i in range(1, 6):
            self.checkbuttons['question '+str(i)].configure(fg='black')
            self.checkbuttonvar[str(i)].set(False)
            self.checkbtntext[str(i)].set(self.text['question'][i])

    def showAnswer(self, event):
        self.givenAnswers = []
        for i in range(1, 6):
            self.givenAnswers.append(self.logic.str2bool(
                self.checkbuttonvar[str(i)].get()))
        
        for i in range(0, 5):
            if self.givenAnswers[i] == self.text['answers'][i]:
                self.checkbuttons['question '+str(i+1)].configure(fg='#009E18')
            else:
                self.checkbuttons['question '+str(i+1)].configure(fg='red')
        self.explanation.pack(anchor = W)

    def OnBigger(self, event):
        '''Make the font 2 points bigger'''
        size = self.font['size']
        self.font.configure(size=size+2)

    def OnSmaller(self, event):
        '''Make the font 2 points smaller'''
        size = self.font['size']
        self.font.configure(size=size-2)

    def wrapWidgets(self):
        self.update()
        for widget in self.widgetwraplist:
            widget.configure(wraplength=self.winfo_width())


def main():
    root = MainWindow()
    root.wrapWidgets()
    root.mainloop()
    
if __name__ == '__main__':
    main()
