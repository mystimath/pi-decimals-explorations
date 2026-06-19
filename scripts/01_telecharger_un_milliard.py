# scripts/01_telecharger_un_milliard.py
"""
🌊 OCEAN PI — Étape 1 : Téléchargement du premier milliard
Télécharge les décimales depuis la source publique du MIT.
"""

import os
import time
import requests

FICHIER_OUT = "pi_decimales.txt"
URL_MIT = "https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt"

def telecharger_premier_milliard():
    if os.path.exists(FICHIER_OUT):
        print(f"✅ Le fichier '{FICHIER_OUT}' est déjà présent localement.")
        return

    print("⏳ Téléchargement de 1 milliard de décimales depuis le MIT...")
    print("   (Cette opération peut prendre quelques minutes selon votre connexion)")
    
    t0 = time.time()
    
    try:
        response = requests.get(URL_MIT, stream=True)
        response.raise_for_status()
        
        # Lecture et écriture par blocs pour économiser la RAM
        with open(FICHIER_OUT, 'w', encoding='utf-8') as f:
            for chunk in response.iter_content(chunk_size=10_000_000, decode_unicode=True):
                if chunk:
                    # On ne garde que les chiffres (enlève les retours à la ligne ou espaces)
                    chiffres = "".join(c for c in chunk if c.isdigit())
                    f.write(chiffres)
                    
        print(f"✅ Téléchargement réussi en {(time.time() - t0) / 60:.1f} minutes.")
        print(f"   Fichier créé : {FICHIER_OUT} ({os.path.getsize(FICHIER_OUT) / 1e6:.1f} Mo)")
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    print("🌊 OCEAN PI — Initialisation du premier milliard")
    print("=" * 60)
    telecharger_premier_milliard()