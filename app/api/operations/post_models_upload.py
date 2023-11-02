import base64
import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from app.api.errors import new_error_response, InvalidDataSourceError, UnsupportedModelTypeError, UnauthorizedError, ForbiddenError
from app.api.resources import Model
from app.api.schemas import UploadModelsBody, Status
from app.model import DelayModel

post_models_upload_router = APIRouter(prefix='/models/upload')

X_API_KEY = APIKeyHeader(name='X-api-key')


def _validate_api_key(x_api_key: str) -> type[UnauthorizedError] | type[ForbiddenError] | None:
    api_user, api_key = os.environ.get('API_KEY').split('=')
    x_api_key = base64.b64decode(x_api_key)
    if '=' not in x_api_key:
        return UnauthorizedError
    x_api_user, x_api_key = x_api_key.split('=')
    if x_api_user != api_user:
        return UnauthorizedError
    if x_api_key != api_key:
        return ForbiddenError


@post_models_upload_router.post('')
async def post_models_upload(config: UploadModelsBody, request: Request, x_api_key: str = Depends(X_API_KEY)) -> JSONResponse:
    if error := _validate_api_key(x_api_key):
        return JSONResponse(content=new_error_response([error()]), status_code=error.status_code)

    model = Model.new_model()
    request.app.state.model_store[str(model.id)] = model
    try:
        delay_model = DelayModel.load(config.model_location)
    except FileNotFoundError:
        return JSONResponse(content=new_error_response([InvalidDataSourceError()]),
                            status_code=InvalidDataSourceError.status_code)
    except (TypeError, ValueError):
        return JSONResponse(content=new_error_response([UnsupportedModelTypeError()]),
                            status_code=UnsupportedModelTypeError.status_code)

    request.app.state.model_store.update_model(str(model.id), delay_model)
    request.app.state.model_store.update_status(str(model.id), Status.COMPLETED)

    headers = {'Location': f'{str(request.url)}/{str(model.id)}'}
    return JSONResponse(content=model.json(), headers=headers, status_code=201)
