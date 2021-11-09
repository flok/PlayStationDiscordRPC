from PyQt5 import QtCore, QtGui
import PyQt5
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from StatusUI import Ui_Form as ui
from PyQt5.QtCore import Qt
import resources


class StatusUI(QMainWindow):



    def __init__(self, parent = None) -> None:
        super(StatusUI, self).__init__()
        self.ui = ui()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowIcon(QtGui.QIcon(':/icons/icon.png'))
        self.parent = parent
        """Pointer to QSystemTrayIcon"""
        # config access
        self.settings = QSettings('flok', 'playstationdiscordrpc')
        """Pointer to global config"""

        self.parent.status_update.connect(self.update_status)
        self.parent.update_pos.connect(self.update_pos)
        # load values from config and apply at startup
        self.ui.label.setPixmap(QtGui.QPixmap(':/discord/discord_icon'))


        # timer for hiding status again
        self.timer = QTimer()
        self.timer.timeout.connect(self.end_timer)

    def update_pos(self, geometry: QtCore.QRect):
        window = self.geometry()
        trayicon = geometry
        half_width = window.width() // 2
        height = window.height() + trayicon.height()
        new_top = QPoint(trayicon.left() - half_width, trayicon.top() - height)
        self.move(new_top)

    def end_timer(self):
        self.hide()


    def update_status(self, update):
        if update[0] == 'None':
            self.ui.le_details.setText('Offline')
            self.ui.le_state.setText('')
            return

        self.ui.le_details.setText(update[1])
        self.ui.le_state.setText(update[0])