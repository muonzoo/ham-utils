#!/usr/bin/env python

# Copyright (C) 2011, Alan Hawrylyshen (K2ACK)
# All rights reserved.
#
# Contact : k2ack@arrl.net
#

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING

# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#
# This script can be called from fldigi on a Mac platform using a macro
# button.
#
# Here is the macro text I use:
#
# <EXEC>$HOME/bin/fldigi-aether-logger.py</EXEC>
#
# This presumes that this script is called fldigi-aether-logger.py AND
# That this script is in $HOME/bin with the execute bit set.
#
#  chmod 755 ~/bin/fldigi-aether-logger.py
#
# man 1 chmod 
# for more.
#
# If you run this with --debug (modify the macro), you should see
# useful debugging info in the transmit window.
#
# If you run this from the command line to test, you can run with
# --test and --debug to use the built in test data. You should see an
# RTTY log entry created for W1AX.
#

import os

fl_env_prefix='FLDIGI_'

def identity(x):    return x
def freq_fmt(s):    return "%11.7g"%(float(s)/1e6,)







# I tried to standardize the modes a little, you might want to just
# return s or modify this to be more sophisticated.

def mode_fmt(s):
    if 'PSK' in s.upper():
        return 'PSK31'
    elif 'RTTY' in s.upper():
        return 'RTTY'
    else:
        return s


# Pull things from the environment dict for logging.
def env_to_dict(e,debug=False):
    env_to_aether = { fl_env_prefix + 'FREQUENCY' : ( 'freq', freq_fmt ),
                      fl_env_prefix + 'MODEM' :  ('mode', mode_fmt ),
                      fl_env_prefix + 'LOG_CALL' : ('call', identity ),
                      fl_env_prefix + 'LOG_RST_IN' : ('rst_in', identity),
                      fl_env_prefix + 'LOG_RST_OUT' : ('rst_out', identity),
                  }

    if debug:
        # show all env entries that start with the fldigi prefix
        for k in e:
            if k[:len(fl_env_prefix)] == fl_env_prefix:
                print k, " : ", e[k]

    simple_dict = dict()
    for k in env_to_aether:
        if e.has_key(k):
            # if the environ has the key, add it to our dict after processing with
            # the function specified in the env_to_aether table 
            simple_dict[env_to_aether[k][0]] = env_to_aether[k][1](e[k])
        else:
            # assume all the above are mandatory for now
            raise Exception('missing mandatory environment var',k)
    return simple_dict

def inform_aether(qso,debug=False):
    from os import system
    # QSO is a dict
    # using a template library seemed like overkill, but this is ugly
    osacmd = """osascript << END
tell application "Aether"
      try
		activate
		tell document 1
			set newQSO to make new qso with properties {callsign:"%s"}
			set selection to newQSO
			set newQSO's frequency to %s 
			set newQSO's mode to "%s"
                        set newQSO's transmitted rst to "%s"
                        set newQSO's received rst to "%s"
			lookup newQSO
		end tell
	on error errMsg number errNum
		display alert "AppleScript Error" message errMsg &  " (" & errNum & ")" buttons {"OK"} default button "OK"
	end try
end tell

END
"""
    osacmd = osacmd % (qso['call'], qso['freq'], qso['mode'],qso['rst_out'],qso['rst_in'],)
    if debug:
        print osacmd

    return system(osacmd)


# Used just for test processing, subst the environment for this, hard coded stuff
# Generate a reasonable dict.
def test_dict() :
    test_vals = { 'FREQUENCY' : '14070000', 'MODEM' : 'RTTY', 'LOG_CALL': 'W1AX',
                  'LOG_RST_IN' : '59', 'LOG_RST_OUT' : '45' }
    d = dict()
    for k in test_vals:
        d[fl_env_prefix+k] = test_vals[k]
    if debug:
        print d
    return d

if __name__ == '__main__':
    from os import environ
    from sys import argv

    debug = False

    d = environ

    while len(argv) > 1:
        if argv[1] == '--test':
            d = test_dict()
        elif argv[1] == '--debug':
            debug = True
        argv = argv[1:]

    inform_aether( env_to_dict(d,debug=debug), debug=debug)
