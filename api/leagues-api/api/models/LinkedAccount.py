from api.app import ma

class LinkedAccountSchema(ma.Schema):
    avatar = ma.Int()
    host = ma.Str()
    name = ma.Str()
    linked_account_id = ma.Str()
    user_id = ma.Str()

class InputLinkedAccountSchema(ma.Schema):
    linked_account_id = ma.Str()
    host = ma.Str()