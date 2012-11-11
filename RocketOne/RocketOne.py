# -*- coding: UTF-8 -*-
'''RocketOne Launcher

RocketOne Launcher is a graphical front-end application for OpenVPN on Windows
and Linux. Build especially for RocketOne Team by Alex Partilov.
'''
from PySide import QtGui
from Connector import Connector
import logging.handlers
import sys

if __name__ == "__main__":
    
    def cleanup():
        # Disconnecting before exit
        logger.debug("Cleanup operations initiated")
        connector.disconnect(status="405")
        connector.view.close()
        logger.debug("All cleanup operations completed")
        
    
    # Logging system initialization
#    sys.stdout = open("log.txt", "a+")
#    sys.stderr = open("errors.txt", "a+") 
    logger = logging.getLogger('RocketOne')
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler('debug.log',
                                      mode='a',
                                      maxBytes=524288,
                                      backupCount=0)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Launch')
    app = QtGui.QApplication(sys.argv)
    
    connector = Connector()
    connector.read_settings()
    # Perform some cleanup before exit
    sys.exitfunc = cleanup
    sys.exit(app.exec_())