"""Mock Chemistry Lab service — realistic quantum chemistry simulation data."""

from __future__ import annotations

import logging
import math
import random
import time
import uuid
from typing import Any

from app.services.base import BaseService


class ChemistryService(BaseService):
    """Provides mock quantum chemistry workflows for demonstration purposes."""

    SERVICE_NAME = "Chemistry Lab"

    def __init__(self, config: Any = None):
        super().__init__(config)
        self._logger = logging.getLogger(__name__)

    @property
    def name(self) -> str:
        return "Chemistry Lab"

    @property
    def is_configured(self) -> bool:
        return True  # No external dependencies

    # ── Molecule library ────────────────────────────────────────────────
    MOLECULES: dict[str, dict[str, Any]] = {
        "water": {
            "name": "Water",
            "formula": "H₂O",
            "atoms": [
                {"element": "O", "x": 0.0000, "y": 0.0000, "z": 0.1173},
                {"element": "H", "x": 0.0000, "y": 0.7572, "z": -0.4692},
                {"element": "H", "x": 0.0000, "y": -0.7572, "z": -0.4692},
            ],
            "bonds": [[0, 1], [0, 2]],
            "n_electrons": 10,
            "n_orbitals": 7,
            "basis_set": "STO-3G",
            "symmetry": "C₂ᵥ",
            "charge": 0,
            "multiplicity": 1,
            "description": "Simple triatomic molecule, fundamental benchmark for quantum chemistry.",
        },
        "hydrogen": {
            "name": "Hydrogen",
            "formula": "H₂",
            "atoms": [
                {"element": "H", "x": 0.0, "y": 0.0, "z": -0.375},
                {"element": "H", "x": 0.0, "y": 0.0, "z": 0.375},
            ],
            "bonds": [[0, 1]],
            "n_electrons": 2,
            "n_orbitals": 2,
            "basis_set": "STO-3G",
            "symmetry": "D∞h",
            "charge": 0,
            "multiplicity": 1,
            "description": "Simplest molecule — the 'hydrogen atom' of quantum chemistry.",
        },
        "lithium_hydride": {
            "name": "Lithium Hydride",
            "formula": "LiH",
            "atoms": [
                {"element": "Li", "x": 0.0, "y": 0.0, "z": -0.798},
                {"element": "H", "x": 0.0, "y": 0.0, "z": 0.798},
            ],
            "bonds": [[0, 1]],
            "n_electrons": 4,
            "n_orbitals": 6,
            "basis_set": "STO-3G",
            "symmetry": "C∞v",
            "charge": 0,
            "multiplicity": 1,
            "description": "Polar diatomic — tests ionic character and correlation effects.",
        },
        "nitrogen": {
            "name": "Nitrogen (N₂)",
            "formula": "N₂",
            "atoms": [
                {"element": "N", "x": 0.0, "y": 0.0, "z": -0.549},
                {"element": "N", "x": 0.0, "y": 0.0, "z": 0.549},
            ],
            "bonds": [[0, 1]],
            "n_electrons": 14,
            "n_orbitals": 10,
            "basis_set": "cc-pVDZ",
            "symmetry": "D∞h",
            "charge": 0,
            "multiplicity": 1,
            "description": "Triple bond benchmark — strong static correlation at stretched geometries.",
        },
        "benzene": {
            "name": "Benzene",
            "formula": "C₆H₆",
            "atoms": [
                {"element": "C", "x":  1.3970, "y":  0.0000, "z": 0.0},
                {"element": "C", "x":  0.6985, "y":  1.2098, "z": 0.0},
                {"element": "C", "x": -0.6985, "y":  1.2098, "z": 0.0},
                {"element": "C", "x": -1.3970, "y":  0.0000, "z": 0.0},
                {"element": "C", "x": -0.6985, "y": -1.2098, "z": 0.0},
                {"element": "C", "x":  0.6985, "y": -1.2098, "z": 0.0},
                {"element": "H", "x":  2.4810, "y":  0.0000, "z": 0.0},
                {"element": "H", "x":  1.2405, "y":  2.1486, "z": 0.0},
                {"element": "H", "x": -1.2405, "y":  2.1486, "z": 0.0},
                {"element": "H", "x": -2.4810, "y":  0.0000, "z": 0.0},
                {"element": "H", "x": -1.2405, "y": -2.1486, "z": 0.0},
                {"element": "H", "x":  1.2405, "y": -2.1486, "z": 0.0},
            ],
            "bonds": [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[0,6],[1,7],[2,8],[3,9],[4,10],[5,11]],
            "n_electrons": 42,
            "n_orbitals": 36,
            "basis_set": "cc-pVDZ",
            "symmetry": "D₆h",
            "charge": 0,
            "multiplicity": 1,
            "description": "Prototypical aromatic — 6 π-electrons, strong delocalization.",
        },
        "caffeine": {
            "name": "Caffeine",
            "formula": "C₈H₁₀N₄O₂",
            "atoms": [
                # Purine ring system (imidazole fused with pyrimidine)
                {"element": "N", "x":  1.2320, "y":  1.1510, "z":  0.0000},  # N1
                {"element": "C", "x":  1.2320, "y": -0.2270, "z":  0.0000},  # C2
                {"element": "N", "x":  0.0000, "y": -0.8500, "z":  0.0000},  # N3
                {"element": "C", "x": -1.1810, "y": -0.0360, "z":  0.0000},  # C4
                {"element": "C", "x": -1.0660, "y":  1.3480, "z":  0.0000},  # C5
                {"element": "C", "x":  0.1860, "y":  1.9100, "z":  0.0000},  # C6
                # Imidazole ring
                {"element": "N", "x": -2.4310, "y":  0.5440, "z":  0.0000},  # N7
                {"element": "C", "x": -2.2500, "y":  1.8520, "z":  0.0000},  # C8
                {"element": "N", "x": -3.6660, "y":  0.0080, "z":  0.0000},  # N9 (methyl)
                # Carbonyl oxygens
                {"element": "O", "x":  2.2920, "y": -0.8440, "z":  0.0000},  # O (on C2)
                {"element": "O", "x":  0.2370, "y":  3.1350, "z":  0.0000},  # O (on C6)
                # Methyl groups: N1-CH3
                {"element": "C", "x":  2.4900, "y":  1.8680, "z":  0.0000},  # C-Me on N1
                {"element": "H", "x":  2.4900, "y":  2.5390, "z":  0.8900},
                {"element": "H", "x":  2.4900, "y":  2.5390, "z": -0.8900},
                {"element": "H", "x":  3.3890, "y":  1.2470, "z":  0.0000},
                # Methyl groups: N3-CH3
                {"element": "C", "x":  0.0000, "y": -2.3000, "z":  0.0000},  # C-Me on N3
                {"element": "H", "x":  0.0000, "y": -2.6620, "z":  1.0280},
                {"element": "H", "x":  0.8900, "y": -2.6620, "z": -0.5140},
                {"element": "H", "x": -0.8900, "y": -2.6620, "z": -0.5140},
                # Methyl groups: N9-CH3
                {"element": "C", "x": -3.8500, "y": -1.4400, "z":  0.0000},  # C-Me on N9
                {"element": "H", "x": -3.8500, "y": -1.8030, "z":  1.0280},
                {"element": "H", "x": -4.7400, "y": -1.8030, "z": -0.5140},
                {"element": "H", "x": -2.9600, "y": -1.8030, "z": -0.5140},
                # C8-H
                {"element": "H", "x": -3.0400, "y":  2.5960, "z":  0.0000},
            ],
            "bonds": [
                # Pyrimidine ring: N1-C2-N3-C4-C5-C6-N1
                [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0],
                # Imidazole ring: C4-N7-C8-N9 (fused at C4-C5)
                [3, 6], [6, 7], [7, 4],
                [6, 8],  # N7-N9 bridge via C4
                # Carbonyl bonds
                [1, 9],   # C2=O
                [5, 10],  # C6=O
                # Methyl on N1
                [0, 11], [11, 12], [11, 13], [11, 14],
                # Methyl on N3
                [2, 15], [15, 16], [15, 17], [15, 18],
                # Methyl on N9 (actually N7 in xanthine numbering)
                [8, 19], [19, 20], [19, 21], [19, 22],
                # C8-H
                [7, 23],
            ],
            "n_electrons": 102,
            "n_orbitals": 80,
            "basis_set": "cc-pVDZ",
            "symmetry": "Cs",
            "charge": 0,
            "multiplicity": 1,
            "description": "Caffeine (1,3,7-trimethylxanthine) — complex heterocyclic pharmaceutical, 24 atoms, 102 electrons. Demonstrates industrial-scale quantum chemistry for drug discovery.",
        },
    }

    # ── Reference energies (Hartrees) ───────────────────────────────────
    REFERENCE_ENERGIES = {
        "water":          {"hf": -75.585354, "fci": -75.728457, "ccsd_t": -75.724892},
        "hydrogen":       {"hf": -1.116715,  "fci": -1.137276,  "ccsd_t": -1.137276},
        "lithium_hydride":{"hf": -7.862403,  "fci": -7.882352,  "ccsd_t": -7.881943},
        "nitrogen":       {"hf": -108.954028, "fci": -109.278132, "ccsd_t": -109.262341},
        "benzene":        {"hf": -230.721572, "fci": -231.547803, "ccsd_t": -231.492187},
        "caffeine":       {"hf": -679.563218, "fci": -680.847531, "ccsd_t": -680.791024},
    }

    def initialize(self) -> None:
        self._initialized = True
        self._logger.info("Chemistry Lab mock service initialized")

    def health_check(self) -> dict:
        return {"status": "active", "mode": "simulation", "molecules": len(self.MOLECULES)}

    # ── Public API ──────────────────────────────────────────────────────

    def list_molecules(self) -> list[dict]:
        """Return summary of all available molecules."""
        return [
            {
                "id": mid,
                "name": m["name"],
                "formula": m["formula"],
                "n_atoms": len(m["atoms"]),
                "n_electrons": m["n_electrons"],
                "n_orbitals": m["n_orbitals"],
                "basis_set": m["basis_set"],
                "symmetry": m["symmetry"],
            }
            for mid, m in self.MOLECULES.items()
        ]

    def get_molecule(self, molecule_id: str) -> dict | None:
        """Return full molecule data."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return None
        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})
        return {**mol, "id": molecule_id, "reference_energies": ref}

    def run_scf(self, molecule_id: str) -> dict:
        """Simulate an SCF / Hartree-Fock convergence run."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}
        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})
        hf_energy = ref.get("hf", -75.5)

        # Generate realistic convergence data
        n_iter = random.randint(10, 18)
        energies = []
        gradient_norms = []
        e = hf_energy + random.uniform(8.0, 15.0)  # start far from converged
        for i in range(n_iter):
            decay = math.exp(-0.45 * (i + 1))
            e = hf_energy + (e - hf_energy) * decay + random.gauss(0, 0.001 * decay)
            energies.append(round(e, 8))
            grad = max(1e-9, 10 ** (-1.5 - 0.55 * i) + random.gauss(0, 1e-5 * decay))
            gradient_norms.append(grad)

        # Final orbital energies (eigenvalues)
        n_occ = mol["n_electrons"] // 2
        n_virt = mol["n_orbitals"] - n_occ
        orbital_energies = sorted(
            [round(random.uniform(-20.5, -0.3), 4) for _ in range(n_occ)]
        ) + sorted(
            [round(random.uniform(0.1, 4.5), 4) for _ in range(n_virt)]
        )
        occupancies = [2] * n_occ + [0] * n_virt
        orbital_labels = [f"{'σ' if i < 2 else 'π' if i % 3 == 0 else 'n'}{i+1}" for i in range(mol["n_orbitals"])]

        return {
            "molecule": molecule_id,
            "method": "RHF / " + mol["basis_set"],
            "converged": True,
            "n_iterations": n_iter,
            "final_energy": round(energies[-1], 8),
            "convergence": {
                "energies": energies,
                "gradient_norms": [round(g, 10) for g in gradient_norms],
            },
            "orbitals": {
                "labels": orbital_labels,
                "energies": orbital_energies,
                "occupancies": occupancies,
            },
            "mulliken_charges": {
                atom["element"]: round(random.uniform(-0.4, 0.4), 4)
                for atom in mol["atoms"]
            },
            "dipole_moment": round(random.uniform(0.0, 2.5), 4),
            "homo_lumo_gap": round(orbital_energies[n_occ] - orbital_energies[n_occ - 1], 4) if n_occ < len(orbital_energies) else 0.0,
        }

    def run_active_space(self, molecule_id: str, n_active_electrons: int | None = None,
                          n_active_orbitals: int | None = None) -> dict:
        """Simulate active space selection (AVAS / automated selection)."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}

        # Default active space
        n_ae = n_active_electrons or min(mol["n_electrons"], 6)
        n_ao = n_active_orbitals or min(mol["n_orbitals"], 8)

        # Make sure they're reasonable
        n_ae = min(n_ae, mol["n_electrons"])
        n_ao = min(n_ao, mol["n_orbitals"])

        # Generate natural orbital occupations
        n_active = min(n_ao, 12)
        occupations = []
        for i in range(n_active):
            if i < n_ae // 2:
                occ = round(2.0 - random.uniform(0.01, 0.15), 4)
            elif i < n_ae:
                occ = round(random.uniform(0.5, 1.5), 4)
            else:
                occ = round(random.uniform(0.001, 0.15), 4)
            occupations.append(occ)

        # Entanglement entropy for orbitals
        entropies = [round(random.uniform(0.0, 1.5), 4) for _ in range(n_active)]

        # Orbital character
        characters = []
        labels_pool = ["σ-bonding", "σ*-antibonding", "π-bonding", "π*-antibonding",
                       "lone pair", "core", "Rydberg", "n(non-bonding)"]
        for i in range(n_active):
            characters.append(random.choice(labels_pool))

        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})
        casci_energy = ref.get("fci", ref.get("hf", -75.5)) + random.gauss(0, 0.01)

        return {
            "molecule": molecule_id,
            "method": f"AVAS ({n_ae}e, {n_ao}o) / {mol['basis_set']}",
            "n_active_electrons": n_ae,
            "n_active_orbitals": n_ao,
            "orbitals": {
                "indices": list(range(n_active)),
                "occupations": occupations,
                "entropies": entropies,
                "characters": characters,
            },
            "selection_criteria": {
                "threshold": 0.02,
                "method": "AVAS (Atomic Valence Active Space)",
                "entanglement_based": True,
            },
            "estimated_casci_energy": round(casci_energy, 6),
            "n_determinants": random.choice([64, 256, 1024, 4096, 16384]),
        }

    def run_qpe(self, molecule_id: str, n_precision_qubits: int = 8) -> dict:
        """Simulate Quantum Phase Estimation for ground-state energy."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}

        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})
        exact_energy = ref.get("fci", ref.get("hf", -75.5))

        # Simulate multiple QPE "shots" with probabilistic outcomes
        n_shots = 200
        phase_bits = n_precision_qubits
        # Main peak at correct energy + noise peaks
        phases = []
        energies = []
        probabilities = []
        counts = []

        # Dominant eigenvalue
        main_phase = (exact_energy % (2 * math.pi)) / (2 * math.pi)
        main_phase = abs(main_phase) % 1.0

        # Generate phase histogram
        n_bins = 2 ** min(phase_bits, 6)  # cap for display
        bin_probs = []
        for b in range(n_bins):
            phase = b / n_bins
            # Peaked distribution around main_phase
            dist = min(abs(phase - main_phase), abs(phase - main_phase + 1), abs(phase - main_phase - 1))
            prob = math.exp(-50 * dist ** 2) + 0.005 * random.random()
            bin_probs.append(prob)

        total = sum(bin_probs)
        bin_probs = [p / total for p in bin_probs]

        for b in range(n_bins):
            cnt = max(0, int(bin_probs[b] * n_shots + random.gauss(0, 1)))
            phase = b / n_bins
            energy = exact_energy + (phase - main_phase) * 10  # map phase to energy
            phases.append(round(phase, 6))
            energies.append(round(energy, 6))
            counts.append(cnt)
            probabilities.append(round(bin_probs[b], 6))

        # QPE result
        best_idx = probabilities.index(max(probabilities))
        estimated_energy = energies[best_idx]

        # Circuit resource estimate
        n_qubits = mol["n_orbitals"] + n_precision_qubits
        t_count = random.randint(500, 5000) * mol["n_orbitals"]
        circuit_depth = random.randint(1000, 10000) * mol["n_orbitals"]

        return {
            "molecule": molecule_id,
            "method": f"QPE ({phase_bits}-bit precision)",
            "n_precision_qubits": phase_bits,
            "estimated_energy": round(estimated_energy, 6),
            "exact_energy": round(exact_energy, 6),
            "energy_error": round(abs(estimated_energy - exact_energy), 8),
            "chemical_accuracy": abs(estimated_energy - exact_energy) < 0.0016,
            "phase_histogram": {
                "phases": phases,
                "energies": energies,
                "counts": counts,
                "probabilities": probabilities,
            },
            "resource_estimate": {
                "total_qubits": n_qubits,
                "t_gates": t_count,
                "circuit_depth": circuit_depth,
                "estimated_runtime_ms": round(circuit_depth * 0.001 * random.uniform(0.8, 1.2), 2),
            },
            "convergence_with_precision": [
                {
                    "n_bits": bits,
                    "energy": round(exact_energy + random.gauss(0, 0.5 / (2 ** bits)), 6),
                    "error": round(0.5 / (2 ** bits) + abs(random.gauss(0, 0.01)), 6),
                }
                for bits in range(3, phase_bits + 1)
            ],
        }

    def run_casci(self, molecule_id: str, n_roots: int = 5) -> dict:
        """Simulate CASCI / FCI calculation for energy spectrum."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}

        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})
        ground_energy = ref.get("fci", ref.get("hf", -75.5))

        # Generate energy spectrum
        states = []
        for i in range(n_roots):
            if i == 0:
                energy = ground_energy
            else:
                energy = ground_energy + random.uniform(0.05 * i, 0.15 * i)

            # CI coefficients (dominant determinants)
            n_dets = random.randint(3, 8)
            dets = []
            remaining = 1.0
            for d in range(n_dets):
                if d == 0 and i == 0:
                    coeff = round(random.uniform(0.85, 0.95), 4)
                else:
                    coeff = round(random.uniform(0.01, remaining * 0.5), 4)
                remaining -= coeff ** 2
                occupation = "".join(random.choice(["2", "u", "d", "0"]) for _ in range(min(mol["n_orbitals"], 8)))
                dets.append({"occupation": occupation, "coefficient": coeff})

            spin = 0 if i % 2 == 0 else 1
            symmetry_labels = ["A₁", "B₁", "B₂", "A₂", "A₁'", "E"]
            states.append({
                "root": i,
                "energy": round(energy, 6),
                "excitation_energy_ev": round((energy - ground_energy) * 27.2114, 4) if i > 0 else 0.0,
                "spin_multiplicity": 2 * spin + 1,
                "symmetry": symmetry_labels[i % len(symmetry_labels)],
                "dominant_determinants": sorted(dets, key=lambda d: abs(d["coefficient"]), reverse=True),
                "ci_weight": round(sum(d["coefficient"] ** 2 for d in dets), 4),
            })

        return {
            "molecule": molecule_id,
            "method": f"CASCI({mol['n_electrons']}e,{mol['n_orbitals']}o) / {mol['basis_set']}",
            "n_roots": n_roots,
            "states": states,
            "correlation_energy": round(ground_energy - ref.get("hf", ground_energy), 6),
            "n_determinants": random.choice([256, 1024, 4096, 16384, 65536]),
            "wall_time_ms": round(random.uniform(50, 800), 1),
        }

    def run_state_prep(self, molecule_id: str) -> dict:
        """Simulate quantum state preparation analysis."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}

        ref = self.REFERENCE_ENERGIES.get(molecule_id, {})

        methods = [
            {
                "name": "Hartree-Fock State",
                "type": "hf",
                "n_qubits": mol["n_orbitals"],
                "circuit_depth": mol["n_orbitals"] * 2,
                "cnot_count": mol["n_orbitals"] - 1,
                "fidelity": round(random.uniform(0.85, 0.92), 4),
                "energy": round(ref.get("hf", -75.5) + random.gauss(0, 0.001), 6),
            },
            {
                "name": "UCCSD Ansatz",
                "type": "uccsd",
                "n_qubits": mol["n_orbitals"],
                "circuit_depth": mol["n_orbitals"] * random.randint(40, 80),
                "cnot_count": mol["n_orbitals"] * random.randint(20, 50),
                "fidelity": round(random.uniform(0.95, 0.995), 4),
                "energy": round(ref.get("ccsd_t", ref.get("hf", -75.5)) + random.gauss(0, 0.005), 6),
            },
            {
                "name": "Hardware-Efficient Ansatz",
                "type": "hea",
                "n_qubits": mol["n_orbitals"],
                "circuit_depth": mol["n_orbitals"] * random.randint(10, 25),
                "cnot_count": mol["n_orbitals"] * random.randint(8, 20),
                "fidelity": round(random.uniform(0.90, 0.97), 4),
                "energy": round((ref.get("hf", -75.5) + ref.get("fci", -75.7)) / 2 + random.gauss(0, 0.02), 6),
            },
            {
                "name": "ADAPT-VQE",
                "type": "adapt",
                "n_qubits": mol["n_orbitals"],
                "circuit_depth": mol["n_orbitals"] * random.randint(15, 40),
                "cnot_count": mol["n_orbitals"] * random.randint(10, 30),
                "fidelity": round(random.uniform(0.97, 0.999), 4),
                "energy": round(ref.get("fci", ref.get("hf", -75.5)) + random.gauss(0, 0.003), 6),
            },
        ]

        return {
            "molecule": molecule_id,
            "methods": methods,
            "qubit_mapping": "Jordan-Wigner",
            "n_system_qubits": mol["n_orbitals"],
            "hamiltonian_terms": random.randint(50, 500) * mol["n_orbitals"],
        }

    def run_full_workflow(self, molecule_id: str) -> dict:
        """Run the entire workflow and return a summary."""
        mol = self.MOLECULES.get(molecule_id)
        if not mol:
            return {"error": "Unknown molecule"}

        job_id = str(uuid.uuid4())[:12]
        return {
            "job_id": job_id,
            "molecule": molecule_id,
            "workflow": "Full Pipeline",
            "steps": [
                {"name": "Molecular Structure", "status": "completed", "time_ms": 5},
                {"name": "SCF / Hartree-Fock", "status": "completed", "time_ms": random.randint(100, 500)},
                {"name": "Active Space Selection", "status": "completed", "time_ms": random.randint(50, 200)},
                {"name": "State Preparation", "status": "completed", "time_ms": random.randint(200, 800)},
                {"name": "QPE Simulation", "status": "completed", "time_ms": random.randint(500, 2000)},
                {"name": "CASCI Analysis", "status": "completed", "time_ms": random.randint(200, 1000)},
            ],
        }
