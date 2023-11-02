from collections.abc import Sequence
from dataclasses import dataclass


def new_error_response(errors: Sequence['Error']) -> dict[str, list[dict[str, str]]]:
    return {
        'errors': [error.json() for error in errors]
    }


@dataclass(init=False)
class Error:
    code: str
    message: str
    status_code: int

    def json(self) -> dict[str, str]:
        return {
            'code': self.code,
            'message': self.message,
            'status': str(self.status_code)
        }
