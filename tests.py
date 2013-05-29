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


from calc import Calc

c = Calc()

def t(testdesc,inp,ans):
    global c
    print("Testing:"),
    print(testdesc),
    print(' '),
    if c.calc(inp) == ans:
        print('PASS')
    else:
        print('FAIL')
        exit()

t('operator +','1234+4321','5555')
t('operator -','9999-1111','8888')
t('operator *','12345*12345','152399025')
t('operator /','222/111','2')
t('operator ^','9^2','81')
t('operator precedens','9^2*2+8/4-2','162')
t('balanced ()','(45+45)/(8+1)','10')
c.calc('a=5')
t('variable assignment','a','5')
c.calc('a=6')
t('variable reassignment','a','6')
c.calc('add(a,b) = a+b')
t('function definition','add(1,2)','3')
t('hex conversion','0xfF-0x01','254')
t('hex display','hex 255','0xff')
t('unbalanced ()','(45+45)/(8+1','Error: Unbalanced parentheses')
t('unbalanced () in function def','unfunc(a,b=a*b','Error: Only alphanumericals allowed in constant names')
t('Empty argument name','unfun(a,,b)=a+b','Error: Argument name cannot be empty')
t('Number as argument name','unfun(1,b)=a+b','Error: Numbers may not be used as argument names')
t('Non alphanum in argument name','unfun(a.c,b)=a+b','Error: Only alphanumericals may be used in argument names')
print('All tests pass!')
