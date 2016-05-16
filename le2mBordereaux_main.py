# -*- coding: utf-8 -*-
"""
Ce module contient le modèle de l'application, c'est à dire les attributs
et méthodes non graphiques
"""
import xlwt
import csv
import logging
from le2mBordereaux_tableModel import BordereauxTableModel
from le2mBordereaux_util import get_prenom


logger = logging.getLogger(__name__)


class Main(object):
    def __init__(self, dossier_courant):
        self._dossier_courant = dossier_courant
        self._nom_experience = ""
        self._ville = ""
        self._premier_bordereau = 0
        self._nombre_bordereaux = 0
        self._table_subjects = BordereauxTableModel()
        self._date = ""
        self._heure = ""
        self._format_date_bord = "%d/%m/%Y"
        self._format_date_fichier = "%Y%m%d"
        self._format_heure_bord = "%Hh%M"
        self._format_heure_fichier = "%Hh%M"

    def add_subject(self, nom, prenom):
        self.table_subjects.ajouter_ligne(
                [nom.upper(), get_prenom(prenom), False])

    def add_subjects(self, fichier):
        """
        Ouvre le fichier et ajoute les sujets dans la table
        """
        logger.debug("traiter_fichier")
        with open(fichier, 'rb') as f:
            fcsv = csv.reader(f, delimiter=',')
            for row in fcsv:
                try:
                    self._table_subjects.ajouter_ligne(
                        [unicode(row[0], "utf-8").upper(),
                         get_prenom(unicode(row[1], "utf-8")), False])
                except UnicodeError:
                    self._table_subjects.ajouter_ligne(
                        [row[0].upper(), get_prenom(row[1]), False])

    def add_vierges(self, nombre):
        for i in xrange(nombre):
            self.table_subjects.ajouter_ligne(["",  "",  True])
        nb_presents = len([sujet for sujet in
                           self.table_subjects.liste_sujets if sujet[2]])
        self.table_subjects.label_suiveur_nombre.setText(
            "{}".format(nb_presents))

    def get_xls(self):
        """
        Renvoie un workbook pour enregistrer dans un fichier excel
        """
        logger.debug("get_xls")
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Bordereau")
        ws.write(0,  0,  u"Date: {} -- Heure: {}".format(
            self.date.strftime(self._format_date_bord),
            self.heure.strftime(self._format_heure_bord))
                )
        ws.write(1,  0,  u"Experience: {}".format(self.nom_experience))
        header = [u"Souche", u"Nom", u"Prenom", u"Gain", u"Forfait", u"Total"]
        format_header = xlwt.easyxf('font: bold 1;')
        for i in range(6):
            ws.write(3, i, header[i], format_header)
        sujets = self._table_subjects.get_presents()
        nombre_a_creer = len(sujets)
        format_money = xlwt.easyxf(num_format_str=u'#,##0.00[$\u20ac-1]')
        for i in xrange(nombre_a_creer):
            numero_bordereau = self._premier_bordereau + i
            ws.write(4+i, 0, numero_bordereau)
            ws.write(4+i, 1, sujets[i][0])
            ws.write(4+i, 2, sujets[i][1])
            ws.write(4+i, 3, 0.00, format_money)
            ws.write(4+i, 4, 6.00, format_money)
            ws.write(4+i, 5, xlwt.Formula('SUM(D{}:E{})'.format(5+i, 5+i)),
                     format_money)
        format_total = xlwt.easyxf("font: bold 1;")
        ws.write(4 + nombre_a_creer, 2, "Total", format_total)
        ws.write(4 + nombre_a_creer + 1,  2, u"Dont")
        ws.write(4 + nombre_a_creer + 2,  2, u"Total forfait 2€", format_total)
        ws.write(4 + nombre_a_creer + 3,  2, u"Total forfait 6€", format_total)
        format_total_money = xlwt.easyxf('font: bold 1;',
                                         num_format_str=u'#,##0.00[$\u20ac-1]')
        ws.write(4 + nombre_a_creer, 3, xlwt.Formula('SUM(D5:D{})'.format(
            4 + nombre_a_creer)), format_total_money)
        ws.write(4 + nombre_a_creer, 4, xlwt.Formula('SUM(E5:E{})'.format(
            4 + nombre_a_creer)), format_total_money)
        ws.write(4 + nombre_a_creer, 5, xlwt.Formula('SUM(F5:F{})'.format(
            4 + nombre_a_creer)), format_total_money)
        ws.write(4 + nombre_a_creer + 2,  4, xlwt.Formula(
            "SUMIF(E5:E{}, 2)".format(4 + nombre_a_creer)), format_total_money)
        ws.write(4 + nombre_a_creer + 3,  4, xlwt.Formula(
            "SUMIF(E5:E{}, 6)".format(4 + nombre_a_creer)), format_total_money)
        return wb  
  
    def get_html(self):
        """
        Renvoie un string avec les bordereaux en html pour impression
        """
        logger.debug("get_html")
        # header
        html = u"<html><head>" \
               u"<meta http-equiv='X-UA-Compatible' content='IE=8' />" \
               u"<meta http-equiv='Content-Type' content='text/html'; " \
               u"charset='utf-8'>" \
               u"</head>" \
               u"<body>"
        # création des bordereaux
        sujets = self._table_subjects.get_presents()
        nombre_a_creer = len(sujets)
        nombre_pages = nombre_a_creer / 4
        if nombre_a_creer % 4 > 0:
            nombre_pages += 1
        numero_bordereau = self._premier_bordereau
        compteur_sujet = 0
        for p in xrange(nombre_pages):
            html += u"<p>Date: {} -- Heure: {} -- Exp&eacute;rience: {}".format(
                self.date.strftime(self._format_date_bord),
                self.heure.strftime(self._format_heure_bord),
                self.nom_experience)
            for i in xrange(4):
                if compteur_sujet >= nombre_a_creer:
                    break
                html += u"<p><table border=1 width = 500 rules = 'none'>" \
                        u"<tr><td colspan=2>Souche N&deg; {}</td></tr>" \
                        u"<tr><td colspan=2>Forfait de d&eacute;placement" \
                        u"<input type = 'checkbox'>2&euro; " \
                        u"<input type = 'checkbox'>6&euro;</td></tr>" \
                        u"<tr><td colspan = 2 align = 'right'>" \
                        u"Montant ____________ &euro;</td></tr>" \
                        u"<tr>" \
                        u"<td colspan=2>Remis &agrave; <b><i>{} {}</i></b></td>" \
                        u"</tr><tr><td colspan=2>la somme de </td></tr>" \
                        u"<tr height=30><td colspan=2><hr /></td></tr>" \
                        u"<tr height = 75 valign='top'><td width=250>" \
                        u"A {} le {}</td><td align='center'>Signature</td></tr>" \
                        u"</table></p>\n".format(
                            numero_bordereau, sujets[compteur_sujet][0],
                            sujets[compteur_sujet][1], self.ville,
                            self.date.strftime(self._format_date_bord))
                numero_bordereau += 1
                compteur_sujet += 1
            if p < nombre_pages - 1:
                html += u"<div style='page-break-after: always'></div>\n"
        html += u"</body></html>"
        return html

    @property
    def dossier_courant(self):
        return self._dossier_courant

    @property
    def table_subjects(self):
        return self._table_subjects

    @property
    def nom_experience(self):
        return self._nom_experience

    @nom_experience.setter
    def nom_experience(self, value):
        self._nom_experience = value

    @property
    def ville(self):
        return self._ville

    @ville.setter
    def ville(self, value):
        self._ville = value

    @property
    def premier_bordereau(self):
        return self._premier_bordereau

    @premier_bordereau.setter
    def premier_bordereau(self, num):
        self._premier_bordereau = num

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def heure(self):
        return self._heure

    @heure.setter
    def heure(self, value):
        self._heure = value

    @property
    def format_date_fichier(self):
        return self._format_date_fichier

    @property
    def format_heure_fichier(self):
        return self._format_heure_fichier