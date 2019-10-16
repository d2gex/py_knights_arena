from flask_restplus import Resource
from src.apis import utils as api_utils
from src.apis import errors as api_errors


class ResourceMixin(Resource):

    @staticmethod
    def check_payload_structure(api, dto):
        '''Ensure that the payload received from client has the expected structure
        '''
        if not isinstance(api.payload, dict):
            raise api_errors.BadRequest400Error(
                message='Incorrect type of object received. Instead a json object is expected',
                envelop=api_utils.RESPONSE_400)

        # Do we have all expected fields?
        expected_fields = dto.keys()
        for key in expected_fields:
            if key not in api.payload:
                raise api_errors.BadRequest400Error(message=f"Required key '{key}' not found",
                                                    envelop=api_utils.RESPONSE_400)
