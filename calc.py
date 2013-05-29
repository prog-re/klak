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

from expr import * 
from parse import * 
from decimal import *
from consts import *
from calchelp import getHelp
dbg = False
       
def normalCalc(inp,constDict,macroDict):
    hexDisp = False
    if inp[:3].lower() == 'hex':
        inp = inp[3:]
        hexDisp = True
    parsed = parse(inp)
    if dbg:
        print('Parse returns:'),
        print(parsed)
        print('Defined consts:'),
        print(constDict)
    if isinstance(parsed,list):
        exp = buildExp(parsed,macroDict)
        if dbg:
            print('buildExp:'),
            print(str(exp))
        res = exp.eval(constDict)
        if dbg:
            print('exp.eval:'),
            print(res)
        if isinstance(res,Decimal):
            constDict['ans'] = res
            if hexDisp and res._isinteger():
                return '0x%02x'%(int(res))
            else:
                return str(res)
        else:
            return 'Unknown: '+ ','.join(res)
    else:
        if parsed[:6] == 'Error:':
            return parsed
        if parsed[:8] == 'Unknown:':
            return parsed
        if parsed in constDict:
            constDict['ans'] = constDict[parsed]
            if hexDisp and constDict[parsed]._isinteger():
                return '0x%02x'%(int(constDict[parsed]))
            else:
                return str(constDict[parsed])
        else:
            try:
                constDict['ans'] = Decimal(parsed)
                if hexDisp and constDict['ans']._isinteger():
                    return '0x%02x'%(int(constDict['ans']))
                else:
                    return str(constDict['ans'])
            except:
                return 'Unknown: '+parsed
       
def constAssign(inp,constDict,macroDict):
    inplst  = [x.strip() for x in inp.split('=')]    
    try:
        Decimal(inplst[0])
        return 'Error: Cant use a number as a name for a constant'
    except:
        if not inplst[0].isalnum():
            return 'Error: Only alphanumericals allowed in constant names' 
        restext = normalCalc(inplst[1],constDict,macroDict)
        try:
            constDict[inplst[0]] = Decimal(restext)
        except:
            return restext 
        return inp

def defExprMacro(inp,exprMacroDict):
    if inp.count('=') != 1:
        return 'Too many \'=\' in expression macro definition'
    macroDef,macroExp = inp.split('=')
    macroName = funcname(macroDef)
    macroArgs = funcargs(macroDef)
    for arg in macroArgs:
        if len(arg) == 0:
            return "Error: Argument name cannot be empty"
        if not arg.isalnum():
            return "Error: Only alphanumericals may be used in argument names"
        if arg.isdigit():
            return "Error: Numbers may not be used as argument names"    
    parsedMacro = parse(macroExp)
    if 'Error:' in parsedMacro:
        return parsedMacro
    em = ExprMacro(parsedMacro,macroArgs)
    exprMacroDict[macroName] = em
    return inp

def hexScan(inpstr):
    hexchars = '0123456789abcdefABCDEF'
    while '0x' in inpstr:
        start = inpstr.index('0x')
        stop = start+2
        while stop < len(inpstr) and inpstr[stop] in hexchars:
            stop += 1
        inpstr = inpstr[:start] +str(int(inpstr[start:stop],16))+ inpstr[stop:]
    return inpstr

def eScan(inpstr):
    m = search("[0-9][E,e]\+[0-9]",inpstr)
    while m:
        div = m.start()+2
        inpstr = inpstr[:div]+inpstr[div+1:]
        m = search("[0-9][E,e]\+[0-9]",inpstr)
    return inpstr

class Calc():
    def __init__(self):
        self.consts = Consts
        self.macroDict = {}

    def calc(self, inp):
        inp = ''.join([c for c in inp if c not in ' \t'])
        if not inp:
            return ''
        if inp[-1] in expr.getOps():
            return inp
        if inp == 'exit' or inp == 'quit':
            exit()
        if 'help' in inp:
            return getHelp(inp)
        inp = hexScan(inp)
        inp = eScan(inp)
        expm = match(".+\(.+\).*=.+",inp)
        constm = match(".+=.+",inp)
        if expm:
            return defExprMacro(inp,self.macroDict)
        elif constm:
            return constAssign(inp,self.consts,self.macroDict)
        else:
            return normalCalc(inp,self.consts,self.macroDict)

if __name__ == '__main__':
    c = Calc()
    while True:
        inp = raw_input(':')
        print(c.calc(inp))

