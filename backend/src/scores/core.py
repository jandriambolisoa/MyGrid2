from backend.db.database import Database
from backend.src.scores.exceptions import NoParametersFoundError
from backend.src.scores.schemas import ScoresParameters


async def score_parameters_of_a_championship(championship_id: int, db: Database, language: str = "en"):
    db.cursor.execute("""
        SELECT * 
        FROM scoresparameters 
        WHERE championship_id = %s""", (championship_id,))
    parameters = db.cursor.fetchall()

    if not parameters:
        raise NoParametersFoundError(language=language)

    # Convert query results into ScoresParameters model
    scores_parameters = dict()
    for param in parameters:
        scores_parameters[param["param"]] = [param[key] for key in list(param.keys()) if "value" in key]

    return ScoresParameters(**scores_parameters)