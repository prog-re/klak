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

""" This module provides an expression abstraction and means to 
expand user defined functions (macros) into evaluable expressions 
"""

from decimal import *
from dectrig import *
import math

def buildExp(parsedLst,macroDict = {}):
    """ Turn the parsed tree into a tree of Expressions
    """
    #If the operator is built in...
    if parsedLst[0] in builtins:
        def expterm(term):
            if isinstance(term,str):
                try:
                    return Decimal(term)
                except:
                    return term
            else:
                return buildExp(term,macroDict)
        #...Turn each of the term into a Decimal if possible, or another expression
        p1 = expterm(parsedLst[1])
        p2 = expterm(parsedLst[2])
        #Return subclassed expression based on the operator   
        return builtins[parsedLst[0]][0](p1,p2)
    #Otherwise check if the operator really is a macro
    elif parsedLst[0] in macroDict:
        #In that case expand the macro and return 
        return macroDict[parsedLst[0]].getExpr(parsedLst[1:],macroDict)
    else:
        return None

def getFuncOpDict():
    """ Get the long name for each of the operations ("mul" for * etc)
    """
    funcops = {}
    for op in builtins:
        funcops[builtins[op][1]] = op
    return funcops

def getOps():
    """ Get the one-char operators sorted by precidence   
    """ 
    presop = [(builtins[x][2],x) for x in builtins]
    presop.sort()
    return [x[1] for x in presop]

class Expr():
    """ Expr is a base class for an expression. It always has 2 parts (p1 and p2) witch 
    can be Decimals, Other expression objects, or strings (unknowns). Since an expression 
    can contain other expressions, the expressions forms a binary tree. This class is 
    subclassed for each of the operations witch are override the "calc" function to be used 
    when both p1 and p2 are decimals.  
    """
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        getcontext().prec = 50

    def __str__(self):
        return 'Expr params:'+str(self.p1)+';'+str(self.p2)

    #used if both p1 and p2 are Decimal
    def calc(self,p1,p2):
        #overide this for each of the predefined expressions
        pass

    #evaluate the expression using the constants defined in constdict
    def eval(self,constdic):
        self.unknowns = []
        #define a function to evaluate a part to a decimal if possible 
        def paramCheck(p,unk):
            tmpres = None
            #If the part is another expression, try to evaluate that (recursion!)
            if isinstance(p,Expr):
                tmpres = p.eval(constdic)
                if isinstance(tmpres,list):
                    unk += tmpres
            #if the part is a string, check if it is in the constant dictionary
            elif isinstance(p,str):
                if p in constdic:
                    tmpres = constdic[p]
                else:
                    unk.append(p)
            else:
                tmpres = p
            return tmpres
        #Evaluate each part
        tmpp1res = paramCheck(self.p1,self.unknowns)
        tmpp2res = paramCheck(self.p2,self.unknowns)
        #If both parts evaluates to Decimals... 
        if isinstance(tmpp1res,Decimal) and isinstance(tmpp2res,Decimal):
            #Run the calc on it (this will torn the 2 decimals into one decimal
            #using the operations in the overriding calc functions
            return self.calc(tmpp1res,tmpp2res)
        else:
            #Otherwise just return all the unknown strings we have found
            return self.unknowns


#Subclasses that defines the calc for each of the operations in Klak

class Add(Expr):
    def calc(self,p1,p2):
        return p1+p2

class Sub(Expr):
    def calc(self,p1,p2):
        return p1-p2

class Mul(Expr):
    def calc(self,p1,p2):
        return p1*p2

class Div(Expr):
    def calc(self,p1,p2):
        if p2 != 0:
            return p1/p2
        else:
            return ["Division by zero"]

class Pow(Expr):
    def calc(self,p1,p2):
        return pow(p1,p2)

class Ln(Expr):
    def calc(self,p1,p2):
        return p1.ln()

class Log(Expr):
    def calc(self,p1,p2):
        return p1.log10()

class Sin(Expr):
    def calc(self,p1,p2):
        return dec_sin(p1)

class Cos(Expr):
    def calc(self,p1,p2):
        return dec_cos(p1)

class Tan(Expr):
    def calc(self,p1,p2):
        return dec_tan(p1)


#The one-charcter representation of each operation

builtins = {
#one-char-op,Expr-class,str-rep,precidence
    '+':(Add,'add',1),
    '-':(Sub,'sub',2),
    '*':(Mul,'mul',3),
    '/':(Div,'div',4),
    '^':(Pow,'pow',5),
    chr(128):(Ln,'ln',6),
    chr(129):(Log,'log',6),
    chr(130):(Sin,'sin',6),
    chr(131):(Cos,'cos',6),
    chr(132):(Tan,'tan',6)
    }


class ExprMacro:
    """ Class to represent a macro (user defined function).   
    """

    def __init__(self,parsedLst,paramLst):
        #The termLst is is the raw parsed tree (but stripped of macro name)
        self.termLst = parsedLst
        #The pList shows witch strings in the parsed tree is parameters to the macro
        self.pLst = paramLst

    def getExpr(self,paramLst,macroDict):
        """ Expand the macro using the supplied parameters
        """
        pKey = dict(zip(self.pLst,paramLst))
        def exchange(x):
            if x in self.pLst:
                return pKey[x]
            return x
        def excLst(lst):
            retlst = []
            for item in lst:
                if isinstance(item,list):
                    retlst.append(excLst(item))
                else:
                    retlst.append(exchange(item))
            return retlst
        ctermlst = excLst(self.termLst)
        #Build a true expression and return
        return buildExp(ctermlst,macroDict)


if __name__ == '__main__':
    exp = Div('V1',Add('V2','V3'))
    expM = ExprMacro(['+','A',['+','B','C']],['A','B','C'])
    nexp = expM.getExpr(['1','2','3'])
    print(nexp.eval({}))
    print(exp.eval({'X':Decimal(56)}))
    
        
