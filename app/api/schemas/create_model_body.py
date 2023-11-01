from pydantic import BaseModel, FilePath, AnyHttpUrl


class CreateModelRequestBody(BaseModel):
    data_source: FilePath | AnyHttpUrl
