from flask import Blueprint, jsonify
from constants import CATEGORIES

meta_bp = Blueprint('meta', __name__)

@meta_bp.route('/meta/categories', methods=['GET'])
def get_categories():
    return jsonify({
        "categories": CATEGORIES
    })
