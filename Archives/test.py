import time

# Nombre total d'étapes
total_steps = 50

# Boucle pour simuler la progression
for i in range(total_steps):
    # Calcul du pourcentage de progression
    progress = (i + 1) / total_steps * 100

    # Barre de progression (utilisation de '\r' pour effacer la ligne précédente)
    print(f"[{'#' * (i + 1)}{' ' * (total_steps - i - 1)}] {progress:.1f}%", end='\r')

    # Pause d'une fraction de seconde pour simuler un processus
    time.sleep(0.1)

# Pour afficher un retour à la ligne à la fin de la progression
print()
