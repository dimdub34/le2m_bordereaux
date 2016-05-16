# -*- coding: utf-8 -*-
"""
Ce module contient les différentes boites de dialogue de l'application
Author: Dimitri DUBOIS
"""

from PyQt4 import QtGui, QtCore
import logging
from le2mBordereauxGui import le2mBordereaux_gui_new, \
    le2mBordereaux_gui_information, le2mBordereaux_gui_requete

logger = logging.getLogger(__name__)


class DNew(QtGui.QDialog):
    """
    Dialogue qui permet de saisir le nom et le prénom du sujet.
    La validation ajoute le sujet à la liste. L'annulation ferme la fenetre.
    """
    def __init__(self, bordereau_main, parent):
        super(DNew, self).__init__(parent)
        self._bordereau_main = bordereau_main
        self.ui = le2mBordereaux_gui_new.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _accept(self):
        try:
            self.nom = unicode(self.ui.lineEdit_nom.text().toUtf8(),
                               "utf-8")
            self.prenom = unicode(self.ui.lineEdit_prenom.text().toUtf8(),
                                  "utf-8")
            if not (self.nom and self.prenom):
                raise ValueError
        except UnicodeEncodeError:
            QtGui.QMessageBox.critical(
                self,  u"Problème",  "Ne pas mettre d'accent svp.")
            return
        except ValueError:
            QtGui.QMessageBox.critical(
                None,  u"Attention",
                    u"Il faut remplir les deux champs, merci.")
            return
        self.accept()

    def get_infos(self):
        return self.nom, self.prenom


class DInformation(QtGui.QDialog):
    def __init__(self, titre, texte, parent):
        super(DInformation, self).__init__(parent)
        self.ui = le2mBordereaux_gui_information.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(titre)
        self.ui.textBrowser_information.setHtml(texte)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setVisible(False)


class DRequete(QtGui.QDialog):
    def __init__(self, parent, experience="", date=QtCore.QDate.currentDate(),
                 horaire=QtCore.QTime.currentTime()):
        super(DRequete, self).__init__(parent)
        self.ui = le2mBordereaux_gui_requete.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.lineEdit_expe.setText(experience)
        self.ui.dateEdit.setDate(date)
        self.ui.timeEdit.setTime(horaire)
        self.ui.buttonBox.accepted.connect(self._accept)

    def _accept(self):
        try:
            self._experience = unicode(self.ui.lineEdit_expe.text().toUtf8(),
                                       "utf-8")
            if not self._experience:
                QtGui.QMessageBox.critical(
                    self, u"Erreur", u"Il faut un nom d'expérience")
        except UnicodeEncodeError:
            QtGui.QMessageBox.critical(
                self, u"Erreur", u"Ne pas mettre d'accents")
            return
        self._date = self.ui.dateEdit.date().toPyDate()
        self._heure = self.ui.timeEdit.time().toPyTime()
        self.accept()

    def get_infos(self):
        return self._experience, self._date, self._heure



