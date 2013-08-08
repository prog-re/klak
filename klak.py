#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#    Copyright (C) 2013 Martin Karlsson 
#    (martin@prog.re)
#
#    This file is part of Klak.
#
#    Klak is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Klak is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Klak.  If not, see <http://www.gnu.org/licenses/>.

""" This module is the main of the Klak app. It provides the GUI and calculator history.
"""

from Tkinter import *
from calc import *
import unicodedata
import platform
import klakicon


class KlakApp_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        #Calc provides the calculator functionality (see calc.py) 
        self.calc = Calc()
        self.history = []
        self.last = ''
        self.historyidx = -1

    def initialize(self):
        #Sets up the GUI
        self.textarea = Text(self,wrap="word")
        self.textarea.pack(side="left",fill="both",expand="yes")
        self.textarea.focus_set()
        self.textarea.insert(END,"""Klak - The simple calculator - Copyright (C) 2013 Martin Karlsson 
This program comes with ABSOLUTELY NO WARRANTY; for details type 'help warranty'. This is free software, and you are welcome to redistribute it under certain conditions. For help with how to use this program type 'help'\n""")    
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side="right",fill="y")
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.textarea.bind("<Key>",lambda ev:self.handleKeys(ev))

     
    def handleKeys(self,ev):
        """ This should be bound to the key events of the text area to
        provide decimal point exchange and history on the arrow keys.
        """
        kk = ev.keycode
        # One way for Windows...
        if platform.system() == "Windows":
            try:
                {13:self.calcLine,
                 38:self.historyUp,
                 40:self.historyDown,
                 110:self.insPoint}[kk]()
            except KeyError:
                pass
            retval = None
            try:
                retval = {13:"break",
                          38:"break",
                          40:"break",
                          110:"break"}[kk]
            except:
                pass
        #...and another for Linux 
        else:
            try:
                {91:self.insPoint,
                 36:self.calcLine,
                 104:self.calcLine,
                 111:self.historyUp,
                 116:self.historyDown}[kk]()
            except KeyError:
                pass
            retval = None
            try:
                retval = {
                    91:"break",
                    36:"break",
                    104:"break",
                    111:"break",
                    116:"break"}[kk]
            except:
                pass
        return retval

    def historyUp(self):
        """ Get next history item """
        if self.historyidx < len(self.history):
            self.historyidx+=1
        if self.historyidx == 0:
            self.historyInsert(self.last)
        else:
            self.historyInsert(self.history[-self.historyidx])

    def historyDown(self):
        """ Get previous history item """
        if self.historyidx > -1:
            self.historyidx-=1
        if self.historyidx == -1:
            self.historyInsert("")
        elif self.historyidx == 0:
            self.historyInsert(self.last)
        else:
            self.historyInsert(self.history[-self.historyidx])


    def historyInsert(self,histStr):
        """ Insert history item in the text area """
        lc = self.textarea.index(INSERT).split('.')
        self.textarea.delete(lc[0]+'.0',lc[0]+'.'+END)
        self.textarea.insert(INSERT,histStr)    

    def insPoint(self):
        """ Insert decimal point (.) at the curent cursor pos """
        self.textarea.insert(INSERT,".")
        return 'break'


    def calcLine(self):
        """ Evaluate the current line with calc (calc.py) and put the result on the next line"""
        lc = self.textarea.index(INSERT).split('.')
        endline = self.textarea.index(END).split('.')
        line = self.textarea.get(lc[0]+'.0',lc[0]+'.'+END)
        print(lc)
        print(self.textarea.index(END))
        realend = str(int(endline[0])-1)
        print('End string lengtth:%x' % (len(self.textarea.get(realend+'.0',realend+'.'+END))))
        if len(line.strip()):
            line = unicodedata.normalize('NFKD', line).encode('ascii','ignore')
            result = self.calc.calc(line)
            resLineCnt = result.count('\n')
            if 'help' not in line:
                self.history.append(line)            
                self.last = result
            self.historyidx = -1
            if len(self.textarea.get(realend+'.0',realend+'.'+END)):
                self.textarea.insert(END,"\n"+result+"\n")    
                self.textarea.mark_set("insert", "%d.%d" % (int(realend)+resLineCnt+2,0))
            else:
                self.textarea.insert(END,result+"\n")
                self.textarea.mark_set("insert", "%d.%d" % (int(realend)+resLineCnt+1,0))
            self.textarea.see(END)
        return 'break'


if __name__ == "__main__":
    #Create GUI and set the icon
    app = KlakApp_tk(None)
    try:
        app.iconbitmap(klakicon.gettempfilename())
    except:
        pass
    app.title('Klak')
    #Run!
    app.mainloop()
    #Remove temp file on exit
    klakicon.removetempfile()
