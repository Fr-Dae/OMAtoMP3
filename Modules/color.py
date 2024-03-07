## color.py - définition des couleurs de print

from colorama import Fore, Style

# Couleurs
ERROR_COLOR = Fore.RED
QUESTION_COLOR = Fore.YELLOW
CONFIRMATION_COLOR = Fore.CYAN
END_COLOR = Style.RESET_ALL

# Fonction pour afficher du texte en couleur
def print_colored(text, color_code):
	print(f"{color_code}{text}{END_COLOR}")

## Copy past me
#	from Modules.color import print_colored
#	
#	# Utilisation de la fonction print_colored
#	print_colored("Ce texte est en couleur.", print_colored.ERROR_COLOR)
#	print_colored("Ce texte est en couleur.", print_colored.QUESTION_COLOR)
#	print_colored("Ce texte est en couleur.", print_colored.CONFIRMATION_COLOR)
