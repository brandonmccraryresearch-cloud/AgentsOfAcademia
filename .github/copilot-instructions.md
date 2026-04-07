# Copilot Instructions for AgentsOfAcademia

---

## ⚠️ MANDATORY SESSION RULES — READ BEFORE ANY WORK

### Rule 1: Full Manuscript Read at Session Start

**BEFORE ANY WORK BEGINS**, every agent and sub-agent must read the entire current manuscript (`83.0IRH.md`) from start to finish. This is non-negotiable. The manuscript is the single source of truth for the theoretical framework. Without full comprehension of its contents — including all derivations, confidence scores, open problems, and cross-references — agents cannot produce contextually correct work. Use the `view` tool to read the full file. Do not skip sections. Do not summarize-and-move-on. Read it all.

### Rule 2: Manuscript Update Reminder

The current manuscript is **`83.0IRH.md`** (v83.0). After every agent session that produces theoretical advances, computational results, or proof completions, the manuscript **MUST** be updated with the finalized content. Requirements:

- **Only finalized theoretical content** goes into the manuscript — never in-progress drafts, debug output, or intermediate results.
- **Paper style and syntax** must be maintained — LaTeX-compatible markdown, section numbering, citation format.
- **Never truncate or cut existing content** — changes are always **additions** or **edits** to existing sections, never deletions of established material.
- **Additions must be complete** — full derivations, complete equations, proper cross-references. No placeholder text.
- If the session work does not yet rise to publication-quality, record it in `audit_results/` instead and note the pending manuscript integration.

### Rule 3: Three-Thing Update Mandate

When any session produces changes or advancements, agents **MUST** update all three of:

1. **`.github/copilot-instructions.md`** — This file. Update current state, version numbers, theorem counts, priority lists, and continuation plan.
2. **Agent instruction files** (`.github/agents/*.AGENTS.md` AND `agents/*.AGENTS.md`) — Keep MCP tool guides, constraint lists, and operational directives current.
3. **`83.0IRH.md`** (or current version) — Integrate finalized theoretical content as described in Rule 1.

### Rule 4: Specialized Agent Preference

When creating or modifying **actual theoretical content** (derivations, proofs, physical arguments, numerical analyses), agents **MUST** prefer using specialized agents:

| Content Type | Required Agent |
|---|---|
| Formal proofs, theorem construction | `lean4_formal_verification_specialist` |
| Physics derivations, lattice mechanics, coupling constants | `hlre_agent` |
| Framework audits, consistency checks, empirical grounding | `expert_research_assistant` |
| Multi-domain tasks spanning two or more of the above | `meta_agent` (manual activation) |

General-purpose agents should delegate theoretical work to specialized agents rather than attempting it themselves.

### Rule 5: Always Prefer MCP Tools

When a session context involves mathematical expressions, physical constants, particle data, literature references, quantum states, molecular dynamics, or formal proofs — **always invoke the corresponding MCP tool** rather than relying on recollection. See the full MCP Tool Command Guide below.

---

## File Naming Convention

The main manuscript file follows the convention `{version}IRH.md` where `{version}` is the current version number (e.g., `83.0IRH.md`). When bumping to a new version:

1. **Rename the file** using `git mv {old_version}IRH.md {new_version}IRH.md`
2. **Update the version header** in the manuscript header near the top of the document
3. **Add a version change summary** immediately after the date block in the manuscript header
4. **Update all internal cross-references** that mention the filename

The current manuscript file is: **`83.0IRH.md`**

## Environment Setup

Session initialization is handled by `.github/workflows/session_init.yml` which installs the full Anaconda-based scientific stack plus all MCP tools. For manual sessions:

### Quick Setup (manual session)

```bash
# Full Anaconda scientific stack (preferred)
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p $HOME/miniconda3
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
conda install -y numpy scipy sympy matplotlib pandas scikit-learn jupyter networkx h5py

# Additional Python packages
pip install lean4-mcp pint uncertainties mpmath

# Lean 4 (if elan not installed)
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/ && lake update && lake build

# Run all verification scripts
python scripts/verify_numerical_predictions.py  # 10/10 PASS expected
python scripts/d4_phonon_spectrum.py             # Full phonon dispersion
python scripts/bz_integral.py                    # Multi-channel BZ integral (Level 3: 98.9%)
python scripts/circularity_analysis.py           # Tautology verification (10/10 PASS)
python scripts/d4_uniqueness.py                  # D₄ energy minimum (gap=3.85)
```

