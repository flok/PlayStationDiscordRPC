from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from psnawp_api import psnawp as psn
from psnawp_api import psnawp_exceptions
from PyQt5.QtWidgets import *
from PyQt5 import *
from  PyQt5.QtCore import *
import sys, os
from PlayStationConnection import PSNThread
from pypresence import Presence
from Settings import SettingsUI
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
    settingsWindow = None
    psn = None
    config = None
    PSNThread = None
    currentGame = None
    def __init__(self) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon(':/icons/playstation.ico'))
        self.setVisible(True)

        self.loadSettings()

        self.setupMenu()

        self.setupPSN()

        self.setupDiscord()

        self.startPSNThread()

    def setupPSN(self):
        if self.settings.value('ssno') == '' or self.settings.value('first_start', type=bool):
            self.settingsWindow.show()


    def setupDiscord(self):
        if self.settings.value('debug', type=bool):
            print(f"Initialize Discord presence with client id: {CLIENT_ID}")
        self.discord = Presence(CLIENT_ID)
        self.discord.connect()

    def startPSNThread(self):
        self.PSNThread = PSNThread(self)
        self.PSNThread.user_presence.connect(self.presence)
        self.PSNThread.start()

    def presence(self, presence):
        # set presence for discord with game title
        if self.settings.value('debug', type=bool):
            print(presence)

        if 'gameTitleInfoList' not in presence.keys():
            # clear status of discord and current game
            self.discord.clear()
            self.currentGame = ""
            return

        gameinfo = presence['gameTitleInfoList'][0]
        gameStatus = None
        if 'gameStatus' in gameinfo:
            gameStatus = gameinfo['gameStatus']
        gameTitle = gameinfo['titleName']


        imageID = gameinfo['npTitleId'].lower()

        # abort updating the game status with the same game
        # if we do this we reset the timer
        if self.currentGame == gameTitle and gameStatus is None:
            return

        if gameStatus is None:
            self.discord.update(state="Currently in game", details=gameTitle, large_image=imageID, small_image="playstation", start=time.time(),small_text="PlayStation 5", large_text=gameTitle)
        else:
            self.discord.update(state=gameStatus, details=gameTitle, large_image=imageID, small_image="playstation", start=time.time(), small_text="PlayStation 5", large_text=gameTitle)

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

        self.settingsWindow = SettingsUI(self)
        self.settingsWindow.reconnect_psn.connect(self.reconnect_psn)

    def reconnect_psn(self):
        if self.PSNThread.isRunning():
            self.PSNThread.stop()
            self.PSNThread.start()
        else:
            self.PSNThread.start()

    """
    def loadConfig(self):
        if os.path.exists('config.yml'):
            self.config = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)
        else:
            # no config file found, create new one

            open('config.yml', 'w').write(config_template)
            self.config = yaml.load(open('config.yml', 'r'), Loader=yaml.FullLoader)
            print(f"config created {self.config}")

    def saveConfig(self):
        yaml.safe_dump(self.config, open('config.yml', 'w'))
        # everytime we save config a change of the ssno could have taken place we reinitialize the psn api
        self.connectPSN()
        self.PSNThread.start(self.psn)
    """

    def setStatus(self, state):
        self.settings.setValue('enabled', state)
        if state == True:
            self.PSNThread.start()

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
    app.setWindowIcon(QtGui.QIcon('images/playstation.ico'))
    screen = Window()
    screen.show()
    sys.exit(app.exec_())