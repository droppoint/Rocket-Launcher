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
import sys

class Connector():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        logger = logging.getLogger('RocketOne.Connector')
        logger.info("Connector start")
        self.view = Interface(self)
        # Пути до OpenVPN
        self.ovpnpath = 'C:\\Program Files (x86)\\OpenVPN'
        self.path = getBasePath() + '/'                 
        self.ovpnconfigpath = self.ovpnpath + '\\config'
        self.ovpnexe = self.ovpnpath + '\\bin\\openvpn.exe'
        self.traymsg = 'OpenVPN Connection Manager'
        #connection
        self.connection = Connection('Soloway')
    
    # Интерфейс обрабатывающий входящие сигналы    
    @QtCore.Slot(str, str)
    def connect(self, word1, word2):
        print "connecting"
        startupinfo = subprocess.STARTUPINFO()
        port = self.getNextAvailablePort()
        subprocess.Popen([self.ovpnexe,
                          '--config', self.ovpnconfigpath + '\\' + self.connection.name + '.ovpn',
                          '--management', '127.0.0.1', '{0}'.format(port),
                          '--management-query-passwords',
                          '--management-log-cache', '200',
                          '--management-hold'],
                          cwd=self.ovpnconfigpath,
                          startupinfo=startupinfo)
        self.connection.sock = ManagementInterfaceHandler(self, '127.0.0.1', port)
        self.connection.port = port
        self.setConnState(index, connecting)
        self.updateConnection(index)
        self.updateToolbar(index)
        print startupinfo

        
    def disconnect(self):
        print "disconnecting"
    
    # Интерфейс испускающий сигналы 
    def emit_connected(self):
        self.view.emit_signal("200")
    
    #Мясцо
    def getNextAvailablePort(self):
        """Returns next minimal unused port starting from 10598."""
        minport = 10598
        found = False
        while not found:
            found = True
            if self.connection.port != 0:
                if self.connection.port == minport:
                    found = False
                    minport += 1
                    break
        return minport

class ManagementInterfaceHandler(asynchat.async_chat):
    def __init__(self, mainwnd, addr, port):
        asynchat.async_chat.__init__(self)
        #print 'ManagementInterfaceHandler construct'
        self.mainwnd = mainwnd
        self.port = port
        self.buf = ''
        self.set_terminator('\n')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((addr, port))
        
    def handle_connect(self):
        #print 'handle_connect ({0})'.format(self.port)
        asynchat.async_chat.handle_connect(self)
        
    def handle_close(self):
        #print 'handle_close'
        self.mainwnd.Disconnected(self.port)
        asynchat.async_chat.handle_close(self)
    
    def collect_incoming_data(self, data):
        #print 'collect_incoming_data ({0}) data: "{1}"'.format(self.port, data)
        self.buf += data
        
    def found_terminator(self):
        #print 'found_terminator ({0}) buf: "{1}"'.format(self.port, self.buf)
        if self.buf.startswith(">PASSWORD:Need 'Auth'"):
            authdlg = AuthDlg(self.mainwnd)
            if authdlg.ShowModal() == wx.ID_OK:
                username = authdlg.username.GetValue()
                password = authdlg.password.GetValue()
                self.send('username "Auth" {0}\n'.format(username))
                self.send('password "Auth" "{0}"\n'.format(escapePassword(password)))
            authdlg.Destroy()
        elif self.buf.startswith('>HOLD:Waiting for hold release'):
            self.send('log on all\n') # enable logging and dump current log contents
            self.send('state on all\n') # ask openvpn to automatically report its state and show current
            self.send('hold release\n') # tell openvpn to continue its start procedure
        elif self.buf.startswith('>LOG:'):
            self.mainwnd.GotLogLine(self.port, self.buf[5:])
        elif self.buf.startswith('>STATE:'):
            self.mainwnd.GotStateLine(self.port, self.buf[7:])
        self.buf = ''
    
# 'enum' of connection states
(disconnected, failed, connecting, disconnecting, connected) = range(5)

class Connection(object):
    def __init__(self, name):
        self.name = name
        self.state = disconnected # do not set this field directly, use MainWindow.setConnState()
        self.sock = None # ManagementInterfaceHandler
        self.port = 0
        self.logbuf = []
        self.logdlg = None # LogDlg
    def stateString(self):
        if self.state == disconnected:
            return 'Disconnected'
        elif self.state == failed:
            return 'Error'
        elif self.state == connecting:
            return 'Connecting'
        elif self.state == disconnecting:
            return 'Disconnecting'
        elif self.state == connected:
            return 'Connected'
        else:
            return 'Error'

def getBasePath():
    if hasattr(sys, "frozen") and sys.frozen == "windows_exe":
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))