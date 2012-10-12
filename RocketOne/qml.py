# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui
import logging.handlers
from Connector import Connector
import sys


#borderless
#view.setWindowFlags(QtCore.Qt.FramelessWindowHint)

#view.rootContext().setContextProperty('provider', provider)

#findchild

#signals connections
#rootObject.messageAcceptance.connect(printed)


#con = Console()
#context = view.rootContext()
#context.setContextProperty("con", con)

if __name__ == "__main__":
    # logger system initialization
    logger = logging.getLogger('RocketOne')
    logger.setLevel(logging.DEBUG)
    #basic config here
    fh = logging.handlers.RotatingFileHandler('debug.log',
                                      mode='w',
                                      maxBytes=524288,
                                      backupCount=1)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('RocketOne. Launch.')

    app = QtGui.QApplication(sys.argv)
    if "-debug" in sys.argv:
        print "CATCH"
    print sys.argv

    controller = Connector()

    sys.exit(app.exec_())