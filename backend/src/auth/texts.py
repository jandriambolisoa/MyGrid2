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
