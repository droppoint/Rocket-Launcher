# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui, QtDeclarative
from PySide import QtSvg

import sys

app = QtGui.QApplication(sys.argv)


class Provider(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(unicode, result='QVariant')
    def get_data(self, something):
        print 'get_data(', something, ') called'


def printed():
    print "signal recieved"


class Console(QtCore.QObject):
    @QtCore.Slot(str)
    def outputStr(self, s):
        print s



#provider = Provider()

view = QtDeclarative.QDeclarativeView()

#borderless
view.setWindowFlags(QtCore.Qt.FramelessWindowHint)

#view.rootContext().setContextProperty('provider', provider)
view.setSource('../QML/RocketLauncher.qml')

#findchild

rootObject = view.rootObject()
rootObject.messageAcceptance.connect(printed)
#connecting to the signal
rootObject.signalize('Signal sended')

con = Console()
context = view.rootContext()
context.setContextProperty("con", con)
view.show()

sys.exit(app.exec_())