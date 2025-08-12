from collections import defaultdict

failed_authorization_message = defaultdict(
    lambda: "Failed authorization.",
    {
        "fr": "L'autorisation a échoué.",
    }
)

expired_session_message = defaultdict(
    lambda: "Session expired.",
    {
        "fr": "La session a expiré.",
    }
)

not_a_user_message = defaultdict(
    lambda: "The requested user does not exist.",
    {
        "fr": "L'utilisateur demandé n'existe pas.",
    }
)

banned_user_message = defaultdict(
    lambda: "You have been banned and can no longer use this app. For any inquiries, contact us at contact@mygrid.fun. Reason for ban: ",
    {
        "fr": "Vous avez été banni et ne pouvez plus utiliser cette application. Pour toute demande, contactez-nous à l’adresse contact@mygrid.fun. Raison du bannissement : "
    }
)

no_user_found_message = defaultdict(
    lambda: "No user found with that username.",
    {
        "fr": "Aucun utilisateur trouvé avec ce nom d'utilisateur."
    }
)