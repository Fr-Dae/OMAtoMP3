## Dat2TxT.py
import os
import subprocess
import chardet

def print_red(text):
	RED = '\033[91m'
	END = '\033[0m'
	print(RED + text + END)

def print_cyan(text):
	CYAN = '\033[96m'
	END = '\033[0m'
	print(CYAN + text + END)

def print_yellow(text):
	YELLOW = '\033[93m'
	END = '\033[0m'
	print(YELLOW + text + END)

# def detect_encoding(file_path):
#	try:
#		with open(file_path, 'rb') as file:
#			result = chardet.detect(file.read())
#		return result['encoding']
#	except Exception as e:
#		print(f"Erreur lors de la détection de l'encodage : {e}")
#		return None

# def extract_text(input_file, output_file):
#     encodings_to_try = ['utf-8', 'ISO-8859-1', 'windows-1252']  # Liste d'encodages à essayer
#     detected_encoding = detect_encoding(input_file)
# 
#     if detected_encoding:
#         encodings_to_try.insert(0, detected_encoding)  # Insérer l'encodage détecté en premier
# 
#     for encoding in encodings_to_try:
#         try:
#             cat_process = subprocess.Popen(['cat', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             cat_output, cat_error = cat_process.communicate()
# 
#             if cat_process.returncode == 0:
#                 with open(output_file, 'w', encoding=encoding, errors='replace') as txt_file:
#                     txt_file.write(cat_output)
#                 print_cyan(f"Extraction terminée avec l'encodage {encoding}. Le contenu textuel est disponible dans {output_file}.")
#                 return
#             else:
#                 print_red(f"Erreur lors de l'extraction avec l'encodage {encoding}: {cat_error}")
#         except Exception as e:
#             print_red(f"Erreur lors de l'extraction avec l'encodage {encoding}: {e}")
# 

def extract_text(input_file, output_file):
    try:
        with open(input_file, 'rb') as dat_file:
            dat_data = dat_file.read()

        with open(output_file, 'wb') as txt_file:
            txt_file.write(dat_data)

        print_cyan(f"Extraction terminée. Le contenu brut est disponible dans {output_file}.")
    except Exception as e:
        print_red(f"Erreur lors de l'extraction : {e}")


def main():
	print_yellow("Veuillez saisir le chemin du répertoire ou du fichier .dat d'entrée : ")
	input_path = input()

	print_yellow("Veuillez saisir le chemin du répertoire de sortie : ")
	output_dir = input()

	result_dir = os.path.join(output_dir, 'Result')
	os.makedirs(result_dir, exist_ok=True)

	extract_text(input_path, os.path.join(result_dir, 'output.txt'))

if __name__ == "__main__":
	main()
