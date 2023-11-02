from app.api.errors.error_response import Error


class InvalidDataSourceError(Error):
    code = 'invalid_data_source'
    message = 'The specified data source either does not exist or could not be read'
    status_code = 400


class DataFormatError(Error):
    code = 'incorrect_columns'
    message = 'The specified data source does not contain the required columns'
    status_code = 400


class ModelNotFoundError(Error):
    code = 'model_not_found'
    message = 'A model with the specified ID could not be located'
    status_code = 404


class InternalServerError(Error):
    code = 'internal_error'
    message = 'An internal error occurred'
    status_code = 500
