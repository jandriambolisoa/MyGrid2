from collections import defaultdict

no_registrations_found_message = defaultdict(
    lambda: "No registration found.",
    {
        "fr": "Aucun enregistrement trouvé.",
    }
)

registration_already_exists_message = defaultdict(
    lambda: "A registration already exists for this session.",
    {
        "fr": "Un enregistrement est déjà existant pour cette session.",
    }
)

invalid_session_registration_attempt_message = defaultdict(
    lambda: "Session registration attempt failed. Existing registrations are deleted. Make sure to use a valid driver_id and team_id.",
    {
        "fr": "La tentative d'enregistrements à une session a échouée. Les enregistrements déjà existants ont été supprimés. Assurez-vous d'utiliser un driver_id et un team_id valide.",
    }
)
