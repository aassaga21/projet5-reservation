\# Projet 5 — Réservation de salles testée avec pytest



Module Python de gestion de réservations de salles, accompagné d'une suite de tests automatisés \*\*pytest\*\* avec mesure de couverture.



\*\*Auteure :\*\* Alexandra Assaga — E3, Bachelor Systèmes et Réseaux, Geneva Institute of Technology

\*\*Cours :\*\* Python — Principes de base



\## Résultats



| Indicateur | Valeur |

|---|---|

| Tests | 30 (9 nominaux + 21 limites/erreurs) |

| Taux de réussite | 100 % |

| Couverture de `src/reservation.py` | 100 % |



\## Structure



```

projet5-reservation/

├── src/reservation.py     # logique métier (aucune entrée/sortie)

├── main.py                # interface en ligne de commande

├── tests/

│   ├── conftest.py        # fixtures partagées

│   ├── test\_nominaux.py   # cas nominaux

│   └── test\_limites.py    # cas limites et erreurs

├── htmlcov/               # rapport de couverture HTML

├── pyproject.toml         # configuration pytest

└── requirements.txt

```



\## Installation (Windows / PowerShell)



```powershell

py -3.13 -m venv .venv

.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

```



\## Utilisation



```powershell

\# Lancer l'application

python main.py



\# Lancer les tests

pytest -v



\# Mesurer la couverture

pytest --cov=src --cov-report=term-missing

pytest --cov=src --cov-report=html

```



\## Règles métier



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



\## Documentation complète



\[HackMD — Projet 5](https://hackmd.io/@Alexandra-ASSAGA/ryV\_28JAGg) \*(lien à remplacer par celui de la note)\*

