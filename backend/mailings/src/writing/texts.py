from collections import defaultdict

no_fields_found_message = defaultdict(
    lambda: "No fields found.",
    {
        "fr": "Aucun mot-clé trouvé.",
    }
)

invalid_fields_message = defaultdict(
    lambda: "Given fields for this template does not match expected fields.",
    {
        "fr": "Les mots-clés donnés pour ce template ne correspondent pas aux mots-clés attendus.",
    }
)