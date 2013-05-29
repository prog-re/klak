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


def getHelp(inp):
    topic = (inp.split('help'))[1]
    if topic == '':
        return """Help is available for:
usage
quickstart
operators
builtins
constants
functions

type "help topic" to display the help text for that topic"""
    elif topic == 'usage':
        return """Klak is intended to replace the desktop calculator that comes with your operating system. Typically this calculator will try to look and feel like a real desk calculator while Klak will focus on actually calculating things. Klak is not intended to be a replacement for advanced math programs like Maple or Matlab. If you need to do anything more complex than simple arithmetic you should use one of those systems instead. 

History:
You always have access to the all calculations that you have preformed previously. Hit the "up" key on your keyboard to flip through the history. The "down" key will get you back again.     

Numbers:
Klak will accept numbers in either decimal format (base 10, like 3.1415) or hex format (base 16, like 0xF1B6). Only integers can be entered in HEX format. The result will always be presented as a decimal number.

Convert to HEX:
The special function hex() will let you view a number or the result of a calculation in hex format. When use the hex() function must be the outermost function (first on the line).

Editing:
Copying and pasting using the mouse and Ctrl-c and Ctrl-v works like expected.
"""
    elif topic == 'quickstart':
        return """Quickstart examples:
Add: 23.45+678.9
Subtract: 123-34.56
Multiply: 2*3
Divide: 42/2
Power: 23^4
Defining constant: a=4
Using constant: (5^2)*pi
Using builtin function: sin(2)
Defining function: add(a,b) = a+b
"""
    elif topic == 'operators':
        return """The klak operators are: 
'+': Used for addition (34+567.8). 
'-': Used for subtraction (54-32.1).
'*': Used for multiplication (12*34.5).
'/': Used for division (76/54).
'^': Used for power (2^3).
"""
    elif topic == 'builtins':
        return """Klak has some built in functions:
Logarithms:
    ln(x): Returns the natural logarithm (base e) of the argument x.
    log(x): Returns the base 10 logarithm  of the argument x.
Trig:
    sin(x): Returns the sine part of the angle x (x is in radians).
    cos(x): Returns the cosine part of the angle x (x is in radians)
    tan(x): Returns the tangent given the angle x (x is in radians)
"""
    elif topic == 'constants':
        return """Klak lets you define constants that you can use in calculations. Simply type the name of the constant you wish to define followed by the '=' character and then the numerical value that you want the name to represent:

myPi = 3.14

You can also use the result of calculations to define constants:

myPi = 22/7

The constant 'ans' is automatically defined as the result of the latest successful calculation.

1+2
3
ans+1
4

The constants 'pi' and 'e' are pre-defined by Klak to pretty good approximations of pi and e."""
    elif topic == 'functions':
        return """Klak lets you define your own functions for calculations that you need to repeat many times. To define a function, type the name of the function you wish to define followed by the names for the parameters that you want to use enclosed in a pair of parentheses. This forms the naming part of the function definition. Conclude this part with the '=' character. Then write the calculation you wish the function to preform, using the named parameters:

myRes(volts,amps) = volts/amps

Then the new function can be used:

myRes(12,2)
6
  
"""
    elif topic == 'warranty':
        return """THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Please refer to the Gnu Genral Public License V3 in the file "LICENSE" for the full licence of this program. If the file was not distributed with your copy of the program, visit http://www.gnu.org/licenses/gpl.txt for the full license.  
"""
    elif topic == 'redist':
        return """ """
    else:
        return "Unknown help topic:%s" % (topic)
