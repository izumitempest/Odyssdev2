# # app/companies/routes.py

# from flask import Blueprint, request, jsonify
# from marshmallow import ValidationError
# from app.companies.schemas import CompanySignupSchema
# from app.companies.services import register_company

# companies_bp = Blueprint("companies", __name__, url_prefix="/companies")

# @companies_bp.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()
#     try:
#         validated = CompanySignupSchema().load(data)
#         company = register_company(validated)
#         return jsonify({
#             "message": "Company registered successfully",
#             "company": {
#                 "id": str(company.id),
#                 "name": company.name,
#                 "email": company.email,
#                 "created_at": company.created_at.isoformat()
#             }
#         }), 201
#     except ValidationError as e:
#         return jsonify({"errors": e.messages}), 400
