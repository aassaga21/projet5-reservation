"""Tests des cas limites et des erreurs attendues."""

from datetime import datetime

import pytest

from reservation import (
    CapaciteDepasseeError,
    ChevauchementError,
    CreneauInvalideError,
    DonneeInvalideError,
    ReservationInexistanteError,
    SalleDejaExistanteError,
    SalleInexistanteError,
)


def h(heure, minute=0):
    """Raccourci : une heure le 10 novembre 2026."""
    return datetime(2026, 11, 10, heure, minute)


# --- Salles ----------------------------------------------------------------

def test_salle_en_double(gestionnaire_avec_salle):
    with pytest.raises(SalleDejaExistanteError):
        gestionnaire_avec_salle.ajouter_salle("Alpha", 5)


@pytest.mark.parametrize("capacite", [0, -1])
def test_capacite_invalide(gestionnaire, capacite):
    with pytest.raises(DonneeInvalideError):
        gestionnaire.ajouter_salle("Alpha", capacite)


# --- Créneaux --------------------------------------------------------------

def test_fin_avant_debut(gestionnaire_avec_salle):
    with pytest.raises(CreneauInvalideError):
        gestionnaire_avec_salle.reserver("Alpha", h(11), h(10), 5)


def test_fin_egale_debut(gestionnaire_avec_salle):
    with pytest.raises(CreneauInvalideError):
        gestionnaire_avec_salle.reserver("Alpha", h(10), h(10), 5)


# --- Participants et capacité ----------------------------------------------

@pytest.mark.parametrize("participants", [0, -3])
def test_participants_invalides(gestionnaire_avec_salle, participants):
    with pytest.raises(DonneeInvalideError):
        gestionnaire_avec_salle.reserver("Alpha", h(10), h(11), participants)


def test_capacite_exacte(gestionnaire_avec_salle):
    reservation = gestionnaire_avec_salle.reserver("Alpha", h(10), h(11), 10)

    assert reservation.participants == 10


def test_capacite_depassee(gestionnaire_avec_salle):
    with pytest.raises(CapaciteDepasseeError):
        gestionnaire_avec_salle.reserver("Alpha", h(10), h(11), 11)


# --- Chevauchements (réservation existante : 10h00 → 11h00) ----------------

@pytest.mark.parametrize(
    "debut, fin",
    [
        (h(9, 30), h(10, 30)),   # chevauche le début
        (h(10, 30), h(11, 30)),  # chevauche la fin
        (h(10, 15), h(10, 45)),  # inclus dans le créneau existant
        (h(9), h(12)),           # englobe le créneau existant
        (h(10), h(11)),          # identique
    ],
    ids=["debut", "fin", "inclus", "englobant", "identique"],
)
def test_chevauchements(gestionnaire_avec_reservation, debut, fin):
    with pytest.raises(ChevauchementError):
        gestionnaire_avec_reservation.reserver("Alpha", debut, fin, 2)


@pytest.mark.parametrize(
    "debut, fin",
    [
        (h(9), h(10)),   # se termine pile quand l'autre commence
        (h(11), h(12)),  # commence pile quand l'autre se termine
    ],
    ids=["juste_avant", "juste_apres"],
)
def test_creneaux_adjacents(gestionnaire_avec_reservation, debut, fin):
    gestionnaire_avec_reservation.reserver("Alpha", debut, fin, 2)

    assert len(gestionnaire_avec_reservation.reservations_de("Alpha")) == 2


# --- Éléments inexistants --------------------------------------------------

def test_salle_inexistante_reserver(gestionnaire):
    with pytest.raises(SalleInexistanteError):
        gestionnaire.reserver("Inconnue", h(10), h(11), 2)


def test_salle_inexistante_lister(gestionnaire):
    with pytest.raises(SalleInexistanteError):
        gestionnaire.reservations_de("Inconnue")


def test_annuler_inexistante(gestionnaire_avec_salle):
    with pytest.raises(ReservationInexistanteError):
        gestionnaire_avec_salle.annuler(999)


def test_annuler_deux_fois(gestionnaire_avec_reservation):
    reservation = gestionnaire_avec_reservation.reservations_de("Alpha")[0]
    gestionnaire_avec_reservation.annuler(reservation.id)

    with pytest.raises(ReservationInexistanteError):
        gestionnaire_avec_reservation.annuler(reservation.id)


# --- Robustesse ------------------------------------------------------------

def test_echec_sans_effet(gestionnaire_avec_reservation):
    avant = gestionnaire_avec_reservation.reservations_de("Alpha")

    with pytest.raises(ChevauchementError):
        gestionnaire_avec_reservation.reserver("Alpha", h(10, 30), h(11, 30), 2)

    assert gestionnaire_avec_reservation.reservations_de("Alpha") == avant
