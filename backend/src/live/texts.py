from collections import defaultdict

openf1_microservice_error_message = defaultdict(
    lambda: "Live session failed. This feature is not available.",
    {
        "fr": "La session en directe a échouée. Cette fonctionnalité n'est pas disponible.",
    }
)

no_live_session_message = defaultdict(
    lambda: "There is no live session for now.",
    {
        "fr": "Il n'y a pas de session en direct pour le moment.",
    }
)
