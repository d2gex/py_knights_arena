from datetime import datetime
from src.app import db
from sqlalchemy.orm import relationship


class Round(db.Model):
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    columns = db.Column(db.Integer)
    settings = relationship("Settings")
    moves = relationship("Moves")


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    settings = relationship("Settings")
    moves = relationship("Moves")


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    settings = relationship("Settings")
    moves = relationship("Moves")


class PlayerStatus(db.Model):
    _tablename__ = 'player_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    settings = relationship("Settings")
    moves = relationship("Moves")


class Moves(db.Model):
    '''Table holding the moves. Each move will correspond only to one move per knight per round.
    '''
    __tablename__ = 'moves'
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    player_status_id = db.Column(db.Integer, db.ForeignKey('player_status.id'), nullable=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    created = db.Column(db.DateTime, default=datetime.utcnow)


class Settings(db.Model):
    '''This class will contain the settings of each round. Each row could be either an item or a knight
    so that when an item its knight foreign key will be set to NULL and vice verse.
    '''
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    player_status_id = db.Column(db.Integer, db.ForeignKey('player_status.id'), nullable=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    attack_score = db.Column(db.Integer)
    defence_score = db.Column(db.Integer)
