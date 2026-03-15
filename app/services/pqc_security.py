"""Post-Quantum Cryptography Security Service.

Provides three capabilities:
1. Quantum Threat Dashboard  — vulnerability assessment of current crypto algorithms
2. PQC Algorithm Comparison  — benchmarks of NIST-standardised PQC algorithms
3. Crypto Readiness Scanner  — analyse a set of algorithms for quantum readiness
"""

from __future__ import annotations

import hashlib
import logging
import random
import time
from typing import Any

from app.services.base import BaseService

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
#  Reference data: current cryptographic algorithms vs quantum threat
# ---------------------------------------------------------------------------
CRYPTO_THREAT_MATRIX: list[dict[str, Any]] = [
    {
        "algorithm": "RSA-2048",
        "category": "Asymmetric",
        "use_case": "Encryption / Signatures",
        "classical_security": 112,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "Migrate to ML-KEM / ML-DSA",
    },
    {
        "algorithm": "RSA-4096",
        "category": "Asymmetric",
        "use_case": "Encryption / Signatures",
        "classical_security": 140,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2033-2038",
        "recommendation": "Migrate to ML-KEM / ML-DSA",
    },
    {
        "algorithm": "ECDSA P-256",
        "category": "Asymmetric",
        "use_case": "Digital Signatures",
        "classical_security": 128,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "Migrate to ML-DSA / SLH-DSA",
    },
    {
        "algorithm": "ECDH P-256",
        "category": "Asymmetric",
        "use_case": "Key Exchange",
        "classical_security": 128,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "Migrate to ML-KEM",
    },
    {
        "algorithm": "AES-128",
        "category": "Symmetric",
        "use_case": "Encryption",
        "classical_security": 128,
        "quantum_security": 64,
        "threat_level": "warning",
        "vulnerable_to": "Grover's Algorithm (√ speedup)",
        "timeline": "Post-2040",
        "recommendation": "Upgrade to AES-256",
    },
    {
        "algorithm": "AES-256",
        "category": "Symmetric",
        "use_case": "Encryption",
        "classical_security": 256,
        "quantum_security": 128,
        "threat_level": "safe",
        "vulnerable_to": "Grover's (still 128-bit quantum)",
        "timeline": "Safe for foreseeable future",
        "recommendation": "No action needed",
    },
    {
        "algorithm": "SHA-256",
        "category": "Hash",
        "use_case": "Integrity / Signatures",
        "classical_security": 256,
        "quantum_security": 128,
        "threat_level": "safe",
        "vulnerable_to": "Grover's (still 128-bit quantum)",
        "timeline": "Safe for foreseeable future",
        "recommendation": "No action needed",
    },
    {
        "algorithm": "SHA-3",
        "category": "Hash",
        "use_case": "Integrity / Signatures",
        "classical_security": 256,
        "quantum_security": 128,
        "threat_level": "safe",
        "vulnerable_to": "Grover's (still 128-bit quantum)",
        "timeline": "Safe for foreseeable future",
        "recommendation": "No action needed",
    },
    {
        "algorithm": "3DES",
        "category": "Symmetric",
        "use_case": "Legacy Encryption",
        "classical_security": 112,
        "quantum_security": 56,
        "threat_level": "critical",
        "vulnerable_to": "Grover's + classical weakness",
        "timeline": "Already vulnerable",
        "recommendation": "Deprecate immediately",
    },
    {
        "algorithm": "Diffie-Hellman 2048",
        "category": "Asymmetric",
        "use_case": "Key Exchange",
        "classical_security": 112,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "Migrate to ML-KEM",
    },
    # ---- Microsoft SymCrypt algorithms ----
    {
        "algorithm": "SymCrypt AES-GCM-256",
        "category": "Symmetric",
        "use_case": "Authenticated Encryption",
        "classical_security": 256,
        "quantum_security": 128,
        "threat_level": "safe",
        "vulnerable_to": "Grover's (still 128-bit quantum)",
        "timeline": "Safe for foreseeable future",
        "recommendation": "No action needed — SymCrypt optimized",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt ECDSA P-384",
        "category": "Asymmetric",
        "use_case": "Digital Signatures (TLS)",
        "classical_security": 192,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "SymCrypt ML-DSA migration path available",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt RSA-OAEP 2048",
        "category": "Asymmetric",
        "use_case": "Key Transport (TLS/CMS)",
        "classical_security": 112,
        "quantum_security": 0,
        "threat_level": "critical",
        "vulnerable_to": "Shor's Algorithm",
        "timeline": "2030-2035",
        "recommendation": "Migrate to SymCrypt ML-KEM",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt HMAC-SHA-256",
        "category": "MAC",
        "use_case": "Message Authentication",
        "classical_security": 256,
        "quantum_security": 128,
        "threat_level": "safe",
        "vulnerable_to": "Grover's (still 128-bit quantum)",
        "timeline": "Safe for foreseeable future",
        "recommendation": "No action needed — SymCrypt optimized",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt ML-KEM-768",
        "category": "Post-Quantum",
        "use_case": "Key Encapsulation (PQC)",
        "classical_security": 192,
        "quantum_security": 192,
        "threat_level": "safe",
        "vulnerable_to": "None (lattice-based, quantum-resistant)",
        "timeline": "N/A — quantum-safe by design",
        "recommendation": "Production-ready in SymCrypt / Windows",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt ML-DSA-65",
        "category": "Post-Quantum",
        "use_case": "Digital Signatures (PQC)",
        "classical_security": 192,
        "quantum_security": 192,
        "threat_level": "safe",
        "vulnerable_to": "None (lattice-based, quantum-resistant)",
        "timeline": "N/A — quantum-safe by design",
        "recommendation": "Production-ready in SymCrypt / Windows",
        "engine": "SymCrypt",
    },
    {
        "algorithm": "SymCrypt XMSS",
        "category": "Post-Quantum",
        "use_case": "Stateful Hash-based Signatures",
        "classical_security": 256,
        "quantum_security": 256,
        "threat_level": "safe",
        "vulnerable_to": "None (hash-based, quantum-resistant)",
        "timeline": "N/A — quantum-safe by design",
        "recommendation": "Use for firmware/code signing via SymCrypt",
        "engine": "SymCrypt",
    },
]

