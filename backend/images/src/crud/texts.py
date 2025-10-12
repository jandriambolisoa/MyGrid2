from collections import defaultdict

image_already_exists_message = defaultdict(
    lambda: "Invalid image name, image already exists.",
    {
        "fr": "Le nom de l'image n'est pas valide, l'image existe déjà.",
    }
)

image_not_found_message = defaultdict(
    lambda: "Image not found.",
    {
        "fr": "Image inexistante.",
    }
)
