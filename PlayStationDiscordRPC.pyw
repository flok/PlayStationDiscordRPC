from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from psnawp_api import psnawp as psn
from PyQt5.QtWidgets import *
from PyQt5 import *
from  PyQt5.QtCore import *
import yaml
import sys, os
from PlayStationConnection import PSNThread
from pypresence import Presence
from Settings import SettingsUI
import resources
from utils import resource_path, config_template
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

        self.loadConfig()

        self.setupMenu()

        self.setupPSN()

        self.setupDiscord()

        self.startPSNThread()

    def setupPSN(self):
        if self.config['ssno'] == 'NPSSO_HERE':
            self.settingsWindow = SettingsUI(self.config, self)
            self.settingsWindow.show()
            print("set up key")
        else:
            self.psn = psn.PSNAWP(self.config['ssno'])


    def setupDiscord(self):
        self.discord = Presence(CLIENT_ID)
        self.discord.connect()

    def startPSNThread(self):
        self.PSNThread = PSNThread(self)
        self.PSNThread.user_presence.connect(self.presence)
        self.PSNThread.start(self.psn)

    def presence(self, presence):
        # set presence for discord with game title
        if self.config['debug']:
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
        print(f"re init psn with {self.config['ssno']}")
        self.psn = psn.PSNAWP(self.config['ssno'])
        self.PSNThread.start(self.psn)

    def setStatus(self, state):
        self.config['enabled'] = state

        self.saveConfig()

    def setupMenu(self):
        menu = QMenu()
        toggleEnable = menu.addAction('Enable')
        toggleEnable.setCheckable(True)
        toggleEnable.setChecked(self.config['enabled'])
        toggleEnable.triggered.connect(self.setStatus)
        settingsAction = menu.addAction('Settings')
        settingsAction.triggered.connect(self.openSettings)
        exitAction = menu.addAction('Quit')
        exitAction.triggered.connect(self.close)

        self.setContextMenu(menu)

    def openSettings(self):
        if self.settingsWindow is None:
            self.settingsWindow = SettingsUI(self.config, self)
            self.settingsWindow.show()
        else:
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