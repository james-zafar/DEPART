from collections.abc import MutableMapping, Iterator
from dataclasses import dataclass, field
from typing import Any, TypeVar

from app.api.resources import Model
from app.model.model import DelayModel
from app.api.schemas import Status

KT = TypeVar('KT', bound=str)
VT = TypeVar('VT', bound=Model)


@dataclass
class ModelStore(MutableMapping[KT, VT]):
    _data: dict[KT, VT] = field(default_factory=dict, init=False)

    def update_status(self, model_id: KT, status: Status) -> None:
        if model_id not in self:
            raise KeyError(f'Unable to locate a model with the specified ID: {model_id}')
        if (model := self[model_id]).status in (Status.FAILED, Status.COMPLETED):
            raise ValueError('The status of a completed or failed model can not be changed.')
        model.status = status

    def add_model(self, model: Model) -> None:
        self[str(model.id)] = model  # type: ignore

    def update_model(self, model_id: KT, model: DelayModel) -> None:
        self[model_id].model = model

    def get(self, model_id: KT) -> VT | None:  # type: ignore
        if model_id in self:
            return self[model_id]
        return None

    def clear(self) -> None:
        self._data.clear()

    def __setitem__(self, model_id: KT, value: VT) -> None:
        self._data[model_id] = value

    def __delitem__(self, model_id: KT) -> None:
        del self._data[model_id]

    def __getitem__(self, model_id: KT) -> VT:
        return self._data[model_id]

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: Any) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[KT]:
        return iter(self._data)
