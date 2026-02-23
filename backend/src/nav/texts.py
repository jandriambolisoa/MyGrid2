from collections import defaultdict

driver_not_registered_for_session_message = defaultdict(
    lambda: "All given drivers are not registered for this session. Your prediction has been erased.",
    {
        "fr": "Tous les pilotes donnés ne font pas parti de cette session. Votre prédiction est effacée.",
    }
)
