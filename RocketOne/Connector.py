# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''

from Interface import Interface
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
        
    def connect(self):
        print "connecting"
        
    def cancel_connection(self):
        pass
    
    