import dataclasses
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from pydantic import BaseModel


@dataclass_json
@dataclass
class PostSignupRequest:
    username: str
    password: str
