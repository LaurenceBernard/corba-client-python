#!/usr/bin/env python

import sys
from omniORB import CORBA
import CosNaming
import mainfiles

# Initialise the ORB
sys.argv.extend(("-ORBInitRef", "NameService=corbaname::localhost"))
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

# Invoke the echoString operation
message = "Mehdi"
result = eo.start(message)
