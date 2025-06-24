# schemas.py
from marshmallow import Schema, fields, validate

class PassengerSchema(Schema):
    user_id = fields.UUID()
    name = fields.String(allow_none=True)
    seat_number = fields.Integer()
    status = fields.String()
    # status can be 'pending', 'paid', 'cancelled'

class BookingRequestSchema(Schema):
    seat_number = fields.Integer(required=True, validate=validate.Range(min=1, max=50))  # or whatever the bus max is

