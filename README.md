# WTFZOMFG-Interpreter
An interpreter made in python for the [WTFZOMFG esolang](https://esolangs.org/wiki/WTFZOMFG), with a focus on functional programming. It is written for the ATP course and has all of the must-haves of the assignment and more.

# WTFZOMFG explanation
## Brainfuck
WTFZOMFG is based on brainfuck, in the way that it uses simple commands to manipulate the memory.

## Memory
The memory of WTFZOMFG is an infinite row of memory cells. These cells can hold an integer or a character. The default cell that is written to is the first cell in the memory, cell 0. To select a different cell, we need to make use of the [pointer](#pointer).

## Pointer
The pointer of the program points to a single cell in the memory. We can manipulate the pointer by moving it one to the right or left of the memory cells. In WTFZOMFG it is also possible to jump the pointer to a specific cell. 

Note that when jumping to a cell, that the numbering of cells starts at 0, so the first cell in memory is cell 0, the second cell in memory is cell 1, the third cell in memory is cell 2, and so on. 
# Video 
For a quick overview of the code you are referred to the video below, which can be found [here](https://www.youtube.com/watch?v=ItVkOeLZ-S0) or below. Not everything could be shown in the video, for example there was no more time to discuss writing WTFZOMFG code yourself, but the [example file](./example.wtf) is quite extensive in its comments.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=ItVkOeLZ-S0
" target="_blank"><img src="http://img.youtube.com/vi/ItVkOeLZ-S0/0.jpg" 
alt="WTFZOMFG Interpreter" width="100%"/></a>

# Running a file
To interpret a file using the interpreter is simple as only two commands are needed after the repository has been cloned. To run a file type the following in the console:
```shell
python ./main.py -f [filename] -m [amount of memory cells] -e [ignore errors, optional]
```
So to run example.wtf type in the following:
```shell
python ./main.py -f ./example.wtf -m 10 -e
```
The -e flag is to ignore the errors that are generated when parsing or lexing the file. Errors generated while executing the code will be returned at the end of the execution phase.

# Assignment requirements
The assignment requirements have been split into two sections, the must-haves, and the should-haves.

## Must-haves
- Classes in the form of data objects
- Inheritance with the errors
- Object printing by implementing `__repr__` and `__str__`
- Private variables in the error objects
- A decorator to see how many times execute was called (this can be used to determine the needed recursion depth)
- Programmed in a functional programming style
- Type annotation in the functions (later this was specified as not being necessary for the comments)
- At least 3 uses of higher-order functions such as map and filter.

## Should haves
- Simple error messaging when appropriate (see [errors](#errors) for more info)
- A simple debug command `w` to use in your WTFZOMFG code to visualize the pointer location and the memory at that time
- Advanced features like comments, I/O support, arithmetic, and program flow control
- A video as discussed [here](#video)


# Errors
The pointer to the memory starts at 0. So if you have 5 memory cells, they are numbered 0, 1, 2, 3, 4

# Writing WTFZOMFG code
If you are ever confused to what each command does, please also refer to the [esolang wiki page on WTFZOMFG](https://esolangs.org/wiki/WTFZOMFG)

## Commenting
Commenting is fairly simple in WTFZOMFG. To do a single line comment use the `#` command. Everything following this until a new line is considered a comment.

Multi-line comments are also supported. Anything between `[` and `]` is considered a comment. The nesting of multi-line comments is not supported.

```
# This is a single line comment
[This is a multi-line comment]
```

## Printing
WTFZOMFG supports two types of printing: printing a single character by using a `.` followed by a character, or by placing what you want to print between a `'` and a `"`.
```
.H .i .\n    # Printing the characters h, i and a newline
'Hi\n"       # Printing the line Hi and the newline
```

Note that you cannot print a single space character using the print single character command, use the following instead:
```
' "
```

## Input Output
To input a character into a cell, use a '^', and to print the cell value as a character, use a `v`. To input a number into a cell use a `/`, and to print the cell value as a number, use a `\`.

```
'Input a character: " ^ v .\n    # Input a character and print input
'Input a number: " / \ .\n       # Input a number and print input
```
## Cell manipulation
There are several ways to change the value of a cell. These are more easily described in code:
```
=0        # Set the cell value to 0
+ + +     # Increase cell value by 3
- - -     # Increase cell value by 3 
=5 ~-2    # Set the cell to 5 and increase the cell value by -2
| w |     # Set cell from 3 to 0 and set it to 1
& %4      # Copy the cell value of 1 to the second cell 
          # and copy it to the cell at the 4th position, cell 5 
=87 @-    # Set the value to 87 and subtract the ASCII value of '-' (45)
```

## Pointer manipulation
Moving a pointer can be done in several ways. One to the left `<` or right `>`, by selecting what cell number `_<n>`, or by moving relative to the current cell `*<n>`. The last one can be done with a negative number to move to the left. 

```
> >      # Move the pointer 2 to the right
<        # Move the pointer one to the left
_7 *2    # Move the pointer to cell number 7 and move it 2 to the right
```

## Arithmetic
WTFZOMFG supports four different types of arithmetic: addition `a`, subtraction `s`, multiplication `m`, and division `d`. This is done by using the value at the current cell and the cell to the right and applying the operator. The result will be stored in the currently selected cell.

```
=6 & a      # Set cell to 6, copy to the right and add them together
> =2 < s    # Move pointer to the right, set cell to 2, 
            # move the pointer back and subtract the second cell from the first 
> =3 < m    # Set the cell at the pointer to the value of 3 and multiply the first cell with the second
& d         # Copy the first cell value to the right and divide the first cell value by the second
```
Note that a division by 0 will be handled as an error and thus ignored.
## Looping
Then the start loop character `(` is read, and the current cell value is not a 0, it will start a loop until the corresponding end loop character `)` is found, and the end of the loop, the program will check the value again and loop if it is not 0. WTFZOMFG supports nested while loops.

```
=5                         # Set value to 5
(                          # Start outer while loop if the value at the current cell is not 0
    'Loops Left: "         # Print 'Loops Left:'
    v -                    # Print amount of loops left and decrease amount
    >                      # Shift pointer one to the right
    + + +                  # Increase pointer value by 3
    ' Small countdown "    # Print 'Small countdown'
    (                      # Start inner while loop if the value at the current cell is not 0
        - v ' "            # Decrease value, print value, and print a space
    )                      # End of the inner while loop
    < .\n                  # Move pointer one to the left and print a newline
)                          # End of the outer while loop
```
## Goto
To make use of a Goto label, you need to declare the label somewhere in your code by using the `;` command. This label can be found from anywhere in the WTFZOMFG code. To go to a label use the `:` command. 

To use a conditional goto, use the `?` command to jump if the current cell value is not 0. To go to a label is the current label is a zero, use the `!` command. 
```
:Start                            # Declare the Start label 
'Go to start? 0 for no, 
anything else for yes: " / .\n    # Ask for user input
?Start                            # If the value at the cell is not a 0, go to Start 
                                  # label declared at the top
!Skip                             # If the value at the cell is a 0, go to Skip label

'This will be skipped"            # This line will be skipped because of the label jump

;Skip                             # Declare the Skip label
```
## If
To declare the start of an if statement, use the `{` command. If the current cell value is not zero, the code until the `}` command will be executed. If the current value is zero, the code will be skipped.

An if else statement would look like this:
```
{ [If statement commands] } | { [Else statement commands] }
```

If statements can be used for condigional branching:
```
;Start                            # Declare Start label
'Go to start? 0 for no, 
anything else for yes: " / .\n    # Ask for user input
{ :Start }                        # If the value is not 0 go to start label
|                                 # Flip value from 1 to 0 or ther way around
{ :End }                          # If value is not 0 Go to End label

'This will also be skipped"       # This line will be skipped because of the label jump

;End                              # Declare End label
```
## Debug
A very valuable command that I added to the is the `w` command. It prints the current pointer value and the memory as a list. The code `=5 > > - - _6 =3 & *-3 w` run using a memory length 10 10 will print this:
```
3 [5, 0, -2, 0, 0, 0, 3, 3, 0, 0]
```
