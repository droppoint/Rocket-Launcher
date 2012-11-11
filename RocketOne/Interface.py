# -*- coding: UTF-8 -*-
'''
Created on 04.10.2012

@author: APartilov
'''
from PySide import QtCore, QtGui, QtDeclarative, QtSvg
import logging

SIGNALS_HASH = {
    "100" : "Подключение инициировано",
    "101" : "Открытие сокета",
    "102" : "Установка туннеля",
    "103" : "Авторизация",
    "104" : "Получение конфигурации",
    "105" : "Получение маршрутов",
    "200" : "Соединение установлено",
    "400" : "Разрыв соединения по неустановленой причине",
    "401" : "Сервер недоступен",
    "402" : "Учетная запись истекла",
    "403" : "Ошибка авторизации (Логин/Пароль не верны)",
    "404" : "Сервер принудительно разорвал соединение",
    "405" : "Пользователь разорвал соединение"
}
ERROR_SIGNALS = ["400", "401", "402", "403", "404", "405"]
CONNECTING_SIGNALS = ["100", "101", "102", "103", "104", "105"]
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
        logger.debug("Interface start")
        #Подключение сигналов
        self.rootObject = self.rootObject()
        self.rootObject.cmd_connect.connect(self.connector.connect)
        self.rootObject.cmd_disconnect.connect(self.connector.disconnect)
        
        self.createActions()
        self.createTrayIcon()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setMinimumSize(QtCore.QSize(300, 560))
        self.setMaximumSize(QtCore.QSize(300, 560))
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
#        self.setWindowIcon()
        self.setWindowTitle("RocketOne")
        self.trayIcon.activated.connect(self.iconActivated)
#        self.emit_signal("101")
        self.trayIcon.show()
        self.show()
#        self.showMessage()=
    
    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.show()
    
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
#            QtGui.QMessageBox.information(self, "Systray",
#                    "The program will keep running in the system tray. To "
#                    "terminate the program, choose <b>Quit</b> in the "
#                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()
    
    def remember(self):
        return self.rootObject.remember()
    
    def emit_signal(self, status):
        self.rootObject.signal(status)
        if status == "200":
            self.buildTrayMenu(connect=True)
            self.showMessage(SIGNALS_HASH[status])
        elif status in ERROR_SIGNALS:
            self.buildTrayMenu()
            if status != "405":
                self.showMessage(SIGNALS_HASH[status], caption="Ошибка")
        elif status in CONNECTING_SIGNALS:
            self.buildTrayMenu(connect=True)
    
    def set_auth(self, login, passwd):
        self.rootObject.set_auth(login, passwd)
    
    def set_remember(self, status):
        self.rootObject.set_remember(status)

    def createActions(self):
        self.disconnectAction = QtGui.QAction(u"Отключить", self,
                triggered=self.rootObject.user_disconnect)
        self.connectAction = QtGui.QAction(u"Подключить", self,
                triggered=self.rootObject.init_connection)
#        self.propertiesAction = QtGui.QAction(u"Настройки", self)
        self.quitAction = QtGui.QAction(u"Выход", self, triggered=QtCore.QCoreApplication.quit)
    
    def buildTrayMenu(self, connect=False):
         self.trayIconMenu = QtGui.QMenu(self)
         if connect:
             self.trayIconMenu.addAction(self.disconnectAction)
         else:
             self.trayIconMenu.addAction(self.connectAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)
         self.trayIcon.setContextMenu(self.trayIconMenu)

    def createTrayIcon(self):
         icon = QtGui.QIcon('../QML/images/trayicon_32px.svg')
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.buildTrayMenu()
         self.trayIcon.setIcon(icon)
         
    def showMessage(self, message, caption="RocketOne", type="info"):
        if type =="error":
            icon = QtGui.QSystemTrayIcon.MessageIcon(
                QtGui.QSystemTrayIcon.Error)
        else:
            icon = QtGui.QSystemTrayIcon.MessageIcon(
                QtGui.QSystemTrayIcon.Information)
        self.trayIcon.showMessage(unicode(caption),
                unicode(message), icon,
                 500)
#        self.trayIcon.messageClicked.connect(self.showFullMessage)
    
        

    def close(self):
        self.hide()
        self.trayIcon.hide()
