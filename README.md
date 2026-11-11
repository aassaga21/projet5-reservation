---
title: Projet 5 — Mini-application de réservation de salles testée avec pytest
tags: GIT, Python, pytest, tests, E3
description: Module Python de réservation de salles et suite de tests automatisés pytest avec mesure de couverture
---

# Projet 5 — Réservation de salles testée avec pytest

[TOC]

:::info
**Étudiante :** Alexandra Assaga
**Classe :** E3 — Bachelor Systèmes et Réseaux, Geneva Institute of Technology
**Cours :** Python — Principes de base
**Durée :** 1 semaine (PPE)
**Dépôt GitHub :** [github.com/aassaga21/projet5-reservation](https://github.com/aassaga21/projet5-reservation)
:::

## 1. Contexte

Avant d'intégrer une équipe de développement, il faut livrer un petit module Python accompagné d'une suite de tests automatisés qui démontre sa fiabilité. Le cas métier retenu est la **gestion de réservations de salles**.

## 2. Objectifs

- Concevoir un module Python organisé en classes et fonctions testables
- Isoler la logique métier des entrées/sorties
- Écrire une suite de tests **pytest** couvrant les cas nominaux, les cas limites et les erreurs attendues
- Mesurer et documenter le taux de réussite et la **couverture** des tests

## 3. Cas métier retenu

:::success
Cas métier validé par le formateur : **réservation de salles**.
:::

**Fonctionnalités :**
- Créer une salle (nom, capacité)
- Réserver une salle sur un créneau (début, fin, nombre de participants)
- Annuler une réservation
- Consulter les réservations d'une salle et vérifier sa disponibilité

**Règles métier :**

| # | Règle |
|---|---|
| R1 | Deux salles ne peuvent pas porter le même nom |
| R2 | La capacité d'une salle doit être un entier strictement positif |
| R3 | L'heure de fin doit être strictement postérieure à l'heure de début |
| R4 | Le nombre de participants doit être ≥ 1 et ≤ capacité de la salle |
| R5 | Deux réservations d'une même salle ne peuvent pas se chevaucher |
| R6 | Des créneaux qui se touchent (fin 10h00 / début 10h00) sont autorisés |
| R7 | Impossible de réserver une salle inexistante |
| R8 | Impossible d'annuler une réservation inexistante |

**Condition de chevauchement :** deux créneaux `[d1, f1[` et `[d2, f2[` se chevauchent si `d1 < f2` **et** `d2 < f1`. Les intervalles sont semi-ouverts : la fin est exclue, ce qui rend la règle R6 vraie.

## 4. Environnement

| Élément | Commande | Version |
|---|---|---|
| OS | `winver` | Windows 11 Professionnel 26H2 |
| Python | `python --version` | 3.13.4 (venv créé avec `py -3.13`) |
| pytest | `pytest --version` | 9.2.0 |
| pytest-cov | `pip show pytest-cov` | 7.1.0 |

:::warning
Deux versions de Python sont installées sur le poste (3.13 et 3.15). Le venv est créé explicitement avec `py -3.13` pour garantir une version stable et compatible avec pytest.
:::

### Installation (Windows / PowerShell)

```powershell
cd $HOME\Documents
mkdir projet5-reservation
cd projet5-reservation
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1

pip install pytest pytest-cov
pip freeze > requirements.txt
```

![image](https://hackmd.io/_uploads/HyOakny0fg.png)
![image](https://hackmd.io/_uploads/H1BCZhJ0Mx.png)
![image](https://hackmd.io/_uploads/BkhmG21Czx.png)
![image](https://hackmd.io/_uploads/rkeZPzn1RMx.png)
![image](https://hackmd.io/_uploads/HJqOfh1AMg.png)

## 5. Architecture du projet

```
projet5-reservation/
├── src/
│   └── reservation.py     # logique métier (aucune entrée/sortie)
├── main.py                # interface en ligne de commande (entrées/sorties)
├── tests/
│   ├── conftest.py        # fixtures partagées
│   ├── test_nominaux.py   # cas nominaux
│   └── test_limites.py    # cas limites et erreurs
├── pyproject.toml         # configuration pytest
├── requirements.txt
└── README.md
```

### Création de la structure

```powershell
mkdir src, tests
New-Item src\reservation.py, main.py, tests\conftest.py, tests\test_nominaux.py, tests\test_limites.py, README.md -ItemType File
Set-Content pyproject.toml "[tool.pytest.ini_options]`npythonpath = [`"src`"]`ntestpaths = [`"tests`"]" -Encoding ascii
Get-Content pyproject.toml
pytest
```

Le premier lancement de `pytest` affiche `no tests ran` : c'est attendu, car les fichiers de tests sont encore vides. La ligne `configfile: pyproject.toml` confirme que la configuration est bien prise en compte.

![image](https://hackmd.io/_uploads/SJDGmnJCfg.png)
![image](https://hackmd.io/_uploads/ByqQm3yRMx.png)
![image](https://hackmd.io/_uploads/H1ahm3JAMe.png)
![image](https://hackmd.io/_uploads/HJHFt2yRze.png)
![image](https://hackmd.io/_uploads/Sk9Uhn10Mx.png)
![image](https://hackmd.io/_uploads/BkI5n310Gl.png)

### Configuration pytest (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

- `pythonpath = ["src"]` permet aux tests d'écrire `from reservation import ...`
- `testpaths = ["tests"]` indique à pytest où chercher les tests

### Principe de conception

La logique métier (`src/reservation.py`) ne contient ni `print()` ni `input()`. Chaque méthode **renvoie une valeur ou lève une exception**, ce qui permet de la tester directement. Toute l'interaction avec l'utilisateur est regroupée dans `main.py`.

```
Utilisateur ⇄ main.py (I/O) ⇄ reservation.py (logique) ⇄ tests pytest
```

### Classes

| Élément | Type | Rôle |
|---|---|---|
| `Salle` | dataclass (immuable) | Nom et capacité d'une salle |
| `Reservation` | dataclass (immuable) | Identifiant, salle, début, fin, nombre de participants |
| `GestionnaireReservations` | classe | Stocke les salles et réservations, applique les règles métier |

### Méthodes de `GestionnaireReservations`

| Méthode | Retour | Règles vérifiées |
|---|---|---|
| `ajouter_salle(nom, capacite)` | `Salle` | R1, R2 |
| `reserver(nom_salle, debut, fin, participants)` | `Reservation` | R3, R4, R5, R6, R7 |
| `annuler(id_reservation)` | `None` | R8 |
| `reservations_de(nom_salle)` | `list[Reservation]` triée par début | R7 |
| `est_disponible(nom_salle, debut, fin)` | `bool` | R3, R5, R7 |

### Choix techniques

| Choix | Raison |
|---|---|
| `Reservation.chevauche()` : `self.debut < fin and debut < self.fin` | Applique la règle des intervalles semi-ouverts : les créneaux adjacents sont autorisés (R6) |
| `_est_entier_positif()` exclut les booléens | En Python, `True == 1` : sans cette vérification, `True` serait accepté comme 1 participant |
| `itertools.count(1)` | Génère des identifiants de réservation uniques et croissants |
| Toutes les vérifications avant l'enregistrement | Une réservation refusée ne laisse aucune trace dans les données |

### Exceptions personnalisées

Toutes héritent de `ReservationError`, ce qui permet de les attraper d'un seul bloc dans `main.py`.

| Exception | Levée quand… | Règle |
|---|---|---|
| `SalleDejaExistanteError` | une salle porte déjà ce nom | R1 |
| `DonneeInvalideError` | capacité ou nombre de participants invalide | R2, R4 |
| `CreneauInvalideError` | fin ≤ début | R3 |
| `CapaciteDepasseeError` | participants > capacité | R4 |
| `ChevauchementError` | le créneau chevauche une réservation existante | R5 |
| `SalleInexistanteError` | la salle demandée n'existe pas | R7 |
| `ReservationInexistanteError` | l'identifiant de réservation est inconnu | R8 |

## 6. Stratégie de tests

### 6.1 Fixtures (`conftest.py`)

Les fixtures sont chaînées : chacune part de la précédente. Chaque test reçoit un état neuf, ce qui rend les tests indépendants les uns des autres.

| Fixture | Contenu |
|---|---|
| `gestionnaire` | Gestionnaire vide |
| `gestionnaire_avec_salle` | Gestionnaire contenant la salle « Alpha » (capacité 10) |
| `gestionnaire_avec_reservation` | « Alpha » réservée de 10h00 à 11h00 |

### 6.2 Cas nominaux (`test_nominaux.py`) — 9 tests

| Test | Ce qui est vérifié |
|---|---|
| `test_ajouter_salle` | La salle est créée avec le bon nom et la bonne capacité |
| `test_reserver_creneau_libre` | La réservation est créée et renvoyée |
| `test_identifiants_uniques` | Deux réservations ont des identifiants différents |
| `test_annuler_reservation` | La réservation disparaît de la liste |
| `test_reservations_triees` | `reservations_de()` renvoie les réservations triées par début (réservées volontairement dans le désordre) |
| `test_est_disponible_vrai` | Un créneau libre est signalé disponible |
| `test_est_disponible_faux` | Un créneau occupé est signalé indisponible |
| `test_reserver_apres_annulation` | Un créneau libéré par annulation peut être réservé à nouveau |
| `test_meme_creneau_salles_differentes` | Deux salles différentes peuvent être réservées au même créneau |

### 6.3 Cas limites et erreurs (`test_limites.py`) — 21 tests

| Test | Situation | Résultat attendu |
|---|---|---|
| `test_salle_en_double` | Ajouter « Alpha » deux fois | `SalleDejaExistanteError` |
| `test_capacite_invalide` *(paramétré : 0, -1)* | Capacité ≤ 0 | `DonneeInvalideError` |
| `test_fin_avant_debut` | Fin antérieure au début | `CreneauInvalideError` |
| `test_fin_egale_debut` | Créneau de durée nulle | `CreneauInvalideError` |
| `test_participants_invalides` *(paramétré : 0, -3)* | Participants ≤ 0 | `DonneeInvalideError` |
| `test_capacite_exacte` | Participants = capacité | Réservation acceptée |
| `test_capacite_depassee` | Participants = capacité + 1 | `CapaciteDepasseeError` |
| `test_chevauchements` *(paramétré : 5 cas)* | Chevauchement au début, à la fin, inclus, englobant, identique | `ChevauchementError` |
| `test_creneaux_adjacents` *(paramétré : 2 cas)* | Créneau finissant à 10h00 / commençant à 11h00 | Réservation acceptée |
| `test_salle_inexistante_reserver` | Réserver « Inconnue » | `SalleInexistanteError` |
| `test_salle_inexistante_lister` | Lister les réservations d'« Inconnue » | `SalleInexistanteError` |
| `test_annuler_inexistante` | Annuler un identifiant inconnu | `ReservationInexistanteError` |
| `test_annuler_deux_fois` | Annuler la même réservation deux fois | `ReservationInexistanteError` au 2e appel |
| `test_echec_sans_effet` | Une réservation refusée n'est pas enregistrée | La liste reste inchangée |

**Schéma des chevauchements testés** (réservation existante : 10h00 → 11h00) :

```
                 09h    10h    11h    12h
Existante               [======[
debut              [======[                 → refusé
fin                        [======[         → refusé
inclus                   [==[               → refusé
englobant        [=====================[    → refusé
identique               [======[            → refusé
juste_avant      [======[                   → accepté (R6)
juste_apres                    [======[     → accepté (R6)
```

### 6.4 Techniques pytest utilisées

| Technique | Usage |
|---|---|
| `@pytest.fixture` | Préparer un état de départ réutilisable entre les tests |
| `pytest.raises(...)` | Vérifier qu'une exception précise est levée |
| `@pytest.mark.parametrize` | Tester plusieurs valeurs avec une seule fonction de test |
| `ids=[...]` | Donner un nom lisible à chaque cas paramétré (ex. `test_chevauchements[inclus]`) |
| `pytest --cov` | Mesurer la couverture du code par les tests |

## 7. Exécution des tests

```powershell
# Exécution détaillée
pytest -v

# Couverture avec lignes non couvertes
pytest --cov=src --cov-report=term-missing

# Rapport HTML (dossier htmlcov/)
pytest --cov=src --cov-report=html
start htmlcov\index.html
```

### Résultats

| Indicateur | Valeur |
|---|---|
| Tests exécutés | 30 (21 limites/erreurs + 9 nominaux) |
| Tests réussis | 30 |
| Taux de réussite | **100 %** |
| Instructions de `reservation.py` | 72 |
| Instructions non couvertes | 0 |
| Couverture de `reservation.py` | **100 %** |
| Durée d'exécution | < 0,5 s |

:::success
Tous les tests passent et chaque ligne de la logique métier est exécutée au moins une fois par la suite de tests.
:::

**Sortie de `pytest -v` :**
![image](https://hackmd.io/_uploads/SkcqIEG0Ge.png)
![image](https://hackmd.io/_uploads/ByJ3IVzRfl.png)

**Rapport de couverture (terminal et HTML) :**
![image](https://hackmd.io/_uploads/BJx5DEfRGe.png)
![image](https://hackmd.io/_uploads/SJRqP4MRMl.png)
![image](https://hackmd.io/_uploads/HyOkdEGRfl.png)

:::warning
**Limite de la couverture :** 100 % signifie que chaque ligne a été exécutée, pas que tous les scénarios possibles ont été testés. C'est pourquoi les cas limites (créneaux adjacents, capacité exacte, chevauchements) ont été choisis délibérément, en plus de la mesure de couverture.
:::

## 8. Démonstration de l'interface (`main.py`)

### Rôle de `main.py`

`main.py` est la seule partie du projet qui dialogue avec l'utilisateur (`input()` / `print()`). Il appelle les méthodes de `GestionnaireReservations` et traduit les exceptions en messages lisibles. La logique métier reste entièrement dans `src/reservation.py`.

| Élément | Rôle |
|---|---|
| Menu en boucle (`while True`) | Affiche les 6 choix jusqu'à ce que l'utilisateur quitte |
| `lire_date()` | Convertit la saisie `AAAA-MM-JJ HH:MM` en `datetime` |
| `except ReservationError` | Attrape les 7 erreurs métier d'un seul bloc grâce à la classe parente commune |
| `except ValueError` | Gère les saisies mal formées (lettres au lieu d'un nombre, mauvais format de date) |

### Lancement

```powershell
python main.py
```

### Scénario de démonstration

| # | Action | Saisies | Résultat |
|---|---|---|---|
| 1 | Ajouter une salle | `E1`, `25` | ✔ Salle 'E1' créée (25 places) |
| 2 | Réserver | `E1`, `2026-11-12 10:00` → `11:00`, `5` pers. | ✔ Réservation n°1 enregistrée |
| 3 | Réserver un créneau qui chevauche | `E1`, `2026-11-12 10:30` → `11:30`, `3` pers. | ✘ Refusé : chevauchement (R5) |
| 4 | Réserver le créneau adjacent | `E1`, `2026-11-12 11:00` → `12:00`, `4` pers. | ✔ Réservation n°2 acceptée (R6) |
| 5 | Lister les réservations | `E1` | Les 2 réservations, triées par heure |
| 6 | Quitter | `0` | Au revoir ! |

**Étape 1 — Création de la salle :**
![image](https://hackmd.io/_uploads/HJhCF4fAMx.png)

**Étapes 2 à 4 — Réservations et refus du chevauchement :**
![image](https://hackmd.io/_uploads/H1_k8rfAzx.png)
![image](https://hackmd.io/_uploads/SykHIBf0Mx.png)

**Étapes 5 et 6 — Liste des réservations et sortie :**
![image](https://hackmd.io/_uploads/S1mOIBMAzl.png)
![image](https://hackmd.io/_uploads/r1DaUHG0Mx.png)

## 9. Difficultés rencontrées

| Difficulté | Cause | Solution |
|---|---|---|
| Deux versions de Python (`python` → 3.13.4, `py` → 3.15.2) | Plusieurs installations sur le poste | Création du venv avec `py -3.13` pour fixer la version du projet |
| `source : Le terme «source» n'est pas reconnu` | `source` est une commande Linux, pas PowerShell | Activation avec `.venv\Scripts\Activate.ps1` |
| Venv créé dans `C:\Users\alexa` au lieu du dossier projet | Commande lancée depuis le mauvais répertoire | Suppression avec `Remove-Item -Recurse -Force C:\Users\alexa\.venv`, puis recréation dans `projet5-reservation` |

## 10. Conclusion

Le module de réservation de salles répond aux objectifs du projet :

- **Conception :** la logique métier est isolée dans `reservation.py`, sans aucune entrée/sortie, ce qui la rend directement testable.
- **Tests :** 30 tests automatisés couvrent les 8 règles métier, avec 9 cas nominaux et 21 cas limites ou erreurs.
- **Fiabilité :** 100 % de réussite et 100 % de couverture du module.

**Limites du module :**
- Pas de persistance : les données sont perdues à la fermeture du programme
- Pas de gestion multi-utilisateurs ni d'authentification
- Pas de gestion des fuseaux horaires

**Améliorations possibles :**
- Sauvegarde des données en JSON ou SQLite
- Exposition du module via une API web (FastAPI, Flask)
- Intégration continue : lancement automatique des tests à chaque push avec GitHub Actions

## 11. Ressources

- [pytest — Documentation officielle](https://docs.pytest.org/en/stable/)
- [pytest — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)