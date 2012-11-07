# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''

from Interface import Interface
from PySide import QtCore
from PySide.QtCore import QTimer, SIGNAL
from ConfigParser import ConfigParser
import logging
import os
import subprocess
import socket, asyncore, asynchat
import time
import sys

logger = logging.getLogger('RocketOne.Connector')

def looper():
    asyncore.poll()
    
def with_delay(func):
    time.sleep(0.001)
    return func

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
        if os.name == "nt":
            #Windows paths
            self.ovpnpath = 'C:\\Program Files (x86)\\OpenVPN'
            self.path = getBasePath() + '/'                 
            self.ovpnconfigpath = self.ovpnpath + '\\config\\'
            self.configfile = 'config.ini' # self.ovpnconfigpath +
            self.ovpnexe = self.ovpnpath + '\\bin\\openvpn.exe'
            self.traymsg = 'OpenVPN Connection Manager'
            logger.debug("Started on Windows")
        elif os.name == "posix":
            #Linux Paths
            self.ovpnpath = ''
            self.path = getBasePath() + '/'                 
            self.ovpnconfigpath = self.ovpnpath + '//home//alexei//SOLOWAY//'
            self.ovpnexe = self.ovpnpath + 'openvpn'
            self.configfile = 'config.ini'
            self.traymsg = 'OpenVPN Connection Manager'
            logger.debug("Started on Linux")
    
    # Интерфейс обрабатывающий входящие сигналы    
    @QtCore.Slot(str, str)
    def connect(self, login, passwd):
        self.port = 0
        port = self.getNextAvailablePort()
        if (not login) or (not passwd):
            return
        self.login = login
        self.password = passwd
        if self.view.remember(): # если галочка на месте
            self.write_settings(login, passwd, remember=True)
        else:
            self.write_settings("", "")

#        startupinfo = subprocess.STARTUPINFO()
#        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.process = subprocess.Popen([self.ovpnexe,
                          '--config', self.ovpnconfigpath + 'Soloway.ovpn',
                          '--management', '127.0.0.1', '{0}'.format(port),
                          '--management-query-passwords',
                          '--management-log-cache', '200',
                          '--management-hold'],
                          cwd=self.ovpnconfigpath)
#                          startupinfo=startupinfo)
        logger.debug("Subprocess started")
        self.timer = QTimer()
        self.timer.connect(SIGNAL("timeout()"), looper)
        self.timer.start(500)
        self.port = port
        self.atimer = QTimer()
        self.atimer.setSingleShot(True)
        self.atimer.timeout.connect(self.manage_process)
        self.atimer.start(1000)
        self.emit_signal("100") #connection started
        
    # Ай молодца, такой качественный костыль придумал
    def manage_process(self):
        self.sock = ManagementInterfaceHandler(self, '127.0.0.1', self.port)

    def read_settings(self):
        self.config = ConfigParser()
        self.config.read(self.configfile)
        if not self.config.has_section('Auth'):
            return
        login = self.config.get('Auth', 'User')
        password = self.config.get('Auth', 'Password')
        if self.config.has_section('Options'):
            remember = self.config.get('Options', 'Remember')
            self.view.set_remember(remember)
        else: 
            self.view.set_remember(False)
        if login and password:
            self.view.set_auth(login, password)
            self.login = login
            self.password = password
        
    def write_settings(self, login, passwd, remember=False):
        self.config = ConfigParser()
        self.config.add_section("Auth")
        self.config.set("Auth", "User", login)
        self.config.set("Auth", "Password", passwd)
        self.config.add_section("Options")
        self.config.set("Options", "Remember", remember)
        with open(self.configfile, 'wb') as configfile:
            self.config.write(configfile)
        
    @QtCore.Slot(str)    
    def disconnect(self, status="400"):
        logger.debug("Shutting down connection")
        self.port = 0
        self.emit_signal(status)
        if hasattr(self, "sock"):
            if self.sock:
                self.sock.send('signal SIGTERM\n')
                self.sock = None
        # уничтожает процесс если он еще не уничтожен
        if hasattr(self, "process"):
            if self.process:
                self.process.terminate()
                self.process = None
        if hasattr(self, "timer"):
            if self.timer:
                self.timer.stop()
                self.timer = None
#            self.sock.send('hold release\n')
    
    # Интерфейс испускающий сигналы 
    def emit_connected(self):
        logger.debug("Connection initiated")
        self.emit_signal("200")
        self.view.hide()
        
    def emit_signal(self, status):
        logger.debug("Emit signal " + status)
        self.view.emit_signal(status)
    
    def got_log_line(self, line):
        """Called from ManagementInterfaceHandler when new log line is received."""
#        print 'got log line: "{0}"'.format(line)
#        self.logbuf.append(line)
#        if self.logdlg != None:
#            self.logdlg.AppendText(line)
        pass

    def got_state_line(self, line):
        """Called from ManagementInterfaceHandler when new line describing current OpenVPN's state is received."""
#        print 'got state line: "{0}"'.format(line)
        list = line.split(',', 2)
        state = list[1]
        if state == 'CONNECTED':
            self.emit_connected()
        elif state == 'TCP_CONNECT':
            self.emit_signal("102")
        elif state == 'AUTH':
            self.emit_signal("103")
        elif state == 'GET_CONFIG':
            self.emit_signal("104")
        elif state == 'ASSIGN_IP':
            self.emit_signal("105")
            
    
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
        self.connector = connector
        self.port = port
        self.buf = ""
        self.set_terminator('\r\n')
#        from connection
        self.logger = logging.getLogger("RocketOne.ManagementInterfaceHandler")
        self.logger.debug("Start")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((addr, port))
        
    def handle_connect(self):
        asynchat.async_chat.handle_connect(self)
    
    def handle_error(self):
        self.logger.error("Connection error")
        self.close()
        raise
        
    def handle_close(self):
        self.logger.debug("Closing socket")
        self.buf = None
        self.close()
        asynchat.async_chat.handle_close(self)
    
    def collect_incoming_data(self, data):
#        print 'collect_incoming_data ({0}) data: "{1}"'.format(self.port, data)
        self.buf += data
#        logger.info(data)
        
    def found_terminator(self):
        if self.buf.startswith('>HOLD:Waiting for hold release'):
            with_delay(self.push('log on all\r\n')) # enable logging and dump current log contents
            with_delay(self.push('state on all\r\n')) # ask openvpn to automatically report its state and show current
            with_delay(self.push('hold release\r\n')) # tell openvpn to continue its start procedure
        elif self.buf.startswith('>FATAL:'):
            self.connector.disconnect(status="400")
        elif self.buf.startswith(">PASSWORD:Need 'Auth'"):
            with_delay(self.push('username \"Auth\" \"{0}\"\r\n'.format(self.connector.login)))
            with_delay(self.push('password \"Auth\" \"{0}\"\r\n'.format(self.connector.password)))
        elif self.buf.startswith('>PASSWORD:Verification Failed:'):
            self.connector.disconnect(status="403")
        elif self.buf.startswith('>LOG:'):
            self.connector.got_log_line(self.buf[5:]) # Пропускает LOG:
        elif self.buf.startswith('>STATE:'):
            self.connector.got_state_line(self.buf[7:]) # Пропускает STATE:
        self.buf = ""
    
# 'enum' of connection states
(disconnected, failed, connecting, disconnecting, connected) = range(5)

def getBasePath():
    if hasattr(sys, "frozen") and sys.frozen == "windows_exe":
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))