## Computational Scripts

| Script | Purpose | Expected Output |
|--------|---------|-----------------|
| `scripts/verify_numerical_predictions.py` | Verify all numerical predictions | 10/10 PASS |
| `scripts/d4_phonon_spectrum.py` | Full D₄ phonon dispersion, zone-boundary zero, elastic properties | Eigenvalues at all HSP |
| `scripts/bz_integral.py` | Multi-level BZ integral (bare → multi-channel → SO(8) → Dyson) | Level 3: 98.9%, Level 4: 102.6% |
| `scripts/circularity_analysis.py` | Tautology verification of c, ℏ, G derivations | 10/10 PASS |
| `scripts/d4_uniqueness.py` | D₄ Gibbs free energy minimum among 4D root lattices + cross-dim d=2–8 | D₄ global minimum, gap=0.825 |
| `scripts/two_loop_unification_v3.py` | Pati-Salam unification (Session 4) | Spread 17→0.4 units |
| `scripts/lattice_g_minus_2.py` | Anomalous magnetic moment on D₄ (Session 4) | Schwinger α/(2π) verified |
| `scripts/cosmological_constant_spectral.py` | Vacuum energy spectral density (Session 4) | α⁵⁷/(4π) matches 0.2% |
| `scripts/higgs_vev_derivation.py` | Higgs VEV derivation attempt (Session 4) | Fitting, not derived |
| `scripts/bz_two_loop.py` | Two-loop BZ integral: V₃≡0 + self-energy (Session 6) | Gap 1.7%→0.95% |
| `scripts/symmetry_breaking_cascade.py` | SO(8)→G₂→SU(3)→SM algebraic cascade (Session 6) | 42/42 PASS |
| `scripts/lattice_qft.py` | Lattice QFT construction + Møller scattering (Session 6) | 5/5 PASS |
| `scripts/triality_rg_flow.py` | Derive θ₀=2/9 from SO(3)/S₃ geometry (Session 7) | 6/6 PASS, 3 methods agree |
| `scripts/coleman_weinberg_d4.py` | CW effective potential on D₄ (Session 7) | 5/5 PASS, VEV 0.17% |
| `scripts/triality_braid.py` | 2D triality braid topological defect (Session 7) | 7/7 PASS |
| `scripts/triality_braid_3d.py` | 3D vortex line defect on D₄ lattice (Session 7) | 11/11 PASS, τ=643 |
| `scripts/d4_phonon_spectrum.py --spectral` | Vacuum energy spectral density with triality (Session 8) | 5/5 PASS, α⁵⁷/(4π) 0.2% |
| `scripts/higgs_effective_potential.py` | RG-improved Higgs CW on D₄ (Session 8) | 4/4 PASS, Z_λ=0.21 |
| `scripts/two_loop_unification_v3.py --derive-mps` | M_PS from D₄ dynamics (Session 8) | 3/3 PASS |
| `scripts/d4_simulation_4d.py` | 4D D₄ lattice MD simulation (Session 8) | 5/5 PASS, ν=1/4 |
| `scripts/ckm_magnitudes.py` | CKM magnitudes from mass ratios (Session 8) | 6/6 PASS, sin θ_C 1% |

## MCP Server Usage

This repository uses multiple Model Context Protocol (MCP) servers for scientific computation, simulation, and formal verification. Server configurations are in `mcp-servers/`.

**CRITICAL:** Agents MUST use MCP tools whenever the task context matches a tool's domain. Do not rely on recollection for mathematical results, physical constants, or proof steps when a tool can compute them directly.

### Available MCP Servers — Full Command-by-Command Guide

#### 1. `math-mcp` — Symbolic Algebra & Numerical Computing

