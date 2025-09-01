# backend/routes.py
from flask import Blueprint, request, jsonify
import src.function as fn

bp = Blueprint('api', __name__)

# @bp.route('/add', methods=['POST'])
# def add_route():
#     data = request.json
#     a = data.get('a')
#     b = data.get('b')
#     result = add_numbers(a, b)
#     return jsonify({'result': result})

# @bp.route('/multiply', methods=['POST'])
# def multiply_route():
#     data = request.json
#     a = data.get('a')
#     b = data.get('b')
#     result = multiply_numbers(a, b)
#     return jsonify({'result': result})
