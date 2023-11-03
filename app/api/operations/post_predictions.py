import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.schemas import PredictionInput

predictions_router = APIRouter(prefix='/predictions')


@predictions_router.post('', status_code=200)
async def post_predictions(predict_input: PredictionInput, request: Request) -> JSONResponse:
    flights = [flight.model_dump(by_alias=True) for flight in predict_input.flights]
    flights_df = pd.DataFrame(flights)
    flights_df = request.app.state.model.preprocess(flights_df)
    preds = request.app.state.model.predict(flights_df)

    return JSONResponse(content={'predictions': preds}, status_code=200)
