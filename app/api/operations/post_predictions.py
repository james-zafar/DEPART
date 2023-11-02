from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.schemas import PredictionInput

predictions_router = APIRouter(prefix='/predictions}')


@predictions_router.post('', status_code=200)
async def post_predictions(predict_input: PredictionInput) -> JSONResponse:
    return JSONResponse(content={}, status_code=200)
