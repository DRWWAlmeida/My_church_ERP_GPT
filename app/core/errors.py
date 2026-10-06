class AppError(Exception):
    def __init__(self, message, status_code=400, field=None, value=None):
        self.message = message
        self.status_code = status_code
        self.field = field
        self.value = value
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, message):
        super().__init__(message=message, status_code=404)


class ValidationError(AppError):
    def __init__(self, message, field=None, value=None):
        super().__init__(
            message=message,
            status_code=400,
            field=field,
            value=value,
        )

class IntegrityError(AppError):
    def __init__(self, message, field=None, value=None):
        super().__init__(
            message=message, 
            status_code=400,
            field=field,
            value=value,
        )

class OperationalError(AppError):
    def __init__(self, message):
        super().__init__(
            message=message,
            status_code=500,
        )





