"""
🌊 OCEAN PI — Étape 3 : Scanner de curiosités numériques

Cherche les positions exactes de chaînes de chiffres dans les décimales de π.

Convention :
    rang 1 = première décimale après la virgule.

Exemples :

    Premier milliard :
    python scripts/03_recherche_sequences.py \
      --file pi_decimales.txt \
      --sequences 834159672

    Second milliard avec offset global :
    python scripts/03_recherche_sequences.py \
      --file mystimath_pi_decimals_1000000001_2000000000.txt.gz \
      --offset 1000000000 \
      --sequences 834159672
"""

import argparse
import gzip
from pathlib import Path


def ouvrir_fichier(path):
    """Ouvre un fichier texte brut ou gzip en mode texte."""
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")

    return open(path, "r", encoding="utf-8", errors="ignore")


def chercher_sequences(file_path, sequences, max_results=5, offset=0):
    positions = {seq: [] for seq in sequences}
    counts = {seq: 0 for seq in sequences}

    print(f"⏳ Scan en cours sur : {file_path}")
    print(f"   Recherche des motifs : {', '.join(sequences)}")
    print(f"   Offset global : {offset:,}")
    print("-" * 60)

    taille_tampon = 10_000_000
    chevauchement = max(len(seq) for seq in sequences) - 1

    # Position locale : rang de la première décimale lue dans CE fichier.
    position_locale = 1

    with ouvrir_fichier(file_path) as f:
        reste = ""

        while True:
            bloc = f.read(taille_tampon)

            if not bloc:
                break

            # Sécurité : on ne garde que les chiffres.
            chiffres_bloc = "".join(c for c in bloc if c.isdigit())

            # Premier bloc seulement :
            # si le fichier commence par "3.", on retire le 3 initial
            # pour respecter la convention :
            # rang 1 = première décimale après la virgule.
            if position_locale == 1 and bloc.lstrip().startswith(("3.", "3,")):
                chiffres_bloc = chiffres_bloc[1:]

            if not chiffres_bloc:
                continue

            contenu_analyse = reste + chiffres_bloc

            for seq in sequences:
                index = 0

                while True:
                    index = contenu_analyse.find(seq, index)

                    if index == -1:
                        break

                    rang_local = position_locale - len(reste) + index
                    rang_global = offset + rang_local

                    counts[seq] += 1

                    if len(positions[seq]) < max_results:
                        positions[seq].append(rang_global)

                    index += 1

            reste = contenu_analyse[-chevauchement:] if chevauchement > 0 else ""
            position_locale += len(chiffres_bloc)

    print("\n📊 RÉSULTATS DES CURIOSITÉS TROUVÉES")
    print("=" * 60)

    for seq in sequences:
        print(f"\nMotif : {seq} (longueur {len(seq)})")
        print(f"   Nombre d'occurrences totales : {counts[seq]:,}")

        if counts[seq] > 0:
            affichage_pos = [f"rang {p:,}" for p in positions[seq]]
            print(f"   Premières positions trouvées : {', '.join(affichage_pos)}")
        else:
            print("   Première occurrence : introuvable dans ce fichier.")


def nettoyer_sequences(sequences):
    return [
        "".join(c for c in sequence if c.isdigit())
        for sequence in sequences
        if "".join(c for c in sequence if c.isdigit())
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scanner de curiosités numériques dans les décimales de π."
    )

    parser.add_argument(
        "--file",
        type=str,
        default="pi_decimales.txt",
        help="Fichier de décimales à scanner (.txt ou .txt.gz).",
    )

    parser.add_argument(
        "--sequences",
        type=str,
        nargs="+",
        required=True,
        help="Liste des séquences de chiffres à chercher.",
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Nombre de positions à afficher par séquence.",
    )

    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Décalage à ajouter aux positions locales pour obtenir le rang global dans π.",
    )

    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        print(f"❌ Erreur : le fichier {args.file} n'existe pas.")
        raise SystemExit(1)

    sequences_nettoyees = nettoyer_sequences(args.sequences)

    if not sequences_nettoyees:
        print("❌ Aucune séquence de chiffres valide fournie.")
        raise SystemExit(1)

    chercher_sequences(
        file_path=path,
        sequences=sequences_nettoyees,
        max_results=args.max_results,
        offset=args.offset,
    )