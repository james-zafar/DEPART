import random
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.errors import new_error_response, ModelNotFoundError, InternalServerError

delete_models_router = APIRouter(prefix='/models/{model_id}')


@delete_models_router.delete('', status_code=204)
async def delete_model(model_id: uuid.UUID, request: Request) -> JSONResponse:
    if str(model_id) not in request.app.state.model_store:
        return JSONResponse(content=new_error_response([ModelNotFoundError()]), status_code=404)
    elif random.randint(0, 100) % 50 == 0:
        return JSONResponse(content=new_error_response([InternalServerError()]), status_code=500)

    del request.app.state.model_store[str(model_id)]

    return JSONResponse(content=None, status_code=204)
