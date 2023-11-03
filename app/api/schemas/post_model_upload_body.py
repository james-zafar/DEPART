from pydantic import BaseModel, FilePath, AnyHttpUrl


class UploadModelsBody(BaseModel):
    model_location: FilePath | AnyHttpUrl
