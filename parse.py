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


""" The parser takes a legal expresion string and tranforms it into an expression
"""


from re import *
import expr


def parse(expstr):
    """ Parse the expression string into a expression tree. Example:
    "a+b*c" becomes ['+','a',['*','b','c']] 
    """
    #First remove all whitespace
    expstr = ''.join([c for c in expstr if c not in ' \t'])
    #Then exchange the built in function strings with their one-character operator 
    expstr = funcOpExchange(expstr)
    if balanced(expstr):
        #Then split on the one-char operators recursively
        return opsplit(expstr)
    else:
        return 'Error: Unbalanced parentheses'


def balanced(expstr):
    """ Check if a string has balance with the parentesises 
    """
    pc = 0
    for c in expstr:
        if c == '(':
            pc += 1
        elif c == ')':
            pc -= 1
            if pc < 0:
                return False
    if pc == 0:
        return True
    else:
        return False


def funcOpExchange(expstr):
    """ Exchange built in functions (sin,log etc) for the single char operators  
    """
    funcOpDict = expr.getFuncOpDict() 
    for funcstr in funcOpDict:
        idx = expstr.find(funcstr)
        if idx >= 0:
            #if we find a function string at idx
            if (idx == 0 or not expstr[idx-1].isalpha()) and expstr[idx+len(funcstr)] == '(':
                fstart = idx
                fstop = 0
                rest = expstr[idx:]
                pdepth = 0
                for i,c in enumerate(rest):
                    if c == '(':
                        pdepth += 1
                    if c == ')':
                        pdepth -= 1
                        if pdepth == 0:
                            fstop = idx+i+1
                            break
                start = expstr[:fstart]
                middle = expstr[fstart:fstop]
                end = expstr[fstop:]
                args = ['('+funcOpExchange(exp)+')' for exp in funcargs(middle)]
                if len(args) == 1:
                    args.append('0')
                expstr = start+funcOpDict[funcstr].join(args)+funcOpExchange(end)
    return expstr

def opsplit(expstr):
    """ Split the expression string into lists of the form ['op','expstr1',expstr2]
    do this recursively untill no more splits are possible (return the string itself)
    """

    #ops are the one char operators (sorted on precidence)
    ops = expr.getOps()
    #Remove outer parentesis if we have them
    if expstr[0] == '(' and expstr[-1] == ')' and balanced(expstr[1:-1]):
        expstr = expstr[1:-1]
    #Add a '0' to the beginning of the string if we start with an operator
    if expstr[0] in ops:
        expstr = '0'+expstr
    for op in ops:
        pc = 0
        cc = len(expstr)-1
        revexpstr = list(expstr)
        revexpstr.reverse()
        #Search for the operator backwards (to preserve operator presidence)
        for c in revexpstr:
            if c == '(':
                pc += 1
            elif c == ')':
                pc -= 1
            if c == op and pc == 0:
                #Build the tree recursively
                return [op,opsplit(expstr[:cc]),opsplit(expstr[cc+1:])]
            cc -=1
    #if we find something that looks like a function, parse it separately 
    if funcpattern(expstr):
        fnamestr = funcname(expstr)
        fargs = funcargs(expstr)
        farglist = [opsplit(arg) for arg in fargs]
        return [fnamestr]+farglist
    return expstr
        
def funcpattern(funcstr):
    """ Returns true if the string looks like a function
    """
    m = match('.*\(.*\)',funcstr)
    if m and m.start() == 0 and m.end() == len(funcstr):
        return True
    return False

def funcargs(funcstr):
    """ Extract the function arguments
    """
    ps = funcstr.find('(')
    argstr = funcstr[ps+1:-1]
    pc = 0
    arglist = []
    argacc = ''
    for c in argstr:
        if c == '(':
            pc += 1
        elif c == ')':
            pc -= 1
        if pc == 0 and c == ',':
            arglist.append(argacc)
            argacc = ''
        else:
            argacc += c
    arglist.append(argacc)
    return arglist

def funcname(funcstr):
    """ Extract the function name
    """
    ps = funcstr.find('(')
    return funcstr[:ps]


if __name__ == '__main__':
    print(balanced('((()())))(()()((()))'))
    print(opsplit('3*34+90*sin(56)'))
    print(funcname('sin(abcdef)'))
    print(funcargs('sin(sin(45),45+67,455)'))
    print(opsplit('sin(34+45,67*67)'))
    print('New test')
    print(opsplit('234'))
