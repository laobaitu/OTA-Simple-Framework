# -*- coding: utf-8 -*-

import configparser
import socket
import logging
import os

logging.basicConfig(level=logging.INFO)

CONFIG_FILE='config.ini'

def ReadConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def InitSocket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Connect to server/port: %s:%s ...' % (ip, port))
    sock.connect((ip, port))
    if RequestHeader(sock):
        RequestPackage(sock)
    RequestExit(sock)
    

def RequestHeader(sock):
    request_data = 'header'.encode('utf-8')
    logging.info('Send { %s } to server ...' % 'header')
    sock.send(request_data)
    return True

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
    config = ReadConfig()
    logging.info('start')
    InitSocket(config['Client']['server'], int(config['Client']['port']))
    pass

