# scripts/02_extraire_second_milliard.py
"""
🌊 OCEAN PI — Étape 2 : Extraction sécurisée du second milliard (1B à 2B)
Lit le gros fichier par blocs pour éviter de saturer la mémoire vive (RAM).
"""

import os
import time

FICHIER_SOURCE = "pi_2000000000_complet.txt"  # Nom du gros fichier issu de pilookup / Archive.org
FICHIER_DEST   = "pi_decimales_2B.txt"        # Destination du second milliard seul
DEBUT          = 1_000_000_000
FIN            = 2_000_000_000
TAILLE_BLOC    = 50_000_000  # 50 Mo chargés à la fois en RAM

def extraire_tranche():
    if not os.path.exists(FICHIER_SOURCE):
        print(f"❌ Fichier source introuvable : {FICHIER_SOURCE}")
        print("   Veuillez placer le fichier complet des 2 milliards de pilookup.com ou Archive.org dans ce dossier.")
        return

    print(f"⏳ Extraction des positions {DEBUT:,} à {FIN:,}...")
    t0 = time.time()

    chiffres_vus = 0
    chiffres_ecrits = 0
    premier_bloc = True

    with open(FICHIER_SOURCE, 'r', encoding='utf-8', errors='ignore') as f_in:
        with open(FICHIER_DEST, 'w', encoding='utf-8') as f_out:
            while chiffres_ecrits < (FIN - DEBUT):
                bloc = f_in.read(TAILLE_BLOC)
                if not bloc:
                    print("\n⚠️ Fin du fichier atteinte avant d'avoir atteint les 2 milliards.")
                    break
                
                # Nettoyage du préfixe "3." s'il est présent au tout début du fichier complet
                if premier_bloc:
                    if '3.' in bloc[:10]:
                        bloc = bloc[bloc.find('3.') + 2:]
                    premier_bloc = False
                
                # Filtrage ultra-rapide des chiffres uniquement
                chiffres = "".join(c for c in bloc if c.isdigit())
                longueur_chiffres = len(chiffres)
                chiffres_vus += longueur_chiffres
                
                # Si on a franchi le cap du premier milliard, on écrit la suite
                if chiffres_vus > DEBUT:
                    if chiffres_vus - longueur_chiffres < DEBUT:
                        # On est sur le bloc frontière contenant la milliardième décimale
                        offset = DEBUT - (chiffres_vus - longueur_chiffres)
                        chiffres = chiffres[offset:]
                    
                    reste_a_ecrire = (FIN - DEBUT) - chiffres_ecrits
                    a_ecrire = chiffres[:reste_a_ecrire]
                    
                    f_out.write(a_ecrire)
                    chiffres_ecrits += len(a_ecrire)
                
                # Progression en temps réel
                pct = min(chiffres_vus / FIN * 100, 100)
                print(f"\r   Progression : {pct:.1f}% | Vus: {chiffres_vus/1e9:.3f}B | Écrits: {chiffres_ecrits/1e6:.0f}M", end="", flush=True)

    print(f"\n\n✅ Extraction terminée en {(time.time() - t0) / 60:.1f} minutes !")
    print(f"   Fichier généré : {FICHIER_DEST} ({os.path.getsize(FICHIER_DEST) / 1e6:.1f} Mo)")

if __name__ == "__main__":
    print("🌊 OCEAN PI — Extraction par Blocs Synchrones")
    print("=" * 60)
    extraire_tranche()