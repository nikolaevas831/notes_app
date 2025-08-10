from dataclasses import dataclass
from typing import Optional


@dataclass
class Note:
    head: str
    body: str
    user_id: int
    id: Optional[int] = None
