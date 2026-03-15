# Azure Quantum Full-stack Accelerator (AQFA) — Quantum Dashboard

The **Azure Quantum Full-stack Accelerator** is an interactive web application for submitting quantum circuits to Azure Quantum, visualizing measurement results, analyzing post-quantum cryptographic readiness, and running end-to-end quantum chemistry simulation pipelines — all from your browser.

Built with Flask, Chart.js, and Lucide icons, the dashboard features a glassmorphism UI with light/dark themes, an animated particle background, and a fully functional demo mode that works without Azure credentials.

## Overview

AQFA provides four integrated modules:

- **Dashboard** — Command center with live service health, job stats, PQC readiness grade, chemistry capabilities, and executive insights
- **Quantum Jobs** — Submit OpenQASM 3.0 circuits to Azure Quantum (Quantinuum), view measurement histograms, and track job history
- **Quantum Security** — Post-Quantum Cryptography threat matrix, NIST PQC benchmarks, crypto readiness scanner, security posture radar, threat timeline, and HNDL simulator
- **Chemistry Lab** — Six-molecule library with a full simulation pipeline: SCF → Active Space → State Preparation → QPE → CASCI, featuring a 2.5D rotating molecule viewer

## Project Structure

```txt
aqfa/
├── app/                        # Flask web application
│   ├── __init__.py
│   ├── config.py               # Dataclass configs loaded from .env
│   ├── main.py                 # App factory — wires services & blueprints
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py              # REST API (30+ endpoints)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract BaseService class
│   │   ├── azure_quantum.py    # Azure Quantum workspace + job lifecycle
│   │   ├── chemistry.py        # Mock quantum chemistry simulation service
│   │   └── pqc_security.py     # PQC threat analysis (6 capabilities)
│   ├── static/
│   │   ├── css/styles.css      # Glassmorphism UI, light/dark themes
│   │   └── js/app.js           # 2 000-line SPA — charts, 2.5D viewer, modules
│   └── templates/
│       └── index.html          # Single-page dashboard template
├── aqfa/                       # Python virtual environment
├── quantum_markmap.md          # Markmap mind-map source
├── quantum_markmap.html        # Rendered interactive mind-map
├── quantum_talktrack.md        # CxO demo talk track & glossary
├── requirements.txt            # Python dependencies
├── run.py                      # Entry point — python run.py
├── LICENSE
└── README.md
```

## Features

### Dashboard (Command Center)

- **Service health cards** — Azure Quantum, PQC Security, Chemistry Lab, Azure OpenAI (coming soon), AI Search (coming soon), Azure Speech (coming soon)
- **Stat counters** — Quantum Targets, Jobs Submitted, Total Shots, Completed Computations
- **Executive Insights** — PQC readiness grade (A+ → F), critical/warning/safe algorithm counts, chemistry capability summary (molecule count, max electrons, max orbitals)
- **Light / Dark theme** toggle with smooth transitions
- **Animated particle field** background

### Quantum Jobs

- **OpenQASM 3.0 editor** with syntax-highlighted text area
- **Quick templates** — Bell State (2 qubits), GHZ State (3 qubits), Superposition (1 qubit), Quantum Random Number (4 qubits)
- **Target backend selection** — Quantinuum H2-1SC (Syntax Checker), Quantinuum H2-1E (Emulator)
- **Configurable shot count** — 1 to 10,000
- **Chart.js measurement histograms** — counts bar chart + probability distribution table
- **Job history table** — status pills (Demo Mode / Submitted / Completed / Error), timestamps, view results
- **Auto-retry** — up to 3 retries with exponential back-off on transient Azure errors
- **Demo mode fallback** — simulated results when Azure Quantum is unavailable

### Quantum Security (PQC Module — 6 Capabilities)

