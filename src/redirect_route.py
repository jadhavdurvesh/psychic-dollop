from flask import redirect, abort
from .app import app, db
from .models import Url

# Reserved paths that should not be treated as short codes
RESERVED_PATHS = {'static', 'health'}

@app.route('/<string:short_code>', methods=['GET'])
def redirect_short_code(short_code):
    # Do not capture reserved routes
    if short_code in RESERVED_PATHS:
        abort(404)

    url_entry = Url.query.filter_by(short_code=short_code).first()
    if not url_entry:
        abort(404)

    try:
        # Safely increment click count (handle None case)
        url_entry.click_count = (url_entry.click_count or 0) + 1
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500)

    return redirect(url_entry.original_url, code=301)
