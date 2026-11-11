"""Gestion de réservations de salles.

Ce module contient uniquement la logique métier : aucun print(), aucun input().
Chaque méthode renvoie une valeur ou lève une exception, ce qui la rend testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from itertools import count


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ReservationError(Exception):
    """Classe de base de toutes les erreurs du module."""


class SalleDejaExistanteError(ReservationError):
    """R1 : une salle porte déjà ce nom."""


class DonneeInvalideError(ReservationError):
    """R2 / R4 : capacité ou nombre de participants invalide."""


class CreneauInvalideError(ReservationError):
    """R3 : l'heure de fin n'est pas postérieure à l'heure de début."""


class CapaciteDepasseeError(ReservationError):
    """R4 : trop de participants pour la salle."""


class ChevauchementError(ReservationError):
    """R5 : le créneau chevauche une réservation existante."""


class SalleInexistanteError(ReservationError):
    """R7 : la salle demandée n'existe pas."""


class ReservationInexistanteError(ReservationError):
    """R8 : l'identifiant de réservation est inconnu."""


# ---------------------------------------------------------------------------
# Modèles de données
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Salle:
    nom: str
    capacite: int


@dataclass(frozen=True)
class Reservation:
    id: int
    salle: str
    debut: datetime
    fin: datetime
    participants: int

    def chevauche(self, debut: datetime, fin: datetime) -> bool:
        """Intervalles semi-ouverts [debut, fin[ : des créneaux adjacents ne se chevauchent pas (R6)."""
        return self.debut < fin and debut < self.fin


# ---------------------------------------------------------------------------
# Gestionnaire
# ---------------------------------------------------------------------------

def _est_entier_positif(valeur: object) -> bool:
    # bool est une sous-classe de int : on l'exclut explicitement (True ne doit pas valoir 1 participant)
    return isinstance(valeur, int) and not isinstance(valeur, bool) and valeur > 0


class GestionnaireReservations:
    """Stocke les salles et les réservations et applique les règles métier."""

    def __init__(self) -> None:
        self._salles: dict[str, Salle] = {}
        self._reservations: dict[int, Reservation] = {}
        self._compteur = count(1)

    # --- méthodes internes -------------------------------------------------

    def _salle(self, nom: str) -> Salle:
        try:
            return self._salles[nom]
        except KeyError:
            raise SalleInexistanteError(f"La salle '{nom}' n'existe pas.") from None

    @staticmethod
    def _verifier_creneau(debut: datetime, fin: datetime) -> None:
        if fin <= debut:
            raise CreneauInvalideError("L'heure de fin doit être postérieure à l'heure de début.")

    # --- API publique ------------------------------------------------------

    def ajouter_salle(self, nom: str, capacite: int) -> Salle:
        if not _est_entier_positif(capacite):
            raise DonneeInvalideError("La capacité doit être un entier strictement positif.")
        if nom in self._salles:
            raise SalleDejaExistanteError(f"La salle '{nom}' existe déjà.")
        salle = Salle(nom, capacite)
        self._salles[nom] = salle
        return salle

    def reserver(self, nom_salle: str, debut: datetime, fin: datetime, participants: int) -> Reservation:
        salle = self._salle(nom_salle)
        self._verifier_creneau(debut, fin)
        if not _est_entier_positif(participants):
            raise DonneeInvalideError("Le nombre de participants doit être un entier strictement positif.")
        if participants > salle.capacite:
            raise CapaciteDepasseeError(
                f"{participants} participants pour une capacité de {salle.capacite}."
            )
        for existante in self.reservations_de(nom_salle):
            if existante.chevauche(debut, fin):
                raise ChevauchementError(
                    f"Le créneau chevauche la réservation n°{existante.id}."
                )
        reservation = Reservation(next(self._compteur), nom_salle, debut, fin, participants)
        self._reservations[reservation.id] = reservation
        return reservation

    def annuler(self, id_reservation: int) -> None:
        if id_reservation not in self._reservations:
            raise ReservationInexistanteError(f"La réservation n°{id_reservation} n'existe pas.")
        del self._reservations[id_reservation]

    def reservations_de(self, nom_salle: str) -> list[Reservation]:
        self._salle(nom_salle)  # lève SalleInexistanteError si besoin
        return sorted(
            (r for r in self._reservations.values() if r.salle == nom_salle),
            key=lambda r: r.debut,
        )

    def est_disponible(self, nom_salle: str, debut: datetime, fin: datetime) -> bool:
        self._verifier_creneau(debut, fin)
        return not any(r.chevauche(debut, fin) for r in self.reservations_de(nom_salle))
