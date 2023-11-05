import uuid
from dataclasses import dataclass, field

from app.api.errors.error_response import Error
from app.api.schemas import Status
from app.model import DelayModel


@dataclass(eq=False)
class Model:
    id: uuid.UUID
    status: Status
    model: DelayModel | None = field(default=None)
    errors: list[Error] = field(default_factory=list)

    @classmethod
    def new_model(cls) -> 'Model':
        return cls(id=uuid.uuid4(), status=Status.PENDING)

    def new_model_response(self, exported: bool | None = None, deployed: bool = False) -> dict[str, str | bool | list[dict[str, str]]]:
        json_resp: dict[str, str | bool | list[dict[str, str]]] = {
            'id': str(self.id),
            'status': self.status.value,
            'deployed': deployed
        }
        if exported:
            json_resp['download'] = 'OK'
        if self.errors:
            json_resp['errors'] = [error.json() for error in self.errors]

        return json_resp
