import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from SettingsUI import Ui_MainWindow as ui
import winreg
import resources

class SettingsUI(QMainWindow):

    reconnect_psn = QtCore.pyqtSignal()

    def __init__(self, parent =None) -> None:
        super(SettingsUI, self).__init__()
        self.ui = ui()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/icon.png'))

        self.parent = parent
        """Pointer to QSystemTrayIcon"""

        # config access
        self.settings = QSettings('flok', 'playstationdiscordrpc')
        """Pointer to global config"""


        # load values from config and apply at startup
        self.ui.lE_ssno.setText(self.settings.value('ssno'))
        self.ui.slider_delay.setValue(self.settings.value('sample_delay'))
        self.ui.cb_debug.setChecked(self.settings.value('debug', type=bool))
        self.ui.cb_autostart.setChecked(self.settings.value('autostart', type=bool))

        # setup connection
        self.ui.label_get_ssno.linkActivated.connect(self.openGETSSNO)
        self.ui.pushButton.clicked.connect(self.press_save)

    def openGETSSNO(self, link):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def press_save(self):

        # save values from interface into global config
        self.settings.setValue('ssno', self.ui.lE_ssno.text())
        self.settings.setValue('sample_delay', self.ui.slider_delay.value())
        self.settings.setValue('debug', self.ui.cb_debug.isChecked())
        self.settings.setValue('autostart', self.ui.cb_autostart.isChecked())

        # update autostart registry
        if self.ui.cb_autostart.isChecked():
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "PlayStationDiscordRPC", 0, winreg.REG_SZ, sys.argv[0])
                winreg.CloseKey(key)
            except OSError:
                raise OSError('Couldnt add Autostart key inside registry')
        else:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, "PlayStationDiscordRPC")
                winreg.CloseKey(key)
            except OSError:
                raise OSError('Couldnt find Autostart key inside registry')

        # hide window
        self.hide()

        if len(self.ui.lE_ssno.text()) == 64:
            self.settings.setValue('first_start', False)
            self.reconnect_psn.emit()