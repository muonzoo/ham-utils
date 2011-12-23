| Copyright (c) 2011 `Alan Hawrylyshen`_
| Covered by the BSD License, see `LICENSE.txt`_.


Aether and Fldigi Logging Script
================================

Author : `Alan Hawrylyshen`_ (K2ACK_)

This script is designed to be called from an `fldigi`_ macro.
It will open a new QSO log in Aether_.

This script can be called from fldigi_ on a Mac_ platform using a macro button.

Note - this script is written in Python_, a powerful scripting
language that is installed on every Mac. You don't need to edit the
script or understand Python_ to make this work for you.

Here is the macro text I use in the fldigi_ macro.:


 <EXEC>$HOME/.fldigi/scripts/fldigi-aether-logger.py & </EXEC>

The above macro can be directly copied into your Log QSO Macro definition window in fldigi_.

Arguments
---------

--no-launch:
  Do not start Aether from the script - assume it is already running.

--test:
  Use internal test data to validate the script from the command line.

--launch:
  Force Aether to launch - default behavior.

--debug:
  Print out key information of script execution on stdout, will appear
  in fldigi window.


This presumes that this script is called fldigi-aether-logger.py AND
That this script is in $HOME/.fldigi/scripts with the execute bit set.

 chmod 755 $HOME/.fldigi/scripts/fldigi-aether-logger.py

for more:

 man  chmod

If you run this with --debug (modify the macro), you should see
useful debugging info in the transmit window.

If you run this from the command line to test, you can run with
--test and --debug to use the built in test data. You should see an
RTTY log entry created for W1AX.


This is a LONG way from complete, but it is working for now.

Best,
73
Alan
K2ACK_

.. _fldigi: http://www.w1hkj.com/Fldigi.html
.. _Alan Hawrylyshen: http://polyphase.ca/
.. _LICENSE.txt: http://github.com/muonzoo/ham-utils/blob/master/LICENSE.txt
.. _Mac: http://apple.com/mac/
.. _Aether: http://aetherlog.com/
.. _K2ACK: http://www.qrz.com/callsign.html?callsign=k2ack
.. _Python: http://www.python.org/
