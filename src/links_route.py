from flask import Blueprint, jsonify

from . import store

links_bp = Blueprint("links", __name__, url_prefix="/api")


@links_bp.route("/links", methods=["GET"])
def get_links():
    """
    Return a JSON array of all shortened links sorted by click count descending.
    Each link is represented by its ``to_dict`` serialization.
    """
    try:
        links = store.get_all_links_sorted()
        result = [link.to_dict() for link in links]
        return jsonify(result), 200
    except Exception as exc:  # pragma: no cover – generic safety net
        # In a real application you would log the exception.
        return jsonify({"error": "Internal Server Error"}), 500