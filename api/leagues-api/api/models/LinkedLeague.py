from api.app import ma
from marshmallow import fields


class LinkedLeagueSchema(ma.Schema):
    host = ma.Str()
    name = ma.Str()
    league_id = ma.Str()
    avatar = ma.Str()
    members = ma.Dict(keys=fields.Int(), values=fields.Str())
