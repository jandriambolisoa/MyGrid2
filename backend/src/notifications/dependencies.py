from backend.src.notifications.exceptions import NotAValidPushTokenError


async def valid_push_token(token: str, language: str = "en") -> str:
    if token.startswith("ExponentPushToken["):
        return token

    raise NotAValidPushTokenError(language)