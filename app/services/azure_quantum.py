"""Azure Quantum workspace service — submits and monitors quantum jobs."""

from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any

from app.config import AzureQuantumConfig, AzureAuthConfig
from app.services.base import BaseService

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Sample circuits (OpenQASM 3.0) for quick demo submission
# ---------------------------------------------------------------------------
SAMPLE_CIRCUITS = {
    "bell_state": {
        "name": "Bell State (2 qubits)",
        "description": "Creates a maximally entangled Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2",
        "qasm": (
            'OPENQASM 3.0;\n'
            'include "stdgates.inc";\n'
            'qubit[2] q;\n'
            'bit[2] c;\n'
            'h q[0];\n'
            'cx q[0], q[1];\n'
            'c[0] = measure q[0];\n'
            'c[1] = measure q[1];\n'
        ),
    },
    "ghz_3": {
        "name": "GHZ State (3 qubits)",
        "description": "Creates a 3-qubit GHZ state (|000⟩ + |111⟩)/√2",
        "qasm": (
            'OPENQASM 3.0;\n'
            'include "stdgates.inc";\n'
            'qubit[3] q;\n'
            'bit[3] c;\n'
            'h q[0];\n'
            'cx q[0], q[1];\n'
            'cx q[0], q[2];\n'
            'c[0] = measure q[0];\n'
            'c[1] = measure q[1];\n'
            'c[2] = measure q[2];\n'
        ),
    },
    "superposition": {
        "name": "Superposition (1 qubit)",
        "description": "Places a single qubit in equal superposition using a Hadamard gate",
        "qasm": (
            'OPENQASM 3.0;\n'
            'include "stdgates.inc";\n'
            'qubit[1] q;\n'
            'bit[1] c;\n'
            'h q[0];\n'
            'c[0] = measure q[0];\n'
        ),
    },
    "random_number": {
        "name": "Quantum Random Number (4 qubits)",
        "description": "Generates a 4-bit random number using quantum superposition",
        "qasm": (
            'OPENQASM 3.0;\n'
            'include "stdgates.inc";\n'
            'qubit[4] q;\n'
            'bit[4] c;\n'
            'h q[0];\n'
            'h q[1];\n'
            'h q[2];\n'
            'h q[3];\n'
            'c[0] = measure q[0];\n'
            'c[1] = measure q[1];\n'
            'c[2] = measure q[2];\n'
            'c[3] = measure q[3];\n'
        ),
    },
}


