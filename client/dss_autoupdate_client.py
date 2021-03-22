# -*- coding: utf-8 -*-

import configparser
import socket
import logging
import json
import os
import time
from calc_md5 import get_md5

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Connect to server/port: %s:%s ...' % (ip, port))
    sock.connect((ip, port))

    if not RequestSecurity(sock, config):
        logging.info('Security check failed, close the connection ...')
        RequestExit(sock)
        return
    
    if not RequestHeader(sock, config):
        RequestExit(sock)
        return

    if not RequestPackage(sock, config):
        RequestExit(sock)
        return

    RequestExit(sock)

    AfterProccess(config)

def RequestSecurity(sock, config):
    buffer_size = int(config['Client']['buffer_size'])
    security = config['Client']['security']
    request_data['request'] = 'handshake'
    request_data['data'] = {'security' : security }
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    response = json.loads(sock.recv(buffer_size))
    logging.info('Response from server is: %s ...' % response) 

    if response['response'] == 'connected':
        return True
    else:
        return False

def RequestHeader(sock, config):
    buffer_size = int(config['Client']['buffer_size'])
    local_latest = config['Client']['latest']
    request_data['request'] = 'header'
    request_data['data'] = {}
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    response = json.loads(sock.recv(buffer_size))
    logging.info('Response from server is: %s ...' % response)

    if response['response'] == 'header':
        logging.info('Current version is: %s ...' % local_latest)   
        if response['data']['latest'] == local_latest:
            logging.info('Already the latest version, ignore...')
            return False
        else:
            logging.info('Upgrade available. Latest is: %s ...' % response['data']['latest']) 
            ans = input('Do you want to upgrade to latest? (y/n)')
            if ans == 'y':  
                logging.info('Ready to upgrade soon...')
                return True
            else:
                logging.info('Upgrade skipped by user...')
                return False
    else:
        logging.info('Response error, ignore...')
        return False

def RequestPackage(sock, config):
    buffer_size = int(config['Client']['buffer_size'])
    path = config['Client']['path']
    request_data['request'] = 'package'
    request_data['data'] = {}
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    response = json.loads(sock.recv(buffer_size))
    logging.info('Response from server is: %s ...' % response)
    
    filepath = path + os.path.sep + response['data']['latest']
    file_size = int(response['data']['size'])
    md5 = response['data']['md5']

    time.sleep(1)

    with open(filepath, 'wb') as fp:
        recieved_size = 0
        while recieved_size < file_size:
            data = sock.recv(buffer_size)
            fp.write(data)
            recieved_size += len(data)
            logging.info('Package size %d out of %d recieved...' % (recieved_size, file_size))
    
    if get_md5(filepath) == md5:
        logging.info('MD5 check success. Latest package is %s ...' % filepath)
        config['Client']['latest'] = response['data']['latest']
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        return True
    else:
        logging.info('MD5 check failed, remove the temporary file ...')
        os.remove(filepath)
        return False 

def RequestExit(sock):
    request_data['request'] = 'exit'
    request_data['data'] = {}
    logging.info('Send { %s } to server ...' % request_data)
    sock.send(json.dumps(request_data).encode('utf-8'))
    sock.close()

def AfterProccess(config):
    logging.info(str(config))
    pass

if __name__=='__main__':    
    InitSocket()
    pass

