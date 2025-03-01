import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LogRequestsMiddleware(MiddlewareMixin):
    """Logging middleware to log request and response details.
    This middleware logs the request method, path, headers, query parameters,
    and body. It also logs the response status code.

    Ordering: This middleware should be placed after the authentication middleware
    to ensure that user information is available in the logs.

    Args:
        MiddlewareMixin (_type_): _description_
    """

    def process_request(self, request):
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request Path: {request.path}")
        logger.info(f"Request Headers: {request.headers}")
        logger.info(f"Query Parameters: {request.GET}")
        if request.body:
            logger.info(f"Request Body: {request.body}")

    def process_response(self, request, response):
        logger.info(f"Response Status Code: {response.status_code}")
        return response
