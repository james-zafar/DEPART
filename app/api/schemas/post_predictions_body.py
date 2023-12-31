from pydantic import BaseModel, Extra, Field


class Flight(BaseModel, extra=Extra.allow):
    opera: str = Field(alias='OPERA')
    tipovuelo: str = Field(alias='TIPOVUELO')
    mes: int = Field(alias='MES')
    Fecha_O: str = Field(alias='Fecha-O')
    Fecha_I: str = Field(alias='Fecha-I')

    class Config:
        populate_by_name = True


class PredictionInput(BaseModel):
    flights: list[Flight] = Field(min_items=1)
