import time
import progressbar

# Créer une barre de progression
bar = progressbar.ProgressBar(maxval=100)

# Mettre à jour la barre de progression
bar.start()
for i in range(101):
    time.sleep(0.1)  # Simuler un travail
    bar.update(i)
bar.finish()

print("Travail terminé !")