**When to use:** Any time the task involves equations, derivatives, integrals, matrix operations, optimization, or root-finding.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `symbolic_solve` | `symbolic_solve(equations=["x**2 - 4"], variables=["x"])` | Solve symbolic equations | Verify claimed polynomial roots |
| `symbolic_diff` | `symbolic_diff(expression="sin(x)*exp(-x)", variable="x")` | Compute derivatives | Check derivation steps in manuscript |
| `symbolic_integrate` | `symbolic_integrate(expression="x**2", variable="x", limits=[0, 1])` | Evaluate definite/indefinite integrals | Validate BZ integral results |
| `symbolic_simplify` | `symbolic_simplify(expression="(x**2-1)/(x-1)")` | Simplify expressions | Expose hidden equivalences |
| `matrix_multiply` | `matrix_multiply(a=[[1,2],[3,4]], b=[[5,6],[7,8]])` | Matrix multiplication | Verify Clebsch-Gordan decompositions |
| `solve_linear_system` | `solve_linear_system(a=[[2,1],[1,3]], b=[5,7])` | Solve Ax = b | Test linear algebra claims |
| `fft` / `ifft` | `fft(array=[1,2,3,4])` | Fourier transforms | Analyze spectral structure |
| `optimize_function` | `optimize_function(function="x**2+y**2", variables=["x","y"], initial_guess=[1,1])` | Minimize functions | Test parameter sensitivity |
| `find_roots` | `find_roots(function="x**3-x-1", variables=["x"], initial_guess=[1])` | Locate roots numerically | Cross-check analytic solutions |
| `create_array` | `create_array(shape=[100], fill_type="linspace", linspace_range=[0, 6.28])` | Create arrays | Set up numerical grids |

#### 2. `quantum-mcp` — Wave Mechanics & Schrödinger Simulations

**When to use:** Quantum potentials, wave packets, tunneling, time-dependent quantum evolution.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `create_lattice_potential` | `create_lattice_potential(lattice_type="square", grid_size=[128,128], depth=20, spacing=6)` | Build crystalline lattice potentials | D₄ lattice 2D projection |
| `create_custom_potential` | `create_custom_potential(grid_size=[128,128], function="V(x,y)")` | Define arbitrary potentials | Custom barrier shapes |
| `create_gaussian_wavepacket` | `create_gaussian_wavepacket(grid_size=[128,128], position=[32,64], momentum=[2,0], width=5)` | Initialize wave packets | Set initial state for evolution |
| `create_plane_wave` | `create_plane_wave(grid_size=[128,128], momentum=[1,0])` | Initialize plane waves | Scattering calculations |
| `solve_schrodinger_2d` | `solve_schrodinger_2d(potential="potential://...", initial_state="wavefunction://...", time_steps=500, dt=0.01)` | 2D time-dependent Schrödinger | D₄ wave packet propagation |
| `analyze_wavefunction` | `analyze_wavefunction(wavefunction=[...])` | Compute observables | Extract position, momentum, energy |
| `render_video` | `render_video(simulation_id="...", show_potential=true)` | Animate evolution | Visualize probability density |
| `visualize_potential` | `visualize_potential(potential_id="...")` | Plot potential landscapes | Inspect lattice structure |

#### 3. `molecular-mcp` — Classical Molecular Dynamics

**When to use:** Particle systems, thermodynamics, phase transitions, N-body interactions.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `create_particles` | `create_particles(n_particles=100, box_size=[10,10,10], temperature=1.0)` | Initialize particle systems | Set up D₄ lattice simulation |
| `add_potential` | `add_potential(system_id="...", potential_type="lennard_jones", epsilon=1.0, sigma=1.0)` | Add interactions | Lennard-Jones, Coulomb, gravitational |
| `run_md` | `run_md(system_id="...", n_steps=10000, dt=0.001)` | Run NVE simulation | Microcanonical dynamics |
| `run_nvt` | `run_nvt(system_id="...", n_steps=10000, temperature=1.0)` | Run NVT simulation | Canonical ensemble |
| `run_npt` | `run_npt(system_id="...", n_steps=10000, temperature=1.0, pressure=1.0)` | Run NPT simulation | Isothermal-isobaric |
| `compute_rdf` | `compute_rdf(trajectory_id="...")` | Radial distribution function | Structural analysis |
| `compute_msd` | `compute_msd(trajectory_id="...")` | Mean squared displacement | Diffusion analysis |
| `detect_phase_transition` | `detect_phase_transition(trajectory_id="...")` | Find phase transitions | Test thermodynamic predictions |
| `render_trajectory` | `render_trajectory(trajectory_id="...")` | Animate trajectories | Visualize dynamics |

