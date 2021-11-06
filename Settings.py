
from PyQt5 import QtCore, QtGui
from PyQt5 import *
from PyQt5.QtWidgets import *
import yaml
from SettingsUI import Ui_MainWindow as ui
import resources

class SettingsUI(QMainWindow):
    def __init__(self, config: dict, parent =None) -> None:
        super(SettingsUI, self).__init__()
        self.setWindowIcon(QtGui.QIcon(':/icons/playstation.ico'))
        self.ui = ui()
        self.ui.setupUi(self)

        self.parent = parent
        """Pointer to QSystemTrayIcon"""

        # config access
        self.config = config
        """Pointer to global config"""


        # load values from config and apply at startup
        self.ui.lE_ssno.setText(self.config['ssno'])
        self.ui.slider_delay.setValue(self.config['sample_delay'])
        self.ui.cb_debug.setChecked(self.config['debug'])

        # setup connection
        self.ui.label_get_ssno.linkActivated.connect(self.openGETSSNO)
        self.ui.pushButton.clicked.connect(self.press_save)

    def openGETSSNO(self, link):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))

    def closeEvent(self, event):
        if event == QtGui.QCloseEvent:
            self.hide()


    def press_save(self):

        # save values from interface into global config
        self.config['ssno'] = self.ui.lE_ssno.text()
        self.config['sample_delay'] = self.ui.slider_delay.value()
        self.config['debug'] = self.ui.cb_debug.isChecked()

        # save config to file
        self.parent.saveConfig()

        # hide window
        self.hide()