from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from psnawp_api import psnawp, psnawp_exceptions

class PSNThread(QtCore.QThread):
    user_presence = QtCore.pyqtSignal(object)
    psn = None

    def __init__(self, parent = None):
        QThread.__init__(self)
        self.parent = parent
        self.settings = QSettings('flok', 'playstationdiscordrpc')
        self.enable = self.settings.value('enabled', type=bool)

    def __del__(self):
        self.wait()

    def start(self):
        if self.settings.value('ssno') == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Information)
            msgBox.setWindowTitle("Information")
            msgBox.setText("No SSNO defined. please add it in the settings.")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok |  QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
            msgBox.exec_()
            return None

        try:
            self.psn: psnawp.PSNAWP = psnawp.PSNAWP(self.settings.value('ssno'))
        except psnawp_exceptions.PSNAWPAuthenticationError:
            self.parent.showMessage("PlayStationDiscordRPC", "NPSSO Token is not valid anymore, please get a new one through the setting and replace it.")
            self.parent.settingsWindow.show()
        except psnawp_exceptions.PSNAWPAuthenticationError:
            self.parent.showMessage("PlayStationDiscordRPC", "Error Authenticating with the Current NPSSO")

        if self.settings.value('debug', type=bool):
            print(f"Initialized PSN with a intervall of {self.settings.value('sample_delay')}")
            self.parent.showMessage("PlayStationDiscordRPC", f"Initialized PSN with a intervall of {self.settings.value('sample_delay')}")

        return super(PSNThread, self).start()

    def set_status(self, enable: bool):
        self.enable = enable

    def stop(self):
        self.enable = False
        self.exit(0)

    def run(self):
        while self.settings.value('enabled', type=bool):
            if self.psn is None:
                self.parent.setStatus(False)
                break
            user = self.psn.user(account_id=self.psn.me().get_account_id()).get_presence()
            self.user_presence.emit(user)
            time.sleep(self.settings.value('sample_delay'))