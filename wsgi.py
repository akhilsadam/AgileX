"""Application entry point."""
from AgileX import init_app

app = init_app()
port = 9050

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False,port=port)


# with help from https://github.com/toddbirchard/plotlydash-flask-tutorial