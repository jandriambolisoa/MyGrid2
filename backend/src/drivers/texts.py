from collections import defaultdict

from backend.src.drivers.constants import (
    CODENAME_LENGTH,
)

not_a_valid_codename_length_message = defaultdict(
    lambda: f"A driver's codename must be {CODENAME_LENGTH} characters long.",
    {
        "fr": f"Le codename d'un pilote doit être d'une longueur de {CODENAME_LENGTH}.",
    }
)

not_a_valid_color_message = defaultdict(
    lambda: "Colors must be written as hexadecimal values.",
    {
        "fr": "Les couleurs doivent être sous forme de valeurs hexadécimales.",
    }
)

driver_not_found_message = defaultdict(
    lambda: "Driver not found.",
    {
        "fr": "Aucun pilote trouvé.",
    }
)

team_not_found_message = defaultdict(
    lambda: "Team not found.",
    {
        "fr": "Aucune équipe trouvée.",
    }
)


driver_does_not_exists_message = defaultdict(
    lambda: "Driver of id {{ DRIVER_ID }} does not exist.",
    {
        "fr": "Le pilote à l'id {{ DRIVER_ID }} n'existe pas.",
    }
)

team_does_not_exists_message = defaultdict(
    lambda: "Team of id {{ TEAM_ID }} does not exist.",
    {
        "fr": "L'équipe à l'id {{ TEAM_ID }} n'existe pas.",
    }
)

driver_already_exists_message = defaultdict(
    lambda: "Operation cancelled because this driver already exists.",
    {
        "fr": "L'opération est annulée car le pilote existe déjà.",
    }
)

team_already_exists_message = defaultdict(
    lambda: "Operation cancelled because this team already exists.",
    {
        "fr": "L'opération est annulée car l'équipe existe déjà.",
    }
)

