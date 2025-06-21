# schemas.py
from marshmallow import Schema, fields

class PassengerSchema(Schema):
    user_id = fields.UUID()
    name = fields.String(allow_none=True)
    seat_number = fields.Integer()
    status = fields.String()
    # status can be 'pending', 'paid', 'cancelled'
