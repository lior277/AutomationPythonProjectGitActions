from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Episode:
    id: int
    name: str
    air_date: str
    episode: str
    characters: List[str]
    url: str
    created: str

@dataclass
class EpisodeResponse:
    results: List[Episode]
    info: Dict[str, Optional[str]]
