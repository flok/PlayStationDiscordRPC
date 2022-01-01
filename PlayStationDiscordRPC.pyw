from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import *
from  PyQt5.QtCore import *
import sys, os
from PlayStationConnection import PSNThread
from pypresence import Presence
from Settings import SettingsUI
from Status import StatusUI
import resources
import time


try:
    from PyQt5.QtWinExtras import QtWin
    appid = 'flok.playstationdiscordrpc'
    QtWin.setCurrentProcessExplicitAppUserModelID(appid)
except ImportError:
    pass


CLIENT_ID = 906197927968526358


class Window(QSystemTrayIcon):

    PSNThread = None
    currentGame = None
    status_update: QtCore.pyqtSignal = QtCore.pyqtSignal(object)
    update_pos: QtCore.pyqtSignal = QtCore.pyqtSignal(object)


    def __init__(self) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon(':/icons/icon.png'))
        self.setVisible(True)
        self.setToolTip("PlayStationDiscordRPC")
        self.activated.connect(self.click_handler)

        self.loadSettings()

        self.setupStatus()

        self.setupMenu()

        self.setupPSN()

        self.setupDiscord()

        self.startPSNThread()


    def click_handler(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # double click on tray icon
            self.statusWindow.show()
            self.statusWindow.timer.start(3000)

    def setupStatus(self):
        self.statusWindow = StatusUI(self)

    def setupPSN(self):
        if self.settings.value('ssno') == '' or self.settings.value('first_start', type=bool):
            self.settingsWindow.show()


    def setupDiscord(self):

        while(self.checkDiscordRunning() is False):
            self.showMessage("PlayStationDiscordRPC", "Discord not running. Trying in 3 second again", QSystemTrayIcon.MessageIcon.Information, 1000)
            time.sleep(3)

        if self.settings.value('debug', type=bool):
            print(f"Initialize Discord presence with client id: {CLIENT_ID}")
            self.showMessage("PlayStationDiscordRPC", "Initialized Discord Presence", QSystemTrayIcon.MessageIcon.Information, 2000)

        self.discord = Presence(CLIENT_ID)
        self.discord.connect()

    def checkDiscordRunning(self):
        import psutil
        ret = False
        try:
            # Check if process name contains the given name string.
            ret = any("discord" in p.name().lower() for p in psutil.process_iter())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        return ret

    def startPSNThread(self):
        self.PSNThread = PSNThread(self)
        self.PSNThread.user_presence.connect(self.presence)
        self.PSNThread.start()

    def presence(self, presence):
        # set presence for discord with game title
        if self.settings.value('debug', type=bool):
            print(presence)

        self.update_pos.emit(self.geometry())

        if 'gameTitleInfoList' not in presence.keys():
            # clear status of discord and current game
            self.discord.clear()
            self.currentGame = ""
            self.status_update.emit(['None'])
            return

        gameinfo = presence['gameTitleInfoList'][0]
        gameStatus = None
        if 'gameStatus' in gameinfo:
            gameStatus = gameinfo['gameStatus']
        gameTitle = gameinfo['titleName']


        imageID = gameinfo['conceptIconUrl']

        # abort updating the game status with the same game
        # if we do this we reset the timer
        if self.currentGame == gameTitle and gameStatus is None:
            return

        if gameStatus is None:
            self.discord.update(state="Currently in game", details=gameTitle, large_image=imageID, small_image="playstation", start=time.time(),small_text="PlayStation 5", large_text=gameTitle)
            self.status_update.emit(['Currently in game', gameTitle])
        else:
            self.discord.update(state=gameStatus, details=gameTitle, large_image=imageID, small_image="playstation", start=time.time(), small_text="PlayStation 5", large_text=gameTitle)
            self.status_update.emit([gameStatus, gameTitle])

        # set current gameTitle to current game
        self.currentGame = gameTitle

    def loadSettings(self):
        self.settings = QSettings('flok', 'playstationdiscordrpc')
        # check if settings are empty -> first start up
        if len(self.settings.allKeys()) == 0:
            self.settings.setValue('enabled', True)
            self.settings.setValue('debug', False)
            self.settings.setValue('sample_delay', 30)
            self.settings.setValue('ssno', '')
            self.settings.setValue('first_start', True)
            self.settings.setValue('autostart', True)

        self.settingsWindow = SettingsUI(self)
        self.settingsWindow.reconnect_psn.connect(self.reconnect_psn)

    def reconnect_psn(self):
        if self.PSNThread.isRunning():
            self.PSNThread.stop()
            self.PSNThread.start()
        else:
            self.PSNThread.start()

    def setStatus(self, state):
        self.settings.setValue('enabled', state)
        if state == True:
            self.PSNThread.start()
        else:
            self.PSNThread.stop()

    def setupMenu(self):
        menu = QMenu()
        toggleEnable = menu.addAction('Enable')
        toggleEnable.setCheckable(True)
        toggleEnable.setChecked(self.settings.value('enabled', type=bool))
        toggleEnable.triggered.connect(self.setStatus)
        settingsAction = menu.addAction('Settings')
        settingsAction.triggered.connect(self.openSettings)
        exitAction = menu.addAction('Quit')
        exitAction.triggered.connect(self.close)

        self.setContextMenu(menu)

    def openSettings(self):
        self.settingsWindow.show()

    def close(self):
        self.PSNThread.stop()
        self.discord.clear()
        self.discord.close()
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("PlayStationDiscordRPC")
    app.setApplicationVersion('1.0.0')
    app.setWindowIcon(QtGui.QIcon('images/playstation.ico'))
    screen = Window()
    screen.show()
    sys.exit(app.exec_())