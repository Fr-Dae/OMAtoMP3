__author__ = 'texom512'
import sys
import time
from math import *

class ProgressBar:
    """
    This class allows you to make easily a progress bar.
    """

    def __init__(self, steps, maxbar=100, title='Chargement'):
        if steps <= 0 or maxbar <= 0 or maxbar > 200:
            raise ValueError

        self.steps = steps
        self.maxbar = maxbar
        self.title = title

    def update(self, step):
        if step < 0 or step > self.steps:
            raise ValueError

        progress = step / self.steps
        num_chars = int(self.maxbar * progress)

        sys.stdout.write(f'\r{self.title} [{"#" * num_chars}{" " * (self.maxbar - num_chars)}] {progress * 100:.1f}%')
        sys.stdout.flush()

# Exemple d'utilisation
if __name__ == "__main__":
    total_steps = 50
    my_progress = ProgressBar(total_steps, title='Téléchargement')

    for i in range(total_steps):
        my_progress.update(i + 1)
        time.sleep(0.1)

    print("\nTéléchargement terminé.")