# ---------------------------------------------------------------------------
#  PQC Algorithm reference data  (NIST FIPS 203/204/205 — Aug 2024)
# ---------------------------------------------------------------------------
PQC_ALGORITHMS: list[dict[str, Any]] = [
    {
        "id": "ml-kem-512",
        "name": "ML-KEM-512",
        "standard": "FIPS 203",
        "family": "CRYSTALS-Kyber",
        "type": "Key Encapsulation",
        "security_level": 1,
        "nist_category": "Category 1 (128-bit)",
        "public_key_bytes": 800,
        "secret_key_bytes": 1632,
        "ciphertext_bytes": 768,
        "keygen_us": 35,
        "encaps_us": 42,
        "decaps_us": 45,
    },
    {
        "id": "ml-kem-768",
        "name": "ML-KEM-768",
        "standard": "FIPS 203",
        "family": "CRYSTALS-Kyber",
        "type": "Key Encapsulation",
        "security_level": 3,
        "nist_category": "Category 3 (192-bit)",
        "public_key_bytes": 1184,
        "secret_key_bytes": 2400,
        "ciphertext_bytes": 1088,
        "keygen_us": 55,
        "encaps_us": 65,
        "decaps_us": 68,
    },
    {
        "id": "ml-kem-1024",
        "name": "ML-KEM-1024",
        "standard": "FIPS 203",
        "family": "CRYSTALS-Kyber",
        "type": "Key Encapsulation",
        "security_level": 5,
        "nist_category": "Category 5 (256-bit)",
        "public_key_bytes": 1568,
        "secret_key_bytes": 3168,
        "ciphertext_bytes": 1568,
        "keygen_us": 82,
        "encaps_us": 93,
        "decaps_us": 95,
    },
    {
        "id": "ml-dsa-44",
        "name": "ML-DSA-44",
        "standard": "FIPS 204",
        "family": "CRYSTALS-Dilithium",
        "type": "Digital Signature",
        "security_level": 2,
        "nist_category": "Category 2 (128-bit)",
        "public_key_bytes": 1312,
        "secret_key_bytes": 2560,
        "signature_bytes": 2420,
        "keygen_us": 68,
        "sign_us": 220,
        "verify_us": 72,
    },
    {
        "id": "ml-dsa-65",
        "name": "ML-DSA-65",
        "standard": "FIPS 204",
        "family": "CRYSTALS-Dilithium",
        "type": "Digital Signature",
        "security_level": 3,
        "nist_category": "Category 3 (192-bit)",
        "public_key_bytes": 1952,
        "secret_key_bytes": 4032,
        "signature_bytes": 3309,
        "keygen_us": 110,
        "sign_us": 340,
        "verify_us": 115,
    },
    {
        "id": "ml-dsa-87",
        "name": "ML-DSA-87",
        "standard": "FIPS 204",
        "family": "CRYSTALS-Dilithium",
        "type": "Digital Signature",
        "security_level": 5,
        "nist_category": "Category 5 (256-bit)",
        "public_key_bytes": 2592,
        "secret_key_bytes": 4896,
        "signature_bytes": 4627,
        "keygen_us": 170,
        "sign_us": 510,
        "verify_us": 175,
    },
    {
        "id": "slh-dsa-128s",
        "name": "SLH-DSA-128s",
        "standard": "FIPS 205",
        "family": "SPHINCS+",
        "type": "Digital Signature",
        "security_level": 1,
        "nist_category": "Category 1 (128-bit)",
        "public_key_bytes": 32,
        "secret_key_bytes": 64,
        "signature_bytes": 7856,
        "keygen_us": 3200,
        "sign_us": 72000,
        "verify_us": 3800,
    },
    {
        "id": "slh-dsa-256f",
        "name": "SLH-DSA-256f",
        "standard": "FIPS 205",
        "family": "SPHINCS+",
        "type": "Digital Signature",
        "security_level": 5,
        "nist_category": "Category 5 (256-bit)",
        "public_key_bytes": 64,
        "secret_key_bytes": 128,
        "signature_bytes": 49856,
        "keygen_us": 850,
        "sign_us": 18000,
        "verify_us": 1200,
    },
]


