"""QDK Chemistry — Quantum Dashboard entry point.

Usage:
    python run.py
"""

from app.config import AppConfig
from app.main import create_app

config = AppConfig()
app = create_app(config)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  QDK Chemistry — Quantum Dashboard")
    print("=" * 60)
    print(f"  URL:     http://localhost:{config.flask.port}")
    print(f"  Debug:   {config.flask.debug}")
    print(f"  Quantum: {'Configured' if config.is_quantum_configured else 'Demo Mode'}")
    print("=" * 60 + "\n")

    app.run(
        host=config.flask.host,
        port=config.flask.port,
        debug=config.flask.debug,
    )
