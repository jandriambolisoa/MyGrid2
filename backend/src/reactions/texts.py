from collections import defaultdict

reaction_is_not_an_emoji_message = defaultdict(
    lambda: "You cannot use {{ reaction }} as emoji reaction.",
    {
        "fr": "Vous ne pouvez pas utiliser {{ reaction }} comme réaction emoji.",
    }
)
