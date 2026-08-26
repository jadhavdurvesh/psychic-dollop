from flask import abort, redirect

from .store import store


def register_redirect(app):
    @app.route("/<code>", methods=["GET"])
    def _redirect(code):
        """
        Redirect the user to the original URL mapped by *code*.
        Returns 404 if the code does not exist.
        """
        original_url = store.get(code)
        if original_url:
            return redirect(original_url)
        abort(404, description="Short code not found")