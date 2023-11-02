import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

deploy_models_router = APIRouter(prefix='/deploy')


@deploy_models_router.put('', status_code=200)
async def post_predictions(model_id: uuid.UUID) -> JSONResponse:
    return JSONResponse(content={}, status_code=200)
