import dataclasses
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from pydantic import BaseModel


@dataclass_json
@dataclass
class PostAddToChartRequest():
    id: str
    cookie: str
    prod_id: int
    flag: bool

