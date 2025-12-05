from collections import defaultdict

unexpected_message = defaultdict(
    lambda: "An error occured, please try again.",
    {
        "fr": "Une erreur est survenue, veuillez réessayer.",
    }
)

forbidden_access_message = defaultdict(
    lambda: "Forbidden access.",
    {
        "fr": "Accès interdit.",
    }
)

missing_english_translation_message = defaultdict(
    lambda: "The mandatory english translation is missing ({name: {'en': 'example'}}).",
    {
        "fr": "La traduction anglaise obligatoire est manquante ({name: {'en': 'example'}}).",
    }
)

obligation_newname = defaultdict(
    lambda: "You have to change your username before continuing.",
    {
        "fr": "Vous devez changer votre pseudo avant de continuer.",
    }
)

obligation_newpwd = defaultdict(
    lambda: "You have to create a password before continuing.",
    {
        "fr": "Vous devez créer un mot de passe avant de continuer.",
    }
)
