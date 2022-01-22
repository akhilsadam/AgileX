"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="AgileX: An Agile Document Editor",
        description="Generate modular Overleaf documentation and automatically web-host results, with Git version control!",
        template="home-template",
        body="This is a homepage served with Flask.",
    )