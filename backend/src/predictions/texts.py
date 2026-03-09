from collections import defaultdict

driver_not_registered_for_session_message = defaultdict(
    lambda: "All given drivers are not registered for this session. Your prediction has been erased.",
    {
        "fr": "Tous les pilotes donnés ne font pas parti de cette session. Votre prédiction est effacée.",
    }
)

prediction_not_available_message = defaultdict(
    lambda: "You cannot look at others predictions if the session is not over.",
    {
        "fr": "Vous ne pouvez pas regarder les pronos des autres si la session n'est pas terminée.",
    }
)

no_prediction_message = defaultdict(
    lambda: "No prediction found.",
    {
        "fr": "Aucun pronostic trouvé.",
    }
)
