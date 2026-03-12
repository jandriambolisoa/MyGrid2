from collections import defaultdict

from backend.src.auth.constants import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PW_MIN_LENGTH

not_a_valid_username_length_message = defaultdict(
    lambda: f"Your username must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters long.",
    {
        "fr": f"Votre nom d'utilisateur doit contenir entre {USERNAME_MIN_LENGTH} et {USERNAME_MAX_LENGTH} caractères.",
    }
)

not_a_valid_username_characters_message = defaultdict(
    lambda: "Your username can only contain letters, digits, underscores, and dashes.",
    {
        "fr": "Votre nom d'utilisateur ne peut contenir que des lettres, des chiffres, des tirets bas et des tirets.",
    }
)

not_a_valid_username_spacebar_message = defaultdict(
    lambda: "Spaces are not allowed in your username.",
    {
        "fr": "Les espaces ne sont pas autorisés dans le nom d'utilisateur.",
    }
)

not_available_username_message = defaultdict(
    lambda: "Username not available.",
    {
        "fr": "Nom d'utilisateur non disponible.",
    }
)

not_a_valid_password_length_message = defaultdict(
    lambda: f"Your password must be at least {PW_MIN_LENGTH} characters long.",
    {
        "fr": f"Votre mot de passe doit contenir au moins {PW_MIN_LENGTH} caractères.",
    }
)

not_a_valid_password_strength_message = defaultdict(
    lambda: "Your password is too weak. It must contain at least three of the following: a lowercase letter, an uppercase letter, a number, or a special character.",
    {
        "fr": "Votre mot de passe est trop faible. Il doit contenir au moins trois des éléments suivants : une lettre minuscule, une lettre majuscule, un chiffre ou un caractère spécial.",
    }
)

not_a_valid_email_message = defaultdict(
    lambda: "Your email is not valid. It must include a @ symbol.",
    {
        "fr": "Votre email n'est pas valide. Il devrait contenir un symbole @.",
    }
)

not_available_email_message = defaultdict(
    lambda: "This email address is already in use.",
    {
        "fr": "Cette adresse e-mail est déjà utilisée.",
    }
)

login_suspended_message = defaultdict(
    lambda: "Too many failed attempts. Your login is suspended for {{ DURATION }} seconds.",
    {
        "fr": "Trop de tentatives échouées. Votre connexion est suspendue pendant {{ DURATION }} secondes.",
    }
)

wrong_credentials_message = defaultdict(
    lambda: "Incorrect username or password.",
    {
        "fr": "Nom d'utilisateur ou mot de passe incorrect.",
    }
)

google_sso_login_failed_message = defaultdict(
    lambda: "Google authentification failed, please try again later.",
    {
        "fr": "L'authentification Google a échouée, veuillez réessayer plus tard.",
    }
)

apple_sso_login_failed_message = defaultdict(
    lambda: "Apple authentification failed, please try again later.",
    {
        "fr": "L'authentification Apple a échouée, veuillez réessayer plus tard.",
    }
)

unverified_user_message = defaultdict(
    lambda: "Your account must be verified to be able to continue.",
    {
        "fr": "Votre compte doit être vérifié pour pouvoir continuer.",
    }
)

mailing_welcome_subject = defaultdict(
    lambda: "👋 Welcome to MyGrid!",
    {
        "fr": "👋 Bienvenue sur MyGrid !",
    }
)

mailing_welcome_preview = defaultdict(
    lambda: "Nice to meet you, {{ USERNAME }}.",
    {
        "fr": "Enchanté, {{ USERNAME }}.",
    }
)

mailing_welcome_body = defaultdict(
    lambda: "It’s time to turn your F1 intuition into glory. Go to the app now to make your first prediction, outsmart the competition, and start your climb to the top of the leaderboard.",
    {
        "fr": "Il est temps de faire valoir votre flair en F1. Rendez-vous sur l'application dès maintenant pour faire votre premier pronostic, surpasser la concurrence et entamer votre ascension vers le sommet du classement.",
    }
)

mailing_welcome_title = defaultdict(
    lambda: "Welcome {{ USERNAME }}!",
    {
        "fr": "Bienvenue {{ USERNAME }} !",
    }
)

mailing_verification_subject = defaultdict(
    lambda: "Verify your email.",
    {
        "fr": "Confirmez votre email.",
    }
)

mailing_verification_confirm = defaultdict(
    lambda: "Verify Email Address",
    {
        "fr": "Vérifiez votre email",
    }
)

mailing_verification_preview = defaultdict(
    lambda: "You will be able to compete on MyGrid.",
    {
        "fr": "Vous pourrez faire vos pronostics sur MyGrid.",
    }
)

mailing_verification_body = defaultdict(
    lambda: "Thank you for joining MyGrid. Please verify your email by clicking the following link :",
    {
        "fr": "Merci d'avoir rejoins MyGrid. Veuillez cliquer sur le lien qui suit pour valider votre email :",
    }
)

mailing_verification_title = defaultdict(
    lambda: "Dear {{ USERNAME }},",
    {
        "fr": "Cher {{ USERNAME }},",
    }
)

mailing_lostpw_subject = defaultdict(
    lambda: "Did you forget your password? 🛡️",
    {
        "fr": "Avez-vous oublié votre mot de passe ? 🛡️",
    }
)

mailing_lostpw_preview = defaultdict(
    lambda: "If not, ignore this email.",
    {
        "fr": "Si non, ignorez cet email.",
    }
)

mailing_lostpw_title = defaultdict(
    lambda: "Dear {{ USERNAME }},",
    {
        "fr": "Cher {{ USERNAME }},",
    }
)

mailing_lostpw_body = defaultdict(
    lambda: "We received a request to reset the password for your account. If you initiated this request, use your username as your identifier and the temporary code below as your password to log in :",
    {
        "fr": "Nous avons bien reçu ta demande de réinitialisation de mot de passe. Si tu es à l'origine de cette démarche, utilise ton nom d'utilisateur en identifiant et le code temporaire ci-dessous comme mot de passe pour te connecter :",
    }
)

mailing_lostpw_instructions = defaultdict(
    lambda: "If you did not request a password reset, you can safely ignore this email. Your account remains secure.",
    {
        "fr": "Si tu n'as pas demandé de réinitialisation, tu peux simplement ignorer cet e-mail. Ton compte reste en sécurité.",
    }
)
