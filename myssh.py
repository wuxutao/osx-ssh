#!/usr/bin/env python
# -*- coding: utf-8 -*-

"' Simple ssh client for OSX,better than default '"


import yaml
import base64
import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input

import paramiko
try:
    import interactive
except ImportError:
    from . import interactive


def createConnect(hostname,port,username,password):
    print hostname, port, username, password
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')
        client.connect(hostname, port, username, password)
        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        interactive.interactive_shell(chan)
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    stream = file('./myssh.yaml', 'r')
    configs = yaml.load(stream)

    if len(sys.argv) > 1:
        hostname = sys.argv[1]
    else:
        exit(1)

    for config in configs['servers']:
        print config
        if config['ip'] == hostname:
            print "find it"
            paramiko.util.log_to_file('demo_simple.log')
            createConnect(hostname,int(config['port']),config['user'],config['pwd'])
            break
