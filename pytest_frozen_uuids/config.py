import uuid
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DefaultConfig:
    obj_path: str = "uuid.uuid4"
    version: int = 4
    namespace: Optional[str] = None
    values: Optional[List[str]] = field(
        default_factory=lambda: ["00000000-0000-0000-0000-000000000000"]
    )
    seed: int = 42
    side_effect: str = "auto_increment"

    def get_uuids(self) -> List[uuid.UUID]:
        assert self.values
        return [uuid.UUID(value) for value in self.values]