# ---------------------------------------------------------------------------
#  PQC Security Service
# ---------------------------------------------------------------------------

class PQCSecurityService(BaseService):
    """Post-Quantum Cryptography analysis and demonstration service.

    Works entirely offline — no external API calls required.
    Uses NIST-published reference data and simulated benchmarks.
    """

    def __init__(self, config: Any = None):
        super().__init__(config)
        self._threat_matrix = CRYPTO_THREAT_MATRIX
        self._pqc_algorithms = PQC_ALGORITHMS
        self._hndl_categories = self.HNDL_DATA_CATEGORIES

    @property
    def name(self) -> str:
        return "PQC Security"

    @property
    def is_configured(self) -> bool:
        return True  # No external dependencies

    def initialize(self) -> None:
        self._initialized = True
        log.info("PQC Security Service initialized (offline mode)")

    def health_check(self) -> dict:
        return {
            "service": self.name,
            "status": "active",
            "mode": "simulation",
            "algorithms_tracked": len(self._pqc_algorithms),
            "threats_monitored": len(self._threat_matrix),
        }

    # ----- Capability 1: Quantum Threat Dashboard --------------------------

    def get_threat_matrix(self) -> dict:
        """Return the full threat matrix with summary statistics."""
        critical = sum(1 for a in self._threat_matrix if a["threat_level"] == "critical")
        warning = sum(1 for a in self._threat_matrix if a["threat_level"] == "warning")
        safe = sum(1 for a in self._threat_matrix if a["threat_level"] == "safe")

        return {
            "algorithms": self._threat_matrix,
            "summary": {
                "total": len(self._threat_matrix),
                "critical": critical,
                "warning": warning,
                "safe": safe,
                "risk_score": round((critical * 3 + warning) / (len(self._threat_matrix) * 3) * 100),
            },
        }

    # ----- Capability 2: PQC Algorithm Comparison --------------------------

    def get_pqc_algorithms(self) -> dict:
        """Return PQC algorithm data for comparison charts."""
        return {
            "algorithms": self._pqc_algorithms,
            "families": list({a["family"] for a in self._pqc_algorithms}),
            "standards": list({a["standard"] for a in self._pqc_algorithms}),
        }

    def run_pqc_benchmark(self, algorithm_ids: list[str] | None = None) -> dict:
        """Simulate a PQC benchmark run with realistic performance data.

        Adds small random jitter to reference values to simulate real execution.
        """
        selected = self._pqc_algorithms
        if algorithm_ids:
            selected = [a for a in self._pqc_algorithms if a["id"] in algorithm_ids]

        results = []
        for algo in selected:
            jitter = lambda v: round(v * random.uniform(0.92, 1.08), 1)  # noqa: E731
            entry = {
                "id": algo["id"],
                "name": algo["name"],
                "family": algo["family"],
                "type": algo["type"],
                "security_level": algo["security_level"],
                "public_key_bytes": algo["public_key_bytes"],
                "secret_key_bytes": algo["secret_key_bytes"],
            }
            # KEM algorithms have encaps/decaps
            if "encaps_us" in algo:
                entry.update({
                    "ciphertext_bytes": algo["ciphertext_bytes"],
                    "keygen_us": jitter(algo["keygen_us"]),
                    "encaps_us": jitter(algo["encaps_us"]),
                    "decaps_us": jitter(algo["decaps_us"]),
                })
            # Signature algorithms have sign/verify
            if "sign_us" in algo:
                entry.update({
                    "signature_bytes": algo["signature_bytes"],
                    "keygen_us": jitter(algo["keygen_us"]),
                    "sign_us": jitter(algo["sign_us"]),
                    "verify_us": jitter(algo["verify_us"]),
                })
            results.append(entry)

        return {
            "benchmark_id": hashlib.md5(str(time.time()).encode()).hexdigest()[:12],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "results": results,
        }

    # ----- Capability 3: Crypto Readiness Scanner --------------------------

    _KNOWN_ALGORITHMS = {
        # Map algorithm names/aliases → threat level and recommendation
        "rsa": ("RSA-2048", "critical"),
        "rsa-2048": ("RSA-2048", "critical"),
        "rsa-4096": ("RSA-4096", "critical"),
        "ecdsa": ("ECDSA P-256", "critical"),
        "ecdsa-p256": ("ECDSA P-256", "critical"),
        "ecdh": ("ECDH P-256", "critical"),
        "ecdh-p256": ("ECDH P-256", "critical"),
        "dh": ("Diffie-Hellman 2048", "critical"),
        "diffie-hellman": ("Diffie-Hellman 2048", "critical"),
        "3des": ("3DES", "critical"),
        "des3": ("3DES", "critical"),
        "triple-des": ("3DES", "critical"),
        "aes-128": ("AES-128", "warning"),
        "aes128": ("AES-128", "warning"),
        "aes-256": ("AES-256", "safe"),
        "aes256": ("AES-256", "safe"),
        "sha-256": ("SHA-256", "safe"),
        "sha256": ("SHA-256", "safe"),
        "sha-3": ("SHA-3", "safe"),
        "sha3": ("SHA-3", "safe"),
        # PQC algorithms — already quantum-safe
        "ml-kem": ("ML-KEM", "quantum-safe"),
        "kyber": ("ML-KEM (Kyber)", "quantum-safe"),
        "ml-dsa": ("ML-DSA", "quantum-safe"),
        "dilithium": ("ML-DSA (Dilithium)", "quantum-safe"),
        "slh-dsa": ("SLH-DSA", "quantum-safe"),
        "sphincs": ("SLH-DSA (SPHINCS+)", "quantum-safe"),
        "falcon": ("FALCON", "quantum-safe"),
        "xmss": ("XMSS", "quantum-safe"),
        "symcrypt aes-gcm": ("SymCrypt AES-GCM-256", "safe"),
        # SymCrypt entries
        "symcrypt": ("SymCrypt (Microsoft)", "quantum-safe"),
        "symcrypt aes-gcm-256": ("SymCrypt AES-GCM-256", "safe"),
        "symcrypt ecdsa": ("SymCrypt ECDSA P-384", "critical"),
        "symcrypt rsa-oaep": ("SymCrypt RSA-OAEP 2048", "critical"),
        "symcrypt hmac-sha-256": ("SymCrypt HMAC-SHA-256", "safe"),
        "symcrypt ml-kem": ("SymCrypt ML-KEM-768", "quantum-safe"),
        "symcrypt ml-dsa": ("SymCrypt ML-DSA-65", "quantum-safe"),
        "symcrypt xmss": ("SymCrypt XMSS", "quantum-safe"),
    }

    def scan_readiness(self, algorithms: list[str]) -> dict:
        """Scan a list of algorithm names and return a readiness report.

        Args:
            algorithms: List of algorithm names (e.g., ["RSA-2048", "AES-256", "SHA-256"])

        Returns:
            Readiness report with per-algorithm analysis and overall score.
        """
        findings = []
        for algo_input in algorithms:
            key = algo_input.strip().lower()
            if key in self._KNOWN_ALGORITHMS:
                name, level = self._KNOWN_ALGORITHMS[key]
                # Find full data from threat matrix
                matrix_entry = next(
                    (a for a in self._threat_matrix if a["algorithm"].lower() == name.lower()),
                    None,
                )
                if matrix_entry:
                    findings.append({
                        "input": algo_input,
                        "algorithm": matrix_entry["algorithm"],
                        "category": matrix_entry["category"],
                        "threat_level": matrix_entry["threat_level"],
                        "quantum_security_bits": matrix_entry["quantum_security"],
                        "vulnerable_to": matrix_entry["vulnerable_to"],
                        "recommendation": matrix_entry["recommendation"],
                        "migration_timeline": matrix_entry["timeline"],
                    })
                else:
                    findings.append({
                        "input": algo_input,
                        "algorithm": name,
                        "category": "Post-Quantum" if level == "quantum-safe" else "Unknown",
                        "threat_level": level,
                        "quantum_security_bits": 128 if level == "quantum-safe" else None,
                        "vulnerable_to": "None (quantum-resistant)" if level == "quantum-safe" else "Unknown",
                        "recommendation": "Already quantum-safe" if level == "quantum-safe" else "Research needed",
                        "migration_timeline": "N/A",
                    })
            else:
                findings.append({
                    "input": algo_input,
                    "algorithm": algo_input,
                    "category": "Unknown",
                    "threat_level": "unknown",
                    "quantum_security_bits": None,
                    "vulnerable_to": "Unknown — not in database",
                    "recommendation": "Manual review required",
                    "migration_timeline": "Unknown",
                })

        # Calculate readiness score
        total = len(findings)
        if total == 0:
            score = 0
        else:
            points = 0
            for f in findings:
                if f["threat_level"] == "quantum-safe":
                    points += 100
                elif f["threat_level"] == "safe":
                    points += 80
                elif f["threat_level"] == "warning":
                    points += 40
                elif f["threat_level"] == "critical":
                    points += 0
                else:
                    points += 20
            score = round(points / total)

        # Grade
        if score >= 80:
            grade = "A"
        elif score >= 60:
            grade = "B"
        elif score >= 40:
            grade = "C"
        elif score >= 20:
            grade = "D"
        else:
            grade = "F"

        critical_count = sum(1 for f in findings if f["threat_level"] == "critical")
        safe_count = sum(1 for f in findings if f["threat_level"] in ("safe", "quantum-safe"))

        return {
            "findings": findings,
            "summary": {
                "total_scanned": total,
                "critical": critical_count,
                "safe": safe_count,
                "readiness_score": score,
                "grade": grade,
                "verdict": (
                    "Quantum-ready!" if score >= 80
                    else "Mostly prepared — address warnings" if score >= 60
                    else "Significant migration needed" if score >= 40
                    else "Critical — immediate action required"
                ),
            },
        }

    # ----- Capability 4: Quantum Threat Timeline ---------------------------

    def get_threat_timeline(self) -> dict:
        """Return quantum computing threat timeline milestones."""
        return {
            "milestones": [
                {"year": 2019, "event": "Google Sycamore claims quantum supremacy (53 qubits)", "category": "hardware", "threat_impact": 0},
                {"year": 2021, "event": "IBM Eagle processor — 127 qubits", "category": "hardware", "threat_impact": 5},
                {"year": 2022, "event": "NIST selects first PQC standards (CRYSTALS, SPHINCS+)", "category": "standards", "threat_impact": 0},
                {"year": 2023, "event": "IBM Condor — 1,121 qubits; Atom Computing 1,225 qubits", "category": "hardware", "threat_impact": 10},
                {"year": 2024, "event": "NIST publishes FIPS 203/204/205; Microsoft SymCrypt adds ML-KEM", "category": "standards", "threat_impact": 0},
                {"year": 2025, "event": "Microsoft Majorana 1 — topological qubit breakthrough", "category": "hardware", "threat_impact": 15},
                {"year": 2026, "event": "Azure Quantum adds hybrid PQC/classical key exchange", "category": "deployment", "threat_impact": 0},
                {"year": 2028, "event": "Projected: 10K+ logical qubits (error-corrected)", "category": "projection", "threat_impact": 30},
                {"year": 2030, "event": "Projected: RSA-2048 becomes breakable window opens", "category": "projection", "threat_impact": 60},
                {"year": 2033, "event": "Projected: Cryptographically-relevant quantum computer (CRQC)", "category": "projection", "threat_impact": 85},
                {"year": 2035, "event": "Projected: All classical asymmetric crypto at risk", "category": "projection", "threat_impact": 100},
            ],
            "qubit_progression": [
                {"year": 2019, "physical_qubits": 53,    "logical_qubits": 0},
                {"year": 2020, "physical_qubits": 65,    "logical_qubits": 0},
                {"year": 2021, "physical_qubits": 127,   "logical_qubits": 0},
                {"year": 2022, "physical_qubits": 433,   "logical_qubits": 0},
                {"year": 2023, "physical_qubits": 1221,  "logical_qubits": 0},
                {"year": 2024, "physical_qubits": 1500,  "logical_qubits": 10},
                {"year": 2025, "physical_qubits": 4000,  "logical_qubits": 50},
                {"year": 2026, "physical_qubits": 10000, "logical_qubits": 200},
                {"year": 2028, "physical_qubits": 50000, "logical_qubits": 2000},
                {"year": 2030, "physical_qubits": 200000,"logical_qubits": 10000},
                {"year": 2033, "physical_qubits": 1000000,"logical_qubits": 50000},
            ],
        }

    # ----- Capability 5: Security Posture Radar ----------------------------

    def get_security_posture(self) -> dict:
        """Return security posture assessment across dimensions."""
        return {
            "dimensions": [
                {"name": "Key Exchange", "current_score": 25, "target_score": 95, "status": "critical",
                 "detail": "RSA/ECDH still primary — migrate to ML-KEM"},
                {"name": "Digital Signatures", "current_score": 30, "target_score": 95, "status": "critical",
                 "detail": "ECDSA/RSA dominant — adopt ML-DSA / SLH-DSA"},
                {"name": "Symmetric Crypto", "current_score": 85, "target_score": 95, "status": "good",
                 "detail": "AES-256 via SymCrypt — quantum-resistant"},
                {"name": "Hash Functions", "current_score": 90, "target_score": 95, "status": "good",
                 "detail": "SHA-256/SHA-3 — safe against Grover's"},
                {"name": "TLS/Protocols", "current_score": 40, "target_score": 90, "status": "warning",
                 "detail": "Hybrid PQC key exchange adoption in progress"},
                {"name": "Certificate Mgmt", "current_score": 20, "target_score": 90, "status": "critical",
                 "detail": "PKI infrastructure needs PQC certificate support"},
                {"name": "Data-at-Rest", "current_score": 80, "target_score": 95, "status": "good",
                 "detail": "AES-256 encryption — SymCrypt optimized"},
                {"name": "Code Signing", "current_score": 35, "target_score": 90, "status": "warning",
                 "detail": "Transition to hash-based signatures (XMSS/LMS)"},
            ],
            "overall_readiness": 50,
        }

    # ----- Capability 6: Harvest Now, Decrypt Later (HNDL) Simulation ------

    HNDL_DATA_CATEGORIES = [
        {
            "id": "classified_gov",
            "name": "Classified Government Data",
            "sensitivity": "Top Secret",
            "required_secrecy_years": 50,
            "data_volume_tb": 2.5,
            "current_encryption": "RSA-2048 + AES-256",
            "icon": "shield",
        },
        {
            "id": "healthcare_phi",
            "name": "Healthcare PHI Records",
            "sensitivity": "High",
            "required_secrecy_years": 30,
            "data_volume_tb": 8.2,
            "current_encryption": "RSA-2048 + AES-128",
            "icon": "heart-pulse",
        },
        {
            "id": "financial_pii",
            "name": "Financial / PII Data",
            "sensitivity": "High",
            "required_secrecy_years": 25,
            "data_volume_tb": 15.7,
            "current_encryption": "ECDSA P-256 + AES-256",
            "icon": "landmark",
        },
        {
            "id": "ip_trade_secrets",
            "name": "IP & Trade Secrets",
            "sensitivity": "Critical",
            "required_secrecy_years": 40,
            "data_volume_tb": 3.1,
            "current_encryption": "RSA-4096 + AES-256",
            "icon": "lightbulb",
        },
        {
            "id": "corporate_email",
            "name": "Corporate Communications",
            "sensitivity": "Medium",
            "required_secrecy_years": 10,
            "data_volume_tb": 45.0,
            "current_encryption": "ECDH P-256 + AES-128",
            "icon": "mail",
        },
        {
            "id": "iot_scada",
            "name": "IoT / SCADA Telemetry",
            "sensitivity": "Medium-High",
            "required_secrecy_years": 20,
            "data_volume_tb": 120.0,
            "current_encryption": "RSA-2048 + AES-128",
            "icon": "cpu",
        },
    ]

    def simulate_hndl(self, quantum_year: int = 2033, harvest_start_year: int = 2024) -> dict:
        """Simulate a Harvest Now, Decrypt Later (HNDL) threat scenario.

        Args:
            quantum_year: Year when a CRQC (Cryptographically Relevant Quantum Computer) arrives.
            harvest_start_year: Year adversaries began harvesting encrypted traffic.

        Returns:
            Risk assessment per data category with timelines.
        """
        current_year = 2026

        results = []
        total_risk = 0
        total_exposed_tb = 0

        for cat in self.HNDL_DATA_CATEGORIES:
            secrecy_end = current_year + cat["required_secrecy_years"]
            harvest_duration = current_year - harvest_start_year
            years_until_decrypt = max(0, quantum_year - current_year)
            years_exposed_after_decrypt = max(0, secrecy_end - quantum_year)

            # Determine if asymmetric key exchange is breakable
            enc = cat["current_encryption"]
            asymmetric_broken = any(k in enc for k in ["RSA", "ECDSA", "ECDH", "Diffie"])
            symmetric_weak = "AES-128" in enc  # Grover reduces to 64-bit

            # Risk score (0-100)
            if not asymmetric_broken:
                risk = 10  # symmetric-only is lower risk
            elif years_exposed_after_decrypt <= 0:
                risk = random.randint(15, 30)  # data expires before CRQC
            else:
                base_risk = min(100, (years_exposed_after_decrypt / cat["required_secrecy_years"]) * 100)
                harvest_factor = min(1.3, 1 + harvest_duration * 0.05)
                volume_factor = min(1.2, 1 + cat["data_volume_tb"] / 100)
                risk = min(100, int(base_risk * harvest_factor * volume_factor))
                if symmetric_weak:
                    risk = min(100, risk + 10)

            status = "critical" if risk >= 70 else "warning" if risk >= 40 else "safe"

            exposed_tb = round(cat["data_volume_tb"] * harvest_duration * random.uniform(0.1, 0.3), 1)
            total_exposed_tb += exposed_tb
            total_risk += risk

            results.append({
                "id": cat["id"],
                "name": cat["name"],
                "sensitivity": cat["sensitivity"],
                "icon": cat["icon"],
                "current_encryption": cat["current_encryption"],
                "required_secrecy_years": cat["required_secrecy_years"],
                "secrecy_expires": secrecy_end,
                "harvest_duration_years": harvest_duration,
                "estimated_harvested_tb": exposed_tb,
                "years_until_decrypt": years_until_decrypt,
                "years_exposed_after_decrypt": years_exposed_after_decrypt,
                "risk_score": risk,
                "status": status,
                "asymmetric_vulnerable": asymmetric_broken,
                "mitigation": (
                    "URGENT: Migrate to PQC key exchange immediately"
                    if risk >= 70 else
                    "HIGH: Plan PQC migration within 12 months"
                    if risk >= 40 else
                    "MONITOR: Continue current approach, plan for PQC"
                ),
            })

        n_cats = len(results)
        avg_risk = round(total_risk / n_cats) if n_cats else 0

        return {
            "scenario": {
                "quantum_year": quantum_year,
                "harvest_start_year": harvest_start_year,
                "current_year": current_year,
                "years_of_harvesting": current_year - harvest_start_year,
                "years_until_crqc": max(0, quantum_year - current_year),
            },
            "categories": results,
            "summary": {
                "total_categories": n_cats,
                "critical": sum(1 for r in results if r["status"] == "critical"),
                "warning": sum(1 for r in results if r["status"] == "warning"),
                "safe": sum(1 for r in results if r["status"] == "safe"),
                "avg_risk_score": avg_risk,
                "total_estimated_harvested_tb": round(total_exposed_tb, 1),
                "verdict": (
                    "CRITICAL — Immediate PQC migration required across all sensitive data"
                    if avg_risk >= 60 else
                    "HIGH RISK — Prioritize PQC migration for critical data categories"
                    if avg_risk >= 40 else
                    "MODERATE — Begin PQC planning; some categories at risk"
                    if avg_risk >= 25 else
                    "LOW — Current posture adequate, maintain monitoring"
                ),
            },
        }