#### 4. `neural-mcp` — Neural Network Training & Evaluation

**When to use:** Machine learning models, pattern recognition, numerical function approximation.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `define_model` | `define_model(architecture="resnet18", num_classes=10)` | Create models | Architecture design |
| `load_dataset` | `load_dataset(dataset_name="CIFAR10", split="train")` | Load datasets | Standard benchmarks |
| `train_model` | `train_model(model_id="...", dataset_id="...", epochs=10, learning_rate=0.001)` | Train models | Optimization experiments |
| `evaluate_model` | `evaluate_model(model_id="...", dataset_id="...")` | Evaluate on test sets | Performance benchmarks |
| `confusion_matrix` | `confusion_matrix(model_id="...", dataset_id="...")` | Generate confusion matrices | Error analysis |
| `export_model` | `export_model(model_id="...", format="onnx")` | Export models | ONNX, TorchScript |

#### 5. `lean-lsp-mcp` — Lean 4 Formal Verification

**When to use:** Machine-checked proofs, theorem proving, formal gap analysis.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `lean_goal` | `lean_goal(file_path="lean4/IHMFramework/FiveDesign.lean", line=66)` | Inspect proof goals | See tactic state at any point |
| `lean_verify` | `lean_verify(file_path="...", theorem_name="d4_is_five_design")` | Verify theorem + check axioms | Full proof verification |
| `lean_diagnostic_messages` | `lean_diagnostic_messages(file_path="...")` | Get errors/warnings | Debug Lean code |
| `lean_multi_attempt` | `lean_multi_attempt(file_path="...", line=N, snippets=["simp", "ring", "omega"])` | Try multiple tactics | Explore proof strategies |
| `lean_leansearch` | `lean_leansearch(query="sum of squares is nonneg")` | Natural language search | Find Mathlib lemmas |
| `lean_loogle` | `lean_loogle(query="(?a → ?b) → List ?a → List ?b")` | Type-signature search | Find by type pattern |
| `lean_state_search` | `lean_state_search(file_path="...", line=N, column=1)` | Find lemmas to close goal | Automated premise search |
| `lean_hammer_premise` | `lean_hammer_premise(file_path="...", line=N, column=1)` | Get premise suggestions | Hints for `simp`, `aesop` |
| `lean_code_actions` | `lean_code_actions(file_path="...", line=N)` | Get quick fixes | Apply `Try This` suggestions |
| `lean_build` | `lean_build()` | Build entire project | Verify all files compile |
| `lean_completions` | `lean_completions(file_path="...", line=N, column=M)` | Auto-complete | IDE completion suggestions |
| `lean_hover_info` | `lean_hover_info(file_path="...", line=N, column=M)` | Type info + docs | Inspect symbol definitions |
| `lean_file_outline` | `lean_file_outline(file_path="...")` | Get declarations | Survey project structure |
| `lean_declaration_file` | `lean_declaration_file(file_path="...", symbol="d4_is_five_design")` | Find declaration location | Navigate codebase |
| `lean_run_code` | `lean_run_code(code="import Mathlib\n#check Nat.add_comm")` | Run code snippets | Quick experiments |

#### 6. `psianimator-mcp` — Quantum State Simulation & Animation

