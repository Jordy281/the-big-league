from api.app import ma
from marshmallow import fields

from api.models import LinkedLeagueSchema

class LeagueSchema(ma.Schema):
    league_id = ma.Int()
    league_name = ma.Str()
    # Location of League Logo in GCS
    avatar = ma.Str()
    # List of Linked League ID's (ID's from sleeper, NFL, Yahoo)
    linked_leagues = ma.List(ma.Str(), dump_default=[], many=True)
