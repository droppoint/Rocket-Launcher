# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui
from Connector import Connector
import logging.handlers
import sys

possible_args = ["--debug", "--help", "-d", "-h"]

if __name__ == "__main__":
    
    def cleanup():
        #Перед выходом отключаем соединение
        logger.info("Cleanup operations initiated")
        connector.disconnect(status="405")
        logger.info("All cleanup operations completed")
    
    # logger system initialization
    logger = logging.getLogger('RocketOne')
    logger.setLevel(logging.DEBUG)
    #basic config here
    fh = logging.handlers.RotatingFileHandler('debug.log',
                                      mode='a',
                                      maxBytes=524288,
                                      backupCount=0)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('RocketOne. Launch.')
    app = QtGui.QApplication(sys.argv)

#debug system
    sys.argv.pop(0)
    for arg in sys.argv:
        #and startswith
        if arg not in possible_args:
            print "HELP!"
            break
    if "--debug" in sys.argv:
        print "CATCH"
    print sys.argv
    connector = Connector()
    connector.read_settings()
    # выполнить небольшую очистку перед выходом
    sys.exitfunc = cleanup
    sys.exit(app.exec_())