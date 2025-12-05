from backend import exceptions as app_exceptions

async def valid_translations(datas: dict, language: str = "en") -> dict:
    if not "en" in list(datas.keys()):
        app_exceptions.MissingEnglishTranslationError(language=language)

    return datas
