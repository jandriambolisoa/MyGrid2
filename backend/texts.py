from collections import defaultdict

days_of_the_week = defaultdict(
    lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    {
        "fr": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    }
)

nice_datetime_format = defaultdict(
    lambda: "{{ day }} at {{ time }}",
    {
        "fr": "Le {{ day }} à {{ time }}"
    }
)

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

microservices_are_off_message = defaultdict(
    lambda: "Microservices are off. Please contact admins.",
    {
        "fr": "Les micro-services sont désactivés. Veuillez contacter un administrateur.",
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

obligation_convertuser = defaultdict(
    lambda: "You have to create an account before continuing.",
    {
        "fr": "Vous devez créer un compte avant de continuer.",
    }
)