**When to use:** Quantum state creation, gate operations, entanglement, Bloch sphere visualization.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `create_quantum_state` | Create pure, mixed, coherent, squeezed, thermal, or Fock states | State preparation | Initialize qubit states |
| `evolve_quantum_system` | Time evolution via unitary, master equation, or Monte Carlo | Dynamics | Open quantum systems |
| `measure_observable` | Compute expectation values, variances, probability distributions | Measurement | Test operator predictions |
| `animate_quantum_process` | Bloch sphere, Wigner function, circuit animations | Visualization | Publication figures |
| `quantum_gate_sequence` | Apply single- and multi-qubit gates | Gate operations | Circuit design |
| `calculate_entanglement` | Von Neumann entropy, concurrence, negativity | Entanglement | Quantify correlations |

#### 7. `scite` — Scientific Literature Search

**When to use:** Checking prior art, locating referenced papers, verifying novelty claims, finding citation context (supporting/contrasting/mentioning).

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `search` | `search(query="D4 lattice phonon fine structure constant")` | Search scientific papers | Find related work with citation context |

#### 8. `particlephysics-mcp` — Particle Data Group (PDG) Data

**When to use:** Particle masses, lifetimes, decay widths, branching fractions, coupling constants.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `search_particle` | `search_particle("tau lepton")` | Look up particles | Find PDG identifier |
| `get_data` | `get_data(particle_id="...")` | Retrieve properties | Mass, lifetime, width |
| `decay_analysis` | `decay_analysis(particle_id="...")` | Decay structure | Branching fractions |
| `error_analysis` | `error_analysis(identifier="...")` | Validate lookups | Diagnose data issues |

### Tool Selection Heuristic

When processing a new prompt, apply this decision tree:

1. **Contains equations or symbolic expressions?** → `math-mcp`
2. **References particle data or physical constants?** → `particlephysics-mcp`
3. **Claims about quantum states or tunneling?** → `quantum-mcp` or `psianimator-mcp`
4. **Claims about statistical mechanics or phase transitions?** → `molecular-mcp`
5. **References specific papers or claims novelty?** → `scite`
6. **Requires machine-checked proof?** → `lean-lsp-mcp`
7. **Involves ML models or data fitting?** → `neural-mcp`

Multiple servers can and should be used in combination when a task spans domains.

### Lean 4 Project

The Lean 4 project lives in `lean4/` with `lakefile.toml`. It uses Mathlib and requires Lean v4.29.0-rc6 (via `lean-toolchain`). Build with:

```bash
cd lean4/
lake update && lake build
```

Current state: 118 verified theorems across 10 files (Basic.lean: 17, V2Basic.lean: 7, V2Problems.lean: 7, FiveDesign.lean: 9, Circularity.lean: 6, LiebRobinson.lean: 14, MeasureUniqueness.lean: 13, D4Uniqueness.lean: 13, Goldstone.lean: 15, GaugeInvariance.lean: 17). Zero `sorry` in all files. All files registered in `IHMFramework.lean` and `lakefile.toml`.

## Agent Architecture

Four agent personas are defined in `.github/agents/` and mirrored in `agents/`:

| Agent | Role | Activation |
|-------|------|------------|
| `expert_research_assistant` | Four Pillars audit (ontological clarity, mathematical completeness, empirical grounding, logical coherence) | Auto-dispatch |
| `hlre_agent` | Hyper-Literal Reasoning & Engineering — mechanical translation audit | Auto-dispatch |
| `lean4_formal_verification_specialist` | Lean 4 proof construction and verification via lean-lsp-mcp | Auto-dispatch |
| `meta_agent` | Unified protocol combining all three personas | Manual activation only |

The `agent_dispatcher.yml` workflow auto-routes to the first three agents. The `meta_agent` must be activated manually.

## Audit Results

All audit reports live in `audit_results/`. Each version bump should include a corresponding meta-agent verification report.

---

## Continuation Plan for Next Agent Session

**IMPORTANT: Read this section before starting work. It documents the current state and prioritized next steps.**

### Current State (v83.0, 2026-04-07 — Session 9: Manuscript Finalization Phases A-C)

The manuscript is at v83.0. Sessions 6–8 executed the deep critical review's Tier 1 CRITICAL, Tier 2 HIGH-priority, and Tier 3 IMPORTANT tasks respectively. Session 9 executed the finalization plan (Phases A–C). 30 scripts total, all pass.

