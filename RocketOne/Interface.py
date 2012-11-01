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
        
        self.createActions()
        self.createTrayIcon()
#        self.emit_signal("101")
        self.trayIcon.show()
        self.show()
        self.showMessage()
    
#    def closeEvent(self, event):
#        if self.trayIcon.isVisible():
#            QtGui.QMessageBox.information(self, "Systray",
#                    "The program will keep running in the system tray. To "
#                    "terminate the program, choose <b>Quit</b> in the "
#                    "context menu of the system tray entry.")
#            self.hide()
#            event.ignore()
    
    def remember(self):
        return self.rootObject.remember()
    
    def emit_signal(self, status):
        self.rootObject.signal(status)
    
    def set_auth(self, login, passwd):
        self.rootObject.set_auth(login, passwd)
    
    def set_remember(self, status):
        self.rootObject.set_remember(status)

    def createActions(self):
        self.disconnectAction = QtGui.QAction(u"Отключить", self,
                triggered=self.connector.disconnect)

        self.propertiesAction = QtGui.QAction(u"Настройки", self)
        self.quitAction = QtGui.QAction(u"Выход", self)
    
    def createTrayIcon(self):
         icon = QtGui.QIcon('../QML/images/trayicon_32px.svg')
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.disconnectAction)
         self.trayIconMenu.addAction(self.propertiesAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)
    
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setIcon(icon)
         self.trayIcon.setContextMenu(self.trayIconMenu)
         
    def showMessage(self):
        icon = QtGui.QSystemTrayIcon.MessageIcon(
                QtGui.QSystemTrayIcon.Information)
        self.trayIcon.showMessage(u"Подключено",
                u"Тестовое сообщение", icon,
                 1000)
