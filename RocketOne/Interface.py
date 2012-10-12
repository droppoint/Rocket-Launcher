# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui, QtDeclarative
import logging

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
        self.rootObject.messageAcceptance.connect(self.connector.connect)
#        self.rootObject.signalize('200')

        self.show()
