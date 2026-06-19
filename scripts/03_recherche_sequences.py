# scripts/03_recherche_sequences.py
"""
🌊 OCEAN PI — Étape 3 : Scanner de curiosités numériques
Cherche les positions exactes de chaînes de chiffres cibles dans les décimales.

Exemple d'utilisation :
    python scripts/03_recherche_sequences.py --file pi_decimales.txt --sequences 63738 16816 123456
"""

import argparse
from pathlib import Path

def chercher_sequences(file_path, sequences, max_results=5):
    # Dictionnaires pour stocker les résultats
    positions = {seq: [] for seq in sequences}
    counts = {seq: 0 for seq in sequences}
    
    print(f"⏳ Scan en cours sur : {file_path}")
    print(f"   Recherche des motifs : {', '.join(sequences)}")
    print("-" * 60)
    
    taille_tampon = 10_000_000
    chevauchement = max(len(seq) for seq in sequences) - 1
    
    position_globale = 1  # Rang de la première décimale lue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reste = ""
        while True:
            bloc = f.read(taille_tampon)
            if not bloc:
                break
            
            # Concaténer le reste du bloc précédent pour éviter de rater un motif à cheval sur deux blocs
            contenu_analyse = reste + bloc
            
            for seq in sequences:
                index = 0
                while True:
                    index = contenu_analyse.find(seq, index)
                    if index == -1:
                        break
                    
                    # Calcul de la position réelle dans Pi
                    rang_reel = position_globale - len(reste) + index
                    counts[seq] += 1
                    
                    if len(positions[seq]) < max_results:
                        positions[seq].append(rang_reel)
                        
                    index += 1  # Permet de trouver les motifs imbriqués s'il y en a
            
            # Préparer le chevauchement pour le prochain bloc
            reste = contenu_analyse[-chevauchement:] if chevauchement > 0 else ""
            position_globale += len(bloc)

    # Affichage des résultats
    print("\n📊 RÉSULTATS DES CURIOSITÉS TROUVÉES :")
    print("=" * 60)
    for seq in sequences:
        print(f"\nMotif : {seq} (Longueur {len(seq)})")
        print(f"   Nombre d'occurrences totales : {counts[seq]:,}")
        if counts[seq] > 0:
            affichage_pos = [f"Rang {p:,}" for p in positions[seq]]
            print(f"   Premières positions trouvées  : {', '.join(affichage_pos)}")
        else:
            print("   Première occurrence          : Introuvable dans ce fichier.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner de curiosités numériques dans Pi.")
    parser.add_file = parser.add_argument("--file", type=str, default="pi_decimales.txt", help="Fichier de décimales à scanner")
    parser.add_argument("--sequences", type=str, nargs="+", required=True, help="Liste des séquences de chiffres à chercher")
    parser.add_argument("--max-results", type=int, default=5, help="Nombre de positions à afficher par séquence")
    
    args = parser.parse_args()
    
    path = Path(args.file)
    if not path.exists():
        print(f"❌ Erreur : Le fichier {args.file} n'existe pas.")
    else:
        # Nettoyer les séquences pour s'assurer qu'il n'y a que des chiffres
        sequences_nettoyees = ["".join(c for c in s if c.isdigit()) for s in args.sequences]
        sequences_nettoyees = [s for s in sequences_nettoyees if s] # Supprimer les entrées vides
        
        if not sequences_nettoyees:
            print("❌ Aucune séquence de chiffres valide fournie.")
        else:
            chercher_sequences(path, sequences_nettoyees, args.max_results)