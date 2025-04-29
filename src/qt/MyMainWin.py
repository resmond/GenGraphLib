from typing import Self

import multiprocessing as mp

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect
from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout, QListView,
    QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTreeView, QWidget
)

from ..gengraphlib.common import keyIndexInfo
from src.qt import QtMsgQueueReader

class MyMainWindow(QMainWindow):
    # Class-level constants for configuration
    WINDOW_TITLE = "Main Window"
    MINIMUM_WIDTH = 800
    MINIMUM_HEIGHT = 600

    def process_data(self: Self, index_info: keyIndexInfo) -> None:
        print(f"{self.WINDOW_TITLE}: {index_info.key} - keycnt: {index_info.keycnt}  refcnt: {index_info.refcnt}  hit%: {index_info.hitpct}")

    def __init__(self: Self, msg_queue: mp.Queue, end_event: mp.Event ) -> None:
        super(MyMainWindow, self).__init__()

        self.msg_queue: mp.Queue = msg_queue
        self.end_event: mp.Event = end_event
        self.queue_reader = QtMsgQueueReader( msg_queue=self.msg_queue, end_event=self.end_event, parent=self )
        self.queue_reader.data_received.connect(self.process_data)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setObjectName("MainWindow")
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

        self.centralwidget:          QWidget     = QWidget(self)

        self.menubar:                  QMenuBar    = QMenuBar(self)
        self.statusbar:                QStatusBar  = QStatusBar(self)
        self.horizontalLayoutWidget:   QWidget     = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2: QWidget     = QWidget(self.centralwidget)

        self.horizontalLayout:       QHBoxLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.listView:               QListView   = QListView(self.horizontalLayoutWidget)
        self.treeView:               QTreeView   = QTreeView(self.horizontalLayoutWidget)

        self.horizontalLayout_2:     QHBoxLayout = QHBoxLayout(self.horizontalLayoutWidget_2)

        self.horizontalSpacer:       QSpacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.start_btn:              QPushButton = QPushButton(self.horizontalLayoutWidget_2)
        self.pause_btn:              QPushButton = QPushButton(self.horizontalLayoutWidget_2)
        self.refresh_btn:            QPushButton = QPushButton(self.horizontalLayoutWidget_2)
        self.exit_btn:               QPushButton = QPushButton(self.horizontalLayoutWidget_2)

        self.centralwidget.setObjectName(u"centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 2251, 1121))
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.listView.setObjectName(u"listView")

        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 2276, 29))
        self.setMenuBar(self.menubar)

        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.horizontalLayout.addWidget(self.listView)

        self.treeView.setObjectName(u"treeView")

        self.horizontalLayout.addWidget(self.treeView)

        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 1130, 2251, 80))
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.start_btn.setObjectName(u"start_btn")
        self.horizontalLayout_2.addWidget(self.start_btn)

        self.pause_btn.setObjectName(u"pause_btn")
        self.horizontalLayout_2.addWidget(self.pause_btn)

        self.refresh_btn.setObjectName(u"refresh_btn")
        self.horizontalLayout_2.addWidget(self.refresh_btn)

        self.exit_btn.setObjectName(u"exit_btn")
        self.horizontalLayout_2.addWidget(self.exit_btn)

        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start Parse", None))
        self.pause_btn.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.refresh_btn.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.exit_btn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))

        self.showMinimized()

        QMetaObject.connectSlotsByName(self)
