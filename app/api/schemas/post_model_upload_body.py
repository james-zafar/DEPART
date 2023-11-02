from pydantic import BaseModel, FilePath, AnyHttpUrl, Field


class UploadModelsBody(BaseModel):
    model_location: FilePath | AnyHttpUrl
    type: str | None = None
