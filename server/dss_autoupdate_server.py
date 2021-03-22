#!/usr/bin python
# -*- coding: utf-8 -*-

import configparser
import socket
import threading
import logging
import os
import json
import time
from calc_md5 import get_md5

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s %(message)s"
)

CONFIG_FILE='config.ini'

response_data = {
    'response' : '',
    'data' : {}
}

def ReadConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

def InitSocket(ip, port, max_clients):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Attempt to bind IP/Port: %s:%d' % (ip, port))
    s.bind((ip, port))
    s.listen(max_clients)
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=ProccessThread, args=(sock, addr))
        t.start()
    pass

def ProccessThread(sock, addr):
    logging.info('Accept new connection from %s:%s...' % addr)
    config = ReadConfig()
    while True:
        try:
            data = json.loads(sock.recv(int(config['Server']['buffer_size'])))
            logging.info('Recieved data is : %s ...' % data)
            if not data:
                continue
            if data['request'] == 'handshake':
                SecurityCheck(sock, config, data['data']['security'])
            elif data['request'] == 'header':
                SendHeader(sock, config)
            elif data['request'] == 'package':
                SendPackage(set, config)
            elif data['request'] == 'exit':
                sock.close()
                break
        except Exception as e:
            logging.exception(e)
            sock.close()
            break
    logging.info('Connection from %s:%s closed.' % addr)


def SecurityCheck(sock, config, security):
    logging.info('Checking security code {%s} VS {%s} ...' % (config['Server']['security'], security))
    if config['Server']['security'] == security:
        response_data['response'] = 'connected'
        response_data['data'] = {}
    else:
        response_data['response'] = 'error'
        response_data['data'] = {}
    logging.info('Send SecurityCheck response %s ...' % response_data)
    sock.send(json.dumps(response_data).encode('utf-8'))

def SendHeader(sock, config):
    response_data['response'] = 'header'
    response_data['data'] = {
        'latest' : '',
        'size' : '',
        'md5' : ''
    }
    response_data['data']['latest'] = config['Server']['latest']
    filepath = config['Server']['path'] + os.path.sep + config['Server']['latest']
    response_data['data']['size'] = str(os.path.getsize(filepath))
    response_data['data']['md5'] = get_md5(filepath)
    logging.info('Send latest package header info: %s ...' % response_data)
    sock.send(json.dumps(response_data).encode('utf-8'))        

def SendPackage(sock, config):
    response_data = {
        'response' : '',
        'latest' : '',
        'size' : '',
        'md5' : ''
    }
    logging.info('Send latest package file: %s ...' % response_data)
    pass

def CloseConnection(sock):
    response_data = {
        'response' : '',
        'latest' : '',
        'size' : '',
        'md5' : ''
    }
    logging.info('Exit proccess ...')
    pass

if __name__=='__main__':
    config = ReadConfig()
    InitSocket(config['Server']['ip'], int(config['Server']['port']), int(config['Server']['max_clients']))
    pass

