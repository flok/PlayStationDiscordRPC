from PyQt5 import *
from PyQt5.QtWidgets import *

from SettingsUI import Ui_MainWindow as ui

class SettingsUI(QMainWindow):
    def __init__(self) -> None:
        super(SettingsUI, self).__init__()
        self.ui = ui()
        self.ui.setupUi(self)