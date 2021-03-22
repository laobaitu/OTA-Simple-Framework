# -*- coding: utf-8 -*-

import configparser
import socket
import logging
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s %(message)s"
)

CONFIG_FILE='config.ini'

request_data = {
    'request' : '',
    'data' : {}
}

def ReadConfig():
    logging.info('Reading configuration from: %s ...' % CONFIG_FILE)
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

def InitSocket():
    config = ReadConfig()
    ip = config['Client']['server']
    port = int(config['Client']['port'])
    security = config['Client']['security']
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Connect to server/port: %s:%s ...' % (ip, port))
    sock.connect((ip, port))

    RequestSecurity(sock, security)
    RequestHeader(sock, config['Client']['latest'])
   

def RequestSecurity(sock, security):
    request_data['request'] = 'handshake'
    request_data['data'] = {'security' : security }
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    response = json.loads(sock.recv(1024))
    logging.info('Response from server is: %s ...' % response) 

    if response['response'] == 'connected':
        return True
    else:
        return False

def RequestHeader(sock, local_latest):
    request_data['request'] = 'header'
    request_data['data'] = {}
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    response = json.loads(sock.recv(1024))
    logging.info('Response from server is: %s ...' % response)

    

def RequestPackage(sock):
    request_data = 'package'.encode('utf-8')
    logging.info('Send { %s } to server ...' % 'package')
    sock.send(request_data)
    return

def RequestExit(sock):
    request_data = 'exit'.encode('utf-8')
    logging.info('Send { %s } to server ...' % 'exit')
    sock.send(request_data)
    pass

if __name__=='__main__':    
    InitSocket()
    pass

