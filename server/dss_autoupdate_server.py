#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import socket
import threading
import logging
import os
import time

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
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        
        logging.info('Recieved data is : %s ...' % (data.decode('utf-8')))
        if data.decode('utf-8') == 'header':
            SendHeader(sock, config)
        elif data.decode('utf-8') == 'package':
            SendPackage(sock, config)
        elif data.decode('utf-8') == 'exit':
            sock.close()
            break
        else:
            continue
    sock.close()
    logging.info('Connection from %s:%s closed.' % addr)

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