| # | Capability | Description |
|---|---|---|
| 1 | **Quantum Threat Matrix** | 16 algorithms (including 7 SymCrypt entries) rated Critical / Warning / Safe with Q-Sec bits, vulnerability source, migration timeline, and recommendation |
| 2 | **PQC Algorithm Benchmarks** | 8 NIST algorithms (ML-KEM-512/768/1024, ML-DSA-44/65/87, SLH-DSA-128s/256f) — key sizes, signature/ciphertext sizes, KeyGen/Encaps/Decaps/Sign/Verify timings in µs; filterable by type (KEM vs. Signature) |
| 3 | **Crypto Readiness Scanner** | Accepts a custom algorithm list or preset (Enterprise / Modern / Legacy / SymCrypt), returns per-algorithm findings with threat levels and an overall readiness score & letter grade (A → F) |
| 4 | **Quantum Threat Timeline** | 11 milestones (2019–2035) with qubit progression (physical + logical) and threat impact %; Chart.js dual-axis line chart |
| 5 | **Security Posture Radar** | 8-dimension radar chart (Key Exchange, Digital Signatures, Symmetric Crypto, Hash Functions, TLS/Protocols, Certificate Mgmt, Data-at-Rest, Code Signing) — current vs. target scores |
| 6 | **HNDL Simulator** | Harvest Now, Decrypt Later threat simulation with interactive sliders for CRQC arrival year and harvesting start year; 6 data categories (Classified Gov, Healthcare PHI, Financial PII, IP/Trade Secrets, Corporate Email, IoT/SCADA) with per-category risk scores, estimated harvested TB, and mitigation recommendations |

### Chemistry Lab (6-Molecule Library + Full Pipeline)

**Molecules:**

| Molecule | Formula | Electrons | Orbitals | Basis Set | Symmetry |
|---|---|---|---|---|---|
| Water | H₂O | 10 | 7 | STO-3G | C₂ᵥ |
| Hydrogen | H₂ | 2 | 2 | STO-3G | D∞h |
| Lithium Hydride | LiH | 4 | 6 | STO-3G | C∞v |
| Nitrogen | N₂ | 14 | 10 | cc-pVDZ | D∞h |
| Benzene | C₆H₆ | 42 | 36 | cc-pVDZ | D₆h |
| Caffeine | C₈H₁₀N₄O₂ | 102 | 80 | cc-pVDZ | Cs |

**Pipeline Steps:**

1. **Molecule Viewer** — 2.5D animated canvas with auto-rotation, element-colored atoms, bond lines, depth-sorted rendering, and glow effects
2. **SCF / Hartree-Fock** — Convergence plot (energy vs. iteration), orbital energy bar chart (occupied green / virtual red), HOMO-LUMO gap, Mulliken charges, dipole moment
3. **Active Space (AVAS)** — Natural orbital occupations bar chart, entanglement entropy radar, orbital character labels, determinant count
4. **State Preparation** — Compares 4 ansatz methods (Hartree-Fock, UCCSD, Hardware-Efficient, ADAPT-VQE) — circuit depth, CNOT count, fidelity, energy; Jordan-Wigner qubit mapping
5. **QPE (Quantum Phase Estimation)** — Phase histogram, precision convergence dual-axis chart, chemical accuracy check (< 1.6 mHa), T-gate & qubit resource estimates
6. **CASCI** — Multi-root energy spectrum bar chart, CI coefficients with dominant determinants, spin multiplicities, excitation energies (eV), correlation energy
7. **Run Full Pipeline** — One-click execution of all 5 computational steps in sequence with animated progress

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv aqfa
aqfa\Scripts\activate        # Windows
# source aqfa/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Configure Azure Quantum — works in Demo Mode without it
#    Create a .env file with your credentials:
#    AZURE_QUANTUM_CONNECTION_STRING=...
#    or AZURE_QUANTUM_RESOURCE_ID=... + AZURE_QUANTUM_API_KEY=...

# 4. Launch the dashboard
python run.py
```

Open **http://localhost:5000** in your browser.

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `AZURE_QUANTUM_CONNECTION_STRING` | No | Azure Quantum workspace connection string (preferred auth) |
| `AZURE_QUANTUM_RESOURCE_ID` | No | Resource ID (alternative auth — requires API key or DefaultAzureCredential) |
| `AZURE_QUANTUM_API_KEY` | No | API key for the workspace |
| `AZURE_QUANTUM_LOCATION` | No | Region (default: `eastus`) |
| `QUANTINUUM_TARGET_SC` | No | Syntax checker target (default: `quantinuum.sim.h2-1sc`) |
| `QUANTINUUM_TARGET_EM` | No | Emulator target (default: `quantinuum.sim.h2-1e`) |
| `FLASK_PORT` | No | Server port (default: `5000`) |
| `FLASK_DEBUG` | No | Enable debug mode (`1` / `0`) |

## REST API Reference

All endpoints are prefixed with `/api`.

### Health & Configuration

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Service health status |
| GET | `/api/config/targets` | Available quantum backends |
| GET | `/api/config/circuits` | Built-in circuit templates |
| GET | `/api/config/services` | All service statuses |

### Quantum Jobs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs` | List job history |
| POST | `/api/jobs` | Submit a quantum job (`circuit_qasm`, `target_id`, `job_name?`, `shots?`) |
| GET | `/api/jobs/<job_id>` | Get job status / results |

