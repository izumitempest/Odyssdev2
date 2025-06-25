# # app/companies/services.py

# from app.models.company import Company
# from app.extensions import db
# from werkzeug.security import generate_password_hash

# def register_company(data):
#     hashed = generate_password_hash(data["password"])
#     company = Company(
#         name=data["name"],
#         email=data["email"],
#         password_hash=hashed,
#         company_name=data["company_name"],
#         company_email=data["company_email"],
#         company_cert=data["company_cert"],
#         access_code=data["access_code"],
#     )
#     db.session.add(company)
#     db.session.commit()
#     return company
