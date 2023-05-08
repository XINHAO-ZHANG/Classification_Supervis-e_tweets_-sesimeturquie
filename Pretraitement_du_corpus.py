import os
import re
import unicodedata
import emoji
import argparse

# Définition d'une fonction pour convertir les caractères spéciaux et les emojis en caractères normaux et en texte, avec ajout d'espaces avant et après le texte de l'emoji
def convert_special_characters(file_path):
    with open(file_path, 'r') as f:
        # Lecture du contenu du fichier
        file_content = f.read()
        
        # Conversion des emojis en texte
        converted_content = emoji.demojize(file_content)

        # Ajout d'espaces avant et après le texte de l'emoji
        spaced_content = re.sub(r'(:(?!\s)([^:\s]*):)', r' \1 ', converted_content)
        
        # Conversion des caractères spéciaux et des emojis en caractères normaux
        normalized_content = ''.join(
            unicodedata.normalize('NFKD', c)
            for c in spaced_content
            if not unicodedata.combining(c)
        )

        # Remplacer les URLS
        normalized_content = re.sub(r'(?<!\S)((?:https?://|www\.)\S+)(?!\S)', r' URL ', normalized_content)

        # Remplacement des • par un espace
        normalized_content = normalized_content.replace('•', ' ')

        # Remplacement de € et $ par leur équivalent en français
        normalized_content = normalized_content.replace('€', ' euros ').replace('$', ' dollars ')

    with open(file_path, 'w') as f:
        # Écriture du contenu converti dans le fichier
        f.write(normalized_content)

def main(directory):
    # Parcours du répertoire et des fichiers
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                convert_special_characters(file_path)
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convertir les caractères spéciaux, les emojis et les URL dans les fichiers .txt dans un répertoire donné')
    parser.add_argument('directory', help='le répertoire à parcourir')
    args = parser.parse_args()

    main(args.directory)
