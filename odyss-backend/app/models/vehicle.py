# from app.extensions import db
# from uuid import uuid4

# class Vehicle(db.Model):
#     __tablename__ = "vehicles"

#     id = db.Column(db.Uuid, primary_key=True, default=uuid4)
#     company_id = db.Column(db.Uuid, db.ForeignKey("companies.id"), nullable=False)
#     plate_number = db.Column(db.String(20), nullable=False, unique=True)
#     vehicle_type = db.Column(db.String(50), nullable=False)  # e.g. Bus, Van, Car
#     capacity = db.Column(db.Integer, nullable=False)
#     image = db.Column(db.Text, nullable=True)  # Base64 encoded image (optional)

#     trips = db.relationship("Trip", backref="vehicle", lazy=True)
