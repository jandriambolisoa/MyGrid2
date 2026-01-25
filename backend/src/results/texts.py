from collections import defaultdict

no_results_found_message = defaultdict(
    lambda: "No session results found.",
    {
        "fr": "Aucun résultat de session trouvé.",
    }
)

invalid_session_result_attempt_message = defaultdict(
    lambda: "Session adding result attempt failed. Existing results are deleted. Make sure to use a valid driver_id.",
    {
        "fr": "La tentative d'ajout des résultats à une session a échouée. Les résultats déjà existants ont été supprimés. Assurez-vous d'utiliser un driver_id valide.",
    }
)
