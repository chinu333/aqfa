"""REST API routes for quantum job management, PQC security, and service health."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Services are injected by the app factory (see main.py)
_quantum_service = None
_pqc_service = None
_chemistry_service = None


def init_api(quantum_service, pqc_service=None, chemistry_service=None):
    """Wire services into route handlers."""
    global _quantum_service, _pqc_service, _chemistry_service
    _quantum_service = quantum_service
    _pqc_service = pqc_service
    _chemistry_service = chemistry_service


# ---- Health & Config -------------------------------------------------------

@api_bp.route("/health", methods=["GET"])
def health():
    """Overall application and service health."""
    services = {}
    if _quantum_service:
        services["quantum"] = _quantum_service.health_check()
    if _pqc_service:
        services["pqc_security"] = _pqc_service.health_check()
    return jsonify({"status": "ok", "services": services})


@api_bp.route("/config/targets", methods=["GET"])
def list_targets():
    """Return available quantum targets."""
    if not _quantum_service:
        return jsonify({"targets": []}), 200
    return jsonify({"targets": _quantum_service.available_targets})


@api_bp.route("/config/circuits", methods=["GET"])
def list_sample_circuits():
    """Return built-in sample circuits."""
    if not _quantum_service:
        return jsonify({"circuits": {}}), 200
    return jsonify({"circuits": _quantum_service.sample_circuits})


@api_bp.route("/config/services", methods=["GET"])
def list_services():
    """Return status of all pluggable services (for the dashboard)."""
    from flask import current_app
    cfg = current_app.config.get("APP_CONFIG")
    services = [
        {"name": "Azure Quantum", "configured": cfg.is_quantum_configured if cfg else False,
         "icon": "atom", "status": "active" if _quantum_service and _quantum_service._initialized else "pending"},
        {"name": "PQC Security", "configured": True,
         "icon": "shield-check", "status": "active" if _pqc_service and _pqc_service._initialized else "pending"},
        {"name": "Chemistry Lab", "configured": True,
         "icon": "flask-conical", "status": "active" if _chemistry_service and _chemistry_service._initialized else "pending"},
        {"name": "Azure OpenAI", "configured": cfg.is_openai_configured if cfg else False,
         "icon": "brain", "status": "coming-soon"},
        {"name": "Azure AI Search", "configured": cfg.is_search_configured if cfg else False,
         "icon": "search", "status": "coming-soon"},
        {"name": "Azure Speech", "configured": cfg.is_speech_configured if cfg else False,
         "icon": "microphone", "status": "coming-soon"},
    ]
    return jsonify({"services": services})


# ---- Quantum Jobs ----------------------------------------------------------

@api_bp.route("/jobs", methods=["GET"])
def list_jobs():
    """Return job history."""
    if not _quantum_service:
        return jsonify({"jobs": []}), 200
    return jsonify({"jobs": _quantum_service.list_jobs()})


@api_bp.route("/jobs", methods=["POST"])
def submit_job():
    """Submit a new quantum job.

    Body JSON: { circuit_qasm, target_id, job_name?, shots? }
    """
    if not _quantum_service:
        return jsonify({"error": "Quantum service unavailable"}), 503

    data = request.get_json(force=True)
    circuit_qasm = data.get("circuit_qasm", "")
    target_id = data.get("target_id", "")
    job_name = data.get("job_name", "")
    shots = int(data.get("shots", 100))

    if not circuit_qasm:
        return jsonify({"error": "circuit_qasm is required"}), 400
    if not target_id:
        return jsonify({"error": "target_id is required"}), 400

    result = _quantum_service.submit_job(circuit_qasm, target_id, job_name, shots)
    return jsonify(result), 202


@api_bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id: str):
    """Get status / results for a specific job."""
    if not _quantum_service:
        return jsonify({"error": "Quantum service unavailable"}), 503
    return jsonify(_quantum_service.get_job_status(job_id))


# ---- PQC Security ----------------------------------------------------------

@api_bp.route("/security/threats", methods=["GET"])
def get_threat_matrix():
    """Return the quantum threat matrix for current crypto algorithms."""
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    return jsonify(_pqc_service.get_threat_matrix())


@api_bp.route("/security/pqc-algorithms", methods=["GET"])
def get_pqc_algorithms():
    """Return NIST PQC algorithm comparison data."""
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    return jsonify(_pqc_service.get_pqc_algorithms())


@api_bp.route("/security/benchmark", methods=["POST"])
def run_benchmark():
    """Run a simulated PQC benchmark.

    Body JSON: { algorithm_ids?: string[] }
    """
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    data = request.get_json(force=True) if request.data else {}
    algo_ids = data.get("algorithm_ids")
    return jsonify(_pqc_service.run_pqc_benchmark(algo_ids))


@api_bp.route("/security/scan", methods=["POST"])
def scan_readiness():
    """Scan a list of algorithms for quantum readiness.

    Body JSON: { algorithms: string[] }
    """
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    data = request.get_json(force=True)
    algorithms = data.get("algorithms", [])
    if not algorithms:
        return jsonify({"error": "algorithms list is required"}), 400
    return jsonify(_pqc_service.scan_readiness(algorithms))


@api_bp.route("/security/timeline", methods=["GET"])
def get_threat_timeline():
    """Return quantum threat timeline milestones."""
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    return jsonify(_pqc_service.get_threat_timeline())


@api_bp.route("/security/posture", methods=["GET"])
def get_security_posture():
    """Return security posture radar data."""
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    return jsonify(_pqc_service.get_security_posture())


@api_bp.route("/security/hndl", methods=["POST"])
def simulate_hndl():
    """Simulate Harvest Now, Decrypt Later scenario.

    Body JSON: { quantum_year?: int, harvest_start_year?: int }
    """
    if not _pqc_service:
        return jsonify({"error": "PQC service unavailable"}), 503
    data = request.get_json(force=True) if request.data else {}
    return jsonify(_pqc_service.simulate_hndl(
        quantum_year=int(data.get("quantum_year", 2033)),
        harvest_start_year=int(data.get("harvest_start_year", 2024)),
    ))


# ---- Chemistry Lab ---------------------------------------------------------

@api_bp.route("/chemistry/molecules", methods=["GET"])
def list_molecules():
    """Return available molecules."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    return jsonify({"molecules": _chemistry_service.list_molecules()})