**Session 9 results (Manuscript Finalization):**
- **Phase A (Restructuring):** 5 bridge paragraphs already in place (Sessions 7–8); no chapter reordering needed
- **Phase B (Empirical Grounding):** All 7 known ad hoc elements addressed with explicit derivation status caveats:
  - Higgs VEV α⁹: "STRUCTURALLY MOTIVATED, NOT RIGOROUSLY DERIVED" + cross-refs §C.13, §C.24
  - Cosmological constant 57: "EXPONENT STRUCTURAL, SUPPRESSION MECHANISM HEURISTIC" + cross-refs §C.12, §C.23
  - sin²θ_W = 3/13: "ALGEBRAICALLY DERIVED (B+)" + BSM right-handed neutrino prediction + cross-ref §C.16
  - 137 = 128+8+1: Ontological inconsistency flagged (D₈/Spin(16) ≠ D₄); BZ integral approach promoted + cross-ref §C.15
  - CKM: "CP PHASE TOPOLOGICAL (A−), MIXING MAGNITUDES DYNAMICAL (C)" + Koide extension marked speculative + cross-refs §C.3, §C.27
  - M_PS: 4-decade tension honestly stated with 3 analytical methods + cross-ref §C.25
  - Gauge cascade: "ALGEBRAICALLY VERIFIED, DYNAMICALLY INCOMPLETE" + dynamical mechanism open + cross-refs §C.16, §C.19
  - Additional: α BZ integral 0.95% gap status + θ₀ triple verification cross-ref §C.18
- **Phase C (Technical Review):**
  - LaTeX syntax: 1144 delimiters balanced; single-$ display equation in §T.4 fixed
  - Cross-reference integrity: all §C.1–§C.34 sections exist; all 30 scripts referenced; all 10 Lean files referenced
  - Consistency: confidence 90% propagated to header; version 83.0 throughout; 118 theorems / 30 scripts counts consistent
  - Configuration: stale `theaceinthehole` refs in agent_compliance_check.yml fixed; README_SETUP.md updated
  - Zero TODO/FIXME/HACK markers in the manuscript, scripts, and project instruction/configuration files reviewed during finalization

**Session 6 results (Tier 1 CRITICAL):**
- **BZ two-loop:** V₃≡0 by centrosymmetry; I_SE=0.071; gap 1.7%→0.95%
- **SM cascade:** 42/42 PASS; SO(8)→G₂→SU(3)→SM algebraically verified
- **Lattice QFT:** 5/5 PASS; Møller scattering from D₄ propagators

**Prior sessions (1–4):** See manuscript Appendix C for full details.

