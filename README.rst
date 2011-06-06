Aether and Fldigi Logging Script
================================

Author : Alan Hawrylyshen
Call   : K2ACK

This script is designed to be called from an fldigi macro.

vvhttp://www.w1hkj.com/Fldigi.html


This script can be called from fldigi on a Mac platform using a macro  button.

Here is the macro text I use:

 <EXEC>$HOME/bin/fldigi-aether-logger.py</EXEC>

This presumes that this script is called fldigi-aether-logger.py AND
That this script is in $HOME/bin with the execute bit set.

  chmod 755 ~/bin/fldigi-aether-logger.py

man 1 chmod 
for more.

If you run this with --debug (modify the macro), you should see
useful debugging info in the transmit window.

If you run this from the command line to test, you can run with
--test and --debug to use the built in test data. You should see an
RTTY log entry created for W1AX.


This is a LONG way from complete, but it is working for now.

Best,
73
Alan
K2ACK

