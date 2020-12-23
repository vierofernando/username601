# Custom Framework for username601
A custom "framework" i made for this bot. You can use this framework!<br>
(not planning to be added to PyPI, sorry)<br>
This is the documentation and the examples.<br>

Several file snippets may be useful to you and you can use, such as:<br>
# Parser object

It parser the arguments in a command. And it is very simple.
```py
parser = Parser(args)
parser.parse()

# this method checks if AT LEAST the user added --argument, despite the value None or not.
if parser.has("argument"):
    print("WOW! YOU ADDED --argument !!!")

# getting the item means getting the value. if this doesn't exists, it returns None
value = parser["argument"]
if value is not None:
    print("THIS IS THE ARGUMENT YOU ADDED AFTER --argument: ", value)

# use this once you are not using the --argument. This dumps the argument and its values to parser.other
parser.shift("argument")
print("Here are the other arguments whice are not used: ", *parser.other)
```
**A simple code snippet of this can be found at this [Github Gist](https://gist.github.com/vierofernando/004372b352f106ba3a3ce8335b6e5b63)**
