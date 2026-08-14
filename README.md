# Détecteur de plaques d'immatriculation sénégalaises 🇸🇳

Système en Python pur capable de détecter et normaliser des plaques d'immatriculation sénégalaises au sein d'un texte quelconque, implémenté selon **deux approches comparées** : analyse par parsing de chaînes et reconnaissance par **automate fini déterministe (DFA)**.

> Projet de groupe — Assignment 2, cours *Programming with Python*, African Institute for Mathematical Sciences (AIMS Sénégal), encadré par Dr Yae U Gaba (Quantum Leap Africa, AIMS RIC), octobre 2025.
>
> **Groupe 10** : Chemegnie Soffo Clarisse, **Malick Ka**, Gnintezemo Mamekem Rosly, Aballo Geraldo Roy, Soukeye Toure.

## Le problème

Détecter automatiquement, dans un texte libre, la présence de plaques d'immatriculation sénégalaises au format `XY-1234-T` ou `XY-1234-ZT`, en gérant :
- l'insensibilité à la casse,
- des séparateurs flexibles (tiret ou espace),
- la tolérance à la ponctuation environnante,
- l'exclusion des faux positifs à l'intérieur de mots plus longs,
- la normalisation en sortie (majuscules, tirets standardisés).

Contrainte technique : **Python pur**, sans bibliothèque externe (pas de `re`, pas de librairie tierce).

## Deux approches implémentées

### 1. Parsing manuel
Analyse séquentielle de la chaîne : normalisation (séparateurs unifiés en `-`, texte en majuscules), puis recherche itérative de motifs `XX-####-X(X)` autour de chaque séparateur, extraction et suppression du motif trouvé jusqu'à épuisement.

- ✅ Simple à implémenter et à comprendre
- ⚠️ Moins structuré, plus difficile à étendre à de nouveaux formats

### 2. Automate fini déterministe (DFA)
Modélisation formelle du problème comme un quintuple `A = (Q, Σ, δ, q₀, F)` avec 8 états (`Q0` à `Q7`), où chaque caractère fait transiter l'automate d'un état à l'autre jusqu'à l'état accepteur `Q7`.

| État | Rôle |
|---|---|
| Q0 | État initial, ignore les délimiteurs |
| Q1 | Deux lettres lues (XY) |
| Q2 | Premier séparateur validé |
| Q3 | Quatre chiffres lus |
| Q4 | Second séparateur validé |
| Q5 / Q6 | Une ou deux lettres finales lues |
| Q7 | État accepteur — plaque valide détectée |

- ✅ Approche formelle, plus facile à prouver correcte, plus facile à étendre à d'autres formats
- ⚠️ Plus long à mettre en place initialement

### Comparaison

| Critère | Parsing | DFA |
|---|---|---|
| Simplicité d'implémentation | Élevée | Modérée |
| Structure formelle | Faible | Élevée |
| Facilité d'extension | Faible | Élevée |
| Complexité temporelle | O(n) | O(n) |
| Résilience aux erreurs | Modérée | Élevée |

**Conclusion du groupe** : les deux méthodes détectent correctement les plaques. Le parsing suffit pour un script court ; le DFA est recommandé pour une solution robuste, extensible et formellement vérifiable.

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `projet.py` | Logique principale de détection |
| `plates.py` | Fonctions de détection / normalisation des plaques |
| `plate_detector_gui.py` | Interface graphique (saisie de texte, analyse, résultats) |
| `roy.ipynb` | Notebook d'exploration / tests |

## Utilisation

```bash
python plate_detector_gui.py
```

L'interface permet de coller un texte, de lancer l'analyse, et affiche la liste des plaques détectées (dédupliquées) ainsi que leur nombre total.

**Exemple** :
```
Entrée : "J'ai vu une voiture avec la plaque DK-2394-T sur la route."
Sortie : ["DK-2394-T"], 1 plaque détectée
```

## Auteurs

Projet réalisé en groupe de 5 dans le cadre du cursus AIMS Sénégal. Contribution de **Malick Ka** au sein du Groupe 10.
