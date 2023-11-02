import uuid
from dataclasses import dataclass, field

from app.api.errors.error_response import Error
from app.api.schemas import Status
from app.model import DelayModel


@dataclass(eq=False)
class Model:
    id: uuid.UUID
    status: Status
    model: DelayModel = field(default=None)
    errors: list[Error] = field(default_factory=list)

    @classmethod
    def new_model(cls) -> 'Model':
        return cls(id=uuid.uuid4(), status=Status.PENDING)

    def json(self) -> dict[str, str]:
        json_resp = {
            'id': str(self.id),
            'status': self.status.value
        }
        if self.errors:
            json_resp['errors'] = [error.json() for error in self.errors]

        return json_resp
