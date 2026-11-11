"""Tests des cas nominaux : le module fonctionne quand on l'utilise correctement."""

from datetime import datetime

from reservation import Reservation, Salle

H09 = datetime(2026, 11, 10, 9, 0)
H10 = datetime(2026, 11, 10, 10, 0)
H11 = datetime(2026, 11, 10, 11, 0)
H12 = datetime(2026, 11, 10, 12, 0)
H14 = datetime(2026, 11, 10, 14, 0)
H15 = datetime(2026, 11, 10, 15, 0)


def test_ajouter_salle(gestionnaire):
    salle = gestionnaire.ajouter_salle("Alpha", 10)

    assert salle == Salle("Alpha", 10)


def test_reserver_creneau_libre(gestionnaire_avec_salle):
    reservation = gestionnaire_avec_salle.reserver("Alpha", H10, H11, 5)

    assert isinstance(reservation, Reservation)
    assert reservation.salle == "Alpha"
    assert reservation.debut == H10
    assert reservation.fin == H11
    assert reservation.participants == 5
    assert gestionnaire_avec_salle.reservations_de("Alpha") == [reservation]


def test_identifiants_uniques(gestionnaire_avec_salle):
    r1 = gestionnaire_avec_salle.reserver("Alpha", H10, H11, 5)
    r2 = gestionnaire_avec_salle.reserver("Alpha", H14, H15, 5)

    assert r1.id != r2.id


def test_annuler_reservation(gestionnaire_avec_reservation):
    reservation = gestionnaire_avec_reservation.reservations_de("Alpha")[0]

    gestionnaire_avec_reservation.annuler(reservation.id)

    assert gestionnaire_avec_reservation.reservations_de("Alpha") == []


def test_reservations_triees(gestionnaire_avec_salle):
    # On réserve volontairement dans le désordre
    tardive = gestionnaire_avec_salle.reserver("Alpha", H14, H15, 3)
    matinale = gestionnaire_avec_salle.reserver("Alpha", H09, H10, 3)
    milieu = gestionnaire_avec_salle.reserver("Alpha", H11, H12, 3)

    assert gestionnaire_avec_salle.reservations_de("Alpha") == [matinale, milieu, tardive]


def test_est_disponible_vrai(gestionnaire_avec_reservation):
    assert gestionnaire_avec_reservation.est_disponible("Alpha", H14, H15) is True


def test_est_disponible_faux(gestionnaire_avec_reservation):
    assert gestionnaire_avec_reservation.est_disponible("Alpha", H10, H11) is False


def test_reserver_apres_annulation(gestionnaire_avec_reservation):
    ancienne = gestionnaire_avec_reservation.reservations_de("Alpha")[0]
    gestionnaire_avec_reservation.annuler(ancienne.id)

    nouvelle = gestionnaire_avec_reservation.reserver("Alpha", H10, H11, 8)

    assert gestionnaire_avec_reservation.reservations_de("Alpha") == [nouvelle]


def test_meme_creneau_salles_differentes(gestionnaire_avec_salle):
    gestionnaire_avec_salle.ajouter_salle("Beta", 20)

    r_alpha = gestionnaire_avec_salle.reserver("Alpha", H10, H11, 5)
    r_beta = gestionnaire_avec_salle.reserver("Beta", H10, H11, 15)

    assert gestionnaire_avec_salle.reservations_de("Alpha") == [r_alpha]
    assert gestionnaire_avec_salle.reservations_de("Beta") == [r_beta]
