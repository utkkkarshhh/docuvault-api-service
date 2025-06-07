from rest_framework.response import Response


class ResponseHandler(Response):
    '''
    Wrapper around rest_framework's Response class to standardize API response.

    parameters
    ----------
    data: data to be returened
    status: a value from rest_framework.status
    success: True/False
    message: If any message to be passed in payload
    errors: List of errors in case api fails
    meta: If any meta data is to be provided in payload
    '''
    def __init__(self, data=None, success=True, status=None,
                 message=None, meta=None, headers=None,
                 errors=None, content_type=None, *args, **kwargs):
        resp_data = {
            'success': success,
        }
        if data is not None:
            resp_data['data'] = data
        if message:
            resp_data['message'] = message
        if meta:
            resp_data['meta'] = meta
        if errors:
            resp_data['errors'] = errors
        resp_data.update(kwargs)
        super().__init__(resp_data, status=status, headers=headers,
                         content_type=content_type)
