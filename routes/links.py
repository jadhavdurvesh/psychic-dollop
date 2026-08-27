from flask import Blueprint, jsonify
from store import get_all_links_sorted

links_bp = Blueprint('links', __name__)

@links_bp.route('/api/links', methods=['GET'])
def list_links():
    """
    Return a JSON array of all shortened links sorted by click count
    (highest first). Each link is represented by its dictionary form.
    """
    links = get_all_links_sorted()
    return jsonify([link.to_dict() for link in links])