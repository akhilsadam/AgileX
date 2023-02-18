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

@app.route("/doc/")
def doc():
    """readme"""
    return render_template(
        "readme.jinja2",
        title="AgileX: An Agile Document Editor | Readme",
        title2="Readers / Reviewers / Advisors",
        title3="Writers / Authors / Students",
        general=
"""This project is a way to quickly generate and view a versioned document in LaTeX, to maintain a history of development for articles like research papers or modular code documentation.<br>
Easy adaptation to other code formats is possible, but has not yet been done.
Any other suggestions / bugfixes / feature requests are highly encouraged, with the caveat that updates are infrequent.<br>
Note also that the site is not very secure, and is expected to run only locally, with only static site deployments (such as this one)""",
        template="home-template",
        body="This is a homepage served with Flask.",
    )