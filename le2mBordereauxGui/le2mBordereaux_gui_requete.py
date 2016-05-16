# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'le2mBordereaux_gui_requete.ui'
#
# Created: Wed Apr 29 08:14:44 2015
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
        Dialog.resize(194, 137)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_expe = QtGui.QLabel(Dialog)
        self.label_expe.setObjectName(_fromUtf8("label_expe"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_expe)
        self.lineEdit_expe = QtGui.QLineEdit(Dialog)
        self.lineEdit_expe.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_expe.setObjectName(_fromUtf8("lineEdit_expe"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_expe)
        self.label_date = QtGui.QLabel(Dialog)
        self.label_date.setObjectName(_fromUtf8("label_date"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_date)
        self.dateEdit = QtGui.QDateEdit(Dialog)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.dateEdit)
        self.label_heure = QtGui.QLabel(Dialog)
        self.label_heure.setObjectName(_fromUtf8("label_heure"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_heure)
        self.timeEdit = QtGui.QTimeEdit(Dialog)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.timeEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Requete ORSEE", None))
        self.label_expe.setText(_translate("Dialog", "Expérience", None))
        self.label_date.setText(_translate("Dialog", "Date", None))
        self.label_heure.setText(_translate("Dialog", "Heure", None))

