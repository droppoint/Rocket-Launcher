# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''

from Interface import Interface
from PySide import QtCore
import logging
import os
import subprocess
import socket, asyncore, asynchat
import threading
import time
import sys

logger = logging.getLogger('RocketOne.Connector')

def zalooper():
    asyncore.loop(timeout=2)

class Connector():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.view = Interface(self)
        # Пути до OpenVPN
#        self.ovpnpath = 'C:\\Program Files (x86)\\OpenVPN'
#        self.path = getBasePath() + '/'                 
#        self.ovpnconfigpath = self.ovpnpath + '\\config'
#        self.ovpnexe = self.ovpnpath + '\\bin\\openvpn.exe'
#        self.traymsg = 'OpenVPN Connection Manager'

        #Linux Paths
        self.ovpnpath = ''
        self.path = getBasePath() + '/'                 
        self.ovpnconfigpath = self.ovpnpath + '//home//alexei//SOLOWAY//'
        self.ovpnexe = self.ovpnpath + 'openvpn'
        self.traymsg = 'OpenVPN Connection Manager'
        logger.info("Connector start")
    
    # Интерфейс обрабатывающий входящие сигналы    
    @QtCore.Slot(str, str)
    def connect(self, login, passwd):
        print "connecting"
        self.port = 0
        port = self.getNextAvailablePort()
        self.login = login
        self.password = passwd
        print login, passwd
        #startupinfo = subprocess.STARTUPINFO()
#        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.process = subprocess.Popen([self.ovpnexe,
                          '--config', self.ovpnconfigpath + 'Soloway.ovpn',
                          '--management', '127.0.0.1', '{0}'.format(port),
                          '--management-query-passwords',
                          '--management-log-cache', '200',
                          '--management-hold'],
                          cwd=self.ovpnconfigpath)
                          #startupinfo=startupinfo)
        self.emit_signal("100") #connection started
        time.sleep(1)
        self.sock = ManagementInterfaceHandler(self, '127.0.0.1', port)
        self.port = port
        self.logbuf = []
        self.logdlg = None
        evLoop = threading.Thread(target=zalooper)
        evLoop.setDaemon(True)
        evLoop.join()
        print "GO!!!"
#        print startupinfo

        
    def disconnect(self):
        logger.info("Shutting down connection")
        self.view.emit_signal(400)
        print "disconnect signal recieved"
        if hasattr(self, "sock"):
            self.sock.send('signal SIGTERM\n')
        # уничтожает процесс если он еще не уничтожен
        self.process.terminate()
#            self.sock.send('hold release\n')
    
    # Интерфейс испускающий сигналы 
    def emit_connected(self):
        logger.info("Connection initiated")
        self.view.emit_signal("200")
        self.view.hide()
        
    def emit_signal(self, status):
        logger.info("Emitted signal to qml")
        logger.info("SIGNAL " + status)
        self.view.emit_signal(status)
    
    def got_log_line(self, line):
        """Called from ManagementInterfaceHandler when new log line is received."""
        #print 'got log line: "{0}"'.format(line)
        self.logbuf.append(line)
        if self.logdlg != None:
            self.logdlg.AppendText(line)

    def got_state_line(self, line):
        """Called from ManagementInterfaceHandler when new line describing current OpenVPN's state is received."""
        #print 'got state line: "{0}"'.format(line)
        list = line.split(',', 2)
        state = list[1]
        if state == 'CONNECTED':
            self.emit_connected()
    
    #Мясцо
    def getNextAvailablePort(self):
        """Returns next minimal unused port starting from 10598."""
        minport = 10598
        found = False
        while not found:
            found = True
            if self.port != 0:
                if self.port == minport:
                    found = False
                    minport += 1
                    break
        return minport

class ManagementInterfaceHandler(asynchat.async_chat):
    def __init__(self, connector, addr, port):
        asynchat.async_chat.__init__(self)
        print addr, port
        self.connector = connector
        self.port = port
        self.buf = ''
        self.set_terminator('\n')
#        from connection
        logger.info("Management Interface Handler started")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((addr, port))
        
    def handle_connect(self):
        print 'handle_connect ({0})'.format(self.port)
        asynchat.async_chat.handle_connect(self)

        
    def handle_close(self):
        # emit signal disconnect
        self.connector.emit_signal("200")
        asynchat.async_chat.handle_close(self)
    
    def collect_incoming_data(self, data):
        print 'collect_incoming_data ({0}) data: "{1}"'.format(self.port, data)
        self.buf += data
        logger.info(data)
        
    def found_terminator(self):
#        print 'found_terminator ({0}) buf: "{1}"'.format(self.port, self.buf)
        if self.buf.startswith('>HOLD:Waiting for hold release'):
            self.send('log on all\n') # enable logging and dump current log contents
            self.send('state on all\n') # ask openvpn to automatically report its state and show current
            self.send('hold release\n') # tell openvpn to continue its start procedure
        elif self.buf.startswith('>FATAL:'):
            self.connector.emit_signal("400")
            self.connector.disconnect()
        elif self.buf.startswith(">PASSWORD:Need 'Auth'"):
            self.send('username "Auth" {0}\n'.format(self.connector.login))
            self.send('password "Auth" "{0}"\n'.format(self.connector.password))
        elif self.buf.startswith('>PASSWORD:Verification Failed:'):
            self.connector.emit_signal("403")
            self.connector.disconnect()
        elif self.buf.startswith('>LOG:'):
            self.connector.got_log_line(self.buf[5:]) # Пропускает LOG:
        elif self.buf.startswith('>STATE:'):
            self.connector.got_state_line(self.buf[7:]) # Пропускает STATE:
        self.buf = ''
    
# 'enum' of connection states
(disconnected, failed, connecting, disconnecting, connected) = range(5)

def getBasePath():
    if hasattr(sys, "frozen") and sys.frozen == "windows_exe":
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))
