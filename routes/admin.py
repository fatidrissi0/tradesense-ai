from flask import Blueprint, jsonify
from flask_restful import Api, Resource

admin_bp = Blueprint('admin_bp', __name__)
api = Api(admin_bp)

class AdminDashboard(Resource):
    def get(self):
        return jsonify({"message": "Admin dashboard"})

api.add_resource(AdminDashboard, '/')
