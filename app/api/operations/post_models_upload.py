from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.errors import new_error_response, InvalidDataSourceError, UnsupportedModelTypeError
from app.api.resources import Model
from app.api.schemas import UploadModelsBody, Status
from app.model import DelayModel

post_models_upload_router = APIRouter(prefix='/models/upload')


@post_models_upload_router.post('')
async def post_models_upload(config: UploadModelsBody, request: Request) -> JSONResponse:
    model = Model.new_model()
    try:
        delay_model = DelayModel.load(str(config.model_location))
    except FileNotFoundError:
        return JSONResponse(content=new_error_response([InvalidDataSourceError()]),
                            status_code=InvalidDataSourceError.status_code)
    except (TypeError, ValueError, AttributeError):
        return JSONResponse(content=new_error_response([UnsupportedModelTypeError()]),
                            status_code=UnsupportedModelTypeError.status_code)

    request.app.state.model_store[str(model.id)] = model
    request.app.state.model_store.update_model(str(model.id), delay_model)
    request.app.state.model_store.update_status(str(model.id), Status.COMPLETED)

    headers = {'Location': f'{str(request.base_url)}v1/models/{str(model.id)}'}
    return JSONResponse(content=model.json(), headers=headers, status_code=201)
