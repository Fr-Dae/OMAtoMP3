"""Affichage de messages de logs colorés."""

from colorama import Fore, Style


ERROR = Fore.RED
QUESTION = Fore.YELLOW
CONFIRMATION = Fore.CYAN
END = Style.RESET_ALL


# Les fonctions préfixées d'un _ sont celles qui sont privées ; qu'on ne va pas
# utiliser en dehors du module
def _print_colored(color_code: str, *values: str, **kwargs) -> None:
    print(color_code + ' '.join(str(value) for value in values) + END, **kwargs)


def error(*values: str, **kwargs) -> None:
    _print_colored(ERROR, *values, **kwargs)


def question(*values: str, **kwargs) -> None:
    _print_colored(QUESTION, *values, **kwargs)


def confirmation(*values: str, **kwargs) -> None:
    _print_colored(CONFIRMATION, *values, **kwargs)