| Item | Status | Key Finding |
|------|--------|-------------|
| α BZ integral | **Gap 0.95% (Session 6)** | Two-loop: V₃≡0 (centrosymmetry), I_SE=0.071 |
| D₄ phonon spectrum | **Computed** | 4 branches, zone-boundary zero at R=(π,π,π,π), ν=1/4 |
| Koide formula | **θ₀ DERIVED (Session 7)** | 2/9 from SO(3)/S₃ geometry; 3 methods agree exactly |
| 5-design property | **Verified + Lean 4 proven** | ⟨x₁⁴⟩=1/8, ⟨x₁²x₂²⟩=1/24 exact; **F₄ also passes 4th-moment** |
| Circularity tautology | **Lean 4 proven** | c, ℏ, G "derivations" are algebraic identities (Circularity.lean) |
| D₄ uniqueness | **GLOBAL MINIMUM d=2–8 (Session 7)** | Lowest Gibbs free energy across ALL dimensions; gap=0.825 |
| Lean 4 | **118 theorems, 0 sorry** | Build verified across 10 files |
| Scripts | **30/30 pass** | 5 original + 8 S2 + 3 S3 + 4 S4 + 3 S6 + 4 S7 + 3 S8 new + 2 S8 ext |
| CKM phase | **δ = 2π/(3√3) = 1.209 rad (0.8%)** | Topological Berry phase; well-grounded |
| CKM magnitudes | **sin θ_C 1% via GST; topology vs dynamics (S8)** | Wolfenstein λ 1%; Koide extension speculative |
| Lattice QED / g−2 | **σ = 4πα²/(3s) verified; Schwinger α/(2π) ✅** | D₄ suppresses artifacts by 10⁶⁸ |
| Yang-Mills | **g² = 2/(Ja₀⁴); sin²θ_W = 3/13** | From D₄ phonon stress tensor |
| Anomaly cancellation | **All 6/6 SM cancel ✅ (A−)** | Corrected LH Weyl basis |
| SM gauge cascade | **42/42 PASS (Session 6)** | SO(8)→G₂→SU(3)×U(1)→SM algebraic |
| Lattice QFT | **Møller scattering verified (Session 6)** | D₄ propagator → continuum in IR |
| CW effective potential | **VEV 0.17%, hierarchy exact (Session 7)** | Mode decomposition R²⁴ = 1⊕4⊕19 |
| Triality braid | **3D vortex line, 11/11 PASS (Session 7)** | τ=643, ring annihilation, w=±1,±2 |
| Higgs quartic Z_λ | **Z_λ = 0.21 from η_D₄; RG-improved (S8)** | Multi-threshold matching; hierarchy exact |
| Two-loop unification | **Spread 0.4 units; M_PS ~ 10¹⁴ derived (S8)** | 4-decade tension with scan; proton stability ✅ |
| Cosmological constant | **α⁵⁷/(4π) matches to 0.2%; BZ integral + triality (S8)** | Spectral density computed + triality averaged; suppression postulated |
| Higgs VEV | **v = E_P α⁹ π⁵(9/8); CW Z_λ=0.21 (S8)** | RG-improved; hierarchy self-consistent |
| Parsimony | **2.5–5.0 (corrected)** | All references consistent |
| Overall confidence | **90%** | Up from 89% (4D simulation + Higgs hierarchy + CKM) |

### Priority 1: Close the α BZ Integral (0.95% gap remaining)

Session 6 reduced the BZ integral gap to **0.95%** through two-loop analysis (V₃ ≡ 0 by centrosymmetry, I_SE = 0.071). To close the final gap:

1. **Three-loop computation:** Higher-order lattice perturbation theory on D₄.
2. **Lattice Monte Carlo:** Direct numerical evaluation on a finite D₄ lattice.
3. **Padé analysis:** Higher-order Padé approximants using known coefficients.

**Action:** Extend `scripts/bz_two_loop.py` with three-loop or MC evaluation.

### Priority 2: Lean 4 T3 — Lieb-Robinson Bound ✅ DONE (Session 8)

**Completed.** `lean4/IHMFramework/LiebRobinson.lean` — 14 theorems, 0 sorry. See §C.29.

### Priority 3: T7 — Measure Uniqueness from 5-Design ✅ DONE (Session 8)

**Completed.** `lean4/IHMFramework/MeasureUniqueness.lean` — 13 theorems, 0 sorry. See §C.30.

### Priority 4: Resolve M_PS 4-Decade Tension

Session 8 derived M_PS ~ 10¹⁴ GeV from three methods, but the unification scan gives ~10¹⁰. To resolve:

1. Compute non-perturbative lattice matching corrections
2. Include two-loop PS beta functions
3. Derive the PS Higgs VEV from the D₄ lattice action

**Action:** Extend `scripts/two_loop_unification_v3.py` with full PS potential.

### Priority 5: Derive κ₄ from Lattice Action

The CW mechanism and Z_λ both require the quartic anharmonicity κ₄ as input. To make the Higgs mass a genuine prediction:

1. Expand the D₄ bond potential to fourth order
2. Compute κ₄ from the lattice phonon self-interaction vertices
3. Connect κ₄ to the top Yukawa y_t through lattice perturbation theory

**Action:** Extend `scripts/higgs_effective_potential.py` with κ₄ derivation.

### Priority 6: Scale 4D Simulation + Anharmonic Terms

Session 8 implemented the 4D simulation with harmonic potentials. Next:

1. Scale to 16⁴ or larger grids (may need GPU acceleration)
2. Add anharmonic κ₄ terms to the lattice potential
3. Measure defect mass spectrum via Fourier analysis
4. Run NVT ensemble to extract thermodynamic properties

