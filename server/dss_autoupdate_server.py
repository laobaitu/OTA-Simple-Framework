#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import socket
import json
import threading
import logging
import os

logging.basicConfig(level=logging.INFO)

CONFIG_FILE='config.ini'

def ReadConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def InitSocket(ip, port, max_clients):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Attempt to bind IP/Port: %s:%d' % (ip, port))
    s.bind((ip, port))
    s.listen(max_clients)
    #while True:
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
        data = json.loads(sock.recv(1024))
        if 'request' not in data:
            continue
        if data['request'] == 'header':
            SendHeader(sock, config)
        elif data['request'] == 'package':
            SendPackage(sock, config)
        elif data['request'] == 'exit':
            sock.close()
            break
        else:
            continue
    pass

def SendHeader(sock, config):
    logging.info('Send latest package header info: %s ...' % (config['Server']['latest']))
    pass

def SendPackage(sock, config):
    logging.info('Send latest package file: %s ...' % (config['Server']['latest']))
    pass

if __name__=='__main__':
    config = ReadConfig()
    InitSocket(config['Server']['ip'], int(config['Server']['port']), int(config['Server']['max_clients']))
    pass

