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