from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Character:
    id: int
    name: str
    status: str
    species: str
    gender: str
    origin: Optional[dict]
    location: Optional[dict]
    image: str
    episode: List[str]
    url: str
    created: str

    def __post_init__(self):

        if not self.location:
            self.location = {"name": "unknown", "url": ""}
        if not self.origin:
            self.origin = {"name": "unknown", "url": ""}

        if not self.episode:
            self.episode = []
