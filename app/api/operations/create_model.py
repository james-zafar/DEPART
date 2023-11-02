from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.resources import Model
from app.api.schemas import CreateModelRequestBody
from app.model import DelayModel

post_models_router = APIRouter(prefix='/models')


@post_models_router.post('')
async def create_model(config: CreateModelRequestBody, request: Request) -> JSONResponse:
    model = Model.new_model()
    request.app.state.model_store[str(model.id)] = model

    delay_model = DelayModel().train(config.data_source)
    request.app.state.model_store.update_model(str(model.id), delay_model)

    headers = {'Location': f'{str(request.url)}/{str(model.id)}'}
    return JSONResponse(content=model.json(), headers=headers, status_code=201)
