import uuid
from dataclasses import dataclass

from app.api.schemas import Status


@dataclass
class Model:
    id: uuid.UUID
    status: Status

    @classmethod
    def new_model(cls) -> 'Model':
        return cls(id=uuid.uuid4(), status=Status.PENDING)

    def json(self) -> dict[str, str]:
        return {
            'id': str(self.id),
            'status': self.status.name
        }
