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

"""
This module provides the key functionality of Klak, the calculations.
Use the module by making an object of the Calc class (this will keep track
of defined constants and macros) and use the calc function of that object. 
"""

from expr import * 
from parse import * 
from decimal import *
from consts import *
from calchelp import getHelp

class Calc():
    def __init__(self):
        #Start with the pre-defined constants...
        self.consts = Consts
        #...and no predefined macros 
        self.macroDict = {}

    def calc(self, inp):
        #Strip all spaces and tabs from the input
        inp = ''.join([c for c in inp if c not in ' \t'])
        #If input is empty now, just return an empty string
        if not inp:
            return ''
        #If the input ends with an operator, strip it and return
        if inp[-1] in expr.getOps():
            return inp
        #If the strings "exit" or "quit" is in the input, just exit
        if inp == 'exit' or inp == 'quit':
            exit()
        #If the string "help" is in the input, attemot to return relevant help
        if 'help' in inp:
            return getHelp(inp)
        #Scan for HEX in the input and replace it with decimal number strings
        inp = hexScan(inp)
        #Scan for engineering notation in the input and replace it with normal number strings
        inp = eScan(inp)
        #Check if the input matches the regex for a macro definition (for example "myAdd(a,b)=a+b") 
        expm = match(".+\(.+\).*=.+",inp)
        #Check if the input matches the regex for a constant definition (for example "myConstant=12345") 
        constm = match(".+=.+",inp)
        if expm:
            #If the input looks like a macro, define the macro and return the result
            return defExprMacro(inp,self.macroDict)
        elif constm:
            #If the input looks like a constant definition, define the constant and return the result
            return constAssign(inp,self.consts,self.macroDict)
        else:
            #Otherwise just try to calculate it
            return normalCalc(inp,self.consts,self.macroDict)

def normalCalc(inp,constDict,macroDict):
    """ Evaluate a normal arithmetic expression
    """
    hexDisp = False
    #If the first thing in the input is the string "hex",
    #set a flag to display any reult as hex if possible
    if inp[:3].lower() == 'hex':
        inp = inp[3:]
        hexDisp = True
    #Parse the input (see parse.py)  
    parsed = parse(inp)
    #If parse returns a list, that means that the parsing was succssesfull  
    if isinstance(parsed,list):
        #Build an expression tree out of the parsed list (see expr.py)...
        exp = buildExp(parsed,macroDict)
        #...And evaluate the extression tree with the previously defined constants
        res = exp.eval(constDict)
        #If the evaluation returns a decimal, the evaluation was successfull
        if isinstance(res,Decimal):
            #Add the result to the constants under the "ans" name
            constDict['ans'] = res
            #If we should display the result as hex, convert to a hex string 
            if hexDisp and res._isinteger():
                return '0x%02x'%(int(res))
            else:
                #Otherwise just convert to string
                return str(res)
        else:
            return 'Unknown: '+ ','.join(res)
    else:
        #If the parse returns a string instead just return the string if it 
        #contains "Error" or "Unknown"
        if parsed[:6] == 'Error:':
            return parsed
        if parsed[:8] == 'Unknown:':
            return parsed
        #If the parse result is the name of a constant, return the number for that constant 
        if parsed in constDict:
            constDict['ans'] = constDict[parsed]
            if hexDisp and constDict[parsed]._isinteger():
                return '0x%02x'%(int(constDict[parsed]))
            else:
                return str(constDict[parsed])
        else:
            #If all else fail, try to convert the returned string to a Decimal and return
            try:
                constDict['ans'] = Decimal(parsed)
                if hexDisp and constDict['ans']._isinteger():
                    return '0x%02x'%(int(constDict['ans']))
                else:
                    return str(constDict['ans'])
            except:
                return 'Unknown: '+parsed
       
def constAssign(inp,constDict,macroDict):
    """ Assign a constant to a name in the provided constant dict
    """
    #Split on "=" to get a list with a name on pos 0 and an expression on pos 1 
    inplst  = [x.strip() for x in inp.split('=')]    
    try:
        Decimal(inplst[0])
        return 'Error: Cant use a number as a name for a constant'
    except:
        if not inplst[0].isalnum():
            return 'Error: Only alphanumericals allowed in constant names' 
        #If we have a valid name, evaluate the expression
        restext = normalCalc(inplst[1],constDict,macroDict)
        try:
            constDict[inplst[0]] = Decimal(restext)
        except:
            return restext 
        return inp

def defExprMacro(inp,exprMacroDict):
    """ Define a macro expression and put it in the macro provided expression dict 
    """
    if inp.count('=') != 1:
        return 'Too many \'=\' in expression macro definition'
    #Split to get the definition and the expression separately
    macroDef,macroExp = inp.split('=')
    #USe the parser functions (parse.py) to find the name and the arguments
    macroName = funcname(macroDef)
    macroArgs = funcargs(macroDef)
    for arg in macroArgs:
        if len(arg) == 0:
            return "Error: Argument name cannot be empty"
        if not arg.isalnum():
            return "Error: Only alphanumericals may be used in argument names"
        if arg.isdigit():
            return "Error: Numbers may not be used as argument names"    
    #If the name is valid, parse the macro expression
    parsedMacro = parse(macroExp)
    if 'Error:' in parsedMacro:
        return parsedMacro
    #If is parses ok, make a macro (expr.py) and add it to the provided macro dict
    em = ExprMacro(parsedMacro,macroArgs)
    exprMacroDict[macroName] = em
    return inp

def hexScan(inpstr):
    """ Scan for hex numbers and replace them with normal decimals
    """
    hexchars = '0123456789abcdefABCDEF'
    while '0x' in inpstr:
        start = inpstr.index('0x')
        stop = start+2
        while stop < len(inpstr) and inpstr[stop] in hexchars:
            stop += 1
        inpstr = inpstr[:start] +str(int(inpstr[start:stop],16))+ inpstr[stop:]
    return inpstr

def eScan(inpstr):
    """ Scan forengineering notation and replace with normal decimals
    """
    m = search("[0-9][E,e]\+[0-9]",inpstr)
    while m:
        div = m.start()+2
        inpstr = inpstr[:div]+inpstr[div+1:]
        m = search("[0-9][E,e]\+[0-9]",inpstr)
    return inpstr

if __name__ == '__main__':
    c = Calc()
    while True:
        inp = raw_input(':')
        print(c.calc(inp))

