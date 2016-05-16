# -*- coding: utf-8 -*-
"""
Ce module contient le modèle de la table dans laquelle sont placés les
bordereaux
"""

from PyQt4 import QtCore 
import logging
from le2mBordereaux_util import get_prenom

logger = logging.getLogger(__name__)

UP = -1
DOWN = 1


class BordereauxTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(BordereauxTableModel, self).__init__(parent)
        self.colonnes = [u"NOM",  u"Prénom",  u"Créer bordereau"]
        self.liste_sujets = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.liste_sujets)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.colonnes)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            ligne, colonne = index.row(), index.column()
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
            elif role == QtCore.Qt.DisplayRole: 
                if colonne < 2:
                    return QtCore.QString.fromUtf8(
                        self.liste_sujets[ligne][colonne])
                else:
                    return QtCore.QVariant()
            elif role == QtCore.Qt.CheckStateRole:
                if colonne == 2: 
                    if self.liste_sujets[ligne][colonne]:
                        return QtCore.QVariant(QtCore.Qt.Checked)
                    else:
                        return QtCore.QVariant(QtCore.Qt.Unchecked)
                else:
                    return QtCore.QVariant()
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal: 
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.colonnes[col])
            elif role == QtCore.Qt.ToolTipRole:
                if col == 2:
                    return QtCore.QVariant(u'Cliquer pour inverser la sélection')
        return QtCore.QVariant()
                
    def flags(self, index):
        if index.isValid():
            if index.column() == 2:
                return QtCore.Qt.ItemFlags(
                    QtCore.QAbstractTableModel.flags(self, index) |
                    QtCore.Qt.ItemIsUserCheckable)
            else:
                return QtCore.Qt.ItemFlags(
                    QtCore.QAbstractTableModel.flags(self, index) |
                    QtCore.Qt.ItemIsEditable)
        return \
            QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, index))
        
    def setData(self, index, value, role):
        if index.isValid():
            ligne, colonne = index.row(), index.column()
            if role == QtCore.Qt.EditRole and colonne < 2: 
                if colonne == 0:
                    self.liste_sujets[ligne][colonne] = unicode(
                        value.toString().toUtf8(), "utf-8").upper()
                elif colonne == 1:
                    temp = unicode(value.toString().toUtf8(), "utf-8")
                    # self.liste_sujets[ligne][colonne] = u"{}{}".format(
                    #     temp[0].upper(), temp[1:].lower()
                    # )
                    self.liste_sujets[ligne][colonne] = get_prenom(temp)
                self.dataChanged.emit(index, index)
                return True
            elif role == QtCore.Qt.CheckStateRole:
                if colonne == 2: 
                    if value == QtCore.Qt.Checked:
                        self.liste_sujets[ligne][2] = True
                    elif value == QtCore.Qt.Unchecked:
                        self.liste_sujets[ligne][2] = False
                    presents = [
                        sujet for sujet in self.liste_sujets if sujet[2]
                    ]
                    self.label_suiveur_nombre.setText("{}".format(
                        len(presents))
                    )
                    return True
        return False
     
    def ajouter_ligne(self, ligne):
        self.insertRow(len(self.liste_sujets), ligne)

    def insertRow(self, row, ligne, parent=QtCore.QModelIndex()):
        logger.info(u"insertRow: {} - {}".format(row, ligne))
        self.beginInsertRows(parent, row, row)
        self.liste_sujets.insert(row, ligne)
        self.endInsertRows()
        return
        
    def removeRow(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        ligne = self.liste_sujets.pop(row)
        logger.info(u"removeRow: {} - {}".format(row, ligne))
        self.endRemoveRows()
        return
        
    def get_presents(self):
        return [ligne for ligne in self.liste_sujets if ligne[2]]
        
    def vider_liste(self):
        logger.info(u"vider_liste")
        while self.liste_sujets:
            self.removeRow(len(self.liste_sujets)-1)
        
    def inverser_selection(self):
        for r in range(self.rowCount()):
            index = self.createIndex(r, 2)
            if not self.liste_sujets[r][2]:
                self.setData(index, QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
            else:
                self.setData(index, QtCore.Qt.Unchecked,
                             QtCore.Qt.CheckStateRole)
            # self.emit(
            #     QtCore.SIGNAL("dataChanged(const QModelIndex &, "
            #                   "const QModelIndex &)"), index, index
            # )
            self.dataChanged.emit(index, index)
    
    def set_suiveur_nombre(self, le_label):
        self.label_suiveur_nombre = le_label
        
    def move(self, index, direction=UP):
        if index + direction < 0 or index + direction > len(self.liste_sujets):
            return
        ligne = self.liste_sujets[index]
        self.removeRow(index)
        index_new = index + direction
        self.insertRow(index_new, ligne)