@api_bp.route("/chemistry/molecules/<molecule_id>", methods=["GET"])
def get_molecule(molecule_id: str):
    """Return full molecule data."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    mol = _chemistry_service.get_molecule(molecule_id)
    if not mol:
        return jsonify({"error": "Unknown molecule"}), 404
    return jsonify(mol)


@api_bp.route("/chemistry/scf", methods=["POST"])
def run_scf():
    """Run SCF / Hartree-Fock calculation."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    data = request.get_json(force=True)
    molecule_id = data.get("molecule_id", "water")
    return jsonify(_chemistry_service.run_scf(molecule_id))


@api_bp.route("/chemistry/active-space", methods=["POST"])
def run_active_space():
    """Run active space selection."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    data = request.get_json(force=True)
    return jsonify(_chemistry_service.run_active_space(
        data.get("molecule_id", "water"),
        data.get("n_active_electrons"),
        data.get("n_active_orbitals"),
    ))


@api_bp.route("/chemistry/qpe", methods=["POST"])
def run_qpe():
    """Run Quantum Phase Estimation."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    data = request.get_json(force=True)
    return jsonify(_chemistry_service.run_qpe(
        data.get("molecule_id", "water"),
        data.get("n_precision_qubits", 8),
    ))


@api_bp.route("/chemistry/casci", methods=["POST"])
def run_casci():
    """Run CASCI calculation."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    data = request.get_json(force=True)
    return jsonify(_chemistry_service.run_casci(
        data.get("molecule_id", "water"),
        data.get("n_roots", 5),
    ))


@api_bp.route("/chemistry/state-prep", methods=["POST"])
def run_state_prep():
    """Run state preparation analysis."""
    if not _chemistry_service:
        return jsonify({"error": "Chemistry service unavailable"}), 503
    data = request.get_json(force=True)
    return jsonify(_chemistry_service.run_state_prep(data.get("molecule_id", "water")))
