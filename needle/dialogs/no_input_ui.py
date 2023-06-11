# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'no_input.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_no_input_dialog(object):
    def setupUi(self, no_input_dialog):
        if not no_input_dialog.objectName():
            no_input_dialog.setObjectName(u"no_input_dialog")
        no_input_dialog.resize(360, 140)
        no_input_dialog.setMinimumSize(QSize(360, 140))
        no_input_dialog.setMaximumSize(QSize(360, 140))
        icon = QIcon()
        icon.addFile(u":/icons/icons/needle.png", QSize(), QIcon.Normal, QIcon.Off)
        no_input_dialog.setWindowIcon(icon)
        no_input_dialog.setStyleSheet(u"#no_input_dialog {\n"
"	background-color:rgb(0, 0, 0);\n"
"}\n"
"\n"
"#Title {\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#Desc {\n"
"	color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QVBoxLayout(no_input_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Title = QGroupBox(no_input_dialog)
        self.Title.setObjectName(u"Title")
        self.horizontalLayout_2 = QHBoxLayout(self.Title)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Icon = QFrame(self.Title)
        self.Icon.setObjectName(u"Icon")
        self.Icon.setMinimumSize(QSize(55, 55))
        self.Icon.setMaximumSize(QSize(55, 55))
        self.Icon.setFocusPolicy(Qt.TabFocus)
        self.Icon.setStyleSheet(u"background-image: url(:/icons/icons/error.ico);\n"
"background-repeat: no-repeat;\n"
"border: none;")
        self.Icon.setFrameShape(QFrame.StyledPanel)
        self.Icon.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.Icon)

        self.Layoout = QVBoxLayout()
        self.Layoout.setObjectName(u"Layoout")
        self.Desc = QLabel(self.Title)
        self.Desc.setObjectName(u"Desc")

        self.Layoout.addWidget(self.Desc)


        self.horizontalLayout_2.addLayout(self.Layoout)


        self.verticalLayout.addWidget(self.Title)


        self.retranslateUi(no_input_dialog)

        QMetaObject.connectSlotsByName(no_input_dialog)
    # setupUi

    def retranslateUi(self, no_input_dialog):
        no_input_dialog.setWindowTitle(QCoreApplication.translate("no_input_dialog", u"CAUTION !", None))
        self.Title.setTitle(QCoreApplication.translate("no_input_dialog", u"No Input Found", None))
        self.Desc.setText(QCoreApplication.translate("no_input_dialog", u"<html><head/><body><p><span style=\" font-size:12pt;\">Please browse or drop the zip file<br/>(*.zip) containing source files. </span></p></body></html>", None))
    # retranslateUi

