import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.errors import new_error_response, ModelNotFoundError, ModelNotReadyError
from app.api.schemas import Status

get_models_router = APIRouter(prefix='/models/{model_id}')


@get_models_router.get('')
async def get_model(model_id: uuid.UUID, request: Request, export: bool | None = None, file_name: str | None = None) -> JSONResponse:
    if str(model_id) not in request.app.state.model_store:
        return JSONResponse(content=new_error_response([ModelNotFoundError()]), status_code=ModelNotFoundError.status_code)
    model = request.app.state.model_store[str(model_id)]
    response_json = model.json()
    if export:
        if model.status != Status.COMPLETED:
            return JSONResponse(content=new_error_response([ModelNotReadyError()]), status_code=ModelNotReadyError.status_code)
        file_name = file_name or f'{model_id}.pkl'
        model.model.save(file_name)
        response_json['export'] = 'OK'
    return JSONResponse(content=response_json, status_code=200)
