"""Interface en ligne de commande du gestionnaire de réservations.

Ce fichier contient toutes les entrées/sorties (input / print).
La logique métier reste dans src/reservation.py.
"""

import sys
from datetime import datetime
from pathlib import Path

# Permet d'importer src/reservation.py quand on lance : python main.py
sys.path.insert(0, str(Path(__file__).parent / "src"))

from reservation import GestionnaireReservations, ReservationError  # noqa: E402

FORMAT_DATE = "%Y-%m-%d %H:%M"

MENU = """
===== Réservation de salles =====
1. Ajouter une salle
2. Réserver une salle
3. Annuler une réservation
4. Lister les réservations d'une salle
5. Vérifier une disponibilité
0. Quitter
"""


def lire_entier(message):
    return int(input(message))


def lire_date(message):
    return datetime.strptime(input(message).strip(), FORMAT_DATE)


def lire_creneau():
    debut = lire_date("Début (AAAA-MM-JJ HH:MM) : ")
    fin = lire_date("Fin   (AAAA-MM-JJ HH:MM) : ")
    return debut, fin


def afficher(reservation):
    print(
        f"  n°{reservation.id} | {reservation.salle} | "
        f"{reservation.debut:%d/%m/%Y %H:%M} → {reservation.fin:%H:%M} | "
        f"{reservation.participants} pers."
    )


def main():
    gestionnaire = GestionnaireReservations()

    while True:
        print(MENU)
        choix = input("Votre choix : ").strip()

        try:
            if choix == "1":
                nom = input("Nom de la salle : ").strip()
                capacite = lire_entier("Capacité : ")
                salle = gestionnaire.ajouter_salle(nom, capacite)
                print(f"✔ Salle '{salle.nom}' créée ({salle.capacite} places).")

            elif choix == "2":
                nom = input("Nom de la salle : ").strip()
                debut, fin = lire_creneau()
                participants = lire_entier("Participants : ")
                reservation = gestionnaire.reserver(nom, debut, fin, participants)
                print("✔ Réservation enregistrée :")
                afficher(reservation)

            elif choix == "3":
                id_reservation = lire_entier("Numéro de la réservation : ")
                gestionnaire.annuler(id_reservation)
                print(f"✔ Réservation n°{id_reservation} annulée.")

            elif choix == "4":
                nom = input("Nom de la salle : ").strip()
                reservations = gestionnaire.reservations_de(nom)
                if not reservations:
                    print("Aucune réservation.")
                for reservation in reservations:
                    afficher(reservation)

            elif choix == "5":
                nom = input("Nom de la salle : ").strip()
                debut, fin = lire_creneau()
                if gestionnaire.est_disponible(nom, debut, fin):
                    print("✔ Créneau disponible.")
                else:
                    print("✘ Créneau occupé.")

            elif choix == "0":
                print("Au revoir !")
                break

            else:
                print("Choix invalide.")

        except ReservationError as erreur:
            # Erreurs métier : message clair venant du module
            print(f"✘ Refusé : {erreur}")
        except ValueError:
            # Saisie mal formée (lettres au lieu d'un nombre, date au mauvais format)
            print("✘ Saisie invalide : vérifiez le format (nombre entier, date AAAA-MM-JJ HH:MM).")


if __name__ == "__main__":
    main()