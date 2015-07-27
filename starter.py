# -*- coding: utf-8 -*-

from Tkinter import Tk, Label, Button, LEFT
from subprocess import call
import exam, quest_by_quest

class StarterWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.exambtn = Button(self, text='start an exam',
                              command=self.startExam)
        self.exambtn.pack()
        self.questbtn = Button(self, text='start single questions',
                               command=self.startQuestions)
        self.questbtn.pack()
        self.um = '''User manual:\n
        Start either an exam or single questions\n
        Go to next question either with mouse or the <right arrow>\n
        Toggle checkboxes either with mouse or keypad buttons 1-6\n
        In single question mode, show answer either with mouse or <return>\n
        In exam mode, results will display after the set question number'''
        self.usermanual = Label(self, text=self.um, justify=LEFT)
        self.usermanual.pack()

    def startExam(self):
        call(["python","exam.py"])

    def startQuestions(self):
        call(["python","quest_by_quest.py"])


def main():
    root = StarterWindow()
    root.mainloop()
    
if __name__ == '__main__':
    main()