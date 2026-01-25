from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session


class ScoresParameters(BaseModel):
    position: list
    top10: list
    top5: list
    top3: list
    top1: list
    penultimate: list
    last: list
    rarity1: list
    rarity2: list
    rarity3: list
    rarity4: list
    rarity5: list
    rarity6: list
    rarity7: list
    rarity8: list
    rarity9: list
    rarity10: list
    rarity11: list
    rarity12: list
    rarity13: list
    rarity14: list
    rarity15: list
    rarity16: list
    rarity17: list
    rarity18: list
    rarity19: list
    rarity20: list
    rarity21: list

