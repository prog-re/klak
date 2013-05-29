# Klak - The simple calculator
## What is this?
Klak is intended to replace the desktop calculator that comes with your operating system. Typically this calculator will try to look and feel like a real desk calculator while Klak will focus on actually calculating things. Klak is not intended to be a replacement for advanced math programs like Maple or Matlab. If you need to do anything more complex than simple arithmetic you should use one of those systems instead. 
## How to run Klak

## How to use Klak
        
### Numbers
Klak will accept numbers in either decimal format (base 10, like 3.1415) or hex format (base 16, like 0xF1B6). Only integers can be entered in HEX format. The result will always be presented as a decimal number.

### Convert to HEX:
The special function hex() will let you view a number or the result of a calculation in hex format. When use the hex() function must be the outermost function (first on the line).

### Editing
Copying and pasting using the mouse and Ctrl-c and Ctrl-v works like expected.

### History
You always have access to the all calculations that you have preformed previously. Hit the "up" key on your keyboard to flip through the history. The "down" key will get you back again.     

### Quickstart
Quickstart examples:
Add: ´´23.45+678.9´´
Subtract: ´´123-34.56´´
Multiply: ´´2*3´´
Divide: ´´42/2´´
Power: ´´23^4´´
Defining constant: ´´a=4´´
Using constant: ´´(5^2)*pi´´
Using builtin function: ´´sin(2)´´
Defining function: ´´add(a,b) = a+b´´

### Operators
The klak operators are: 
- ´´+´´ Used for addition (34+567.8). 
- ´´-´´ Used for subtraction (54-32.1).
- ´´*´´ Used for multiplication (12*34.5).
- ´´/´´ Used for division (76/54).
- ´´^´´ Used for power (2^3).

### Builtins
Klak has some built in functions:
#### Logarithms
    ´´ln(x)´´ Returns the natural logarithm (base e) of the argument x.
    ´´log(x)´´ Returns the base 10 logarithm  of the argument x.
#### Trig
    ´´sin(x)´´ Returns the sine part of the angle x (x is in radians).
    ´´cos(x)´´ Returns the cosine part of the angle x (x is in radians)
    ´´tan(x)´´ Returns the tangent given the angle x (x is in radians)

### Constants
Klak lets you define constants that you can use in calculations. Simply type the name of the constant you wish to define followed by the ´´=´´ character and then the numerical value that you want the name to represent:

    myPi = 3.14

You can also use the result of calculations to define constants:

    myPi = 22/7

The constant ´´ans´´ is automatically defined as the result of the latest successful calculation.

    1+2
    3
    ans+1
    4

The constants 'pi' and 'e' are pre-defined by Klak to pretty good approximations of pi and e.
### Functions
Klak lets you define your own functions for calculations that you need to repeat many times. To define a function, type the name of the function you wish to define followed by the names for the parameters that you want to use enclosed in a pair of parentheses. This forms the naming part of the function definition. Conclude this part with the '=' character. Then write the calculation you wish the function to preform, using the named parameters:

    myRes(volts,amps) = volts/amps

Then the new function can be used:

    myRes(12,2)
    6

## Revison history
### 0.1
Initial release
 