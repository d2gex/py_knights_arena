import json

from flask import request, send_from_directory
from flask_restplus import Resource, fields
from werkzeug.exceptions import NotFound
from src.apis import utils as api_utils, errors as api_errors
from src.apis.namespace import NameSpace
from src.apis.handler import api_v1


api = NameSpace('round', description="Resource that allows creating a round and returned game context for particular "
                                     "round")

cell_content = {
    'name': fields.String(max_length=20, required=True, description="Name of the knight"),
    'nickname': fields.String(max_length=20, required=True, description="Nickname of the knight"),
    'attack_score': fields.Integer(required=True, description="Attack score the knight will start with"),
    'defence_score': fields.Integer(required=True, description="Defence score the knight will start with")
}
knight_data = {'status_score': fields.Integer(required=True, description="Status the knight will start with")}
knight_data.update(cell_content)

knight_dto = api.model('Knight data', knight_data)
item_dto = api.model('Items Data', cell_content)
round_dto = api.model('Round Context Data', {
    'knights': fields.List(fields.Nested(knight_dto)),
    'items': fields.List(fields.Nested(item_dto)),
    'rows': fields.Integer(required=True, description="Board's number of rows"),
    'columns': fields.Integer(required=True, description="Board's number of columns")
})


@api.route('/')
@api.response_error(api_errors.Server500Error(message=api_utils.RESPONSE_500))
class Round(Resource):

    @api.expect(round_dto)
    @api.response_error(api_errors.BadRequest400Error(message=api_utils.RESPONSE_400))
    @api.response_error(api_errors.NotFound404Error(message=api_utils.RESPONSE_404))
    @api.response_error(api_errors.Conflict409Error(message=api_utils.RESPONSE_409))
    @api.response(201, json.dumps(api_utils.RESPONSE_201), body=False)
    def post(self):
        pass
