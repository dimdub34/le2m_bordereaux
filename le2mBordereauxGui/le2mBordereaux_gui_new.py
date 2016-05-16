# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'le2mBordereaux_gui_new.ui'
#
# Created: Tue Feb  2 09:42:42 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(244, 170)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(244, 170))
        Dialog.setMaximumSize(QtCore.QSize(244, 170))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 23, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_nom = QtGui.QLabel(Dialog)
        self.label_nom.setObjectName(_fromUtf8("label_nom"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_nom)
        self.lineEdit_nom = QtGui.QLineEdit(Dialog)
        self.lineEdit_nom.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEdit_nom.setObjectName(_fromUtf8("lineEdit_nom"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_nom)
        self.label_prenom = QtGui.QLabel(Dialog)
        self.label_prenom.setObjectName(_fromUtf8("label_prenom"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_prenom)
        self.lineEdit_prenom = QtGui.QLineEdit(Dialog)
        self.lineEdit_prenom.setMaximumSize(QtCore.QSize(100, 100))
        self.lineEdit_prenom.setObjectName(_fromUtf8("lineEdit_prenom"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_prenom)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Nouveau bordereau", None))
        self.label_nom.setText(_translate("Dialog", "Nom", None))
        self.label_prenom.setText(_translate("Dialog", "Prénom", None))

