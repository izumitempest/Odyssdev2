# seed_data.py
# odyss-backend/scripts/seed.py
from uuid import uuid4
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

from app import create_app, db
from app.models.user import User
from app.models.trip import Trip
from app.models.booking import Booking

def seed():
    print("🌱 Starting seeding process...")
    with app.app_context():
        # Purge all tables
        Booking.query.delete()
        Trip.query.delete()
        User.query.delete()
        db.session.commit()

        print("🔁 Tables cleared...")

        # Create a user (you 😉)
        izu_id = uuid4()
        user = User(
            id=izu_id,
            email="izumi@test.com",
            password_hash=generate_password_hash("password123"),
            name="Izumi The Hacker",
            avatar="https://i.imgur.com/Sagfcji",
            created_at=datetime.utcnow()
        )
        db.session.add(user)

        print("👤 User created")

        # Create sample trips
        trips = []
        for i in range(3):
            trip = Trip(
                id=uuid4(),
                origin=random.choice(["Enugu", "Lagos", "Ibadan"]),
                destination=random.choice(["Abuja", "Port Harcourt", "Kaduna"]),
                departure_time=datetime.utcnow() + timedelta(days=i+1, hours=8),
                arrival_time=datetime.utcnow() + timedelta(days=i+1, hours=14),
                seats_total=14,
                seats_available=14,
                price=random.randint(5000, 10000)
            )
            trips.append(trip)
            db.session.add(trip)

        db.session.flush()
        print(f"🚌" f"{len(trips)} trips created")

        # Create a booking for Izumi
        booking = Booking(
            id=uuid4(),
            user_id=izu_id,
            trip_id=trips[0].id,
            seat_number=1,
            status="confirmed",
            created_at=datetime.utcnow()
        )
        db.session.add(booking)

        db.session.commit()
        print("✅ Seeding complete!")

if __name__ == "__main__":
    app = create_app()
    seed()
