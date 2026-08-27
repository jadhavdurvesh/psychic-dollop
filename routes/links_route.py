from flask import Blueprint, jsonify, current_app

links_bp = Blueprint("links", __name__)

@links_bp.route("/links", methods=["GET"])
def list_links():
    """
    Return a JSON array of all shortened links sorted by click count (descending).
    Each link is represented by its dictionary form as defined by Link.to_dict().
    """
    store = current_app.store
    links = store.get_all_links_sorted()
    # Convert each Link object to a serializable dict
    links_dicts = [link.to_dict() for link in links]
    return jsonify(links_dicts), 200