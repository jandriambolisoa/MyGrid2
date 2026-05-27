from collections import defaultdict

no_league_found_message = defaultdict(
    lambda: "No league found.",
    {
        "fr": "Aucune ligue n'a été trouvée.",
    }
)

league_does_not_exists_message = defaultdict(
    lambda: "League of id {{ league_id }} does not exist.",
    {
        "fr": "La ligue d'id {{ league_id }} n'existe pas.",
    }
)

league_not_owned_message = defaultdict(
    lambda: "You are not an organizer of this league ({{ league_id }}).",
    {
        "fr": "Vous n'êtes pas un organisateur de cette ligue ({{ league_id }}).",
    }
)

max_league_creation_message = defaultdict(
    lambda: "You have reached the maximum number of league you can create.",
    {
        "fr": "Tu as atteins le nombre maximum de ligue que tu peux créer.",
    }
)

not_a_valid_league_name_length_message = defaultdict(
    lambda: "You have reached the maximum number of leagues you can create.",
    {
        "fr": "Tu as atteint le nombre maximum de ligues que tu peux créer.",
    }
)

not_a_valid_league_name_characters_message = defaultdict(
    lambda: "The league name contains invalid characters.",
    {
        "fr": "Le nom de la ligue contient des caractères non valides.",
    }
)

not_available_league_name_message = defaultdict(
    lambda: "This league name is not available.",
    {
        "fr": "Ce nom de ligue n'est pas disponible.",
    }
)

league_already_exists_message = defaultdict(
    lambda: "This league already exists.",
    {
        "fr": "Cette league existe déjà.",
    }
)
