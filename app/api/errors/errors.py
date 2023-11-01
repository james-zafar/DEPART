from app.api.errors.error_response import Error


class ModelNotFoundError(Error):
    code = 'model_not_found'
    message = 'A model with the specified ID could not be located'
    status_code = 404