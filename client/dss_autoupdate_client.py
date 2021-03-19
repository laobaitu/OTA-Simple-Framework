#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import socket
import json
import logging
import os

logging.basicConfig(level=logging.INFO)

CONFIG_FILE='config.ini'

request_data = {
    'request' : None
}

def ReadConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def InitSocket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    if RequestHeader(sock):
        RequestPackage(sock)
    RequestExit(sock)
    

def RequestHeader(sock):
    request_data['request'] = 'header'
    sock.send(json.dumps(request_data))
    return True

def RequestPackage(sock):
    request_data['request'] = 'package'
    sock.send(json.dumps(request_data))
    return

def RequestExit(sock):
    request_data['request'] = 'exit'
    sock.send(json.dumps(request_data))
    pass

if __name__=='__main__':
    config = ReadConfig()
    InitSocket(config['Client']['ip'], int(config['Client']['port']))
    pass

