#!/usr/bin/env python

# Copyright (C) 2011, Alan Hawrylyshen (K2ACK)
# All rights reserved.
#
# Contact : k2ack@polyphase.ca
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
# See README.rst file distributed with this script.
#
# Here is the macro text I use:
#
# <EXEC>$HOME/.fldigi/scripts/fldigi-aether-logger.py & </EXEC>
#
# If you run this with --debug (modify the macro), you should see
# useful debugging info in the transmit window.
#
# If you run this from the command line to test, you can run with
# --test and --debug to use the built in test data. You should see an
# RTTY log entry created for W1AX.
#

import os

debug=False
mandatory=False

fl_env_prefix='FLDIGI_'
def callsign_fmt(s): return s.strip()
def identity(x):     return x
def freq_fmt(s):     return "%11.7f"%(float(s)/1e6,)

def trace(message=None,force=False):
    if debug or force:
        import inspect
        print "TR: ",inspect.currentframe().f_back.f_lineno,
        if not message is None:
            print ':',message

# I tried to standardize the modes a little, you might want to just
# return s or modify this to be more sophisticated.

def mode_fmt(s):
    return s

# Pull things from the environment dict for logging.
# Examples:
#TR:  93 : FLDIGI_DIAL_FREQUENCY        :	14076000
#TR:  93 : FLDIGI_MODEM_LONG_NAME       :	MFSK-4
#TR:  93 : FLDIGI_AUDIO_FREQUENCY       :	3039
#TR:  93 : FLDIGI_LOG_RST_IN    :	In
#TR:  93 : FLDIGI_LOG_NAME      :	Name
#TR:  93 : FLDIGI_LOG_RST_OUT   :	Out
#TR:  93 : FLDIGI_LOG_FREQUENCY         :	14079.039
#TR:  93 : FLDIGI_MY_CALL       :	K2ACK
#TR:  93 : FLDIGI_LOG_TIME_OFF  :	1856
#TR:  93 : FLDIGI_LOG_QTH       :
#TR:  93 : FLDIGI_LOG_TIME_ON   :	1853
#TR:  93 : FLDIGI_MY_LOCATOR    :	CM86xx
#TR:  93 : FLDIGI_FREQUENCY     :	14079039
#TR:  93 : FLDIGI_LOG_LOCATOR   :
#TR:  93 : FLDIGI_VERSION       :	3.21.33
#TR:  93 : FLDIGI_MODEM         :	MFSK4
#TR:  93 : FLDIGI_LOG_CALL      :	N0CALL
#TR:  93 : FLDIGI_LOG_NOTES     :

def osa_preamble():
    return "tell application \"Aether\"\ntry\n\tactivate\n\ttell document 1\n\t\tset newQSO to make new qso\n\t\tset selection to newQSO\n"

def osa_set_callsign(code,prop,value):
    return osa_lookup_qso(osa_set_property(code,prop,value))

def osa_set_property(code,prop,value):
    return "%s\t\tset newQSO's %s to \"%s\"\n"%(code,prop,value,)

def osa_set_cb_property(code,prop,value):
    trace()
    return "%s\t\tset callbook's %s to \"%s\"\n"%(code,prop,value,)

def osa_lookup_qso(code):
    trace('osa_lookup_qso')
    return "%s\t\tlookup newQSO\n\t\tset callbook to newQSO's callbook info\n"%(code,)

def osa_postamble(code):
    return "%s\tend tell\n\ton error errMsg number errNum\n\t\tdisplay alert \"AppleScript Error\" message errMsg &  \" (\" & errNum & \")\" buttons {\"OK\"} default button \"OK\"\n\tend try\nend tell\n"%(code,)

def osa_collect_property(code, prop, value):
    return "%s\t\t\t--%s:%s\n"%(code,prop,value,)

def inform_aether(env,debug=False,launch=True):
    trace('inform_aether()')
    from os import system
    # QSO is a dict
    # using a template library seemed like overkill, but this is ugly
    if launch:
        trace('telling Finder to open Aether')
        system('open -a Aether')
        trace('post-open')

    pre_lookup_env_to_aether = {
                      fl_env_prefix + 'FREQUENCY' :
                       ( freq_fmt, osa_set_property, {'prop':'frequency'} ),
                      fl_env_prefix + 'MODEM' :
                       ( mode_fmt, osa_set_property, {'prop':'mode'}),
                      fl_env_prefix + 'LOG_RST_IN' :
                       (identity,osa_set_property , {'prop':'received rst'}),
                      fl_env_prefix + 'LOG_RST_OUT' :
                       (identity,osa_set_property,{'prop':'transmitted rst'}),
                      fl_env_prefix + 'LOG_TIME_ON' :
                       (identity,osa_collect_property,{'prop':'note'}),
                        }

    callsign_actions = {fl_env_prefix+'LOG_CALL':
                        (callsign_fmt,osa_set_callsign,{'prop':'callsign'})}

    post_lookup_env_to_aether = {
      fl_env_prefix + 'LOG_NOTES' :
      (identity,osa_collect_property,{'prop':'note'}),
      fl_env_prefix + 'LOG_MODEM_LONG_NAME' :
      (identity,osa_collect_property,{'prop':'note'}),
      fl_env_prefix + 'LOG_LOCATOR' :
      (identity,osa_set_cb_property,{'prop':'grid square'})
    }

    if debug:
        for k in env:
            if k[:len(fl_env_prefix)] == fl_env_prefix:
                trace('%s \t:\t%s'%(k,env[k],))

    script = osa_preamble()
    csp = False

    trace()

    for d in [ pre_lookup_env_to_aether,
               callsign_actions,
               post_lookup_env_to_aether ]:
        trace()
        for k in d:
            trace()
            if k in env:
                trace("processing %s"%(k,))
                e2a=d[k]
                trace(str(e2a[2]))
                script = e2a[1](code=script,
                                value = e2a[0](env[k]),**e2a[2])

    trace()
    script = osa_postamble(script)
    osacmd = "osascript << END\n%s\nEND"%(script,)
    trace(osacmd)
    rval = system(osacmd)
    trace(message='~inform_aether(%d)'%(rval,))
    return rval


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
    launch_arg = True

    d = environ
    trace()

    while len(argv) > 1:
        if argv[1] == '--test':
            if debug:
                trace("test mode enabled",force=True)
            d = test_dict()
        elif argv[1] == '--debug':
            debug = True
            trace(message="debugging mode enabled",force=True)
        elif argv[1] == '--launch':
            launch_arg = True
            trace('will launch aether')
        elif argv[1] == '--no-launch':
            trace('will not launch aether')
            launch_arg = False
        argv = argv[1:]
    trace('finished arg processing')
    inform_aether( d, launch=launch_arg,debug=debug)
    trace('exiting')