### PQC Security

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/security/threats` | Quantum threat matrix |
| GET | `/api/security/pqc-algorithms` | NIST PQC algorithm data |
| POST | `/api/security/benchmark` | Run PQC performance benchmark |
| POST | `/api/security/scan` | Readiness scan (`algorithms: string[]`) |
| GET | `/api/security/timeline` | Quantum threat timeline |
| GET | `/api/security/posture` | Security posture radar |
| POST | `/api/security/hndl` | HNDL simulation (`quantum_year?`, `harvest_start_year?`) |

### Chemistry Lab

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/chemistry/molecules` | List available molecules |
| GET | `/api/chemistry/molecules/<id>` | Full molecule data + reference energies |
| POST | `/api/chemistry/scf` | Run SCF / Hartree-Fock (`molecule_id`) |
| POST | `/api/chemistry/active-space` | Active space selection (`molecule_id`, `n_active_electrons?`, `n_active_orbitals?`) |
| POST | `/api/chemistry/state-prep` | State preparation analysis (`molecule_id`) |
| POST | `/api/chemistry/qpe` | Quantum Phase Estimation (`molecule_id`, `n_precision_qubits?`) |
| POST | `/api/chemistry/casci` | CASCI multi-root calculation (`molecule_id`, `n_roots?`) |

## Azure Services Roadmap

| Service | Status | Description |
|---|---|---|
| Azure Quantum | ✅ Active | Submit & monitor quantum jobs on Quantinuum H2-1SC / H2-1E |
| PQC Security | ✅ Active | 6-capability threat analysis module (offline, no external dependencies) |
| Chemistry Lab | ✅ Active | 6-molecule simulation engine with full QPE/CASCI pipeline |
| Azure OpenAI (GPT-4) | 🔜 Planned | Natural-language interaction with quantum chemistry |
| Azure AI Search | 🔜 Planned | RAG over chemistry literature & results |
| Azure Speech | 🔜 Planned | Voice-driven circuit design & results narration |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Browser (SPA)                                          │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │Dashboard│ │Quantum   │ │Security  │ │Chemistry    │ │
│  │         │ │Jobs      │ │(PQC)     │ │Lab          │ │
│  └────┬────┘ └────┬─────┘ └────┬─────┘ └──────┬──────┘ │
└───────┼───────────┼────────────┼───────────────┼────────┘
        │    REST API (Flask)    │               │
┌───────┼───────────┼────────────┼───────────────┼────────┐
│  /api/health  /api/jobs  /api/security/*  /api/chemistry/*│
│       │           │            │               │        │
│  ┌────┴────┐ ┌────┴─────┐ ┌───┴────┐ ┌───────┴──────┐  │
│  │BaseService│AzureQuantum│PQCSecurity│ChemistryService│ │
│  │(abstract)│ │Service   │ │Service │ │              │  │
│  └─────────┘ └────┬─────┘ └────────┘ └──────────────┘  │
│                    │                                    │
│              Azure Quantum                              │
│              (or Demo Mode)                             │
└─────────────────────────────────────────────────────────┘
```

## Contributing

There are many ways in which you can participate in this project, for example:

- [Submit bugs and feature requests](https://github.com/microsoft/qdk-chemistry/issues), and help us verify as they are checked in
- Review [source code changes](https://github.com/microsoft/qdk-chemistry/pulls)
- Review the documentation and make pull requests for anything from typos to additional and new content

If you are interested in fixing issues and contributing directly to the code base,
please see the document [How to Contribute](https://github.com/microsoft/qdk-chemistry/blob/main/CONTRIBUTING.md).

## Support

For help and questions about using this project, please see [SUPPORT](./SUPPORT.md).

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](LICENSE.txt) license.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos is subject to those third-parties' policies.