class AzureQuantumService(BaseService):
    """Manages connection to Azure Quantum workspace and job lifecycle."""

    def __init__(self, quantum_config: AzureQuantumConfig, auth_config: AzureAuthConfig):
        super().__init__(quantum_config)
        self._auth = auth_config
        self._workspace = None
        self._jobs: list[dict] = []  # local cache of submitted jobs

    # ---- properties -------------------------------------------------------

    @property
    def is_configured(self) -> bool:
        cfg = self._config
        return bool(cfg.connection_string or cfg.resource_id)

    @property
    def available_targets(self) -> list[dict]:
        return [
            {
                "id": self._config.target_sc,
                "name": "Quantinuum H2-1SC (Syntax Checker)",
                "description": "Free syntax checker — validates circuit structure",
                "provider": "Quantinuum",
                "type": "syntax-checker",
            },
            {
                "id": self._config.target_em,
                "name": "Quantinuum H2-1E (Emulator)",
                "description": "Full state-vector emulator with realistic noise model",
                "provider": "Quantinuum",
                "type": "emulator",
            },
        ]

    @property
    def sample_circuits(self) -> dict:
        return SAMPLE_CIRCUITS

    # ---- lifecycle --------------------------------------------------------

    def initialize(self) -> None:
        """Connect to the Azure Quantum workspace using API key authentication."""
        if not self.is_configured:
            logger.warning("Azure Quantum not configured — running in demo mode")
            self._initialized = False
            return

        try:
            logger.info("[INIT] Step 1: Importing azure.quantum.Workspace...")
            from azure.quantum import Workspace
            logger.info("[INIT] Step 1: ✓ Import successful")

            cfg = self._config
            if cfg.connection_string:
                logger.info("[INIT] Step 2: Creating workspace from connection string...")
                logger.info("[INIT]   Connection string length: %d chars", len(cfg.connection_string))
                self._workspace = Workspace.from_connection_string(cfg.connection_string)
                logger.info("[INIT] Step 2: ✓ Workspace created from connection string")
            elif cfg.resource_id and cfg.api_key:
                logger.info("[INIT] Step 2: Creating workspace with API key + resource ID...")
                from azure.core.credentials import AzureKeyCredential
                self._workspace = Workspace(
                    resource_id=cfg.resource_id,
                    location=cfg.location,
                    credential=AzureKeyCredential(cfg.api_key),
                )
                logger.info("[INIT] Step 2: ✓ Workspace created with API key")
            elif cfg.resource_id:
                logger.info("[INIT] Step 2: Creating workspace with DefaultAzureCredential...")
                self._workspace = Workspace(
                    resource_id=cfg.resource_id,
                    location=cfg.location,
                )
                logger.info("[INIT] Step 2: ✓ Workspace created with default credential")
            else:
                logger.warning("[INIT] No valid Azure Quantum credentials — running in demo mode")
                self._initialized = False
                return

            self._initialized = True
            logger.info("[INIT] ✓ Azure Quantum workspace connected (API key auth)")
        except Exception:
            logger.error("[INIT] ✗ Failed to connect to Azure Quantum:\n%s", traceback.format_exc())
            self._initialized = False

    def health_check(self) -> dict:
        status = "connected" if self._initialized else "disconnected"
        return {
            **self.to_status_dict(),
            "status": status,
            "workspace": self._config.workspace_name or "N/A",
            "location": self._config.location,
            "targets": [t["id"] for t in self.available_targets],
        }

    # ---- job operations ---------------------------------------------------

    def submit_job(self, circuit_qasm: str, target_id: str, job_name: str = "",
                   shots: int = 100) -> dict:
        """Submit a quantum circuit to a target backend.

        Returns a dict with job metadata (or a demo-mode placeholder).
        """
        job_name = job_name or f"qdk-demo-{datetime.now(timezone.utc).strftime('%H%M%S')}"
        job_record = {
            "id": None,
            "name": job_name,
            "target": target_id,
            "shots": shots,
            "status": "Submitted",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "results": None,
        }

        if not self._initialized or self._workspace is None:
            # Demo mode — return a simulated response
            job_record["id"] = f"demo-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            job_record["status"] = "Demo Mode"
            job_record["results"] = self._simulate_result(circuit_qasm, shots)
            self._jobs.append(job_record)
            return job_record

        try:
            import time
            logger.info("[SUBMIT] Step 1: Importing Quantinuum target module...")
            from azure.quantum.target.quantinuum import Quantinuum
            logger.info("[SUBMIT] Step 1: ✓ Import successful (no qiskit/qsharp needed)")

            logger.info("[SUBMIT] Step 2: Creating Quantinuum target '%s'...", target_id)
            target = Quantinuum(workspace=self._workspace, name=target_id)
            logger.info("[SUBMIT] Step 2: ✓ Target created")

            # Retry up to 3 times for transient Azure internal errors
            max_retries = 3
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info("[SUBMIT] Step 3 (attempt %d/%d): Submitting QASM circuit (%d chars, shots=%d, name='%s')...",
                                attempt, max_retries, len(circuit_qasm), shots, job_name)
                    job = target.submit(
                        circuit=circuit_qasm,
                        name=job_name,
                        shots=shots,
                    )
                    logger.info("[SUBMIT] Step 3: ✓ Job submitted with ID: %s", job.id)

                    job_record["id"] = job.id
                    job_record["status"] = "Submitted"
                    self._jobs.append(job_record)
                    return job_record
                except Exception as retry_err:
                    last_error = retry_err
                    err_name = type(retry_err).__name__
                    if "InternalError" in str(retry_err) and attempt < max_retries:
                        wait = attempt * 3  # 3s, 6s
                        logger.warning("[SUBMIT]   Attempt %d failed (%s) — retrying in %ds...",
                                       attempt, err_name, wait)
                        time.sleep(wait)
                    else:
                        raise last_error

        except Exception as e:
            # Real submission failed — fall back to demo mode with simulated results
            logger.warning("[SUBMIT] ✗ Azure Quantum submission failed at runtime.")
            logger.warning("[SUBMIT]   Error type: %s", type(e).__name__)
            logger.warning("[SUBMIT]   Error message: %s", e)
            logger.warning("[SUBMIT]   Full traceback:\n%s", traceback.format_exc())
            logger.info("[SUBMIT] Falling back to demo mode with simulated results.")
            job_record["id"] = f"demo-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            job_record["status"] = "Demo Mode"
            job_record["results"] = self._simulate_result(circuit_qasm, shots)
            job_record["note"] = f"Simulated (live submission error: {type(e).__name__}: {e})"
            self._jobs.append(job_record)
            return job_record

    def get_job_status(self, job_id: str) -> dict:
        """Poll the status of a previously submitted job."""
        for job_rec in self._jobs:
            if job_rec["id"] == job_id:
                if job_rec["status"] == "Demo Mode":
                    return job_rec
                # Try to pull live status
                if self._workspace:
                    try:
                        from azure.quantum import Job
                        job = self._workspace.get_job(job_id)
                        job_rec["status"] = str(job.details.status)
                        if job.has_completed():
                            job_rec["results"] = job.get_results()
                    except Exception as e:
                        job_rec["error"] = str(e)
                return job_rec
        return {"error": f"Job {job_id} not found"}

    def list_jobs(self) -> list[dict]:
        """Return locally cached job history."""
        return list(reversed(self._jobs))

    # ---- helpers ----------------------------------------------------------

    @staticmethod
    def _simulate_result(circuit_qasm: str, shots: int) -> dict:
        """Generate plausible demo results by inspecting the circuit."""
        import random

        # Count qubits from the QASM
        n_qubits = 2
        for line in circuit_qasm.splitlines():
            if "qubit[" in line.lower():
                try:
                    n_qubits = int(line.split("[")[1].split("]")[0])
                except (IndexError, ValueError):
                    pass

        # Generate plausible measurement distribution
        if n_qubits <= 1:
            outcomes = {"0": shots // 2, "1": shots - shots // 2}
        elif "cx" in circuit_qasm or "cnot" in circuit_qasm.lower():
            # Entangled circuit — correlated outcomes
            zero_state = "0" * n_qubits
            one_state = "1" * n_qubits
            count_0 = shots // 2 + random.randint(-shots // 20, shots // 20)
            outcomes = {zero_state: count_0, one_state: shots - count_0}
        else:
            # Superposition — roughly uniform
            states = [format(i, f"0{n_qubits}b") for i in range(2 ** n_qubits)]
            remaining = shots
            outcomes = {}
            for i, s in enumerate(states):
                if i == len(states) - 1:
                    outcomes[s] = remaining
                else:
                    c = shots // len(states) + random.randint(-shots // 40, shots // 40)
                    c = max(0, min(remaining, c))
                    outcomes[s] = c
                    remaining -= c

        return {"counts": outcomes, "shots": shots, "n_qubits": n_qubits}
