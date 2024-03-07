from tqdm import tqdm
import time

elements = list(range(100))

# Créer une barre de progression avec tqdm
with tqdm(total=len(elements), desc="Traitement en cours") as pbar:
    for element in elements:
        time.sleep(0.1)
        pbar.update(1) 
        
# Barre de progression
print("Exemple de barre de progression :")
for i in tqdm(range(100), desc="Progress"):
    time.sleep(0.03)
    
print("Traitement terminé !")
