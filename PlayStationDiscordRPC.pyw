from PyQt5.QtGui import QIcon
from psnawp_api import psnawp as psn
from PyQt5.QtWidgets import *
from PyQt5 import *
from  PyQt5.QtCore import *
import yaml
import sys
from PlayStationConnection import PSNThread
from pypresence import Presence
from Settings import SettingsUI
import time


class Window(QSystemTrayIcon):
    settingsWindow = None
    psn = None
    config = None
    PSNThread = None
    currentGame = None
    def __init__(self) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon('images/playstation.png'))

        self.setVisible(True)

        self.loadConfig()

        self.setupMenu()

        self.setupPSN()

        self.setupDiscord()

        self.startPSNThread()

    def setupPSN(self):
        self.psn = psn.PSNAWP(self.config['ssno'])
        print(f"{self.psn.me()}")

    def setupDiscord(self):
        self.discord = Presence(898856060058763286)
        self.discord.connect()

    def startPSNThread(self):
        self.PSNThread = PSNThread(self)
        self.PSNThread.user_presence.connect(self.presence)
        self.PSNThread.start(self.psn)

    def presence(self, presence):
        # set presence for discord with game title
        print(presence)

        if 'gameTitleInfoList' not in presence.keys():
            self.discord.clear()
            self.currentGame = ""
            # clear if something was there
            return


        gameinfo = presence['gameTitleInfoList'][0]
        gameTitle = gameinfo['titleName']
        imageID = gameinfo['npTitleId'].lower()

        # abort updating the game status with the same game
        # if we do this we reset the timer
        if self.currentGame == gameTitle:
            return


        self.discord.update(state="Currently in game", details=gameTitle, large_image=imageID, small_image="playstation", start=time.time())

        self.currentGame = gameTitle

    def loadConfig(self):
        self.config = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)

    def setupMenu(self):
        menu = QMenu()
        toggleEnable = menu.addAction('Enable')
        settingsAction = menu.addAction('Settings')
        settingsAction.triggered.connect(self.openSettings)
        exitAction = menu.addAction('Quit')
        exitAction.triggered.connect(self.close)

        self.setContextMenu(menu)

    def openSettings(self):
        if self.settingsWindow is None:
            self.settingsWindow = SettingsUI()
            self.settingsWindow.show()
        else:
            self.settingsWindow = None

    def close(self):
        self.PSNThread.stop()
        self.discord.close()
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())