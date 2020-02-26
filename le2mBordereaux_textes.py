# -*- coding: utf-8 -*-
"""
Ce module contient les textes et les méthodes statiques de l'application
"""
__author__ = 'Dimitri DUBOIS'

AIDE = u"<html><body>" \
        u"<h4>Cr&eacute;ation de bordereaux pour la " \
        u"r&eacute;mun&eacute;ration des sujets</h4>" \
        u"Plusieurs possibilit&eacute;s" \
        u"<ul>" \
        u"<li>Importer la liste des sujets depuis un fichier csv " \
        u"cr&eacute;&eacute; depuis phpmyadmin</li>" \
        u"<li>Cr&eacute;er les bordereaux un par un</li>" \
        u"<li>Cr&eacute;er des bordereaux vierges</li>" \
        u"</ul>" \
        u"<p>Ensuite, cocher les sujets présents, puis enregistrer et " \
        u"imprimer</p>" \
        u"<h4>Enregistrer</h4>" \
        u"<p>Cr&eacute;e un fichier *.xls avec les sujets. Pr&eacute;pare " \
        u"le fichier pour la comptabilit&eacute;.</p>" \
        u"<h4>Imprimer</h4>" \
        u"<p>Cr&eacute;e un fichier html temporaire qui est " \
        u"imm&eacute;diatement affich&eacute; dans le navigateur. Il faut, " \
        u"depuis le navigateur, imprimer le fichier.</p>" \
        u"<h4>Requ&ecirc;te pour obtenir la liste des participants</h4>" \
        u"<p>Rentrer les informations nécessaires (nom public de " \
        u"l'exp&eacute;rience, date et heure de la session). Cette " \
        u"requ&ecirc;te est &agrave; copier dans une requ&ecirc;te phpmyadmin " \
        u"sur la table ORSEE.</p>" \
        u"<p>&nbsp;</p>" \
        u"</body></html>"

AUTEUR = u"<hml><body>" \
        u"<p>D&eacute;velopp&eacute; par Dimitri DUBOIS<br/>" \
        u"Contact: " \
        u"<a href=\"mailto:dimitri.dubois@lameta.univ-montp1.fr\">" \
        u"dimitri.dubois@lameta.univ-montp1.fr</a><br/><br/>" \
        u"LAMETA - CNRS<br/>" \
        u"Facult&eacute; d'Economie de Montpellier<br/>" \
        u"Web: " \
        u"<a href=\"http://www.duboishome.info/dimitri/\">" \
        u"http://www.duboishome.info/dimitri</a></p>" \
        u"<p>Autre projet: " \
        u"<a href=\"http://www.duboishome.info/dimitri/" \
        u"index.php?page=le2m&lang=fr\">LE2M</a></p>" \
        u"</body></html>"


# def get_requete(expe, date, heure):
#     req = u"SELECT sub.lname, sub.fname\n" \
#           u"FROM or_participants sub, or_experiments exp, or_sessions " \
#           u"sess, or_participate_at part\n" \
#           u"WHERE exp.experiment_name = '{}'\n" \
#           u"AND sess.experiment_id = exp.experiment_id\n" \
#           u"AND sess.session_start_month = {}\n" \
#           u"AND sess.session_start_day = {}\n" \
#           u"AND sess.session_start_hour = {}\n" \
#           u"AND sess.session_start_minute = {}\n" \
#           u"AND part.session_id = sess.session_id\n" \
#           u"AND part.registered = 'y'\n" \
#           u"AND sub.participant_id = part.participant_id\n" \
#           u"order by sub.lname".format(expe, date.month, date.day,
#                                        heure.hour, heure.minute)
#     return req


def get_requete(expe, date, heure):
    req = u"SELECT sub.lname, sub.fname\n" \
          u"FROM or_participants sub, or_experiments exp, or_sessions " \
          u"sess, or_participate_at part\n" \
          u"WHERE exp.experiment_name = '{}'\n" \
          u"AND sess.experiment_id = exp.experiment_id\n" \
          u"AND sess.session_start = {}{}\n" \
          u"AND part.session_id = sess.session_id\n" \
          u"AND sub.participant_id = part.participant_id\n" \
          u"order by sub.lname sub.fname".format(expe, date.strftime("%Y%m%d"), heure.strftime("%H%M"))
    return req