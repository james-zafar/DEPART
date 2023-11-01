from pydantic import BaseModel


class PredictionInput(BaseModel):
    predict: str
