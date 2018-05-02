#!/usr/bin/env python

import sys
from omniORB import CORBA
import CosNaming
import mainfiles

# Initialise the ORB
sys.argv.extend(("-ORBInitRef", "NameService=corbaname::localhost:1050"))
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)


# Resolve the name "test.my_context/ExampleEcho.Object"
name = [CosNaming.NameComponent("HangmanGame", "")]

try:
    obj = rootContext.resolve(name)

except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

#Narrow the object to an mainfiles::Hangman
eo = obj._narrow(mainfiles.Hangman)

if eo is None:
    print "Object reference is not an Example::Echo"
    sys.exit(1)

print "WELCOME TO HANGMAN GAME"

# Invoke the echoString operation
name = raw_input("What is your name? ")
result = eo.start(name)

length = eo.length(name)

format_list = [name, length]
print "Hello {}. You must guess a word with {} character".format(*format_list)

guessed = ""
letters = ""
while True:
    letter = raw_input("Please enter a letter? ")

    if letter is None or len(letter) > 1:
        print "you should enter 1 character in each phase only"

    res = eo.play(name, letter)

    letters += letter + " - "


    #guess correctly
    if res == 2:
        print "'{}' is a correct guess".format(letter)
        guessed = eo.guessedWord(name)
        print "your present guesses are: ", guessed
        print "======================="
        print ""
        continue

    if res == 3:
        print "'{}' is a wrong guess".format(letter)
        guessed = eo.guessedWord(name)
        print "your present guesses are: ", guessed
        print "======================="
        print ""
        continue

    if res == 4:
        print ""
        print ""
        print "GAME OVER"
        sys.exit()

    if res == 5:
        print ""
        print ""
        print "WOOOOOOOOOOOAAAAAAA WINNER"
        sys.exit()






	


