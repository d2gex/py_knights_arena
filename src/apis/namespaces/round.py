import json

from flask_restplus import Resource, fields
from src.apis import utils as api_utils, errors as api_errors
from src.apis.namespace import NameSpace
from src.apis.resource import ResourceMixin
from src import models
from src.app import db


api = NameSpace('round', description="Resource that allows creating a round and returned game context for particular "
                                     "round")

cell_content = {
    'name': fields.String(max_length=20, required=True, description="Name of the knight"),
    'nickname': fields.String(max_length=20, required=True, description="Nickname of the knight"),
    'attack_score': fields.Integer(required=True, description="Attack score the knight will start with"),
    'defence_score': fields.Integer(required=True, description="Defence score the knight will start with"),
    'x': fields.Integer(required=True, description="Coordinate 'x' of object position"),
    'y': fields.Integer(required=True, description="Coordinate 'x' of object position")
}
knight_data = {'status': fields.Integer(required=True, description="Status the knight will start with")}
knight_data.update(cell_content)

knight_dto = api.model('Knight data', knight_data)
item_dto = api.model('Items Data', cell_content)
round_dto = api.model('Round Context Data', {
    'knights': fields.List(fields.Nested(knight_dto)),
    'items': fields.List(fields.Nested(item_dto)),
    'rows': fields.Integer(required=True, description="Board's number of rows"),
    'columns': fields.Integer(required=True, description="Board's number of columns")
})


class RoundResource(ResourceMixin):

    def create_round(self, data):

        db_round = models.Round(rows=data['rows'], columns=data['columns'])
        db.session.add(db_round)
        db.session.commit()

        for knight in data['knights']:
            knight_obj = models.Player()
            knight_obj.name, knight_obj.nickname = knight['name'], knight['nickname']
            db.session.add(knight_obj)
            db.session.commit()
            x, y, status = knight['x'], knight['y'], knight['status']
            attack_score, defence_score = knight['attack_score'], knight['defence-score']
            settings = models.Settings(round_id=db_round.id,
                                       player_id=knight_obj.id,
                                       player_status_id=status,
                                       x=x,
                                       y=y,
                                       attack_score=attack_score,
                                       defence_score=defence_score)
            db.session.add(settings)
            db.session.commit()


@api.route('/')
@api.response_error(api_errors.Server500Error(message=api_utils.RESPONSE_500))
class Round(ResourceMixin):

    @api.expect(round_dto)
    @api.response_error(api_errors.BadRequest400Error(message=api_utils.RESPONSE_400))
    @api.response_error(api_errors.NotFound404Error(message=api_utils.RESPONSE_404))
    @api.response_error(api_errors.Conflict409Error(message=api_utils.RESPONSE_409))
    @api.response(201, json.dumps(api_utils.RESPONSE_201), body=False)
    def post(self):
        pass