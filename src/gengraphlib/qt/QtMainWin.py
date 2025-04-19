from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (
    QHBoxLayout, QListView,
    QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTreeView, QWidget)


# noinspection PyAttributeOutsideInit
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2276, 1270)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 2251, 1121))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.horizontalLayoutWidget)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout.addWidget(self.listView)

        self.treeView = QTreeView(self.horizontalLayoutWidget)
        self.treeView.setObjectName(u"treeView")

        self.horizontalLayout.addWidget(self.treeView)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 1130, 2251, 80))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.start_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.start_btn.setObjectName(u"start_btn")

        self.horizontalLayout_2.addWidget(self.start_btn)

        self.pause_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.pause_btn.setObjectName(u"pause_btn")

        self.horizontalLayout_2.addWidget(self.pause_btn)

        self.refresh_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.refresh_btn.setObjectName(u"refresh_btn")

        self.horizontalLayout_2.addWidget(self.refresh_btn)

        self.exit_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.exit_btn.setObjectName(u"exit_btn")

        self.horizontalLayout_2.addWidget(self.exit_btn)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 2276, 29))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start Parse", None))
        self.pause_btn.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.refresh_btn.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.exit_btn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
    # retranslateUi

