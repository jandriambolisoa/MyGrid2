from collections import defaultdict

from backend.config import settings as app_settings

failed_authorization_message = defaultdict(
    lambda: "Failed authorization.",
    {
        "fr": "L'autorisation a échoué.",
    }
)

expired_session_message = defaultdict(
    lambda: "Session expired. Please log in again.",
    {
        "fr": "Session expirée. Veuillez vous reconnecter.",
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

cannot_update_username_message = defaultdict(
    lambda: "You are not allowed to change your username.",
    {
        "fr": "Vous n'êtes pas autorisé à changer votre nom d'utilisateur."
    }
)

successful_password_update_message = defaultdict(
    lambda: "You have successfully updated your password. You are now logged out, please login again.",
    {
        "fr": "Vous avez mis à jour votre mot de passe. Vous êtes maintenant déconnecté, merci de vous reconnecter."
    }
)

email_verification_sent_message = defaultdict(
    lambda: f"Email verification sent. If you still can't verify your email, please contact us at {app_settings.contact_email}",
    {
        "fr": f"Un email de vérification vous a été envoyé. Si vous ne parvenez toujours pas à vérifier votre addresse, contactez nous à {app_settings.contact_email}"
    }
)