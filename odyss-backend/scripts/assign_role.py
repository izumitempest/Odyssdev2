from app import create_app
from app.models.user import User
from app.models.role import Role
from app.extensions import db

app = create_app()

with app.app_context():
    db.session.rollback()

    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session.add(admin_role)
        db.session.commit()
        print("Created admin role.")

    user = User.query.filter_by(email="newuser@odyss.ng").first()
    print("admin_role:", admin_role)
    print("user:", user)

    if not user:
        print("User not found!")
    else:
        user.role = admin_role
        db.session.commit()
        print("Role assigned and committed.")