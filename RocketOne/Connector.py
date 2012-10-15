# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''

from Interface import Interface
from PySide import QtCore
import logging

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
    
    # Интерфейс обрабатывающий входящие сигналы    
    @QtCore.Slot(str, str)
    def connect(self, word1, word2):
        print "connecting"
        print word1
        print word2
        
    def disconnect(self):
        print "disconnecting"
    
    # Интерфейс испускающий сигналы 
    def emit_connected(self):
        self.view.emit_signal("200")