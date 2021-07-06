# PyLine
This is a custom python terminal with function saving, python intergrated dynamic functions, and more.
The commands available so far are:

# Syntax
The syntax for PyLine is simple.

<h3>Python</h3>
```
function(parameter, parameter)
```python

<h3>PyLine</h3>
~~~
function parameter parameter
~~~

# Commands
() = parameters  
  
commands - shows all commands in the current terminal  
create (name, params) - creates a python function saved in a file for the current terminal  
edit (command) - edits command  
family (command, type, command2) - type can be parent or child. Used for subcommands  
hi (text) - says 'HELLO' and then text  
hi lower - says 'hello'  
terminal (terminal) - changes terminal or creates a new one  
terminals - shows terminals  
delterm (terminal) - deletes terminal  
delete (command) - deletes command  
stop - exits PyLine  

# Requirements

Python 3.9.1 - https://www.python.org/downloads/release/python-391/  

PyMation - 'pip install pymation'