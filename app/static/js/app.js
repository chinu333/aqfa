/* ==========================================================================
   QDK Chemistry — Quantum Dashboard  ·  Client Application
   ========================================================================== */

(() => {
    "use strict";

    // ======================================================================
    //  STATE
    // ======================================================================
    const State = {
        currentSection: "dashboard",
        targets: [],
        circuits: {},
        jobs: [],
        resultChart: null,
        dashboardChart: null,
    };

    // ======================================================================
    //  API HELPERS
    // ======================================================================
    const API = {
        async get(path)  { return (await fetch(`/api${path}`)).json(); },
        async post(path, body) {
            return (await fetch(`/api${path}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            })).json();
        },
    };

    // ======================================================================
    //  THEME
    // ======================================================================
    const Theme = {
        init() {
            const saved = localStorage.getItem("qdk-theme") || "light";
            this.apply(saved);
            document.getElementById("themeToggle").addEventListener("click", () => {
                const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
                this.apply(next);
            });
        },
        apply(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("qdk-theme", theme);
            const lightIcon = document.getElementById("themeIconLight");
            const darkIcon  = document.getElementById("themeIconDark");
            if (theme === "dark") {
                lightIcon.style.display = "none";
                darkIcon.style.display  = "inline";
            } else {
                lightIcon.style.display = "inline";
                darkIcon.style.display  = "none";
            }
            // Update Chart.js if rendered
            Charts.updateTheme();
        },
    };

    // ======================================================================
    //  NAVIGATION
    // ======================================================================
    const Nav = {
        init() {
            document.querySelectorAll(".nav-btn[data-section]").forEach(btn => {
                btn.addEventListener("click", () => {
                    if (btn.disabled) return;
                    this.goTo(btn.dataset.section);
                });
            });
        },
        goTo(section) {
            State.currentSection = section;
            document.querySelectorAll(".section").forEach(s => s.classList.add("hidden"));
            const target = document.getElementById(`section-${section}`);
            if (target) target.classList.remove("hidden");

            document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
            const btn = document.querySelector(`.nav-btn[data-section="${section}"]`);
            if (btn) btn.classList.add("active");

            lucide.createIcons();
        },
    };

    // ======================================================================
    //  TOAST NOTIFICATIONS
    // ======================================================================
    const Toast = {
        show(message, type = "info") {
            const icons = { success: "check-circle", error: "x-circle", info: "info" };
            const el = document.createElement("div");
            el.className = `toast toast--${type}`;
            el.innerHTML = `<i data-lucide="${icons[type] || "info"}"></i><span>${message}</span>`;
            document.getElementById("toastContainer").appendChild(el);
            lucide.createIcons({ nameAttr: "data-lucide" });
            setTimeout(() => { el.style.opacity = "0"; setTimeout(() => el.remove(), 300); }, 4000);
        },
    };

    // ======================================================================
    //  CHARTS (Chart.js)
    // ======================================================================
    const Charts = {
        getColors() {
            const dark = document.documentElement.getAttribute("data-theme") === "dark";
            return {
                grid: dark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)",
                text: dark ? "#aaa" : "#555",
                bars: [
                    "rgba(92,107,192,0.8)", "rgba(171,71,188,0.8)",
                    "rgba(41,182,246,0.8)", "rgba(255,183,77,0.8)",
                    "rgba(67,160,71,0.8)",  "rgba(229,57,53,0.8)",
                    "rgba(0,150,136,0.8)",  "rgba(255,112,67,0.8)",
                    "rgba(94,53,177,0.8)",  "rgba(0,172,193,0.8)",
                    "rgba(192,202,51,0.8)", "rgba(121,85,72,0.8)",
                    "rgba(63,81,181,0.8)",  "rgba(244,67,54,0.8)",
                    "rgba(33,150,243,0.8)", "rgba(76,175,80,0.8)",
                ],
                barsBorder: [
                    "rgba(92,107,192,1)", "rgba(171,71,188,1)",
                    "rgba(41,182,246,1)", "rgba(255,183,77,1)",
                    "rgba(67,160,71,1)",  "rgba(229,57,53,1)",
                    "rgba(0,150,136,1)",  "rgba(255,112,67,1)",
                    "rgba(94,53,177,1)",  "rgba(0,172,193,1)",
                    "rgba(192,202,51,1)", "rgba(121,85,72,1)",
                    "rgba(63,81,181,1)",  "rgba(244,67,54,1)",
                    "rgba(33,150,243,1)", "rgba(76,175,80,1)",
                ],
            };
        },

        renderResultChart(counts) {
            const ctx = document.getElementById("resultChart");
            if (State.resultChart) State.resultChart.destroy();
            const c = this.getColors();
            const labels = Object.keys(counts);
            const data   = Object.values(counts);
            const total  = data.reduce((a, b) => a + b, 0);

            State.resultChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Counts",
                        data,
                        backgroundColor: labels.map((_, i) => c.bars[i % c.bars.length]),
                        borderColor: labels.map((_, i) => c.barsBorder[i % c.barsBorder.length]),
                        borderWidth: 1.5,
                        borderRadius: 6,
                    }],
                },
                options: {
                    responsive: true,
                    animation: { duration: 800, easing: "easeOutQuart" },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: item => `Probability: ${((item.raw / total) * 100).toFixed(1)}%`,
                            },
                        },
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text, font: { family: "'Inter'" } } },
                        y: { grid: { color: c.grid }, ticks: { color: c.text, font: { family: "'Inter'" } },
                             title: { display: true, text: "Counts", color: c.text } },
                    },
                },
            });

            // Populate table
            const tbody = document.querySelector("#resultTable tbody");
            tbody.innerHTML = labels.map((lbl, i) =>
                `<tr><td><strong>|${lbl}⟩</strong></td><td>${data[i]}</td><td>${((data[i]/total)*100).toFixed(2)}%</td></tr>`
            ).join("");
        },

        renderDashboardChart() {
            const ctx = document.getElementById("dashboardChart");
            if (!ctx) return;
            if (State.dashboardChart) State.dashboardChart.destroy();
            const c = this.getColors();

            if (State.jobs.length === 0) {
                State.dashboardChart = new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: ["No data yet"],
                        datasets: [{ data: [1], backgroundColor: ["rgba(150,150,150,0.15)"], borderWidth: 0 }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: c.text } } },
                        cutout: "65%",
                    },
                });
                return;
            }

            // Aggregate last job results
            const lastJob = State.jobs.find(j => j.results);
            if (lastJob && lastJob.results && lastJob.results.counts) {
                const counts = lastJob.results.counts;
                const labels = Object.keys(counts);
                const data   = Object.values(counts);
                State.dashboardChart = new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: labels.map(l => `|${l}⟩`),
                        datasets: [{
                            data,
                            backgroundColor: labels.map((_, i) => c.bars[i % c.bars.length]),
                            borderWidth: 0,
                        }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { labels: { color: c.text, font: { family: "'Inter'" } } } },
                        cutout: "60%",
                        animation: { animateRotate: true, duration: 1000 },
                    },
                });
            }
        },

        updateTheme() {
            if (State.resultChart) {
                const counts = {};
                const ds = State.resultChart.data;
                ds.labels.forEach((l, i) => counts[l] = ds.datasets[0].data[i]);
                this.renderResultChart(counts);
            }
            this.renderDashboardChart();
            // Re-render security chart on theme change
            if (Security.benchmarkChart) {
                Security.renderBenchmarkChart();
            }
            if (Security.postureChart) {
                Security.loadPosture();
            }
            if (Security.timelineChart) {
                Security.loadTimeline();
            }
        },
    };

    // ======================================================================
    //  HERO PARTICLES CANVAS
    // ======================================================================
    const Particles = {
        init() {
            const canvas = document.getElementById("heroParticles");
            if (!canvas) return;
            const ctx = canvas.getContext("2d");
            const W = canvas.width, H = canvas.height;
            const pts = Array.from({ length: 40 }, () => ({
                x: Math.random() * W, y: Math.random() * H,
                vx: (Math.random() - 0.5) * 0.8, vy: (Math.random() - 0.5) * 0.8,
                r: Math.random() * 2 + 1,
            }));

            const draw = () => {
                ctx.clearRect(0, 0, W, H);
                const dark = document.documentElement.getAttribute("data-theme") === "dark";
                const color = dark ? "rgba(124,140,240," : "rgba(92,107,192,";

                pts.forEach(p => {
                    p.x += p.vx; p.y += p.vy;
                    if (p.x < 0 || p.x > W) p.vx *= -1;
                    if (p.y < 0 || p.y > H) p.vy *= -1;

                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fillStyle = `${color}0.7)`;
                    ctx.fill();
                });

                // Draw connections
                for (let i = 0; i < pts.length; i++) {
                    for (let j = i + 1; j < pts.length; j++) {
                        const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < 90) {
                            ctx.beginPath();
                            ctx.moveTo(pts[i].x, pts[i].y);
                            ctx.lineTo(pts[j].x, pts[j].y);
                            ctx.strokeStyle = `${color}${0.25 * (1 - dist / 90)})`;
                            ctx.lineWidth = 0.8;
                            ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(draw);
            };
            draw();
        },
    };

    // ======================================================================
    //  QUANTUM JOB MANAGEMENT
    // ======================================================================
    const Quantum = {
        async loadTargets() {
            try {
                const data = await API.get("/config/targets");
                State.targets = data.targets || [];
                const sel = document.getElementById("targetSelect");
                sel.innerHTML = State.targets.map(t =>
                    `<option value="${t.id}">${t.name}</option>`
                ).join("");
                document.getElementById("statTargets").textContent = State.targets.length;
            } catch { /* silent */ }
        },

        async loadCircuits() {
            try {
                const data = await API.get("/config/circuits");
                State.circuits = data.circuits || {};
                const row = document.getElementById("templateChips");
                row.innerHTML = Object.entries(State.circuits).map(([key, c]) =>
                    `<button class="chip" data-circuit="${key}" title="${c.description}">${c.name}</button>`
                ).join("");

                row.querySelectorAll(".chip").forEach(chip => {
                    chip.addEventListener("click", () => {
                        row.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
                        chip.classList.add("active");
                        const key = chip.dataset.circuit;
                        document.getElementById("circuitEditor").value = State.circuits[key].qasm;
                    });
                });
            } catch { /* silent */ }
        },

        async loadServices() {
            try {
                const data = await API.get("/config/services");
                const grid = document.getElementById("servicesGrid");
                const iconMap = {
                    atom: "atom", brain: "brain", search: "search",
                    microphone: "mic", "file-text": "file-text",
                    "shield-check": "shield-check",
                };
                grid.innerHTML = (data.services || []).map(s => `
                    <div class="service-card glass">
                        <div class="service-card__icon"><i data-lucide="${iconMap[s.icon] || s.icon}"></i></div>
                        <div>
                            <div class="service-card__name">${s.name}</div>
                            <div class="service-card__status ${s.status}">${
                                s.status === "active" ? "● Active" :
                                s.status === "pending" ? "◐ Connecting…" : "◌ Coming Soon"
                            }</div>
                        </div>
                    </div>
                `).join("");
                lucide.createIcons();
            } catch { /* silent */ }
        },

        async submitJob() {
            const qasm     = document.getElementById("circuitEditor").value.trim();
            const targetId = document.getElementById("targetSelect").value;
            const jobName  = document.getElementById("jobName").value.trim();
            const shots    = parseInt(document.getElementById("shotsInput").value, 10) || 100;

            if (!qasm)     { Toast.show("Please enter or select a circuit", "error"); return; }
            if (!targetId) { Toast.show("Please select a target backend", "error"); return; }

            const btn = document.getElementById("submitJobBtn");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Submitting…';
            lucide.createIcons();

            try {
                const result = await API.post("/jobs", {
                    circuit_qasm: qasm,
                    target_id: targetId,
                    job_name: jobName,
                    shots,
                });

                State.jobs.unshift(result);
                this.updateStats();
                this.updateJobHistory();
                this.updateRecentJobs();

                if (result.results && result.results.counts) {
                    this.showResults(result);
                }

                Toast.show(`Job submitted: ${result.name || result.id}`, "success");
                Charts.renderDashboardChart();
            } catch (e) {
                Toast.show(`Submission failed: ${e.message}`, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="rocket"></i> Submit Job';
                lucide.createIcons();
            }
        },

        showResults(job) {
            document.getElementById("resultPlaceholder").classList.add("hidden");
            document.getElementById("resultContainer").classList.remove("hidden");

            const meta = document.getElementById("resultMeta");
            const statusClass = job.status === "Demo Mode" ? "demo" :
                                job.status === "Error" ? "error" : "success";
            meta.innerHTML = `
                <span><strong>ID:</strong> ${job.id}</span>
                <span><strong>Target:</strong> ${job.target}</span>
                <span><strong>Shots:</strong> ${job.shots}</span>
                <span class="status-pill status-pill--${statusClass}">${job.status}</span>
            `;

            if (job.results && job.results.counts) {
                Charts.renderResultChart(job.results.counts);
            }
        },

        updateStats() {
            document.getElementById("statJobs").textContent = State.jobs.length;
            const totalShots = State.jobs.reduce((s, j) => s + (j.shots || 0), 0);
            document.getElementById("statShots").textContent = totalShots.toLocaleString();
            const completed = State.jobs.filter(j => j.results).length;
            document.getElementById("statCompleted").textContent = completed;
        },

        updateJobHistory() {
            const tbody = document.querySelector("#jobHistoryTable tbody");
            tbody.innerHTML = State.jobs.map(j => {
                const sc = j.status === "Demo Mode" ? "demo" :
                           j.status === "Error" ? "error" :
                           j.results ? "success" : "pending";
                return `<tr>
                    <td><code>${(j.id || "—").substring(0, 16)}</code></td>
                    <td>${j.name || "—"}</td>
                    <td>${j.target || "—"}</td>
                    <td>${j.shots || "—"}</td>
                    <td><span class="status-pill status-pill--${sc}">${j.status}</span></td>
                    <td>${j.submitted_at ? new Date(j.submitted_at).toLocaleTimeString() : "—"}</td>
                    <td>${j.results ? `<button class="btn btn--outline btn--sm" onclick="QDKApp.viewJob('${j.id}')">View</button>` : ""}</td>
                </tr>`;
            }).join("");
        },

        updateRecentJobs() {
            const list = document.getElementById("recentJobsList");
            if (State.jobs.length === 0) {
                list.innerHTML = `<p class="muted">No jobs yet. Submit your first quantum circuit!</p>`;
                return;
            }
            list.innerHTML = State.jobs.slice(0, 5).map(j => {
                const sc = j.status === "Demo Mode" ? "demo" :
                           j.status === "Error" ? "error" :
                           j.results ? "success" : "pending";
                return `<div class="job-item">
                    <span class="job-item__name">${j.name || j.id}</span>
                    <span class="job-item__info">
                        <span class="status-pill status-pill--${sc}">${j.status}</span>
                        <span>${j.shots} shots</span>
                    </span>
                </div>`;
            }).join("");
        },
    };

    // ======================================================================
    //  QUANTUM SECURITY MODULE
    // ======================================================================
    const Security = {
        benchmarkChart: null,
        threatData: null,
        pqcData: null,
        postureChart: null,
        timelineChart: null,
        hndlRiskChart: null,
        hndlTimelineChart: null,

        // --- Preset algorithm stacks for the scanner ---
        presets: {
            enterprise: ["RSA-2048", "AES-256", "SHA-256", "ECDSA", "ECDH", "3DES"],
            modern:     ["AES-256", "SHA-3", "ML-KEM", "ML-DSA", "ECDH"],
            legacy:     ["RSA-2048", "3DES", "AES-128", "SHA-256", "Diffie-Hellman"],
            symcrypt:   ["SymCrypt AES-GCM-256", "SymCrypt ML-KEM", "SymCrypt ML-DSA", "SymCrypt XMSS", "SymCrypt HMAC-SHA-256", "SymCrypt ECDSA", "SymCrypt RSA-OAEP"],
        },

        async init() {
            // Wire preset chips
            document.querySelectorAll(".scanner-presets .chip[data-preset]").forEach(chip => {
                chip.addEventListener("click", () => {
                    document.querySelectorAll(".scanner-presets .chip").forEach(c => c.classList.remove("active"));
                    chip.classList.add("active");
                    const preset = chip.dataset.preset;
                    if (this.presets[preset]) {
                        document.getElementById("scanInput").value = this.presets[preset].join("\n");
                    }
                });
            });

            // Wire buttons
            document.getElementById("runBenchmarkBtn")?.addEventListener("click", () => this.runBenchmark());
            document.getElementById("runScanBtn")?.addEventListener("click", () => this.runScan());
            document.getElementById("pqcTypeFilter")?.addEventListener("change", () => this.renderBenchmarkChart());

            // HNDL controls
            const hndlQY = document.getElementById("hndlQuantumYear");
            const hndlHY = document.getElementById("hndlHarvestYear");
            if (hndlQY) {
                hndlQY.addEventListener("input", () => {
                    document.getElementById("hndlQuantumYearLabel").textContent = hndlQY.value;
                });
            }
            if (hndlHY) {
                hndlHY.addEventListener("input", () => {
                    document.getElementById("hndlHarvestYearLabel").textContent = hndlHY.value;
                });
            }
            document.getElementById("hndlRunBtn")?.addEventListener("click", () => this.runHNDL());

            // Load data
            await Promise.all([
                this.loadThreats(),
                this.loadPqcAlgorithms(),
                this.loadPosture(),
                this.loadTimeline(),
            ]);
        },

        // --- Capability 1: Threat Dashboard ---
        async loadThreats() {
            try {
                this.threatData = await API.get("/security/threats");
                this.renderThreatMatrix();
                this.updateSecurityStats();
            } catch (e) {
                console.error("Failed to load threat data:", e);
            }
        },

        renderThreatMatrix() {
            if (!this.threatData) return;
            const tbody = document.querySelector("#threatMatrix tbody");
            tbody.innerHTML = this.threatData.algorithms.map(a => {
                const badgeClass = `threat-badge threat-badge--${a.threat_level}`;
                const qSec = a.quantum_security === 0
                    ? '<span style="color:var(--error);font-weight:700">0</span>'
                    : `${a.quantum_security}`;
                const isSymCrypt = a.engine === "SymCrypt" || a.algorithm.startsWith("SymCrypt");
                const rowClass = isSymCrypt ? ' class="symcrypt-row"' : '';
                const vulnClass = a.vulnerable_to && a.vulnerable_to.includes("Shor") ? 'color:var(--error);font-weight:600' :
                                  a.vulnerable_to && a.vulnerable_to.includes("Grover") ? 'color:var(--warning);font-weight:600' : '';
                return `<tr${rowClass}>
                    <td><strong>${isSymCrypt ? '🔐 ' : ''}${a.algorithm}</strong></td>
                    <td>${a.category}</td>
                    <td style="white-space:nowrap">${a.use_case || '—'}</td>
                    <td><span class="${badgeClass}">${a.threat_level}</span></td>
                    <td>${qSec}</td>
                    <td style="${vulnClass};white-space:nowrap">${a.vulnerable_to || '—'}</td>
                    <td style="white-space:nowrap">${a.timeline || '—'}</td>
                    <td>${a.recommendation || '—'}</td>
                </tr>`;
            }).join("");
        },

        updateSecurityStats() {
            if (!this.threatData) return;
            const s = this.threatData.summary;
            document.getElementById("secCritical").textContent = s.critical;
            document.getElementById("secWarning").textContent = s.warning;
            document.getElementById("secSafe").textContent = s.safe;
            // SymCrypt count
            const symCount = this.threatData.algorithms.filter(a =>
                a.engine === "SymCrypt" || a.algorithm.startsWith("SymCrypt")
            ).length;
            const symEl = document.getElementById("secSymCryptCount");
            if (symEl) symEl.textContent = symCount;
        },

        // --- Capability 2: PQC Benchmarks ---
        async loadPqcAlgorithms() {
            try {
                this.pqcData = await API.get("/security/pqc-algorithms");
                if (this.pqcData && this.pqcData.algorithms) {
                    document.getElementById("secPqcCount").textContent = this.pqcData.algorithms.length;
                }
                this.renderBenchmarkChart();
            } catch (e) {
                console.error("Failed to load PQC data:", e);
            }
        },

        renderBenchmarkChart() {
            if (!this.pqcData) return;
            const filter = document.getElementById("pqcTypeFilter").value;
            let algos = this.pqcData.algorithms;
            if (filter !== "all") {
                algos = algos.filter(a => a.type === filter);
            }

            const ctx = document.getElementById("pqcBenchmarkChart");
            if (!ctx) return;
            if (this.benchmarkChart) this.benchmarkChart.destroy();

            const c = Charts.getColors();
            const labels = algos.map(a => a.name);

            // Show key sizes (public_key_bytes) as horizontal bar chart
            const pubKeyData = algos.map(a => a.public_key_bytes);
            const sigOrCtData = algos.map(a => a.signature_bytes || a.ciphertext_bytes || 0);

            this.benchmarkChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Public Key (bytes)",
                            data: pubKeyData,
                            backgroundColor: "rgba(92,107,192,0.7)",
                            borderColor: "rgba(92,107,192,1)",
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                        {
                            label: "Signature / Ciphertext (bytes)",
                            data: sigOrCtData,
                            backgroundColor: "rgba(171,71,188,0.7)",
                            borderColor: "rgba(171,71,188,1)",
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                    ],
                },
                options: {
                    indexAxis: "y",
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: c.text, font: { family: "'Inter'", size: 10 } },
                            position: "top",
                        },
                        tooltip: {
                            callbacks: {
                                afterBody: (items) => {
                                    const idx = items[0].dataIndex;
                                    const algo = algos[idx];
                                    const lines = [];
                                    lines.push(`Security Level: ${algo.security_level}`);
                                    lines.push(`Standard: ${algo.standard}`);
                                    if (algo.keygen_us) lines.push(`KeyGen: ${algo.keygen_us} µs`);
                                    if (algo.encaps_us) lines.push(`Encaps: ${algo.encaps_us} µs`);
                                    if (algo.decaps_us) lines.push(`Decaps: ${algo.decaps_us} µs`);
                                    if (algo.sign_us) lines.push(`Sign: ${algo.sign_us} µs`);
                                    if (algo.verify_us) lines.push(`Verify: ${algo.verify_us} µs`);
                                    return lines;
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            grid: { color: c.grid },
                            ticks: { color: c.text, font: { family: "'Inter'", size: 10 } },
                            title: { display: true, text: "Bytes", color: c.text, font: { size: 10 } },
                        },
                        y: {
                            grid: { display: false },
                            ticks: { color: c.text, font: { family: "'Inter'", size: 10 } },
                        },
                    },
                },
            });
        },

        async runBenchmark() {
            const btn = document.getElementById("runBenchmarkBtn");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…';
            lucide.createIcons();

            try {
                const result = await API.post("/security/benchmark", {});
                // Update chart with benchmark results (includes jitter)
                if (result.results) {
                    this.pqcData.algorithms = result.results;
                    this.renderBenchmarkChart();
                    Toast.show(`Benchmark complete — ${result.results.length} algorithms tested`, "success");
                }
            } catch (e) {
                Toast.show("Benchmark failed: " + e.message, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="play"></i> Run Benchmark';
                lucide.createIcons();
            }
        },

        // --- Capability 3: Readiness Scanner ---
        async runScan() {
            const input = document.getElementById("scanInput").value.trim();
            if (!input) {
                Toast.show("Enter at least one algorithm to scan", "error");
                return;
            }

            const algorithms = input.split("\n").map(s => s.trim()).filter(Boolean);

            const btn = document.getElementById("runScanBtn");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Scanning…';
            lucide.createIcons();

            try {
                const result = await API.post("/security/scan", { algorithms });
                this.displayScanResults(result);
                Toast.show(`Scanned ${result.summary.total_scanned} algorithms — Grade: ${result.summary.grade}`, "info");
            } catch (e) {
                Toast.show("Scan failed: " + e.message, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="scan-line"></i> Scan Readiness';
                lucide.createIcons();
            }
        },

        displayScanResults(result) {
            const container = document.getElementById("scanResults");
            container.classList.remove("hidden");

            const { summary, findings } = result;

            // Update score circle
            const circle = document.getElementById("scoreCircle");
            circle.className = "score-circle grade-" + summary.grade.toLowerCase();
            document.getElementById("scoreValue").textContent = summary.readiness_score;
            document.getElementById("scoreGrade").textContent = `Grade ${summary.grade}`;
            document.getElementById("scoreVerdict").textContent = summary.verdict;

            // Render findings
            const findingsEl = document.getElementById("scanFindings");
            findingsEl.innerHTML = findings.map(f => {
                const badgeClass = `threat-badge threat-badge--${f.threat_level === "quantum-safe" ? "safe" : f.threat_level}`;
                return `<div class="scan-finding">
                    <div>
                        <span class="scan-finding__name">${f.algorithm}</span>
                        <span class="${badgeClass}" style="margin-left:0.4rem">${f.threat_level}</span>
                    </div>
                    <span class="scan-finding__rec">${f.recommendation}</span>
                </div>`;
            }).join("");
        },

        // --- Capability 4: Security Posture Radar ---
        async loadPosture() {
            try {
                const data = await API.get("/security/posture");
                this.renderPostureRadar(data);
            } catch (e) { console.error("Posture load:", e); }
        },

        renderPostureRadar(data) {
            const ctx = document.getElementById("secPostureRadar");
            if (!ctx) return;
            if (this.postureChart) this.postureChart.destroy();
            const c = Charts.getColors();

            this.postureChart = new Chart(ctx, {
                type: "radar",
                data: {
                    labels: data.dimensions.map(d => d.name),
                    datasets: [
                        {
                            label: "Current Posture",
                            data: data.dimensions.map(d => d.current_score),
                            backgroundColor: "rgba(229,57,53,0.15)",
                            borderColor: "rgba(229,57,53,0.8)",
                            pointBackgroundColor: "rgba(229,57,53,1)",
                            pointRadius: 5,
                            borderWidth: 2,
                        },
                        {
                            label: "Target (Post-PQC)",
                            data: data.dimensions.map(d => d.target_score),
                            backgroundColor: "rgba(67,160,71,0.1)",
                            borderColor: "rgba(67,160,71,0.6)",
                            pointBackgroundColor: "rgba(67,160,71,1)",
                            pointRadius: 4,
                            borderWidth: 2,
                            borderDash: [5, 3],
                        },
                    ],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200 },
                    plugins: { legend: { labels: { color: c.text, font: { size: 10 } } } },
                    scales: {
                        r: {
                            min: 0, max: 100,
                            grid: { color: c.grid },
                            angleLines: { color: c.grid },
                            pointLabels: { color: c.text, font: { size: 9.5, weight: 600 } },
                            ticks: { color: c.text, backdropColor: "transparent", stepSize: 25 },
                        },
                    },
                },
            });

            // Detail list
            const el = document.getElementById("postureDetails");
            if (el) {
                el.innerHTML = data.dimensions.map(d => {
                    const statusColor = d.status === "critical" ? "var(--error)" :
                                        d.status === "warning" ? "var(--warning)" : "var(--success)";
                    return `<div class="sec-posture-item">
                        <span class="sec-posture-item__name">${d.name}</span>
                        <span class="sec-posture-item__bar"><span class="sec-posture-item__fill" style="width:${d.current_score}%;background:${statusColor}"></span></span>
                        <span class="sec-posture-item__score" style="color:${statusColor}">${d.current_score}%</span>
                    </div>`;
                }).join("");
            }
        },

        // --- Capability 5: Quantum Threat Timeline ---
        async loadTimeline() {
            try {
                const data = await API.get("/security/timeline");
                this.renderTimeline(data);
            } catch (e) { console.error("Timeline load:", e); }
        },

        renderTimeline(data) {
            const ctx = document.getElementById("secTimelineChart");
            if (!ctx) return;
            if (this.timelineChart) this.timelineChart.destroy();
            const c = Charts.getColors();

            const qp = data.qubit_progression;
            this.timelineChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: qp.map(q => q.year.toString()),
                    datasets: [
                        {
                            label: "Physical Qubits",
                            data: qp.map(q => q.physical_qubits),
                            borderColor: "rgba(92,107,192,1)",
                            backgroundColor: "rgba(92,107,192,0.1)",
                            fill: true, tension: 0.3, pointRadius: 4,
                            yAxisID: "y",
                        },
                        {
                            label: "Logical Qubits",
                            data: qp.map(q => q.logical_qubits),
                            borderColor: "rgba(171,71,188,1)",
                            backgroundColor: "rgba(171,71,188,0.1)",
                            fill: true, tension: 0.3, pointRadius: 4,
                            yAxisID: "y",
                        },
                        {
                            label: "Threat Impact %",
                            data: data.milestones.map(m => m.threat_impact),
                            borderColor: "rgba(229,57,53,0.8)",
                            borderDash: [5, 3],
                            tension: 0.3, pointRadius: 3,
                            yAxisID: "y1",
                        },
                    ],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200 },
                    plugins: {
                        legend: { labels: { color: c.text, font: { size: 9 } } },
                        tooltip: {
                            callbacks: {
                                afterBody: (items) => {
                                    const year = parseInt(items[0].label);
                                    const ms = data.milestones.find(m => m.year === year);
                                    return ms ? [ms.event] : [];
                                },
                            },
                        },
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text, font: { size: 9 } } },
                        y: { type: "logarithmic", position: "left",
                             title: { display: true, text: "Qubits (log)", color: c.text, font: { size: 9 } },
                             grid: { color: c.grid }, ticks: { color: c.text, font: { size: 9 } } },
                        y1: { position: "right", min: 0, max: 100,
                              title: { display: true, text: "Threat %", color: c.text, font: { size: 9 } },
                              grid: { display: false }, ticks: { color: c.text, font: { size: 9 } } },
                    },
                },
            });

            // Milestones list
            const el = document.getElementById("timelineMilestones");
            if (el) {
                el.innerHTML = data.milestones.slice(-6).map(m => {
                    const catColors = { hardware: "var(--accent)", standards: "var(--success)",
                                        deployment: "var(--info)", projection: "var(--warning)" };
                    const color = catColors[m.category] || "var(--text-muted)";
                    const isPast = m.year <= 2026;
                    return `<div class="sec-timeline-item ${isPast ? '' : 'sec-timeline-item--future'}">
                        <span class="sec-timeline-dot" style="background:${color}"></span>
                        <span class="sec-timeline-year">${m.year}</span>
                        <span class="sec-timeline-event">${m.event}</span>
                    </div>`;
                }).join("");
            }
        },

        // --- Capability 6: HNDL Simulator ---
        async runHNDL() {
            const btn = document.getElementById("hndlRunBtn");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Simulating…';
            lucide.createIcons();

            const quantumYear = parseInt(document.getElementById("hndlQuantumYear").value, 10);
            const harvestYear = parseInt(document.getElementById("hndlHarvestYear").value, 10);

            try {
                const data = await API.post("/security/hndl", {
                    quantum_year: quantumYear,
                    harvest_start_year: harvestYear,
                });
                this.renderHNDLResults(data);
                Toast.show(`HNDL Simulation: ${data.summary.critical} critical, ${data.summary.total_estimated_harvested_tb} TB estimated harvested`, "info");
            } catch (e) {
                Toast.show("HNDL simulation failed: " + e.message, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="play"></i> Simulate HNDL Scenario';
                lucide.createIcons();
            }
        },

        renderHNDLResults(data) {
            document.getElementById("hndlResults").classList.remove("hidden");
            const c = Charts.getColors();
            const { scenario, categories, summary } = data;

            // Summary bar
            const summaryEl = document.getElementById("hndlSummary");
            const verdictColor = summary.avg_risk_score >= 60 ? "var(--error)" :
                                 summary.avg_risk_score >= 40 ? "var(--warning)" : "var(--success)";
            summaryEl.innerHTML = `
                <div class="hndl-summary__stats">
                    <div class="hndl-stat">
                        <span class="hndl-stat__value" style="color:var(--error)">${summary.critical}</span>
                        <span class="hndl-stat__label">Critical</span>
                    </div>
                    <div class="hndl-stat">
                        <span class="hndl-stat__value" style="color:var(--warning)">${summary.warning}</span>
                        <span class="hndl-stat__label">Warning</span>
                    </div>
                    <div class="hndl-stat">
                        <span class="hndl-stat__value" style="color:var(--success)">${summary.safe}</span>
                        <span class="hndl-stat__label">Safe</span>
                    </div>
                    <div class="hndl-stat">
                        <span class="hndl-stat__value">${summary.total_estimated_harvested_tb} TB</span>
                        <span class="hndl-stat__label">Estimated Harvested</span>
                    </div>
                    <div class="hndl-stat">
                        <span class="hndl-stat__value" style="color:${verdictColor}">${summary.avg_risk_score}%</span>
                        <span class="hndl-stat__label">Avg Risk</span>
                    </div>
                </div>
                <div class="hndl-summary__verdict" style="border-left:3px solid ${verdictColor}">
                    ${summary.verdict}
                </div>
            `;

            // Risk chart (horizontal bars per category)
            if (this.hndlRiskChart) this.hndlRiskChart.destroy();
            const ctx1 = document.getElementById("hndlRiskChart");
            this.hndlRiskChart = new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: categories.map(cat => cat.name),
                    datasets: [{
                        label: "HNDL Risk Score",
                        data: categories.map(cat => cat.risk_score),
                        backgroundColor: categories.map(cat =>
                            cat.status === "critical" ? "rgba(229,57,53,0.7)" :
                            cat.status === "warning" ? "rgba(255,183,77,0.7)" :
                            "rgba(67,160,71,0.7)"
                        ),
                        borderColor: categories.map(cat =>
                            cat.status === "critical" ? "rgba(229,57,53,1)" :
                            cat.status === "warning" ? "rgba(255,183,77,1)" :
                            "rgba(67,160,71,1)"
                        ),
                        borderWidth: 1.5,
                        borderRadius: 4,
                    }],
                },
                options: {
                    indexAxis: "y",
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1000, easing: "easeOutQuart" },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: (item) => {
                                    const cat = categories[item.dataIndex];
                                    return [
                                        `Sensitivity: ${cat.sensitivity}`,
                                        `Encryption: ${cat.current_encryption}`,
                                        `Harvested: ~${cat.estimated_harvested_tb} TB`,
                                        `Years exposed post-CRQC: ${cat.years_exposed_after_decrypt}`,
                                        cat.mitigation,
                                    ];
                                },
                            },
                        },
                    },
                    scales: {
                        x: { min: 0, max: 100,
                             title: { display: true, text: "Risk Score", color: c.text },
                             grid: { color: c.grid }, ticks: { color: c.text } },
                        y: { grid: { display: false }, ticks: { color: c.text, font: { size: 9 } } },
                    },
                },
            });

            // Category detail cards
            const catEl = document.getElementById("hndlCategories");
            catEl.innerHTML = categories.map(cat => {
                const statusColor = cat.status === "critical" ? "var(--error)" :
                                    cat.status === "warning" ? "var(--warning)" : "var(--success)";
                return `<div class="hndl-cat-card glass">
                    <div class="hndl-cat-card__header">
                        <i data-lucide="${cat.icon}"></i>
                        <strong>${cat.name}</strong>
                        <span class="threat-badge threat-badge--${cat.status}" style="margin-left:auto">${cat.status}</span>
                    </div>
                    <div class="hndl-cat-card__body">
                        <div class="hndl-cat-detail"><span>Encryption</span><span>${cat.current_encryption}</span></div>
                        <div class="hndl-cat-detail"><span>Secrecy Required</span><span>${cat.required_secrecy_years} years (until ${cat.secrecy_expires})</span></div>
                        <div class="hndl-cat-detail"><span>Harvested</span><span>~${cat.estimated_harvested_tb} TB over ${cat.harvest_duration_years} yrs</span></div>
                        <div class="hndl-cat-detail"><span>Exposed after CRQC</span><span style="color:${statusColor};font-weight:700">${cat.years_exposed_after_decrypt} years</span></div>
                    </div>
                    <div class="hndl-cat-card__risk">
                        <div class="hndl-cat-risk-bar"><div class="hndl-cat-risk-fill" style="width:${cat.risk_score}%;background:${statusColor}"></div></div>
                        <span style="color:${statusColor};font-weight:700;font-size:0.8rem">${cat.risk_score}%</span>
                    </div>
                    <div class="hndl-cat-card__action" style="color:${statusColor}">${cat.mitigation}</div>
                </div>`;
            }).join("");
            lucide.createIcons();

            // HNDL Timeline visualization
            if (this.hndlTimelineChart) this.hndlTimelineChart.destroy();
            const ctx2 = document.getElementById("hndlTimelineChart");
            const currentYear = scenario.current_year;
            const years = [];
            for (let y = scenario.harvest_start_year; y <= Math.max(scenario.quantum_year + 5, currentYear + 15); y++) {
                years.push(y);
            }
            // Build datasets: harvest period, danger zone, safe zone
            const harvestData = years.map(y => y >= scenario.harvest_start_year && y <= currentYear ? 40 : null);
            const storageData = years.map(y => y > currentYear && y < scenario.quantum_year ? 30 : null);
            const dangerData = years.map(y => y >= scenario.quantum_year ? 80 : null);

            this.hndlTimelineChart = new Chart(ctx2, {
                type: "bar",
                data: {
                    labels: years.map(String),
                    datasets: [
                        { label: "🔴 Harvesting Period", data: harvestData, backgroundColor: "rgba(229,57,53,0.6)", borderRadius: 2, barPercentage: 1, categoryPercentage: 1 },
                        { label: "📦 Data in Storage (encrypted)", data: storageData, backgroundColor: "rgba(255,183,77,0.5)", borderRadius: 2, barPercentage: 1, categoryPercentage: 1 },
                        { label: "⚡ CRQC Decryption Window", data: dangerData, backgroundColor: "rgba(156,39,176,0.6)", borderRadius: 2, barPercentage: 1, categoryPercentage: 1 },
                    ],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 800 },
                    plugins: {
                        legend: { labels: { color: c.text, font: { size: 9 } }, position: "top" },
                        tooltip: {
                            callbacks: {
                                afterLabel: (item) => {
                                    const year = parseInt(item.label);
                                    if (year === currentYear) return ["← Current Year"];
                                    if (year === scenario.quantum_year) return ["← CRQC arrives"];
                                    if (year === scenario.harvest_start_year) return ["← Harvesting begins"];
                                    return [];
                                },
                            },
                        },
                    },
                    scales: {
                        x: { stacked: true, grid: { display: false }, ticks: { color: c.text, font: { size: 9 } } },
                        y: { stacked: true, display: false },
                    },
                },
            });
        },
    };

    // ======================================================================
    //  CHEMISTRY LAB MODULE
    // ======================================================================
    const Chemistry = {
        charts: {},
        currentMolecule: null,
        moleculeData: null,
        molRotation: 0,
        molAnimFrame: null,

        async init() {
            // Load molecule list
            try {
                const data = await API.get("/chemistry/molecules");
                const sel = document.getElementById("chemMolSelect");
                (data.molecules || []).forEach(m => {
                    const opt = document.createElement("option");
                    opt.value = m.id;
                    opt.textContent = `${m.formula}  —  ${m.name}  (${m.n_atoms} atoms, ${m.n_electrons}e⁻)`;
                    sel.appendChild(opt);
                });
            } catch (e) { console.error("Chem init:", e); }

            // Wire molecule select
            document.getElementById("chemMolSelect").addEventListener("change", (e) => {
                this.selectMolecule(e.target.value);
            });

            // Wire buttons
            document.getElementById("chemRunSCF").addEventListener("click", () => this.runSCF());
            document.getElementById("chemRunAS").addEventListener("click", () => this.runActiveSpace());
            document.getElementById("chemRunStatePrep").addEventListener("click", () => this.runStatePrep());
            document.getElementById("chemRunQPE").addEventListener("click", () => this.runQPE());
            document.getElementById("chemRunCASCI").addEventListener("click", () => this.runCASCI());
            document.getElementById("chemRunAll").addEventListener("click", () => this.runFullPipeline());

            // Wire pipeline step clicks
            document.querySelectorAll(".chem-pipeline__step[data-step]").forEach(step => {
                step.addEventListener("click", () => this.scrollToStep(step.dataset.step));
            });
        },

        async selectMolecule(id) {
            if (!id) return;
            this.currentMolecule = id;

            // Enable buttons
            ["chemRunSCF","chemRunAS","chemRunStatePrep","chemRunQPE","chemRunCASCI","chemRunAll"].forEach(
                btnId => { document.getElementById(btnId).disabled = false; }
            );

            // Hide all result panels
            document.querySelectorAll(".chem-result-panel").forEach(p => p.classList.add("hidden"));

            // Reset pipeline
            document.querySelectorAll(".chem-pipeline__step").forEach(s => {
                s.classList.remove("active", "completed");
            });
            document.getElementById("pipeStep-molecule").classList.add("active");

            // Fetch molecule data
            try {
                const mol = await API.get(`/chemistry/molecules/${id}`);
                this.moleculeData = mol;
                this.renderMolecule(mol);
                this.renderMolInfo(mol);
                this.setPipelineStep("molecule", "completed");
                Toast.show(`Loaded ${mol.formula} — ${mol.name}`, "success");
            } catch (e) {
                Toast.show("Failed to load molecule", "error");
            }
        },

        renderMolInfo(mol) {
            const el = document.getElementById("molInfo");
            el.innerHTML = `
                <div class="chem-mol-props">
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">Formula</span><span class="chem-mol-prop__value">${mol.formula}</span></div>
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">Electrons</span><span class="chem-mol-prop__value">${mol.n_electrons}</span></div>
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">Orbitals</span><span class="chem-mol-prop__value">${mol.n_orbitals}</span></div>
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">Symmetry</span><span class="chem-mol-prop__value">${mol.symmetry}</span></div>
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">Basis</span><span class="chem-mol-prop__value">${mol.basis_set}</span></div>
                    <div class="chem-mol-prop"><span class="chem-mol-prop__label">HF Energy</span><span class="chem-mol-prop__value">${mol.reference_energies.hf?.toFixed(4) || '—'} Ha</span></div>
                </div>
                <p class="muted" style="margin-top:0.5rem;font-size:0.78rem">${mol.description}</p>
            `;
        },

        // ── 2.5D Molecule Renderer ──
        renderMolecule(mol) {
            const canvas = document.getElementById("molCanvas");
            const ctx = canvas.getContext("2d");
            if (this.molAnimFrame) cancelAnimationFrame(this.molAnimFrame);

            const W = canvas.width, H = canvas.height;
            const atoms = mol.atoms;
            const bonds = mol.bonds || [];

            // Element colors & radii
            const elemColors = { H: "#ffffff", C: "#333333", N: "#3050f8", O: "#ff0d0d", Li: "#b491c8", S: "#ffff30", F: "#90e050", Cl: "#1ff01f" };
            const elemRadii  = { H: 8, C: 14, N: 13, O: 13, Li: 16, S: 16, F: 11, Cl: 14 };
            const dark = () => document.documentElement.getAttribute("data-theme") === "dark";

            // Compute bounding box for scaling
            const xs = atoms.map(a => a.x), ys = atoms.map(a => a.y);
            const minX = Math.min(...xs), maxX = Math.max(...xs);
            const minY = Math.min(...ys), maxY = Math.max(...ys);
            const rangeX = maxX - minX || 1, rangeY = maxY - minY || 1;
            const scale = Math.min((W - 80) / rangeX, (H - 80) / rangeY, 80);
            const cx = W / 2, cy = H / 2;
            const midX = (minX + maxX) / 2, midY = (minY + maxY) / 2;

            const draw = () => {
                ctx.clearRect(0, 0, W, H);
                this.molRotation += 0.008;
                const cosA = Math.cos(this.molRotation);
                const sinA = Math.sin(this.molRotation);

                // Project atoms with rotation
                const projected = atoms.map(a => {
                    const rx = (a.x - midX);
                    const ry = (a.y - midY);
                    const rz = (a.z || 0);
                    const px = rx * cosA - rz * sinA;
                    const pz = rx * sinA + rz * cosA;
                    return {
                        sx: cx + px * scale,
                        sy: cy + ry * scale,
                        sz: pz,
                        element: a.element,
                    };
                });

                // Sort by depth
                const order = projected.map((p, i) => i).sort((a, b) => projected[a].sz - projected[b].sz);

                // Draw bonds first
                bonds.forEach(([i, j]) => {
                    const a = projected[i], b = projected[j];
                    const grad = ctx.createLinearGradient(a.sx, a.sy, b.sx, b.sy);
                    const ac = elemColors[a.element] || "#888";
                    const bc = elemColors[b.element] || "#888";
                    grad.addColorStop(0, ac);
                    grad.addColorStop(1, bc);
                    ctx.beginPath();
                    ctx.moveTo(a.sx, a.sy);
                    ctx.lineTo(b.sx, b.sy);
                    ctx.strokeStyle = dark() ? "rgba(160,170,255,0.5)" : "rgba(100,110,180,0.5)";
                    ctx.lineWidth = 2.5;
                    ctx.stroke();
                });

                // Draw atoms
                order.forEach(idx => {
                    const p = projected[idx];
                    const r = (elemRadii[p.element] || 12) * (1 + p.sz * 0.05);
                    const col = elemColors[p.element] || "#888";

                    // Glow
                    const glow = ctx.createRadialGradient(p.sx, p.sy, 0, p.sx, p.sy, r * 2.5);
                    glow.addColorStop(0, col + "40");
                    glow.addColorStop(1, "transparent");
                    ctx.beginPath();
                    ctx.arc(p.sx, p.sy, r * 2.5, 0, Math.PI * 2);
                    ctx.fillStyle = glow;
                    ctx.fill();

                    // Atom sphere
                    const grad = ctx.createRadialGradient(p.sx - r * 0.3, p.sy - r * 0.3, r * 0.1, p.sx, p.sy, r);
                    grad.addColorStop(0, "#fff");
                    grad.addColorStop(0.5, col);
                    grad.addColorStop(1, dark() ? "#111" : "#333");
                    ctx.beginPath();
                    ctx.arc(p.sx, p.sy, r, 0, Math.PI * 2);
                    ctx.fillStyle = grad;
                    ctx.fill();
                    ctx.strokeStyle = dark() ? "rgba(255,255,255,0.2)" : "rgba(0,0,0,0.15)";
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    // Label
                    ctx.fillStyle = dark() ? "#e0e0ff" : "#222";
                    ctx.font = "bold 10px Inter, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(p.element, p.sx, p.sy + r + 12);
                });

                this.molAnimFrame = requestAnimationFrame(draw);
            };
            draw();
        },

        // ── Pipeline Helpers ──
        setPipelineStep(step, state) {
            const el = document.getElementById(`pipeStep-${step}`);
            if (!el) return;
            el.classList.remove("active", "completed");
            if (state) el.classList.add(state);
        },

        scrollToStep(step) {
            const panelMap = {
                "molecule": null,
                "scf": "chemSCFPanel",
                "active-space": "chemASPanel",
                "state-prep": "chemStatePrepPanel",
                "qpe": "chemQPEPanel",
                "casci": "chemCASCIPanel",
            };
            const panelId = panelMap[step];
            if (panelId) {
                const el = document.getElementById(panelId);
                if (el && !el.classList.contains("hidden")) {
                    el.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }
        },

        async showProgress(label, pct) {
            const wrap = document.getElementById("chemProgress");
            const fill = document.getElementById("chemProgressFill");
            const lbl  = document.getElementById("chemProgressLabel");
            wrap.classList.remove("hidden");
            lbl.textContent = label;
            fill.style.width = pct + "%";
            await new Promise(r => setTimeout(r, 300));
        },

        hideProgress() {
            document.getElementById("chemProgress").classList.add("hidden");
        },

        destroyChart(key) {
            if (this.charts[key]) { this.charts[key].destroy(); this.charts[key] = null; }
        },

        // ── SCF ──
        async runSCF() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunSCF");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…'; lucide.createIcons();
            this.setPipelineStep("scf", "active");
            await this.showProgress("Running SCF / Hartree-Fock...", 30);

            try {
                const res = await API.post("/chemistry/scf", { molecule_id: this.currentMolecule });
                await this.showProgress("SCF converged!", 100);
                this.renderSCFResults(res);
                this.setPipelineStep("scf", "completed");
                Toast.show(`SCF converged in ${res.n_iterations} iterations — E = ${res.final_energy.toFixed(6)} Ha`, "success");
            } catch (e) {
                Toast.show("SCF failed: " + e.message, "error");
            } finally {
                this.hideProgress();
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="play"></i> Run SCF'; lucide.createIcons();
            }
        },

        renderSCFResults(res) {
            document.getElementById("chemSCFPanel").classList.remove("hidden");
            const c = Charts.getColors();

            // Convergence chart
            this.destroyChart("scfConv");
            const ctx1 = document.getElementById("scfConvergenceChart");
            this.charts.scfConv = new Chart(ctx1, {
                type: "line",
                data: {
                    labels: res.convergence.energies.map((_, i) => `${i + 1}`),
                    datasets: [{
                        label: "Total Energy (Ha)",
                        data: res.convergence.energies,
                        borderColor: "rgba(92,107,192,1)",
                        backgroundColor: "rgba(92,107,192,0.1)",
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 7,
                    }],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200, easing: "easeOutQuart" },
                    plugins: { legend: { labels: { color: c.text } } },
                    scales: {
                        x: { title: { display: true, text: "Iteration", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                        y: { title: { display: true, text: "Energy (Ha)", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                    },
                },
            });

            // Orbital energy chart
            this.destroyChart("orbE");
            const ctx2 = document.getElementById("orbitalEnergyChart");
            const occ = res.orbitals.occupancies;
            this.charts.orbE = new Chart(ctx2, {
                type: "bar",
                data: {
                    labels: res.orbitals.labels,
                    datasets: [{
                        label: "Orbital Energy (Ha)",
                        data: res.orbitals.energies,
                        backgroundColor: occ.map(o => o > 0 ? "rgba(67,160,71,0.7)" : "rgba(229,57,53,0.5)"),
                        borderColor: occ.map(o => o > 0 ? "rgba(67,160,71,1)" : "rgba(229,57,53,1)"),
                        borderWidth: 1.5,
                        borderRadius: 4,
                    }],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1000, easing: "easeOutBounce" },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: (item) => occ[item.dataIndex] > 0 ? "● Occupied" : "○ Virtual",
                            },
                        },
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text } },
                        y: { title: { display: true, text: "Energy (Ha)", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                    },
                },
            });

            // Summary
            document.getElementById("scfSummary").innerHTML = `
                <div class="chem-summary-grid">
                    <div><span class="chem-summary-label">Final Energy</span><strong>${res.final_energy.toFixed(6)} Ha</strong></div>
                    <div><span class="chem-summary-label">HOMO-LUMO Gap</span><strong>${res.homo_lumo_gap.toFixed(4)} Ha</strong></div>
                    <div><span class="chem-summary-label">Dipole</span><strong>${res.dipole_moment.toFixed(3)} D</strong></div>
                    <div><span class="chem-summary-label">Converged</span><strong style="color:var(--success)">✓ ${res.n_iterations} iter</strong></div>
                </div>
            `;

            setTimeout(() => this.scrollToStep("scf"), 200);
        },

        // ── Active Space ──
        async runActiveSpace() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunAS");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…'; lucide.createIcons();
            this.setPipelineStep("active-space", "active");
            await this.showProgress("Running Active Space Selection (AVAS)...", 50);

            try {
                const res = await API.post("/chemistry/active-space", { molecule_id: this.currentMolecule });
                await this.showProgress("Active space selected!", 100);
                this.renderASResults(res);
                this.setPipelineStep("active-space", "completed");
                Toast.show(`Active Space: (${res.n_active_electrons}e, ${res.n_active_orbitals}o) — ${res.n_determinants} determinants`, "success");
            } catch (e) {
                Toast.show("Active space failed: " + e.message, "error");
            } finally {
                this.hideProgress();
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="grid-3x3"></i> Active Space'; lucide.createIcons();
            }
        },

        renderASResults(res) {
            document.getElementById("chemASPanel").classList.remove("hidden");
            const c = Charts.getColors();

            // Occupation chart
            this.destroyChart("asOcc");
            const ctx1 = document.getElementById("asOccupationChart");
            this.charts.asOcc = new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: res.orbitals.indices.map(i => `Orb ${i+1}`),
                    datasets: [{
                        label: "Natural Occupation",
                        data: res.orbitals.occupations,
                        backgroundColor: res.orbitals.occupations.map(o =>
                            o > 1.8 ? "rgba(67,160,71,0.7)" :
                            o > 0.2 ? "rgba(255,183,77,0.7)" :
                            "rgba(229,57,53,0.5)"
                        ),
                        borderRadius: 4,
                        borderWidth: 1.5,
                        borderColor: res.orbitals.occupations.map(o =>
                            o > 1.8 ? "rgba(67,160,71,1)" :
                            o > 0.2 ? "rgba(255,183,77,1)" :
                            "rgba(229,57,53,1)"
                        ),
                    }],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1000, easing: "easeOutQuart" },
                    plugins: {
                        legend: { display: false },
                        tooltip: { callbacks: { afterLabel: (item) => `Character: ${res.orbitals.characters[item.dataIndex]}` } },
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text } },
                        y: { title: { display: true, text: "Occupation", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text }, min: 0, max: 2.1 },
                    },
                },
            });

            // Entropy chart
            this.destroyChart("asEnt");
            const ctx2 = document.getElementById("asEntropyChart");
            this.charts.asEnt = new Chart(ctx2, {
                type: "radar",
                data: {
                    labels: res.orbitals.indices.map(i => `Orb ${i+1}`),
                    datasets: [{
                        label: "Entanglement Entropy",
                        data: res.orbitals.entropies,
                        backgroundColor: "rgba(171,71,188,0.2)",
                        borderColor: "rgba(171,71,188,0.8)",
                        pointBackgroundColor: "rgba(171,71,188,1)",
                        pointRadius: 4,
                    }],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200 },
                    plugins: { legend: { labels: { color: c.text } } },
                    scales: {
                        r: {
                            grid: { color: c.grid },
                            angleLines: { color: c.grid },
                            pointLabels: { color: c.text, font: { size: 10 } },
                            ticks: { color: c.text, backdropColor: "transparent" },
                        },
                    },
                },
            });

            document.getElementById("asSummary").innerHTML = `
                <div class="chem-summary-grid">
                    <div><span class="chem-summary-label">Active Space</span><strong>(${res.n_active_electrons}e, ${res.n_active_orbitals}o)</strong></div>
                    <div><span class="chem-summary-label">Determinants</span><strong>${res.n_determinants.toLocaleString()}</strong></div>
                    <div><span class="chem-summary-label">Method</span><strong>${res.selection_criteria.method}</strong></div>
                    <div><span class="chem-summary-label">Est. CASCI Energy</span><strong>${res.estimated_casci_energy.toFixed(4)} Ha</strong></div>
                </div>
            `;
            setTimeout(() => this.scrollToStep("active-space"), 200);
        },

        // ── State Prep ──
        async runStatePrep() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunStatePrep");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…'; lucide.createIcons();
            this.setPipelineStep("state-prep", "active");
            await this.showProgress("Analyzing state preparation methods...", 40);

            try {
                const res = await API.post("/chemistry/state-prep", { molecule_id: this.currentMolecule });
                await this.showProgress("State prep analysis complete!", 100);
                this.renderStatePrepResults(res);
                this.setPipelineStep("state-prep", "completed");
                Toast.show(`Compared ${res.methods.length} ansatz methods — Qubit mapping: ${res.qubit_mapping}`, "success");
            } catch (e) {
                Toast.show("State prep failed: " + e.message, "error");
            } finally {
                this.hideProgress();
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="circuit-board"></i> State Prep'; lucide.createIcons();
            }
        },

        renderStatePrepResults(res) {
            document.getElementById("chemStatePrepPanel").classList.remove("hidden");
            const c = Charts.getColors();

            // Grouped bar chart: depth and CNOT count
            this.destroyChart("statePrep");
            const ctx = document.getElementById("statePrepChart");
            this.charts.statePrep = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: res.methods.map(m => m.name),
                    datasets: [
                        { label: "Circuit Depth", data: res.methods.map(m => m.circuit_depth), backgroundColor: "rgba(41,182,246,0.7)", borderRadius: 4 },
                        { label: "CNOT Count", data: res.methods.map(m => m.cnot_count), backgroundColor: "rgba(255,112,67,0.7)", borderRadius: 4 },
                    ],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1000 },
                    plugins: { legend: { labels: { color: c.text } } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text } },
                        y: { grid: { color: c.grid }, ticks: { color: c.text }, title: { display: true, text: "Count", color: c.text } },
                    },
                },
            });

            // Table
            const tbody = document.querySelector("#statePrepTable tbody");
            tbody.innerHTML = res.methods.map(m => `
                <tr>
                    <td><strong>${m.name}</strong></td>
                    <td>${m.n_qubits}</td>
                    <td>${m.circuit_depth.toLocaleString()}</td>
                    <td>${m.cnot_count.toLocaleString()}</td>
                    <td><span style="color:${m.fidelity > 0.95 ? 'var(--success)' : m.fidelity > 0.9 ? 'var(--warning)' : 'var(--error)'};font-weight:700">${(m.fidelity * 100).toFixed(1)}%</span></td>
                    <td>${m.energy.toFixed(4)}</td>
                </tr>
            `).join("");

            setTimeout(() => this.scrollToStep("state-prep"), 200);
        },

        // ── QPE ──
        async runQPE() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunQPE");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…'; lucide.createIcons();
            this.setPipelineStep("qpe", "active");
            await this.showProgress("Running Quantum Phase Estimation...", 20);

            const nBits = parseInt(document.getElementById("chemQPEBits").value, 10) || 8;
            try {
                await this.showProgress("Simulating QPE circuit...", 60);
                const res = await API.post("/chemistry/qpe", { molecule_id: this.currentMolecule, n_precision_qubits: nBits });
                await this.showProgress("QPE complete!", 100);
                this.renderQPEResults(res);
                this.setPipelineStep("qpe", "completed");
                const acc = res.chemical_accuracy ? "✓ Chemical accuracy" : "✗ Not chemical accuracy";
                Toast.show(`QPE: E = ${res.estimated_energy.toFixed(6)} Ha — ${acc}`, res.chemical_accuracy ? "success" : "info");
            } catch (e) {
                Toast.show("QPE failed: " + e.message, "error");
            } finally {
                this.hideProgress();
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="gauge"></i> Run QPE'; lucide.createIcons();
            }
        },

        renderQPEResults(res) {
            document.getElementById("chemQPEPanel").classList.remove("hidden");
            const c = Charts.getColors();

            // Histogram
            this.destroyChart("qpeHist");
            const ctx1 = document.getElementById("qpeHistogramChart");
            const maxCount = Math.max(...res.phase_histogram.counts);
            this.charts.qpeHist = new Chart(ctx1, {
                type: "bar",
                data: {
                    labels: res.phase_histogram.energies.map(e => e.toFixed(2)),
                    datasets: [{
                        label: "Counts",
                        data: res.phase_histogram.counts,
                        backgroundColor: res.phase_histogram.counts.map(cnt =>
                            cnt === maxCount ? "rgba(67,160,71,0.8)" : "rgba(92,107,192,0.6)"
                        ),
                        borderRadius: 3,
                    }],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200, easing: "easeOutQuart" },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: (item) => {
                                    const idx = item.dataIndex;
                                    return [
                                        `Phase: ${res.phase_histogram.phases[idx]}`,
                                        `Energy: ${res.phase_histogram.energies[idx].toFixed(6)} Ha`,
                                        `Prob: ${(res.phase_histogram.probabilities[idx] * 100).toFixed(1)}%`,
                                    ];
                                },
                            },
                        },
                    },
                    scales: {
                        x: { title: { display: true, text: "Energy (Ha)", color: c.text }, grid: { display: false }, ticks: { color: c.text, maxRotation: 45 } },
                        y: { title: { display: true, text: "Counts", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                    },
                },
            });

            // Precision convergence
            this.destroyChart("qpePrec");
            const ctx2 = document.getElementById("qpePrecisionChart");
            this.charts.qpePrec = new Chart(ctx2, {
                type: "line",
                data: {
                    labels: res.convergence_with_precision.map(p => `${p.n_bits}-bit`),
                    datasets: [
                        {
                            label: "Energy Estimate (Ha)",
                            data: res.convergence_with_precision.map(p => p.energy),
                            borderColor: "rgba(92,107,192,1)",
                            backgroundColor: "rgba(92,107,192,0.1)",
                            fill: true, tension: 0.3, pointRadius: 5,
                            yAxisID: "y",
                        },
                        {
                            label: "Error (Ha)",
                            data: res.convergence_with_precision.map(p => p.error),
                            borderColor: "rgba(229,57,53,0.8)",
                            borderDash: [5, 3],
                            tension: 0.3, pointRadius: 4,
                            yAxisID: "y1",
                        },
                    ],
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1000 },
                    plugins: { legend: { labels: { color: c.text } } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: c.text } },
                        y: { position: "left", title: { display: true, text: "Energy (Ha)", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                        y1: { position: "right", title: { display: true, text: "Error (Ha)", color: c.text }, grid: { display: false }, ticks: { color: c.text } },
                    },
                },
            });

            // Summary
            document.getElementById("qpeSummary").innerHTML = `
                <div class="chem-summary-grid">
                    <div><span class="chem-summary-label">Estimated Energy</span><strong>${res.estimated_energy.toFixed(6)} Ha</strong></div>
                    <div><span class="chem-summary-label">Exact (FCI)</span><strong>${res.exact_energy.toFixed(6)} Ha</strong></div>
                    <div><span class="chem-summary-label">Error</span><strong style="color:${res.chemical_accuracy ? 'var(--success)' : 'var(--error)'}">${res.energy_error.toFixed(6)} Ha</strong></div>
                    <div><span class="chem-summary-label">Chemical Accuracy</span><strong style="color:${res.chemical_accuracy ? 'var(--success)' : 'var(--error)'}">${res.chemical_accuracy ? '✓ Yes' : '✗ No'}</strong></div>
                    <div><span class="chem-summary-label">Total Qubits</span><strong>${res.resource_estimate.total_qubits}</strong></div>
                    <div><span class="chem-summary-label">T-Gates</span><strong>${res.resource_estimate.t_gates.toLocaleString()}</strong></div>
                    <div><span class="chem-summary-label">Circuit Depth</span><strong>${res.resource_estimate.circuit_depth.toLocaleString()}</strong></div>
                    <div><span class="chem-summary-label">Est. Runtime</span><strong>${res.resource_estimate.estimated_runtime_ms} ms</strong></div>
                </div>
            `;
            setTimeout(() => this.scrollToStep("qpe"), 200);
        },

        // ── CASCI ──
        async runCASCI() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunCASCI");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running…'; lucide.createIcons();
            this.setPipelineStep("casci", "active");
            await this.showProgress("Running CASCI multi-root calculation...", 40);

            try {
                const res = await API.post("/chemistry/casci", { molecule_id: this.currentMolecule });
                await this.showProgress("CASCI complete!", 100);
                this.renderCASCIResults(res);
                this.setPipelineStep("casci", "completed");
                Toast.show(`CASCI: ${res.n_roots} roots — Ground E = ${res.states[0].energy.toFixed(4)} Ha`, "success");
            } catch (e) {
                Toast.show("CASCI failed: " + e.message, "error");
            } finally {
                this.hideProgress();
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="layers"></i> CASCI'; lucide.createIcons();
            }
        },

        renderCASCIResults(res) {
            document.getElementById("chemCASCIPanel").classList.remove("hidden");
            const c = Charts.getColors();

            // Energy spectrum (horizontal bars for states)
            this.destroyChart("casciSpec");
            const ctx = document.getElementById("casciSpectrumChart");
            this.charts.casciSpec = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: res.states.map(s => `S${s.root} (${s.symmetry})`),
                    datasets: [{
                        label: "Energy (Ha)",
                        data: res.states.map(s => s.energy),
                        backgroundColor: res.states.map((_, i) => c.bars[i % c.bars.length]),
                        borderColor: res.states.map((_, i) => c.barsBorder[i % c.barsBorder.length]),
                        borderWidth: 1.5,
                        borderRadius: 6,
                    }],
                },
                options: {
                    indexAxis: "y",
                    responsive: true, maintainAspectRatio: false,
                    animation: { duration: 1200, easing: "easeOutQuart" },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                afterLabel: (item) => {
                                    const s = res.states[item.dataIndex];
                                    return [
                                        `Multiplicity: ${s.spin_multiplicity}`,
                                        s.excitation_energy_ev > 0 ? `Excitation: ${s.excitation_energy_ev.toFixed(3)} eV` : "Ground State",
                                        `CI Weight: ${(s.ci_weight * 100).toFixed(1)}%`,
                                    ];
                                },
                            },
                        },
                    },
                    scales: {
                        x: { title: { display: true, text: "Energy (Ha)", color: c.text }, grid: { color: c.grid }, ticks: { color: c.text } },
                        y: { grid: { display: false }, ticks: { color: c.text } },
                    },
                },
            });

            // State details
            const el = document.getElementById("casciStates");
            el.innerHTML = res.states.map(s => `
                <div class="chem-casci-state">
                    <div class="chem-casci-state__header">
                        <strong>State ${s.root}</strong>
                        <span class="chip chip--info" style="font-size:0.65rem;padding:0.1rem 0.4rem">${s.symmetry}</span>
                        <span style="font-size:0.75rem;color:var(--text-muted)">2S+1 = ${s.spin_multiplicity}</span>
                    </div>
                    <div class="chem-casci-state__energy">
                        <span>E = ${s.energy.toFixed(6)} Ha</span>
                        ${s.excitation_energy_ev > 0 ? `<span style="color:var(--accent)">ΔE = ${s.excitation_energy_ev.toFixed(3)} eV</span>` : '<span style="color:var(--success)">Ground State</span>'}
                    </div>
                    <div class="chem-casci-state__dets">
                        ${s.dominant_determinants.slice(0, 3).map(d => `
                            <span class="chem-det"><code>${d.occupation}</code> <small>(${d.coefficient.toFixed(3)})</small></span>
                        `).join("")}
                    </div>
                </div>
            `).join("") + `
                <div class="chem-summary-grid" style="margin-top:0.75rem">
                    <div><span class="chem-summary-label">Correlation Energy</span><strong>${res.correlation_energy.toFixed(6)} Ha</strong></div>
                    <div><span class="chem-summary-label">Determinants</span><strong>${res.n_determinants.toLocaleString()}</strong></div>
                    <div><span class="chem-summary-label">Wall Time</span><strong>${res.wall_time_ms.toFixed(0)} ms</strong></div>
                </div>
            `;
            setTimeout(() => this.scrollToStep("casci"), 200);
        },

        // ── Full Pipeline ──
        async runFullPipeline() {
            if (!this.currentMolecule) return;
            const btn = document.getElementById("chemRunAll");
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Running Pipeline…'; lucide.createIcons();

            const steps = [
                { fn: () => this.runSCF(), label: "SCF / Hartree-Fock", pct: 16 },
                { fn: () => this.runActiveSpace(), label: "Active Space Selection", pct: 33 },
                { fn: () => this.runStatePrep(), label: "State Preparation", pct: 50 },
                { fn: () => this.runQPE(), label: "QPE", pct: 75 },
                { fn: () => this.runCASCI(), label: "CASCI", pct: 100 },
            ];

            for (const step of steps) {
                await step.fn();
                await new Promise(r => setTimeout(r, 400)); // visual pause
            }

            Toast.show("Full quantum chemistry pipeline completed!", "success");
            btn.disabled = false;
            btn.innerHTML = '<i data-lucide="rocket"></i> Run Full Pipeline'; lucide.createIcons();
        },
    };

    // ======================================================================
    //  HEALTH CHECK
    // ======================================================================
    async function checkHealth() {
        const badge = document.getElementById("connectionBadge");
        const text  = document.getElementById("connectionText");
        try {
            const data = await API.get("/health");
            const q = data.services?.quantum;
            if (q && q.status === "connected") {
                badge.className = "status-badge glass connected";
                text.textContent = "Connected";
            } else {
                badge.className = "status-badge glass";
                text.textContent = "Demo Mode";
            }
        } catch {
            badge.className = "status-badge glass error";
            text.textContent = "Offline";
        }
    }

    // ======================================================================
    //  INIT
    // ======================================================================
    async function init() {
        Theme.init();
        Nav.init();
        Particles.init();
        lucide.createIcons();

        // Wire submit button
        document.getElementById("submitJobBtn").addEventListener("click", () => Quantum.submitJob());

        // Load data in parallel
        await Promise.all([
            Quantum.loadTargets(),
            Quantum.loadCircuits(),
            Quantum.loadServices(),
            Security.init(),
            Chemistry.init(),
            checkHealth(),
        ]);

        Charts.renderDashboardChart();
        populateDashInsights();
        lucide.createIcons();
    }

    // ── Dashboard Executive Insights ──────────────────────────────────
    async function populateDashInsights() {
        // --- PQC Readiness ---
        try {
            const threat = await API.get("/security/threats");
            if (threat && threat.algorithms) {
                const s = threat.summary || {};
                const total = threat.algorithms.length;
                const critical = s.critical || 0;
                const warning = s.warning || 0;
                const safe = s.safe || 0;
                const pqcSafe = threat.algorithms.filter(a =>
                    a.engine === "SymCrypt" || a.algorithm.startsWith("SymCrypt") ||
                    a.threat_level === "quantum-safe"
                ).length;

                // Calculate grade
                const score = total > 0
                    ? Math.round(((safe * 80 + pqcSafe * 100 + warning * 40) / (total * 100)) * 100)
                    : 0;
                let grade = "F";
                if (score >= 90) grade = "A+";
                else if (score >= 80) grade = "A";
                else if (score >= 70) grade = "B+";
                else if (score >= 60) grade = "B";
                else if (score >= 50) grade = "C";
                else if (score >= 40) grade = "D";

                const gradeEl = document.getElementById("insightGrade");
                if (gradeEl) gradeEl.textContent = grade;

                const el = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
                el("insightCritical", critical);
                el("insightWarning", warning);
                el("insightSafe", safe);
                el("insightPqcSafe", pqcSafe);

                const bar = document.getElementById("insightBar");
                if (bar) bar.style.width = score + "%";

                const cap = document.getElementById("insightCaption");
                if (cap) {
                    if (critical > 0) {
                        cap.textContent = `⚠ ${critical} algorithms need urgent PQC migration before CRQC arrival`;
                        cap.style.color = "var(--error)";
                    } else {
                        cap.textContent = "✓ All algorithms are quantum-safe or resistant";
                        cap.style.color = "var(--success)";
                    }
                }
            }
        } catch (e) { console.warn("Insight PQC:", e); }

        // --- Chemistry Capabilities ---
        try {
            const chem = await API.get("/chemistry/molecules");
            if (chem && chem.molecules) {
                const mols = chem.molecules;
                const el = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
                el("chemMolCount", mols.length);
                el("chemMaxElectrons", Math.max(...mols.map(m => m.n_electrons)));
                el("chemMaxOrbitals", Math.max(...mols.map(m => m.n_orbitals)));
            }
        } catch (e) { console.warn("Insight Chem:", e); }
    }

    // ======================================================================
    //  PUBLIC API  (accessible from HTML onclick handlers)
    // ======================================================================
    window.QDKApp = {
        navigateTo: (section) => Nav.goTo(section),
        viewJob: (id) => {
            const job = State.jobs.find(j => j.id === id);
            if (job) {
                Nav.goTo("quantum");
                Quantum.showResults(job);
            }
        },
    };

    // Kick off
    document.addEventListener("DOMContentLoaded", init);

    // Add spin animation for loaders
    const style = document.createElement("style");
    style.textContent = `@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}.spin{animation:spin 1s linear infinite}`;
    document.head.appendChild(style);
})();
