import os
from flask import Flask, render_template
from dotenv import load_dotenv

import pulumi.automation as auto

load_dotenv()

def ensure_plugins():
    ws = auto.LocalWorkspace()
    ws.install_plugin("aws", "v4.0.0")


def create_app():
    ensure_plugins()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        PROJECT_NAME=os.environ.get("PULUMI_ORG"),
        PULUMI_ORG=os.environ.get("PULUMI_ORG"),
    )

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    from . import sites

    app.register_blueprint(sites.bp)

    from . import virtual_machines

    app.register_blueprint(virtual_machines.bp)

    return app