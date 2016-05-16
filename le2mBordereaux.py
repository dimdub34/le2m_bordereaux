#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Ce module contient tous les éléments graphiques de l'application
"""
__author__ = 'Dimitri DUBOIS'

from PyQt4 import QtGui, QtCore
import sys
import os
import webbrowser
import tempfile
import codecs
import logging

import le2mBordereaux_main
from le2mBordereauxGui import le2mBordereaux_gui_main
from le2mBordereaux_dialogs import DNew, DInformation, DRequete
import le2mBordereaux_config as config
import le2mBordereaux_textes as textes

logger = logging.getLogger(__name__)


class GuiMain(QtGui.QMainWindow):
    def __init__(self, bordereau_main):
        super(GuiMain, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self._bordereau_main = bordereau_main
        dossier_images = os.path.join(
            self._bordereau_main.dossier_courant, "le2mBordereauxImages")
        self.ui = le2mBordereaux_gui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(u"LE2M - Bordereaux")

        self._config_actions()

        self.ui.label_description.setText(config.TITLE)
        self.ui.label_logo.setPixmap(
            QtGui.QPixmap(os.path.join(dossier_images, config.LOGO)))
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit.setToolTip(u"Date de la session")
        self.ui.timeEdit.setTime(QtCore.QTime.currentTime())
        self.ui.timeEdit.setToolTip(u"Heure de début de la session")
        self.ui.lineEdit_ville.setText(config.VILLE)
        self.ui.spinBox_premierBordereau.setValue(1)

        # La table qui contient les sujets
        self.ui.tableView_sujets.setModel(self._bordereau_main.table_subjects)
        self.ui.tableView_sujets.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.ui.tableView_sujets.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.ui.tableView_sujets.setAlternatingRowColors(False)
        self._bordereau_main.table_subjects.set_suiveur_nombre(
            self.ui.label_presents_nb)
        self.ui.tableView_sujets.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        self.ui.tableView_sujets.horizontalHeader().setClickable(True)
        self.ui.tableView_sujets.horizontalHeader().sectionClicked[int].connect(
            self._bordereau_main.table_subjects.inverser_selection)
        self.ui.tableView_sujets.verticalHeader(). \
            sectionCountChanged[int, int].connect(
                self.ui.tableView_sujets.resizeRowsToContents)

        # boutons
        self.ui.pushButton_add.setIcon(
            QtGui.QIcon(os.path.join(dossier_images, "plus.jpg")))
        self.ui.pushButton_add.setToolTip(u"Ajouter un sujet")
        self.ui.pushButton_add.clicked.connect(self._add_new)
        self.ui.pushButton_monter.setIcon(
            QtGui.QIcon(os.path.join(dossier_images, "up.jpg")))
        self.ui.pushButton_monter.setToolTip(
                u"Déplacer la sélection vers le haut")
        self.ui.pushButton_monter.clicked.connect(self._move_line)
        self.ui.pushButton_descendre.setIcon(
            QtGui.QIcon(os.path.join(dossier_images, "down.jpg")))
        self.ui.pushButton_descendre.setToolTip(
                u"Déplacer la sélection vers le bas")
        self.ui.pushButton_descendre.clicked.connect(self._move_line)
        self.ui.pushButton_remove.setIcon(
            QtGui.QIcon(os.path.join(dossier_images, "moins.jpg")))
        self.ui.pushButton_remove.setToolTip(u"Supprimer la sélection")
        self.ui.pushButton_remove.clicked.connect(self._remove_selected)

        self.setFixedSize(670, 750)
        ecran = QtGui.QApplication.desktop()
        ecran_w = ecran.width()
        ecran_h = ecran.height()
        self.move((ecran_w - self.width()) / 2, (ecran_h - self.height()) / 2)

    def _config_actions(self):
        # Menu Fichier
        self.ui.action_ouvrir.setShortcut("Ctrl+o")
        self.ui.action_ouvrir.triggered.connect(self._add_subjects)
        self.ui.action_enregistrer.setShortcut("Ctrl+s")
        self.ui.action_enregistrer.triggered.connect(self._create_compta_file)
        self.ui.action_imprimer.setShortcut("Ctrl+p")
        self.ui.action_imprimer.triggered.connect(self._create_html_file)
        self.ui.action_quitter.setShortcut("Ctrl+q")
        self.ui.action_quitter.triggered.connect(self.close)

        # Menu Edition
        action_vierges = QtGui.QAction(u"Créer des bordereaux vierges", self)
        action_vierges.triggered.connect(self._add_vierges)
        self.ui.menuEdition.addAction(action_vierges)
        action_requete = QtGui.QAction(u"Créer requête ORSEE", self)
        action_requete.triggered.connect(self._creer_requete)
        self.ui.menuEdition.addAction(action_requete)
        action_clear = QtGui.QAction(u"Vider la liste", self)
        action_clear.triggered.connect(self._vider_liste)
        self.ui.menuEdition.addAction(action_clear)
        # Menu Aide
        self.ui.action_afficherAide.triggered.connect(self._afficher_aide)
        self.ui.action_afficherPropos.triggered.connect(self._afficher_propos)

    def _add_subjects(self):
        """
        Récupère le fichier csv avec la liste des sujets et le fait charger
        dans la table
        """
        fichier = self._get_fichier()
        if fichier:
            self._bordereau_main.add_subjects(fichier)

    def _add_new(self):
        logger.info("_afficher_new")
        ecran_new = DNew(self._bordereau_main, self)
        if ecran_new.exec_():
            nom, prenom = ecran_new.get_infos()
            self._bordereau_main.add_subject(nom, prenom)

    def _add_vierges(self):
        """
        Input dialog qui demande le nombre de bordereaux à créer
        """
        nombre, ok = QtGui.QInputDialog.getInt(
            self,  u"Bordereaux vierges", u"Nombre de borderaux à créer",
            value=1,  min=1, max=200, step=1)
        if ok:
            self._bordereau_main.add_vierges(nombre)

    def _remove_selected(self):
        selec_model = self.ui.tableView_sujets.selectionModel()
        selected = selec_model.selectedRows()
        if not selected:
            return
        confirmation =  QtGui.QMessageBox.question(
            self, u"Supprimer?", u"Supprimer la sélection?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if confirmation != QtGui.QMessageBox.Yes:
            return
        for i in selected:
            self._bordereau_main.table_subjects.removeRow(i.row())

    def _set_data(self):
        """
        Récupération des informations de l'interface graphique
        (saisies ou valeurs par défault)
        """
        logger.debug("_set_data")
        try:
            nom_experience = unicode(self.ui.lineEdit_nomExperience.text().
                                     toUtf8(), "utf-8")
            ville = unicode(self.ui.lineEdit_ville.text().toUtf8(), "utf-8")
            if not (nom_experience and ville):
                QtGui.QMessageBox.critical(
                    self, u"Erreur", u"Il faut remplir tous les champs"
                )
                return
        except UnicodeEncodeError:
            QtGui.QMessageBox.critical(
                self,  u"Problème",  u"Ne pas mettre d'accents svp.")
            return

        self._bordereau_main.nom_experience = nom_experience
        self._bordereau_main.ville = ville
        self._bordereau_main.premier_bordereau = self.ui.\
            spinBox_premierBordereau.value()
        self._bordereau_main.date = self.ui.dateEdit.date().toPyDate()
        self._bordereau_main.heure = self.ui.timeEdit.time().toPyTime()
        return 1

    def _create_html_file(self):
        """
        On crée un fichier html temporaire puis on le fait afficher
        dans le navigateur.
        Il suffit alors d'imprimer depuis le navigateur.
        """
        logger.debug("_exporter_html")
        if self._set_data():
            temp = tempfile.mkstemp('.html')
            with (codecs.open(temp[1], 'wb', "utf-8")) as f:
                f.write(self._bordereau_main.get_html())
            webbrowser.open(f.name) 
    
    def _create_compta_file(self):
        """
        Création du fichier de comptabilité, enregistré dans un fichier xls
        """
        logger.debug("_exporter_xls")
        if self._set_data():
            fichier_name = "{}_{}_{}.xls".format(
                self._bordereau_main.date.strftime(
                    self._bordereau_main.format_date_fichier),
                self._bordereau_main.heure.strftime(
                    self._bordereau_main.format_heure_fichier),
                self._bordereau_main.nom_experience)
            fichier = QtGui.QFileDialog.getSaveFileName(
                self,  "Enregistrer sous ...",  fichier_name)
            if fichier:
                self._bordereau_main.get_xls().save(fichier)
    
    def _vider_liste(self):
        logger.info("_vider_liste")
        self._bordereau_main.table_subjects.vider_liste()

    def _creer_requete(self):
        ecran_req = DRequete(self,
                             experience=self.ui.lineEdit_nomExperience.text(),
                             date=self.ui.dateEdit.date(),
                             horaire=self.ui.timeEdit.time())
        if ecran_req.exec_():
            expe, date, heure = ecran_req.get_infos()
            dinfo = DInformation(u"Requête ORSEE",
                                 textes.get_requete(expe, date, heure), self)
            dinfo.exec_()

    def _afficher_aide(self):
        logger.info(u"_afficher_aide")
        ecran_information = DInformation(
            u"Aide", textes.AIDE, self)
        ecran_information.setFixedSize(500, 600)
        ecran_information.exec_()
    
    def _afficher_propos(self):
        logger.info(u"_afficher_propos")
        ecran_information = DInformation(
            u"A propos", textes.AUTEUR, self)
        ecran_information.exec_()
        
    def _move_line(self):
        sender = self.sender()
        direction = -1 if sender == self.ui.pushButton_monter else 1
        selec_model = self.ui.tableView_sujets.selectionModel()
        selected = selec_model.selectedRows()
        if not selected:
            return
        index = selected[0]
        self._bordereau_main.table_subjects.move(index.row(), direction)
        row_new = index.row() + direction
        index_new = self._bordereau_main.table_subjects.createIndex(row_new, 0)
        selec_model.clearSelection()
        selec_model.select(index_new,
                           QtGui.QItemSelectionModel.SelectCurrent |
                           QtGui.QItemSelectionModel.Rows
                          )

    def _get_fichier(self, extension="csv"):
        fichier = QtGui.QFileDialog.getOpenFileName(
            self, u"Sélectionner le fichier", "",
            u"Fichier {0} (*.{0})".format(extension))
        return fichier

    def closeEvent(self, event):
        confirmation = QtGui.QMessageBox.question(
            self,  u"Confirmation",  u"Quitter l'application?",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if confirmation == QtGui.QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    dossier_courant = os.path.abspath(
        os.path.dirname(os.path.realpath(__file__)))
    logging.basicConfig(
        filename=os.path.join(dossier_courant, 'LE2M_bordereaux.log'),
        filemode='w', level=logging.INFO)
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(u"LE2M Bordereaux")
    # pour que les boites et boutons systèmes soient en français
    translator = QtCore.QTranslator()
    locale = QtCore.QLocale.system().name()
    translator.load(
        QtCore.QString("qt_") + locale, QtCore.QLibraryInfo.location(
            QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)
    main = le2mBordereaux_main.Main(dossier_courant)
    ecran = GuiMain(main)
    ecran.show()
    sys.exit(app.exec_())