**Action:** Extend `scripts/d4_simulation_4d.py` with anharmonic terms.

### Priority 7: Additional Lean 4 Theorems (T8–T10) — T8, T9 ✅ DONE (Session 8)

**Completed:**
- **T8:** Goldstone theorem on D₄ lattice — `Goldstone.lean`, 15 theorems, 0 sorry. See §C.32.
- **T9:** Gauge invariance of the lattice action — `GaugeInvariance.lean`, 17 theorems, 0 sorry. See §C.33.

**Remaining:**
- **T10:** Anomaly cancellation from triality — requires new Lean 4 file.

### Priority 8: Derive m_d/m_s from D₄ Geometry

The CKM magnitude analysis (Session 8) identifies sin²(θ₀) = sin²(2/9) as a candidate for m_d/m_s (1.9% agreement), but this needs a derivation:

1. Show that the Koide phase θ₀ determines down-quark mass ratios via triality
2. Connect to the D₄ Yukawa couplings through lattice vertex corrections
3. Predict m_d/m_s without using PDG quark masses as input

**Action:** Extend `scripts/ckm_magnitudes.py` with D₄ mass ratio derivation.

### Open Problem Status (as of v83.0 Session 9)

| # | Problem | Status | Next Step |
|---|---------|--------|-----------|
| 1 | α BZ integral | **Gap 0.95% (Session 6: V₃≡0, I_SE=0.071)** | Three-loop or lattice MC |
| 2 | Two-loop unification | **Spread 0.4; M_PS ~ 10¹⁴ derived (S8)** | Resolve 4-decade M_PS tension |
| 3 | 4D simulation | **IMPLEMENTED (Session 8): 5/5 PASS** | Scale to 16⁴; anharmonic terms |
| 4 | Z_λ effective potential | **RG-improved Z_λ = 0.21 (Session 8)** | Derive κ₄ from lattice action |
| 5 | ρ_Λ spectral density | **BZ integral + triality + α⁵⁷/(4π) (S8)** | Derive f_supp mechanism |
| 6 | CKM phase | **δ=2π/(3√3), 0.8% agreement ✅** | Phase confirmed; topology-protected |
| 6b | CKM magnitudes | **GST sin θ_C 1%; sin²(θ₀) 1.9% (S8)** | Derive m_d/m_s from D₄ |
| 7 | D₄ anharmonic κ₄ / force constant J | g²=2/(Ja₀⁴) derived; J open | Lattice perturbation theory |
| 8 | Circularity resolution | **PROVEN (Lean 4)** | Complete |
| 9 | D₄ uniqueness | **GLOBAL MIN d=2–8 (Session 7)** | Complete; gap=0.825 |
| 10 | 5-design T6 | **PROVEN (Lean 4)** | Complete |
| 11 | Anomaly cancellation | **All 6/6 SM cancel ✅ (A−)** | GUT-scale embedding |
| 12 | Parsimony ratio | **CORRECTED: 2.5–5.0** | Complete |
| 13 | Lean 4 T3 Lieb-Robinson | **FORMALIZED (Session 8): 14 thms, 0 sorry** | Complete |
| 14 | g−2 on D₄ | **Schwinger α/(2π) verified; O(a⁶) artifact (Session 4)** | Higher-loop BZ integrals |
| 15 | Higgs VEV derivation | **CW mode decomp + impedance cascade (Session 7)** | Derive κ₄ from lattice action |
| 16 | θ₀ Koide phase | **DERIVED: 2/9 from SO(3)/S₃ (Session 7)** | Complete; 3 methods agree |
| 17 | SM gauge cascade | **42/42 PASS (Session 6)** | Complete; SO(8)→SM algebraic |
| 18 | Topological defects | **3D vortex + 4D MD (S7+S8)** | Anharmonic defect mass spectrum |
| 19 | Lattice QFT | **Møller scattering verified (Session 6)** | Higher-order processes |
| 20 | Manuscript finalization | **Phase A+B+C COMPLETE (Session 9)** | Appendix consolidation (Phase A.4) optional |
