from collections import defaultdict

from backend.src.drivers.constants import (
    CODENAME_LENGTH,
)

championship_already_exists_message = defaultdict(
    lambda: "Operation cancelled because this championship already exists.",
    {
        "fr": "L'opération est annulée car ce championnat existe déjà.",
    }
)

event_already_exists_message = defaultdict(
    lambda: "Operation cancelled because this event already exists.",
    {
        "fr": "L'opération est annulée car cet évènement existe déjà.",
    }
)

session_already_exists_message = defaultdict(
    lambda: "Operation cancelled because this session already exists.",
    {
        "fr": "L'opération est annulée car cette session existe déjà.",
    }
)

invalid_datetime_string_message = defaultdict(
    lambda: "The datetime have to be ISO 8601 format.",
    {
        "fr": "La datetime doit être au format ISO 8601.",
    }
)

championship_not_found_message = defaultdict(
    lambda: "No championship found.",
    {
        "fr": "Aucun championnat trouvé.",
    }
)

event_not_found_message = defaultdict(
    lambda: "No event found.",
    {
        "fr": "Aucun évènement trouvé.",
    }
)

session_not_found_message = defaultdict(
    lambda: "No session found.",
    {
        "fr": "Aucune session trouvé.",
    }
)

championship_does_not_exists_message = defaultdict(
    lambda: "Championship of id {{ championship_id }} does not exist.",
    {
        "fr": "Le championnat à l'id {{ championship_id }} n'existe pas.",
    }
)

event_does_not_exists_message = defaultdict(
    lambda: "Event of id {{ event_id }} does not exist.",
    {
        "fr": "L'évènement à l'id {{ event_id }} n'existe pas.",
    }
)

session_does_not_exists_message = defaultdict(
    lambda: "Session of id {{ session_id }} does not exist.",
    {
        "fr": "La session à l'id {{ session_id }} n'existe pas.",
    }
)

session_started_message = defaultdict(
    lambda: "Request aborted because the session already started.",
    {
        "fr": "La requête est annulée car la session a déjà commencée.",
    }
)
