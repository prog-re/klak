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

from Tkinter import *
from calc import *
import unicodedata
import platform
import klakicon

class klakapp_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.calc = Calc()
        self.history = []
        self.last = ''
        self.historyidx = -1

    def initialize(self):
        self.textarea = Text(self,wrap="word")
        self.textarea.pack(side="left",fill="both",expand="yes")
        self.textarea.focus_set()
        self.textarea.insert(END,"""Klak - The simple calculator - (C) 2013 Martin Karlsson 
This program comes with ABSOLUTELY NO WARRANTY; for details type 'help warranty'. This is free software, and you are welcome to redistribute it under certain conditions. For help with how to use this program type 'help'\n""")    
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side="right",fill="y")
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.textarea.bind("<Key>",lambda ev:self.handleKeys(ev))

    def calcColWidth(self):
        prew = self.textarea.winfo_width()
        self.textarea.config(width=self.width+1)
        self.update_idletasks() 
        aftw = self.textarea.winfo_width()
        self.textarea.config(width=self.width)
        self.colwidth = aftw-prew
        self.colwidth /= 2
        print(self.colwidth)

    def handleKeys(self,ev):
        kk = ev.keycode
        print(self.winfo_width())
        print(ev.keysym),
        print(ev.keycode)
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
        if self.historyidx < len(self.history):
            self.historyidx+=1
        if self.historyidx == 0:
            self.historyInsert(self.last)
        else:
            self.historyInsert(self.history[-self.historyidx])

    def historyDown(self):
        if self.historyidx > -1:
            self.historyidx-=1
        if self.historyidx == -1:
            self.historyInsert("")
        elif self.historyidx == 0:
            self.historyInsert(self.last)
        else:
            self.historyInsert(self.history[-self.historyidx])


    def historyInsert(self,histStr):
        lc = self.textarea.index(INSERT).split('.')
        self.textarea.delete(lc[0]+'.0',lc[0]+'.'+END)
        self.textarea.insert(INSERT,histStr)    

    def calcLine(self):
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

    def insPoint(self):
        self.textarea.insert(INSERT,".")
        return 'break'

if __name__ == "__main__":
    app = klakapp_tk(None)
    try:
        app.iconbitmap(klakicon.gettempfilename())
    except:
        pass
    app.title('Klak')
    app.mainloop()
    klakicon.removetempfile()
