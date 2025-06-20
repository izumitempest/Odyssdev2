import os

# Your root project folder
BASE_DIR = "odyss-backend"

# Tree definition (flattened and easier to maintain)
TREE = [
    "app/__init__.py",
    "app/config.py",
    "app/extensions.py",

    # Core
    "app/core/__init__.py",
    "app/core/database.py",
    "app/core/dependencies.py",
    "app/core/exceptions.py",
    "app/core/constants.py",
    "app/core/postgres_utils.py",

    # Models
    "app/models/__init__.py",
    "app/models/base.py",
    "app/models/user.py",
    "app/models/trip.py",
    "app/models/booking.py",
    "app/models/payment.py",
    "app/models/role.py",
    "app/models/permission.py",

    # Auth
    "app/auth/__init__.py",
    "app/auth/models.py",
    "app/auth/routes.py",
    "app/auth/services.py",
    "app/auth/guards.py",
    "app/auth/rbac.py",
    "app/auth/utils.py",

    # Trips
    "app/trips/__init__.py",
    "app/trips/routes.py",
    "app/trips/services.py",
    "app/trips/repositories.py",
    "app/trips/schemas.py",
    "app/trips/utils.py",

    # Bookings
    "app/bookings/__init__.py",
    "app/bookings/routes.py",
    "app/bookings/services.py",
    "app/bookings/repositories.py",
    "app/bookings/schemas.py",
    "app/bookings/utils.py",

    # Payments
    "app/payments/__init__.py",
    "app/payments/routes.py",
    "app/payments/services.py",
    "app/payments/repositories.py",
    "app/payments/schemas.py",
    "app/payments/utils.py",
    "app/payments/processors/__init__.py",
    "app/payments/processors/base.py",
    "app/payments/processors/stripe.py",
    "app/payments/processors/paypal.py",

    # Users
    "app/users/__init__.py",
    "app/users/routes.py",
    "app/users/services.py",
    "app/users/repositories.py",
    "app/users/schemas.py",
    "app/users/utils.py",

    # Admin
    "app/admin/__init__.py",
    "app/admin/routes.py",
    "app/admin/services.py",
    "app/admin/repositories.py",
    "app/admin/schemas.py",
    "app/admin/dashboard.py",

    # Search
    "app/search/__init__.py",
    "app/search/routes.py",
    "app/search/services.py",
    "app/search/filters.py",
    "app/search/utils.py",

    # Notifications
    "app/notifications/__init__.py",
    "app/notifications/routes.py",
    "app/notifications/services.py",
    "app/notifications/providers/__init__.py",
    "app/notifications/providers/email.py",
    "app/notifications/providers/sms.py",
    "app/notifications/providers/push.py",
    "app/notifications/templates/email/",
    "app/notifications/templates/sms/",

    # Common
    "app/common/__init__.py",
    "app/common/decorators.py",
    "app/common/validators.py",
    "app/common/serializers.py",
    "app/common/pagination.py",
    "app/common/errors.py",
    "app/common/helpers.py",

    # API v1
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/routes.py",
    "app/api/middleware.py",

    # Migrations
    "migrations/alembic.ini",
    "migrations/env.py",
    "migrations/script.py.mako",
    "migrations/versions/",

    # Tests
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/factories.py",
    "tests/unit/test_auth.py",
    "tests/unit/test_trips.py",
    "tests/unit/test_bookings.py",
    "tests/unit/test_payments.py",
    "tests/integration/test_trip_booking_flow.py",
    "tests/integration/test_payment_flow.py",
    "tests/fixtures/",

    # Scripts
    "scripts/init_db.py",
    "scripts/seed_data.py",
    "scripts/backup_db.py",
    "scripts/restore_db.py",
    "scripts/deploy.py",

    # Logs
    "logs/app.log",
    "logs/error.log",

    # Requirements
    "requirements/base.txt",
    "requirements/development.txt",
    "requirements/production.txt",
    "requirements/testing.txt",

    # Root files
    ".env.example",
    ".gitignore",
    "README.md",
    "Dockerfile",
    "docker-compose.yml",
    "wsgi.py",
    "run.py"
]


def generate_structure():
    for path in TREE:
        full_path = os.path.join(BASE_DIR, path)
        dir_name = os.path.dirname(full_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if not path.endswith("/"):  # means it's a file
            with open(full_path, "w") as f:
                if path.endswith(".py"):
                    f.write(f"# {os.path.basename(path)}\n")

    print(f"✅ Structure for '{BASE_DIR}' created successfully!")


if __name__ == "__main__":
    generate_structure()
