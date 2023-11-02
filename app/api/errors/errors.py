from app.api.errors.error_response import Error


class DataFormatError(Error):
    code = 'incorrect_columns'
    message = 'The specified data source does not contain the required columns'
    status_code = 400


class InvalidDataSourceError(Error):
    code = 'invalid_data_source'
    message = 'The specified data source either does not exist or could not be read'
    status_code = 400


class ModelNotReadyError(Error):
    code = 'model_not_ready'
    message = 'A model can not be exported until it has completed'
    status_code = 400


class UnsupportedModelTypeError(Error):
    code = 'unsupported_model'
    message = 'The model type specified is not supported'
    status_code = 400


class UnauthorizedError(Error):
    code = 'operation_not_allowed'
    message = 'The model type specified is not supported'
    status_code = 401


class ForbiddenError(Error):
    code = 'unsupported_model'
    message = 'The model type specified is not supported'
    status_code = 403


class ModelNotFoundError(Error):
    code = 'model_not_found'
    message = 'A model with the specified ID could not be located'
    status_code = 404


class InternalServerError(Error):
    code = 'internal_error'
    message = 'An internal error occurred'
    status_code = 500
