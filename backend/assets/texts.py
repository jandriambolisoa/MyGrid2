from collections import defaultdict

asset_file_already_exists_message = defaultdict(
    lambda: "Invalid file name. This file already exists.",
    {
        "fr": "Nom du fichier invalide. Le nom du fichier existe déjà.",
    }
)

file_not_found_message = defaultdict(
    lambda: "File not found.",
    {
        "fr": "Fichier introuvable.",
    }
)
