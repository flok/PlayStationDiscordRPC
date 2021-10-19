from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from psnawp_api import psnawp

class PSNThread(QtCore.QThread):
    user_presence = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PSNThread, self).__init__(parent)
        self.parent = parent
        self.enable = True

    def start(self, psn):
        self.psn: psnawp.PSNAWP = psn
        return super(PSNThread, self).start()

    def set_status(self, enable: bool):
        self.enable = enable

    def stop(self):
        self.enable = False
        self.exit(0)

    def run(self):
        while self.enable or self.parent().isRunning():
            user = self.psn.user(account_id=self.psn.me().get_account_id()).get_presence()
            self.user_presence.emit(user)
            time.sleep(self.parent.config['sample_delay'])