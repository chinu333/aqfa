"""Flask application factory."""

from __future__ import annotations

import logging
from flask import Flask, render_template
from flask_cors import CORS

from app.config import AppConfig
from app.services.azure_quantum import AzureQuantumService
from app.services.pqc_security import PQCSecurityService
from app.services.chemistry import ChemistryService
from app.routes.api import api_bp, init_api

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s")


def create_app(config: AppConfig | None = None) -> Flask:
    """Create and configure the Flask application."""
    config = config or AppConfig()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.secret_key = config.flask.secret_key
    app.config["APP_CONFIG"] = config
    CORS(app)

    # ---- Initialize services ------------------------------------------------
    quantum_service = AzureQuantumService(config.quantum, config.auth)
    quantum_service.initialize()

    pqc_service = PQCSecurityService()
    pqc_service.initialize()

    chemistry_service = ChemistryService()
    chemistry_service.initialize()

    init_api(quantum_service, pqc_service, chemistry_service)

    # ---- Register blueprints ------------------------------------------------
    app.register_blueprint(api_bp)

    # ---- Frontend route -----------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    return app
