# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:17:33 2015

@author: RLSR
"""

from Tkinter import Tk, Label, Checkbutton, W, S, BooleanVar, Button, LEFT
from Tkinter import StringVar
import tkFont
import os
import sys
from random import randint


class InvokableCheckbutton(Checkbutton):
    '''
    Subclass Tkinter.Checkbutton to allow keyboard binding of Checkbutton.invoke
    through a wrapping method
    '''
    def __init__(self, parent, *args, **kwargs):
        Checkbutton.__init__(self, parent, *args, **kwargs)

    def customInvoke(self, event):
        self.invoke()

class Logic:
    def __init__(self):
		self.quest_dir = os.path.join(os.path.dirname(__file__), 'resource')
		self.filenames = [f for f in os.listdir(self.quest_dir) if os.path.isfile(os.path.join(self.quest_dir,f))]
		self.questiondict = {}
		self.questioncount = 0
		self.EXAM_END = int(sys.argv[1])
		self.file_count = len([name for name in os.listdir('./resource') if os.path.isfile(os.path.join('./resource', name))])

    def chooseQuestion(self):
        self.f = self.filenames[randint(0, self.file_count)]
        if self.f not in self.questiondict:
            self.questionpath = os.path.join(self.quest_dir, self.f)
            self.questiondict[str(self.questionpath)] = {}
        else:
            self.chooseQuestion()
        return open(self.questionpath, 'r')
        
    def parseQuestion(self, question):
        q = question.readlines()
        to_delete = []
        for l in range(len(q)):
            if (q[l] == '' or q[l] == '\r\n' or q[l] == '\n'):
                to_delete.append(l)
        for i in list(reversed(to_delete)):
            del q[i]
        answers = []
        try:
            l = 0
            for i in range(1, 6):
                l += 1
                answers.append(self.str2bool(q[i].split(',', 1)[0]))
                q[i] = q[i].split(',', 1)[1]
                question.close()
            return {'answers': answers, 'question': q}
        except IndexError:
            raise Exception(
                'There was a mistake in {} formatting: \n\n'.format(self.f)
                + 'on line {}: '.format(l) + q[4] +'\n'
                + 'QUESTION: \n'                
                + '{}\n\n'.format(q)
                + 'ANSWERS: \n'
                + '{}\n'.format(answers))

    def prepareQuestion(self):
        q = self.chooseQuestion()
        d = self.parseQuestion(q)
        self.questiondict[self.questionpath]['correct answers'] = d['answers']
        return d

    def calculateScore(self):
        total = 0
        correct = 0
        for q in self.questiondict:
            for a in range(5):
                total += 1
                if (self.questiondict[q]['correct answers'][a] == 
                        self.questiondict[q]['given answers'][a]):
                    correct += 1
        return (correct*100)/total
        
    def str2bool(self, v):
        if str(v).lower() in ('true', 'True', '1'):
            return True
        else:
            return False
        

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.bind("<Down>", self.OnSmaller)
        self.bind("<Up>", self.OnBigger)
        self.bind("<Right>", self.nextQuestion)
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
            self.checkbuttons['question '+str(i)] = InvokableCheckbutton(self,
                              textvariable = self.checkbtntext[str(i)],
                              variable = self.checkbuttonvar[str(i)],
                              font=self.font)
            self.checkbuttons['question '+str(i)].pack(anchor = W)
            self.widgetwraplist.append(self.checkbuttons['question '+str(i)])         
            self.bind("<Key-"+str(i)+">", self.checkbuttons['question '+str(i)].customInvoke)
        self.explvar = StringVar()
        self.explvar.set(' '.join(self.text['question'][6:]))
        self.explanation = Label(self, textvariable=self.explvar,
                                 font=self.font, justify=LEFT)
        self.widgetwraplist.append(self.explanation)
        self.buttonNext = Button(self, text = 'Next question',
                                 command = lambda: self.nextQuestion(1),
                                 font=self.font)
        self.buttonNext.pack(anchor = S)

    def nextQuestion(self, event):
        given_answers = []
        self.logic.questioncount += 1
        for i in range(1, 6):
            given_answers.append(self.logic.str2bool(self.checkbuttonvar[str(i)].get()))
        self.logic.questiondict[self.logic.questionpath]['given answers'] = given_answers
        if (self.logic.questiondict[self.logic.questionpath]['correct answers'] == 
            self.logic.questiondict[self.logic.questionpath]['given answers']):
                self.logic.questiondict[self.logic.questionpath]['is correct'] = True
        else:
            self.logic.questiondict[self.logic.questionpath]['is correct'] = False
        if self.logic.questioncount < self.logic.EXAM_END:
            if self.logic.questioncount == self.logic.EXAM_END-1:
                self.buttonNext.configure(text='Finish exam')
            self.text = self.logic.prepareQuestion()
            self.stmtvar.set(self.text['question'][0])
            self.explvar.set(' '.join(self.text['question'][6:]))
            self.explanation.pack_forget()
            for i in range(1, 6):
                self.checkbuttons['question '+str(i)].configure(fg='black')
                self.checkbuttonvar[str(i)].set(False)
                self.checkbtntext[str(i)].set(self.text['question'][i])
        else:
            self.stmtvar.set('You scored {}%'.format(str(self.logic.calculateScore())))
            if self.logic.calculateScore() >= 80:
                self.statement.configure(foreground='#009E18')
            else:
                self.statement.configure(foreground='red')
            for i in range(1, 6):
                self.checkbuttons['question '+str(i)].pack_forget()
            if self.logic.calculateScore() == 100:
                self.buttonNext.configure(text='Start a new exam')
                self.buttonNext.configure(command=lambda: self.startNewExam(1))
                self.bind("<Right>", self.startNewExam)
            else:
                self.bind("<Right>", self.reviewWindow)
                self.buttonNext.configure(text='Review wrong answers')
                self.buttonNext.configure(command= lambda: self.reviewWindow(1))

    def reviewWindow(self, event):
        self.reviewed = 0
        self.buttonNext.configure(text='Next')
        self.buttonNext.pack_forget()
        for i in range(1, 6):
            self.checkbuttons['question '+str(i)].pack(anchor = W)
        self.explanation.pack(anchor = W)
        self.buttonNext.pack(anchor = S)
        self.showAnswer(1)

    def showAnswer(self, event):
        if self.reviewed == 0:
            self.bind("<Right>", self.showAnswer)
            self.buttonNext.configure(command= lambda: self.showAnswer(1))
        for q in self.logic.questiondict:
            if self.logic.questiondict[q]['is correct'] == False:
                f = open(q, 'r')
                lines = self.logic.parseQuestion(f)
                self.stmtvar.set(lines['question'][0])
                self.statement.configure(foreground='black')
                self.explvar.set(' '.join(lines['question'][6:]))
                for i in range(1, 6):
                    self.checkbtntext[str(i)].set(lines['question'][i])
                    self.checkbuttonvar[str(i)].set(self.logic.questiondict[q]['given answers'][i-1])
                    if (self.logic.questiondict[q]['correct answers'][i-1] == 
                        self.logic.questiondict[q]['given answers'][i-1]):
                        self.checkbuttons['question '+str(i)].configure(fg='#009E18')
                    else:
                        self.checkbuttons['question '+str(i)].configure(fg='red')
                del self.logic.questiondict[q]
                self.reviewed += 1
                break
        if self.reviewed == self.logic.EXAM_END:
            self.buttonNext.configure(text='Start a new exam')
            self.buttonNext.configure(command=lambda: self.startNewExam(1))
            self.bind("<Right>", self.startNewExam)
            
    def startNewExam(self, event):
        self.logic.questioncount = 0
        self.questiondict = {}
        self.text = self.logic.prepareQuestion()
        self.stmtvar.set(self.text['question'][0])
        for i in range(1, 6):
                self.checkbuttons['question '+str(i)].configure(fg='black')
                self.checkbuttonvar[str(i)].set(False)
                self.checkbtntext[str(i)].set(self.text['question'][i])
        self.explanation.pack_forget()
        self.buttonNext.configure(text='next')
        self.buttonNext.configure(command=lambda: self.nextQuestion(1))
        self.bind("<Right>", self.nextQuestion)            

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
    print 'Argument List:', str(sys.argv)
    root = MainWindow()
    root.wrapWidgets()
    root.mainloop()
    
if __name__ == '__main__':
    main()
