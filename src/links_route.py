from flask import Blueprint, jsonify, current_app

from src.store import get_all_links_sorted

links_bp = Blueprint('links', __name__)

@links_bp.route('/api/links', methods=['GET'])
def get_links():
    """
    Return a JSON array of all shortened links ordered by click count descending.
    """
    try:
        links = get_all_links_sorted()
        result = [link.to_dict() for link in links]
        return jsonify(result), 200
    except Exception as e:
        # Log the error for debugging purposes
        current_app.logger.error(f"Failed to retrieve links: {e}")
        return jsonify({"error": "Internal server error"}), 500