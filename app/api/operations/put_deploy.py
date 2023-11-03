import os
import uuid

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from app.api.errors import new_error_response, UnauthorizedError, ForbiddenError, ModelNotFoundError, ModelNotReadyError
from app.api.schemas import Status

deploy_models_router = APIRouter(prefix='/models/deploy')

X_API_KEY = APIKeyHeader(name='X-api-key')


def _validate_api_key(x_api_key: str) -> type[UnauthorizedError] | type[ForbiddenError] | None:
    api_user, api_key = os.environ.get('API_KEY').split('=')
    if '=' not in x_api_key:
        return UnauthorizedError
    x_api_user, x_api_key = x_api_key.split('=')
    if x_api_user != api_user:
        return UnauthorizedError
    if x_api_key != api_key:
        return ForbiddenError
    return None


@deploy_models_router.put('', status_code=200)
async def deploy_model(request: Request, model_id: uuid.UUID = Query(alias='model-id'),
                       x_api_key: str = Depends(X_API_KEY)) -> JSONResponse:
    if error := _validate_api_key(x_api_key):
        return JSONResponse(content=new_error_response([error()]), status_code=error.status_code)
    if not (model := request.app.state.model_store.get(str(model_id))):
        return JSONResponse(content=new_error_response([ModelNotFoundError()]),
                            status_code=ModelNotFoundError.status_code)
    if model.status != Status.COMPLETED:
        return JSONResponse(content=new_error_response([ModelNotReadyError()]),
                            status_code=ModelNotReadyError.status_code)

    request.app.state.model = model.model
    response_json = {
        'id': str(model.id),
        'deployed': 'OK'
    }
    return JSONResponse(content=response_json, status_code=200)
