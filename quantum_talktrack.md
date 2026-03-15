# AQFA Quantum Dashboard: CxO Talk Track & Glossary

> **Purpose:** This document is a presenter guide for demonstrating the Azure Quantum Full-stack Accelerator (AQFA) Quantum Dashboard to CxO-level executives. It provides talk-track narratives for each tab and plain-English explanations of every technical term shown in the UI.

---

## Table of Contents

1. [Dashboard Tab](#1-dashboard-tab)
2. [Quantum Jobs Tab](#2-quantum-jobs-tab)
3. [Quantum Security Tab](#3-quantum-security-tab)
4. [Chemistry Lab Tab](#4-chemistry-lab-tab)
5. [Master Glossary](#5-master-glossary)

---

## 1. Dashboard Tab

### Talk Track

> *"This is the command center. It shows the health of every Azure service we've integrated — Azure Quantum for running quantum computations, our Post-Quantum Cryptography (PQC) Security module, the Chemistry Lab, and upcoming AI Assistant capabilities. The stat cards at the top give you an at-a-glance count of how many quantum backends we have access to and how many jobs have been run."*

> *"Below the service cards, the **Executive Insights** panel gives leadership an immediate readiness snapshot. The PQC Readiness Grade — from A+ down to F — summarizes how exposed our crypto stack is to quantum attack, with breakdowns of critical, warning, safe, and quantum-safe algorithm counts. On the chemistry side, we show how many molecules are in our simulation library, plus the largest system we can model (max electrons and orbitals). This panel updates live as you run scans and add molecules."*

### Key Terms on This Screen

| Term | Plain-English Meaning |
|---|---|
| **Quantum Targets** | The quantum computer backends (simulators or real hardware) available through Azure Quantum. Think of these as "printers" you can send work to — each has different capabilities. |
| **Jobs Submitted** | A "job" is a single computation sent to a quantum computer. Like submitting a print job, but instead of printing, the quantum machine runs a calculation. |
| **Shots** | Each quantum computation is inherently probabilistic (like flipping coins). "Shots" is how many times we repeat the same experiment to get statistically reliable results. 100 shots = run the circuit 100 times. |
| **Azure Quantum** | Microsoft's cloud platform that gives you access to quantum computers and simulators from multiple hardware providers (IonQ, Quantinuum, etc.) through a single Azure interface. |
| **PQC Security** | Post-Quantum Cryptography — new encryption algorithms designed to be secure even against future quantum computers. |
| **Chemistry Lab** | A quantum chemistry simulation workspace for modeling molecules and chemical reactions on quantum computers. |
| **Demo Mode** | The dashboard can operate without a live Azure Quantum connection by simulating results locally — useful for demonstrations and development. |
| **Executive Insights** | A dashboard panel that aggregates PQC readiness grades (A+ → F) and chemistry simulation capabilities into a single leadership-friendly view. Pulls live data from the Security and Chemistry modules. |
| **PQC Readiness Grade** | A letter grade (A+ through F) summarizing the organization's quantum readiness based on the proportion of algorithms that are quantum-safe vs. critically vulnerable. |

---

## 2. Quantum Jobs Tab

### Talk Track

> *"Here we submit actual quantum programs to Azure Quantum. We write the program in a standard language called OpenQASM, pick a target backend, set how many shots we want, and submit. Results come back as a distribution of measurement outcomes — like a histogram showing which answers the quantum computer found most often. The taller the bar, the higher the probability of that result."*

### Key Terms on This Screen

| Term | Plain-English Meaning |
|---|---|
| **OpenQASM 3.0** | Open Quantum Assembly Language — the industry-standard programming language for writing quantum circuits. Think of it as "source code" that tells the quantum computer what operations to perform, qubit by qubit. |
| **Quantum Circuit** | A sequence of operations (gates) applied to qubits. Analogous to a flowchart or a recipe — each step manipulates quantum bits to perform a computation. |
| **Target Backend** | The specific quantum computer or simulator that will execute your circuit. Different targets have different qubit counts, error rates, and capabilities. |
| **Quantinuum H2-1SC** | Quantinuum's free syntax checker — validates that your circuit follows correct OpenQASM grammar and is compatible with the hardware. Does not run the circuit. |
| **Quantinuum H2-1E** | Quantinuum's full state-vector emulator with a realistic noise model. Simulates the circuit as if it were running on real trapped-ion hardware. |
| **Quick Templates** | Pre-built quantum circuits (Bell State, GHZ State, Superposition, Quantum Random Number) that demonstrate common quantum computing patterns. |
| **Bell State** | The simplest example of quantum entanglement — two qubits linked so that measuring one instantly determines the other, no matter the distance. Einstein called this "spooky action at a distance." |
| **GHZ State** | A Bell State extended to 3+ qubits — all particles entangled simultaneously. Used to demonstrate multi-party quantum correlations. |
| **Measurement Counts** | After running a circuit many times (shots), we count how often each possible outcome appeared. This gives us the probability distribution of results. |
| **Probability** | The likelihood (0–100%) of each measurement outcome. Quantum computers give probabilistic answers, so we run many shots to find the most likely solution. |
| **\|0⟩, \|1⟩, \|00⟩, etc.** | Quantum state notation. \|0⟩ and \|1⟩ are the two possible states of a single qubit (like a coin being heads or tails). \|00⟩, \|01⟩ etc. represent multi-qubit states. |
| **Auto-Retry** | The dashboard automatically retries failed submissions up to 3 times with increasing wait times (3s, 6s) to handle transient Azure errors. |
| **Demo Mode Fallback** | If the live Azure submission fails at runtime, the dashboard automatically returns simulated results so the demonstration can continue uninterrupted. |

---

## 3. Quantum Security Tab

### Talk Track

> *"Quantum computers don't just do chemistry — they also pose a major threat to current encryption. This tab shows exactly where our organization is vulnerable, what the industry is doing about it via new NIST standards, and lets you simulate real attack scenarios."*

> *"The Threat Matrix shows every encryption algorithm we use today and rates it: green = safe from quantum attacks, yellow = needs attention, red = broken once a large quantum computer exists. Notice the SymCrypt algorithms from Microsoft — some are already quantum-safe."*

> *"The HNDL Simulator at the bottom is especially important for executives to understand: adversaries are recording encrypted data **right now**, planning to decrypt it years from now when quantum computers are powerful enough. Any data that needs to stay secret for 10+ years is at risk **today**."*

### Key Terms on This Screen

| Term | Plain-English Meaning |
|---|---|
| **Post-Quantum Cryptography (PQC)** | A new generation of encryption algorithms mathematically designed to resist attacks from both classical and quantum computers. These are the "quantum-proof locks" being standardized worldwide. |
| **Quantum Threat Matrix** | A table showing every encryption algorithm in use today alongside its vulnerability to quantum attack. Like a risk register specifically for cryptographic assets. 16 algorithms are tracked, including 7 SymCrypt entries. |
| **Threat Level: Critical** | This algorithm will be completely broken by a sufficiently large quantum computer (e.g., RSA, ECDSA). Must be replaced. |
| **Threat Level: Warning** | This algorithm is weakened by quantum computers but not completely broken (e.g., AES-128). Should be upgraded. |
| **Threat Level: Safe** | This algorithm remains secure even against quantum computers (e.g., AES-256, SHA-256). No action needed. |
| **Q-Sec (Quantum Security bits)** | How many bits of security remain after a quantum attack. **0** means completely broken. **128** means still very strong. Think of it as "how thick the safe door is against a quantum drill." |
| **Shor's Algorithm** | A quantum algorithm (discovered in 1994) that can factor large numbers exponentially faster than any classical computer. This is what breaks RSA and elliptic-curve encryption. |
| **Grover's Algorithm** | A quantum algorithm that speeds up brute-force search by a square-root factor. It halves the effective key length of symmetric encryption (e.g., AES-256 becomes equivalent to AES-128 strength). |
| **PQC Benchmarks** | Performance comparison of the new post-quantum algorithms — how large are the keys, how fast are the operations. Helps architects choose which PQC algorithms to adopt. |

### PQC Benchmarks — Deep Dive

> *"This panel answers the CTO's first question: 'Ok, we need to migrate — but what are the trade-offs?' Each bar in the chart shows a different PQC algorithm's key size or operation speed. The takeaway is that post-quantum keys are larger and operations are slightly slower than today's RSA/ECC, but the overhead is very manageable — especially with ML-KEM, where a key exchange adds less than 2KB and takes under 100 microseconds."*

> *"The type filter lets you switch between Key Encapsulation (KEM) and Digital Signature algorithms to focus the comparison. Click 'Run Benchmark' to simulate a real performance run — the numbers jitter slightly each time to show realistic variation."*

| Term | Plain-English Meaning |
|---|---|
| **ML-KEM-512 / 768 / 1024** | Three strength levels of the new NIST key exchange standard (FIPS 203). 512 = 128-bit security, 768 = 192-bit (recommended default), 1024 = 256-bit (highest). Higher number = more secure but slightly larger keys. |
| **ML-DSA-44 / 65 / 87** | Three strength levels of the new NIST digital signature standard (FIPS 204). 44 = 128-bit, 65 = 192-bit (recommended), 87 = 256-bit. These replace RSA and ECDSA signatures. |
| **SLH-DSA-128s / 256f** | SPHINCS+ hash-based signatures (FIPS 205). The "s" = small (compact signature, slower), "f" = fast (larger signature, faster). These are the backup standard using completely different math from lattice-based algorithms. |
| **Public Key bytes** | Size of the key that gets shared publicly (e.g., embedded in a TLS certificate). ML-KEM-768 = 1,184 bytes vs. RSA-2048 = 256 bytes. Slightly larger but trivial for modern networks. |
| **Secret Key bytes** | Size of the private key stored locally. ML-KEM-768 = 2,400 bytes vs. RSA-2048 = 1,024 bytes. Manageable increase. |
| **Ciphertext bytes** | Size of the encrypted key exchange message. ML-KEM-768 = 1,088 bytes. This is what gets sent across the wire during a TLS handshake. |
| **Signature bytes** | Size of a digital signature. ML-DSA-65 = 3,309 bytes vs. RSA-2048 = 256 bytes. Larger, but SLH-DSA-128s = only 7,856 bytes for the hash-based alternative. |
| **KeyGen (µs)** | Time to generate a new key pair, in microseconds. ML-KEM-768 ≈ 55µs — nearly instant. Even SLH-DSA-128s at 3,200µs is only 3 milliseconds. |
| **Encaps / Decaps (µs)** | Time to encapsulate (encrypt) and decapsulate (decrypt) a shared key using ML-KEM. Under 100µs for all variants — comparable to current RSA key exchange. |
| **Sign / Verify (µs)** | Time to create and verify a digital signature. ML-DSA-65: sign ≈ 340µs, verify ≈ 115µs. SLH-DSA is the outlier: sign ≈ 72ms (slower, but still under 0.1 seconds). |
| **NIST Security Category 1–5** | NIST's classification: Category 1 = at least as hard to break as AES-128, Category 3 = AES-192, Category 5 = AES-256. Most organizations should target Category 3 (ML-KEM-768, ML-DSA-65). |
| **Key Encapsulation vs. Digital Signature** | Use the type filter dropdown to compare only KEM algorithms or only signature algorithms. KEMs protect data in transit (TLS, VPN); signatures protect authenticity (certificates, code signing, email). |
| **Run Benchmark** | Simulates a benchmark run showing comparative performance bars. Use this to explain to architects why ML-KEM-768 is the recommended default: it balances security (192-bit) with small keys and fast operations. |
| **FIPS 203 / 204 / 205** | The official U.S. government standards (published by NIST in August 2024) for post-quantum encryption. FIPS 203 = ML-KEM (key exchange), FIPS 204 = ML-DSA (signatures), FIPS 205 = SLH-DSA (hash-based signatures). |
| **ML-KEM (CRYSTALS-Kyber)** | The new NIST-standardized algorithm for securely exchanging encryption keys. Replaces RSA and Diffie-Hellman for key exchange. Based on hard mathematical "lattice" problems that quantum computers can't solve efficiently. |
| **ML-DSA (CRYSTALS-Dilithium)** | The new NIST-standardized algorithm for digital signatures. Replaces RSA and ECDSA signatures. Also lattice-based. |
| **SLH-DSA (SPHINCS+)** | A backup digital signature algorithm based on hash functions (not lattices). Slower but uses completely different math — provides defense-in-depth in case lattice problems are unexpectedly broken. |
| **Key Encapsulation** | The process of securely sharing an encryption key between two parties. ML-KEM does this in a quantum-resistant way. Think of it as "putting the key inside a quantum-proof envelope." |
| **Digital Signature** | A cryptographic proof that a message or document is authentic and hasn't been tampered with. Like a tamper-evident seal that only the signer can produce. |
| **Public Key / Secret Key / Ciphertext bytes** | The sizes of the cryptographic objects. Larger = more bandwidth and storage needed, but doesn't necessarily mean more secure. These sizes matter for performance in TLS, email, IoT. |
| **SymCrypt** | Microsoft's core cryptographic engine — the library that powers encryption in Windows, Azure, Xbox, Office 365, and more. When we say "SymCrypt ML-KEM," we mean Microsoft has already integrated the post-quantum algorithm into its production crypto library. |
| **SymCrypt ML-KEM-768** | Microsoft's production implementation of the post-quantum key exchange algorithm within SymCrypt. Already shipping in Windows and Azure services. |
| **SymCrypt ML-DSA-65** | Microsoft's production implementation of the post-quantum digital signature algorithm within SymCrypt. |
| **SymCrypt XMSS** | eXtended Merkle Signature Scheme — a hash-based quantum-safe signature algorithm implemented in SymCrypt, primarily used for firmware and code signing. |
| **Readiness Scanner** | A tool that analyzes a list of encryption algorithms (your organization's crypto inventory) and gives an overall "quantum readiness" grade (A–F) based on how many are vulnerable. |
| **Enterprise / Modern / Legacy / SymCrypt Stack** | Pre-configured sets of algorithms representing common organizational profiles. Click one to simulate scanning that type of organization. |

### Readiness Scanner — Deep Dive

> *"This is the action panel. In a real engagement, we'd feed in your organization's actual crypto inventory — every algorithm used across TLS, certificates, VPNs, databases, code signing, and email. The scanner grades you A through F and flags every algorithm that needs to be migrated before a quantum computer arrives."*

> *"Try clicking the preset buttons: 'Enterprise' shows a typical Fortune 500 mix — lots of RSA and ECDSA, you'll see the grade drop. 'SymCrypt' shows what happens when you've adopted Microsoft's PQC-ready crypto stack — near-perfect score. The gap between those two grades is your migration project."*

| Term | Plain-English Meaning |
|---|---|
| **Crypto Inventory** | The complete list of encryption algorithms your organization uses across all systems. Most enterprises don't have one — creating it is the first step of a PQC migration. |
| **Grade A–F** | Overall quantum readiness score. **A** = 90%+ of algorithms are quantum-safe. **F** = majority are critically vulnerable. Most enterprises today score C or D without PQC migration. |
| **Readiness Score (0–100)** | The numeric score behind the letter grade. Calculated by weighting each algorithm: quantum-safe = 100 points, safe (symmetric) = 80, warning = 40, critical = 0. The weighted average is your score. |
| **Enterprise Preset** | Simulates a typical large organization: RSA-2048, AES-256, SHA-256, ECDSA, ECDH, 3DES. Mix of critical, warning, and safe — usually grades B- to C+. |
| **Modern Preset** | Simulates an organization already adopting PQC: AES-256, SHA-3, ML-KEM, ML-DSA, ECDH. Grades A or A+. |
| **Legacy Preset** | Simulates an organization with outdated crypto: RSA-2048, 3DES, AES-128, SHA-256, Diffie-Hellman. Grades D or F — maximum urgency. |
| **SymCrypt Preset** | Simulates Microsoft's SymCrypt stack: SymCrypt AES-GCM-256, SymCrypt ML-KEM, SymCrypt ML-DSA, SymCrypt XMSS, SymCrypt HMAC-SHA-256, SymCrypt ECDSA, SymCrypt RSA-OAEP. Shows the realistic mixed profile — PQC-ready algorithms alongside legacy ones still in use. |
| **Per-Algorithm Findings** | Each algorithm in the scan gets a detailed row: threat level, quantum security bits remaining, which quantum algorithm breaks it, recommended replacement, and migration timeline. |
| **Migration Timeline** | When each vulnerable algorithm must be replaced: "2030-2035" for RSA means you have roughly 4–9 years. Shorter timelines need higher priority in the migration roadmap. |
| **Critical / Warning / Safe / Quantum-Safe counts** | Summary stats at the top of scan results. Critical = must replace immediately, Warning = upgrade recommended, Safe = acceptable for now, Quantum-Safe = already migrated to PQC. |
| **"Already quantum-safe"** | Algorithms like ML-KEM, ML-DSA, SLH-DSA, and XMSS that were designed from the ground up to resist quantum attacks. These are the target state for every algorithm flagged as critical. |
| **"Manual review required"** | The scanner didn't recognize this algorithm name. Typically means a proprietary or niche algorithm that needs a cryptographer's assessment. |
| **Security Posture Radar** | A radar (spider) chart showing your organization's quantum-readiness across 8 dimensions — from key exchange to code signing. Red = current state, green-dashed = post-PQC target. The gap between the two lines is your migration work. |
| **Key Exchange** | When two computers establish a secret key to encrypt their communication (e.g., when you connect to your bank's website). Currently uses RSA or ECDH; needs to migrate to ML-KEM. |
| **TLS/Protocols** | Transport Layer Security — the protocol behind the padlock icon in your browser. Needs to be updated to use PQC key exchange before quantum computers arrive. |
| **Certificate Management** | Digital certificates (like website SSL certs) rely on signatures. The entire PKI (Public Key Infrastructure) that issues and validates certificates must transition to PQC signature algorithms. |
| **Quantum Threat Timeline** | A chart tracking the growth of quantum computers (physical and logical qubits) over time alongside the increasing threat level to current encryption. The crossover point is when your crypto becomes breakable. |
| **Physical Qubits** | The actual quantum bits on a chip. Today's qubits are noisy and error-prone. You need ~1,000 physical qubits for each reliable "logical qubit." |
| **Logical Qubits** | Error-corrected, reliable quantum bits — the ones that actually perform useful computation. Current machines have very few. The milestone to watch is ~4,000 logical qubits — enough to break RSA-2048. |
| **CRQC (Cryptographically Relevant Quantum Computer)** | A quantum computer powerful enough to break current public-key encryption (RSA, ECDSA, ECDH). Projected to exist between 2030–2035. This is the deadline your PQC migration must beat. |
| **Majorana 1** | Microsoft's 2025 topological qubit processor — a breakthrough approach that creates inherently more stable qubits, potentially accelerating the path to a CRQC. |

### Harvest Now, Decrypt Later (HNDL)

| Term | Plain-English Meaning |
|---|---|
| **HNDL (Harvest Now, Decrypt Later)** | A real and active threat: nation-state adversaries are intercepting and storing encrypted internet traffic **today**, knowing they can decrypt it once quantum computers are powerful enough. If your data needs to stay secret for 10+ years, it is effectively already at risk. This is the #1 reason organizations must act on PQC **now**, not when quantum computers arrive. |
| **CRQC Arrival Year** | The year a cryptographically-relevant quantum computer is projected to exist. The slider lets you see how risk changes with earlier or later timelines. |
| **Harvesting Started** | The year adversaries began capturing encrypted data. Intelligence agencies have likely been harvesting since at least 2015–2020. |
| **Risk Score (0–100%)** | How exposed each data category is under the HNDL scenario. Factors in: how long the data must stay secret, what encryption it uses, how long adversaries have been harvesting, and data volume. |
| **Data Categories** | The 6 types of data assessed: Classified Government, Healthcare PHI, Financial PII, IP & Trade Secrets, Corporate Communications, and IoT/SCADA Telemetry. Each has different secrecy requirements and risk profiles. |
| **Estimated Harvested TB** | An estimate of how much encrypted data adversaries may have already captured and stored, based on data volume and harvesting duration. |
| **Years Exposed After CRQC** | How many years the data remains sensitive **after** a quantum computer can decrypt it. If your data needs 30 years of secrecy and a CRQC arrives in 7 years, you have 23 years of exposure. |
| **Mitigation** | The recommended action: URGENT (migrate immediately), HIGH (plan migration within 12 months), or MONITOR (current approach is acceptable). |

---

## 4. Chemistry Lab Tab

### Talk Track

> *"This is where quantum computing delivers real business value — molecular simulation. Drug discovery, materials science, catalyst design, and battery chemistry all depend on understanding how electrons behave in molecules. Classical computers can't accurately simulate this beyond very small molecules. Quantum computers are purpose-built for this problem."*

> *"Start by selecting a molecule from the dropdown. We have six molecules in the library, ranging from H₂ (the simplest — 2 electrons) all the way up to Caffeine (102 electrons, 24 atoms). The 2.5D viewer shows the molecule rotating in real-time — each element has its own color and glow effect, and you can watch the 3D structure as it spins."*

> *"The pipeline bar at the top shows the end-to-end workflow: load a molecule, run the classical pre-computation (SCF), select which electrons matter most (Active Space), compare quantum state preparation methods, then run the actual quantum algorithm (QPE) to find the ground-state energy, and finally CASCI for the full energy spectrum. You can run each step individually or click **Run Full Pipeline** to execute the entire workflow in sequence."*

> *"Why does this matter? If you can accurately compute molecular energies, you can predict which drug molecules will bind to a target protein, which materials will be superconductors, or which catalysts will make industrial processes more efficient — all without building and testing physical prototypes."*

### Molecule Library

| Molecule | Formula | Atoms | Electrons | Orbitals | Basis Set | Symmetry | Use Case |
|---|---|---|---|---|---|---|---|
| Water | H₂O | 3 | 10 | 7 | STO-3G | C₂ᵥ | Fundamental benchmark |
| Hydrogen | H₂ | 2 | 2 | 2 | STO-3G | D∞h | Simplest molecule — "hydrogen atom of quantum chemistry" |
| Lithium Hydride | LiH | 2 | 4 | 6 | STO-3G | C∞v | Polar diatomic — ionic character & correlation |
| Nitrogen | N₂ | 2 | 14 | 10 | cc-pVDZ | D∞h | Triple bond — strong static correlation |
| Benzene | C₆H₆ | 12 | 42 | 36 | cc-pVDZ | D₆h | Aromatic — 6 π-electron delocalization |
| Caffeine | C₈H₁₀N₄O₂ | 24 | 102 | 80 | cc-pVDZ | Cs | Complex heterocyclic pharmaceutical — industrial-scale demo |

### 2.5D Molecule Viewer

> *"The interactive viewer uses a canvas with auto-rotation around the Y-axis, depth-sorted atom rendering, element-specific colors (O = red, N = blue, C = dark gray, H = white), radial gradient spheres for a '2.5D' effect, glow halos, and bond lines colored by element. It adapts to light/dark theme automatically."*

### Workflow Pipeline — Step by Step

| Pipeline Step | What It Does | Business Analogy |
|---|---|---|
| **Molecule** | Load the molecular structure (atoms, bonds, geometry) and display in 2.5D viewer. | Loading the blueprint of the building you want to analyze. |
| **SCF (Self-Consistent Field)** | A classical calculation that finds an approximate starting point for the electron configuration. Runs on regular computers. Produces convergence plot, orbital energies, HOMO-LUMO gap. | Creating a rough first draft before bringing in the expensive specialists. |
| **Active Space** | Identifies which electrons and orbitals are most important for the chemistry — the rest can be ignored. Uses the AVAS method. Dramatically reduces the problem size for the quantum computer. | Figuring out which 5 team members (out of 1,000) are critical to the project, so you only need to model their interactions. |
| **State Prep** | Compares 4 different quantum circuit strategies (HF, UCCSD, Hardware-Efficient, ADAPT-VQE) side-by-side — circuit depth, CNOT count, fidelity, and energy. Uses Jordan-Wigner qubit mapping. | Choosing the right format and tools before starting the quantum computation. |
| **QPE (Quantum Phase Estimation)** | The core quantum algorithm — uses the quantum computer to find the exact ground-state energy of the molecule. This is the step that classical computers cannot do efficiently for large molecules. | Using the quantum computer as a "super-microscope" to measure the molecule's true energy. |
| **CASCI** | Complete Active Space Configuration Interaction — computes not just the lowest energy but multiple excited states. Shows the full energy spectrum of the molecule with spin multiplicities and excitation energies. | Getting the complete picture — not just the ground floor, but all the floors of the building. |
| **Run Full Pipeline** | One-click execution of all 5 steps above in sequence with animated progress bars. | Running the complete engineering analysis end-to-end — one button, full report. |

### Key Terms on This Screen

| Term | Plain-English Meaning |
|---|---|
| **SCF / Hartree-Fock (HF)** | Self-Consistent Field — the standard classical chemistry method that finds an approximate solution by treating each electron as if it moves in the average field of all the others. It's fast but misses the fine-grained quantum correlations between electrons. It's the "starting point" before quantum refinement. |
| **SCF Convergence** | The iterative process of the SCF calculation getting closer and closer to the correct answer. The chart shows the energy decreasing toward a stable value — when the line flattens, the calculation has "converged" (found its answer). |
| **Orbital Energies** | Electrons in a molecule occupy "orbitals" — regions of space where they're likely to be found. Each orbital has an energy level. Green bars = occupied (has electrons), red bars = virtual (empty, higher energy). The gap between the highest occupied and lowest empty orbital is key to a molecule's chemical properties. |
| **HOMO-LUMO Gap** | Highest Occupied Molecular Orbital – Lowest Unoccupied Molecular Orbital gap. This single number predicts a molecule's stability, color, conductivity, and reactivity. A larger gap = more stable molecule. This is one of the most important numbers in computational chemistry. |
| **Mulliken Charges** | A method for assigning partial electric charges to each atom in a molecule. Positive = electron-deficient, negative = electron-rich. Useful for predicting reactivity and intermolecular interactions. |
| **Dipole Moment** | A measure of the overall charge separation in a molecule, in Debye (D). Water has a large dipole (~1.85 D) which is why it dissolves salts so well. A molecule with zero dipole is nonpolar. |
| **Basis Set (STO-3G, cc-pVDZ, etc.)** | The mathematical building blocks used to describe electron orbitals. A larger basis set = more accurate but more expensive computation. Think of it as the "resolution" setting — higher resolution = better picture but longer computation time. |
| **Active Space Selection (AVAS)** | Atomic Valence Active Space — an automated method that identifies which orbitals are most chemically important. The quantum computer only needs to simulate these "active" orbitals, making the problem tractable. |
| **Natural Orbital Occupations** | Shows how many electrons are in each active orbital. Values near 2.0 = fully occupied, near 0.0 = empty, values in between (0.2–1.8) = partially occupied = the "quantum-y" orbitals where quantum computing adds the most value. |
| **Entanglement Entropy** | A measure of how quantum-mechanically correlated an orbital is with the rest of the molecule. High entropy = this orbital is strongly entangled = a classical computer struggles here = a quantum computer thrives. Shown as a radar chart. |
| **(Ne, No) — e.g., (6e, 8o)** | Active space size: 6 electrons in 8 orbitals. This is the "problem size" for the quantum computer. Current quantum computers can handle roughly (10e, 10o); future machines will handle (50e, 50o) and beyond. |
| **Determinants** | A determinant is one possible arrangement of electrons in orbitals. The number of determinants grows exponentially — 16,384 determinants means the quantum computer is exploring 16,384 possible electron configurations simultaneously. This exponential parallelism is quantum computing's core advantage. |
| **State Preparation / Ansatz** | The quantum circuit used to prepare the molecule's quantum state on the quantum computer. Different "ansätze" (plural of ansatz) trade off accuracy vs. circuit complexity. The dashboard compares all 4 side-by-side. |
| **UCCSD (Unitary Coupled Cluster)** | A chemistry-inspired ansatz that's highly accurate but requires deep circuits. Best for near-term quantum computers with low error rates. |
| **Hardware-Efficient Ansatz (HEA)** | A generic circuit structure designed to run well on today's noisy quantum hardware, even if it's not chemically motivated. Trades some accuracy for practicality. |
| **ADAPT-VQE** | An adaptive algorithm that builds the circuit one piece at a time, adding only the operations that improve the energy estimate. Often achieves the best accuracy-to-depth ratio. |
| **Fidelity** | How close the quantum state preparation is to the true molecular state (0–100%). Higher fidelity = more accurate results. 99%+ is the target for useful chemistry. |
| **Circuit Depth** | How many sequential layers of quantum gates the circuit has. Deeper circuits = more potential for errors on noisy hardware. A key metric for quantum hardware requirements. |
| **CNOT Count** | The number of two-qubit entangling gates in the circuit. These are the most error-prone operations on quantum hardware. Fewer CNOTs = more likely to run successfully on real hardware. |
| **Jordan-Wigner Mapping** | A mathematical method to translate the chemistry problem (fermions) into the language of quantum computers (qubits). One of several possible "encodings" — like choosing between metric and imperial units. |
| **QPE (Quantum Phase Estimation)** | The gold-standard quantum algorithm for finding molecular energies. It encodes the energy as a "phase" (angle) on ancilla qubits, then reads it out. Requires a fault-tolerant quantum computer for industrial-scale problems. |
| **Phase Histogram** | The output of QPE — a histogram showing which energy values the quantum computer measured most frequently. The tallest bar (highlighted in green) is the best estimate of the true ground-state energy. |
| **Precision Convergence** | A dual-axis chart showing how QPE energy estimates improve as you increase the number of precision qubits (3-bit → 8-bit). Error decreases exponentially — demonstrates the power of adding more precision. |
| **Chemical Accuracy** | An energy error of less than 1.6 milliHartree (~1 kcal/mol). This is the gold standard in computational chemistry — below this threshold, computed results are reliable enough to predict real-world chemical behavior. |
| **T-Gates** | A type of quantum gate that's especially expensive in error-corrected quantum computing. The T-gate count is the best single metric for "how hard is this problem for a quantum computer." |
| **Resource Estimate** | How many qubits, gates, and time the quantum computation requires. This tells you what size quantum computer you need to solve the problem. |
| **Hartree (Ha)** | The atomic unit of energy used in quantum chemistry. 1 Hartree ≈ 627.5 kcal/mol. All energies in the Chemistry Lab are reported in Hartrees. |
| **Correlation Energy** | The energy difference between the simple Hartree-Fock approximation and the exact quantum answer. This is precisely what quantum computers compute better than classical ones — it captures the quantum interactions between electrons that classical methods miss. |
| **CASCI (Complete Active Space CI)** | Configuration Interaction within the active space — computes multiple electronic excited states (not just the ground state). Shows the full energy spectrum, spin states, symmetry labels, and dominant CI determinants. |
| **Energy Spectrum** | The set of energy levels a molecule can occupy — ground state (lowest) and excited states (higher). Like the rungs of a ladder. The gaps between rungs determine the molecule's optical and electronic properties. |
| **Spin Multiplicity** | Whether the electrons are all paired (singlet, 2S+1=1) or have unpaired electrons (triplet, 2S+1=3, etc.). Determines whether a molecule is magnetic and affects its reactivity. |
| **Excitation Energy (eV)** | The energy required to push the molecule from its ground state to an excited state, measured in electron volts. Determines what wavelength of light the molecule absorbs — crucial for drug design, solar cells, and display technologies. |
| **Hamiltonian** | The mathematical operator that describes all the energy interactions in a molecule — kinetic energy, electron-nucleus attraction, electron-electron repulsion. The quantum computer's job is to find the lowest eigenvalue (ground-state energy) of this operator. In business terms, it's the "complete mathematical model" of the molecule. |

---

## 5. Master Glossary

Quick-reference alphabetical listing of all terms.

| Term | Category | One-Line Definition |
|---|---|---|
| ADAPT-VQE | Chemistry | Adaptive circuit-building algorithm — adds gates one at a time for optimal accuracy-to-depth ratio |
| Active Space | Chemistry | Subset of orbitals/electrons that matter most for the chemistry — reduces problem to tractable size |
| AES-128 / AES-256 | Security | Symmetric encryption standard; 256-bit variant is quantum-safe, 128-bit variant is weakened |
| Ansatz | Chemistry | Template quantum circuit used to represent a molecular state |
| Auto-Retry | Platform | Dashboard retries failed Azure submissions up to 3 times with increasing wait times |
| Azure Quantum | Platform | Microsoft's cloud platform providing access to quantum computers and simulators |
| Basis Set | Chemistry | Mathematical resolution setting for orbital calculations; larger = more accurate but slower |
| Bell State | Quantum | Simplest example of two-qubit entanglement |
| Caffeine (C₈H₁₀N₄O₂) | Chemistry | Complex 24-atom heterocyclic pharmaceutical — largest molecule in the library (102 electrons) |
| CASCI | Chemistry | Multi-root calculation revealing the molecule's full energy spectrum |
| Chemical Accuracy | Chemistry | Error < 1.6 milliHartree — the threshold for reliable chemistry predictions |
| Circuit Depth | Quantum | Number of sequential gate layers; deeper = more error-prone on real hardware |
| CNOT | Quantum | Two-qubit entangling gate; most error-prone operation on current hardware |
| Correlation Energy | Chemistry | Energy missed by classical approximation — precisely what quantum computers capture |
| CRQC | Security | Cryptographically Relevant Quantum Computer — powerful enough to break RSA |
| Demo Mode Fallback | Platform | Automatic simulated results when Azure Quantum submission fails at runtime |
| Determinant | Chemistry | One electron configuration; quantum computers explore exponentially many simultaneously |
| Digital Signature | Security | Cryptographic proof of authenticity and integrity |
| Dipole Moment | Chemistry | Measure of charge separation in a molecule (Debye); predicts solubility and reactivity |
| ECDSA / ECDH | Security | Elliptic-curve crypto for signatures / key exchange — broken by Shor's algorithm |
| Entanglement Entropy | Chemistry | Measure of quantum correlation; high = quantum computing adds most value |
| Excitation Energy | Chemistry | Energy to reach a higher electronic state; determines optical properties |
| Executive Insights | Platform | Dashboard panel summarizing PQC readiness grade and chemistry capabilities for leadership |
| FIPS 203/204/205 | Security | NIST post-quantum cryptography standards (2024) |
| Full Pipeline | Chemistry | One-click execution of SCF → Active Space → State Prep → QPE → CASCI in sequence |
| GHZ State | Quantum | Multi-qubit entangled state for testing quantum correlations |
| Grover's Algorithm | Security | Quantum search speedup — halves effective security of symmetric encryption |
| Hamiltonian | Chemistry | Complete mathematical energy model of a molecule |
| Hartree (Ha) | Chemistry | Atomic unit of energy (1 Ha ≈ 627.5 kcal/mol) |
| HNDL | Security | Harvest Now Decrypt Later — adversaries storing encrypted data for future quantum decryption |
| HOMO-LUMO Gap | Chemistry | Energy gap predicting stability, reactivity, and electronic properties |
| Jordan-Wigner | Chemistry | Method to encode chemistry on qubits |
| Key Encapsulation | Security | Quantum-safe method for sharing encryption keys (ML-KEM) |
| Logical Qubits | Quantum | Error-corrected, reliable qubits — the ones that do useful work |
| Majorana 1 | Quantum | Microsoft's 2025 topological qubit processor |
| ML-DSA | Security | NIST-standardized post-quantum digital signature algorithm (FIPS 204) |
| ML-KEM | Security | NIST-standardized post-quantum key encapsulation (FIPS 203) |
| Molecule Viewer (2.5D) | Chemistry | Animated canvas renderer with auto-rotation, depth sorting, glow effects, and element colors |
| Mulliken Charges | Chemistry | Partial electric charges assigned to atoms; predicts reactivity |
| OpenQASM | Quantum | Standard programming language for quantum circuits |
| Orbital | Chemistry | Spatial region where an electron is likely found; has a defined energy level |
| Physical Qubits | Quantum | Actual quantum bits on chip — noisy, need ~1000:1 ratio for one logical qubit |
| PQC | Security | Post-Quantum Cryptography — encryption resistant to quantum attacks |
| PQC Readiness Grade | Security | Letter grade (A+ → F) summarizing organizational quantum readiness |
| Precision Convergence | Chemistry | Chart showing QPE accuracy improving as precision qubits are added |
| QPE | Chemistry | Quantum Phase Estimation — core algorithm for finding molecular energies |
| Quantinuum H2-1SC | Quantum | Free syntax checker target — validates circuit structure without executing |
| Quantinuum H2-1E | Quantum | Full state-vector emulator with realistic noise model |
| Qubit | Quantum | Quantum bit — can be 0, 1, or a superposition of both simultaneously |
| RSA | Security | Widely-used public-key encryption — will be broken by quantum computers |
| Run Full Pipeline | Chemistry | One-click button that chains SCF → Active Space → State Prep → QPE → CASCI |
| SCF / Hartree-Fock | Chemistry | Classical starting-point calculation for electron configuration |
| Shor's Algorithm | Security | Quantum algorithm that breaks RSA and elliptic-curve encryption |
| Shots | Quantum | Number of times a quantum circuit is repeated for statistical reliability |
| SLH-DSA | Security | Hash-based quantum-safe signature algorithm (FIPS 205, SPHINCS+) |
| Spin Multiplicity | Chemistry | Electron pairing state (singlet/triplet) — affects magnetism and reactivity |
| State Preparation | Chemistry | Converting a chemistry problem into a runnable quantum circuit |
| SymCrypt | Security | Microsoft's production crypto engine powering Windows, Azure, Office 365 |
| T-Gate | Quantum | Expensive error-corrected gate; T-count = best proxy for quantum problem difficulty |
| UCCSD | Chemistry | High-accuracy chemistry ansatz requiring deep quantum circuits |

---

## Demo Flow Recommendation

1. **Dashboard** (30 sec) — Show service health cards, stat counters, and **Executive Insights** (PQC grade + chemistry capabilities). Orient the audience.
2. **Quantum Security** (3–4 min) — Start with Threat Matrix → show SymCrypt entries → PQC Benchmarks (filter KEM vs. Signature) → Readiness Scanner (try Enterprise preset, then SymCrypt preset — compare grades) → Posture Radar → **Timeline** (builds urgency) → **HNDL Simulator** (strongest CxO impact — "your data is being harvested NOW")
3. **Chemistry Lab** (3–4 min) — Select **Caffeine** (C₈H₁₀N₄O₂ — 24 atoms, 102 electrons; visually impressive in the 2.5D viewer) → Click **Run Full Pipeline** → walk through each result panel as it completes, emphasizing this is an end-to-end quantum chemistry workflow running automatically. Alternatively, select **Benzene** (C₆H₆) and run steps individually if you want more control.
4. **Quantum Jobs** (1–2 min) — Submit a Bell State to show real Azure Quantum integration

### Key Messages for CxOs

- **Why now?** The HNDL threat means PQC migration is urgent *today*, not when quantum computers arrive.
- **Why Microsoft?** SymCrypt already ships PQC algorithms in production. Azure Quantum provides the hardware path.
- **What's the business value of quantum chemistry?** Drug discovery timelines measured in months instead of years. Materials designed computationally before a single experiment. Catalyst optimization for industrial processes.
- **What scale can we handle?** The Caffeine molecule (102 electrons, 80 orbitals) demonstrates industrial-scale quantum chemistry — well beyond toy problems.
- **What's needed?** A quantum readiness assessment, PQC migration roadmap, and pilot quantum chemistry use cases aligned to your R&D portfolio.

---

*Document generated for the AQFA Quantum Dashboard — March 2026*
