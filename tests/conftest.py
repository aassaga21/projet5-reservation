"""Fixtures partagées par tous les fichiers de tests."""

from datetime import datetime

import pytest

from reservation import GestionnaireReservations

# Dates de référence réutilisées dans les tests
H10 = datetime(2026, 11, 10, 10, 0)
H11 = datetime(2026, 11, 10, 11, 0)


@pytest.fixture
def gestionnaire():
    """Gestionnaire vide."""
    return GestionnaireReservations()


@pytest.fixture
def gestionnaire_avec_salle(gestionnaire):
    """Gestionnaire contenant la salle « Alpha » (capacité 10)."""
    gestionnaire.ajouter_salle("Alpha", 10)
    return gestionnaire


@pytest.fixture
def gestionnaire_avec_reservation(gestionnaire_avec_salle):
    """« Alpha » réservée de 10h00 à 11h00 pour 5 personnes."""
    gestionnaire_avec_salle.reserver("Alpha", H10, H11, 5)
    return gestionnaire_avec_salle
