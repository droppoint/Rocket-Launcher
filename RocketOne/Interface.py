# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui, QtDeclarative
import logging

#borderless
#view.setWindowFlags(QtCore.Qt.FramelessWindowHint)
class Interface(QtDeclarative.QDeclarativeView):
    '''
    Connects with qml interface
    '''
    
    def __init__(self, connector):
        '''
        Constructor
        '''
        super(Interface, self).__init__()
        self.connector = connector
        self.setSource('../QML/RocketLauncher.qml')
        logger = logging.getLogger('RocketOne.Interface')
        logger.info("Interface start")
        #Подключение сигналов
        self.rootObject = self.rootObject()
        self.rootObject.cmd_connect.connect(self.connector.connect)
        self.rootObject.cmd_disconnect.connect(self.connector.disconnect)
        self.emit_signal("101")
        self.show()
        
    def emit_signal(self, status):
        self.rootObject.signal(status)
