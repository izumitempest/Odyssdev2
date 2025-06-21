import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.user import User
from app.auth.models import OAuthIdentity
from app.extensions import db
import uuid

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    # 💉 This is your safe zone — anything using db.session or current_app goes here


# Grab any user from DB
    user = User.query.filter_by(email="izumi@test.com").first()

    # THEN create OAuthIdentity
    oauth = OAuthIdentity(
        id=uuid.uuid4(),
        user_id=user.id,
        provider="google",
        provider_user_id="google-oauth-485",
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MDUxNzIzNywianRpIjoiYmQ1NGYzNzQtM2IzZS00ZjQ0LThkZjUtMzVlYTlkNzlhZjUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQ4NTA4M2EwLWYyNjQtNDNjOS1hNDZiLTJkYzMyMDA4NTUxNiIsIm5iZiI6MTc1MDUxNzIzNywiY3NyZiI6ImFlMWI4OWZlLWNkN2EtNDcyNS04M2E0LTNlMjM4ZGFkODkyNyIsImV4cCI6MTc1MDUyMDgzNywiZW1haWwiOiJpenVtaUB0ZXN0LmNvbSIsIm5hbWUiOm51bGx9.dSVFhn8BTFp92BXp6PBhko3ztcf6sVbT3IGZwYuzaDA"
    )

    db.session.add(oauth)
    db.session.commit()
