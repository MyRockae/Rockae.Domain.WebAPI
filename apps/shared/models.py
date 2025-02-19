from rest_framework.exceptions import APIException

class InternalServerError(APIException):
    status_code = 500
    default_detail = "An unexpected error occurred. Please try again later."
    default_code = "internal_error"

    def __init__(self, detail=None):
        """
        Allow passing a custom error message.
        If no message is provided, use the default.
        """
        if detail is None:
            detail = self.default_detail
        super().__init__(detail)
