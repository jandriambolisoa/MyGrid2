from collections import defaultdict

openf1_cannot_get_access_token = defaultdict(
    lambda: "Could not get OpenF1 API access token.",
    {
        "fr": "Impossible d'obtenir le token d'accès à OpenF1 API.",
    }
)

openf1_connection_failed_message = defaultdict(
    lambda: "Connection to OpenF1 MQTT broker failed.",
    {
        "fr": "La connexion à OpenF1 via MQTT a échouée.",
    }
)
