# 🌌 Ocean Pi — Chasse aux Curiosités Numériques dans π

Ce projet est un laboratoire d'exploration arithmétique appliqué aux décimales de la constante $\pi$. L'objectif n'est pas d'étudier la normalité statistique, mais d'utiliser l'immense flux de chiffres généré par $\pi$ comme un canevas pour **dénicher des coïncidences numériques, des alignements surprenants et des liens cachés**.

En recherchant des chaînes de nombres connues ou géométriques (comme les constantes de carrés magiques, les suites arithmétiques, etc.), nous analysons leurs rangs et leurs positions d'apparition pour en extraire de "petites curiosités arithmétiques".

---

## 🛠️ Installation et Utilisation

### 1. Prérequis
Assurez-vous d'avoir Python 3.8+ installé. Clonez le dépôt puis installez les dépendances :

```bash
pip install -r requirements.txt

```

### 2. Guide des Scripts

Les outils sont classés et s'exécutent de la manière suivante :

* `python scripts/01_telecharger_un_milliard.py` : Télécharge et nettoie le premier milliard de décimales (Source : MIT).
* `python scripts/02_extraire_second_milliard.py` : Permet d'extraire par flux de lecture le second milliard (1B à 2B) depuis un fichier complet de 2 Go sans saturer la mémoire (RAM).
* `python scripts/03_recherche_sequences.py` : Notre scanner en ligne de commande.

### Exemple d'exploration avec le scanner :

Pour chercher la position de la somme d'un carré magique ou d'une suite particulière (ex: `63738`, `16816`) dans votre fichier :

```bash
python scripts/03_recherche_sequences.py --file pi_decimales.txt --sequences 63738 16816

```

---

## 🤝 Participer aux Explorations

Vous avez trouvé une chaîne intrigante ? Un lien particulier entre le rang d'une séquence et une propriété d'un carré magique ?

1. **Ouvrez une Issue** pour partager votre trouvaille ou proposer de nouveaux motifs à scanner.
2. **Proposez des optimisations** ou de nouveaux scripts d'analyse géométrique des positions.

Découvrez nos articles complets sur le site officiel : [mystimath.org](https://mystimath.org)

```