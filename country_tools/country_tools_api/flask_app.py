import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from flask import Flask
from flask_graphql import GraphQLView

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.schemas import schema
from country_tools.country_tools_api.sitemap import generate_sitemap


app = Flask(__name__)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/sitemap")
@app.route("/sitemap.xml")
def sitemap():
    update_date = "2025-11-20"
    return generate_sitemap(update_date)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
