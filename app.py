"""
Flask dev server for the InnWash static site.

Run: python app.py
  or: flask --app app run --debug --reload

The reloader watches this file plus *.html / *.css in the project directory.
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

from flask import Flask, abort, send_from_directory

ROOT = Path(__file__).resolve().parent


def _watched_files() -> list[str]:
    """Paths for Werkzeug reloader (HTML/CSS and this app)."""
    patterns = ["*.html", "*.css"]
    out: list[str] = [str(ROOT / "app.py")]
    for pat in patterns:
        out.extend(glob.glob(str(ROOT / pat)))
    return out


app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:filename>")
def static_files(filename: str):
    if os.sep in filename or (os.altsep and os.altsep in filename):
        abort(404)
    path = ROOT / filename
    if not path.is_file():
        abort(404)
    return send_from_directory(ROOT, filename)


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    # Debug + reloader: restarts when app.py or watched static files change.
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=True,
        use_reloader=True,
        extra_files=_watched_files(),
    )
