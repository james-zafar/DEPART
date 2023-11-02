import uuid
from dataclasses import dataclass, field

from app.api.schemas import Status
from app.model import DelayModel


@dataclass(eq=False)
class Model:
    id: uuid.UUID
    status: Status
    model: DelayModel = field(default=None)

    @classmethod
    def new_model(cls) -> 'Model':
        return cls(id=uuid.uuid4(), status=Status.PENDING)

    def json(self) -> dict[str, str]:
        return {
            'id': str(self.id),
            'status': self.status.name
        }
