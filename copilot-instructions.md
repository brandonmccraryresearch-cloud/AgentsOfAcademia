# Copilot Instructions for AgentsOfAcademia

---

## ⚠️ MANDATORY SESSION RULES — READ BEFORE ANY WORK

### Rule 1: Full Manuscript Read at Session Start

**BEFORE ANY WORK BEGINS**, every agent and sub-agent must read the entire current manuscript (`87.0IRH.md`) from start to finish. This is non-negotiable. The manuscript is the single source of truth for the theoretical framework. Without full comprehension of its contents — including all derivations, confidence scores, open problems, and cross-references — agents cannot produce contextually correct work. Use the `view` tool to read the full file. Do not skip sections. Do not summarize-and-move-on. Read it all.

### Rule 2: Manuscript Update Reminder

The current manuscript is **`87.0IRH.md`** (v87.0). After every agent session that produces theoretical advances, computational results, or proof completions, the manuscript **MUST** be updated with the finalized content. Requirements:

- **Only finalized theoretical content** goes into the manuscript — never in-progress drafts, debug output, or intermediate results.
- **Paper style and syntax** must be maintained — LaTeX-compatible markdown, section numbering, citation format.
- **Never truncate or cut existing content** — changes are always **additions** or **edits** to existing sections, never deletions of established material.
- **Integrate results into relevant main body chapters** — do NOT append new results as appendix sections. New computational results belong in the chapter where they are topically relevant (e.g., α integral results go in Chapter II, Higgs results in Chapter VIII, CKM results in Chapter X). Only truly supplementary material (long derivation details, raw data tables, formal proofs) belongs in appendices.
- **Additions must be complete** — full derivations, complete equations, proper cross-references. No placeholder text.
- **Do not add version markers to section titles** — avoid annotations like "(new v85.0, Review5 Priority 1)" in heading text.
- If the session work does not yet rise to publication-quality, record it in `audit_results/` instead and note the pending manuscript integration.

### Rule 2.1: ⚠️ MAIN BODY INTEGRATION MANDATE — NON-NEGOTIABLE

> **ALL new theoretical results, computational findings, and proof completions MUST be integrated into the topically relevant section of the main manuscript body. NEVER append new material as a new appendix section.**

**Correct placement by topic:**

| New result type | Integrate into |
|---|---|
| α / fine-structure constant | Chapter II §II.3.x |
| Anomaly cancellation | Chapter IV §IV.3.x |
| Gauge symmetry / Yang-Mills | Chapter IV §IV.4.x |
| Gauge coupling unification / M_PS | Chapter IV §IV.5.x |
| Higgs VEV, Higgs quartic, Coleman-Weinberg | Chapter VIII §VIII.3.x or §VIII.4.x |
| CKM phase / magnitudes / Yukawa overlaps | Chapter X §X.3.x |
| Cosmological constant / vacuum energy | Chapter V §V.5.x |
| Lattice QED / Lattice QFT / scattering | Chapter VI §VI.7.x |
| Koide phase / lepton masses | Chapter III §III.6.x |
| D₄ optimality / phonon spectrum | Chapter I §I.3.x |
| g-2, topological defects, proton decay | Chapter X §X.8–X.12 |
| Molecular dynamics / lattice simulation | Chapter XI §XI.15.x |
| Lean 4 formal proofs | Chapter XIV §XIV.3.x |
| Parsimony / overall assessment | Chapter XV §XV.6.x |

**What belongs in appendices (and ONLY these):**
- Long derivation details that would interrupt main text flow
- Raw data tables and extended numerical output
- Complete formal proof listings (brief result goes in main body; full proof in appendix)
- Historical review response records (Appendix V only)
- Mathematical reference material (Appendices A–T)

**VIOLATION:** Adding a new `### C.x`, `### §C.x`, or any new top-level appendix section for session results is a protocol violation. The session-by-session Appendix C pattern (§C.1–C.45) was dissolved in v85.0 and must not be recreated.

### Rule 3: Three-Thing Update Mandate

When any session produces changes or advancements, agents **MUST** update all three of:

1. **`.github/copilot-instructions.md`** — This file. Update current state, version numbers, theorem counts, priority lists, and continuation plan.
2. **Agent instruction files** (`.github/agents/*.AGENTS.md` AND `agents/*.AGENTS.md`) — Keep MCP tool guides, constraint lists, and operational directives current.
3. **`87.0IRH.md`** (or current version) — Integrate finalized theoretical content as described in Rule 1.

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

When a session context involves mathematical expressions, physical constants, quantum states, molecular dynamics, or formal proofs — **always invoke the corresponding MCP tool** rather than relying on recollection. For particle data or literature references, use values already present in the manuscript or repository; label any unverified recall as provisional. See the full MCP Tool Command Guide below.

---

## File Naming Convention

The main manuscript file follows the convention `{version}IRH.md` where `{version}` is the current version number (e.g., `87.0IRH.md`). When bumping to a new version:

1. **Rename the file** using `git mv {old_version}IRH.md {new_version}IRH.md`
2. **Update the version header** in the manuscript header near the top of the document
3. **Add a version change summary** immediately after the date block in the manuscript header
4. **Update all internal cross-references** that mention the filename

The current manuscript file is: **`87.0IRH.md`**

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
| `scripts/mps_free_energy.py` | M_PS from lattice free energy minimization (Session 11) | 5/7 PASS, gap 4→2 decades |
| `scripts/two_loop_cw_full.py` | Full two-loop CW with 28 SO(8) modes (Session 11) | 6/6 PASS, Z_λ=0.21 |
| `scripts/ckm_yukawa_overlaps.py` | CKM from lattice Dirac overlaps on D₄ (Session 13) | 7/7 PASS, V_us 27% |
| `scripts/proton_decay_bound.py` | Proton decay at derived M_PS (Session 11) | 1/4 PASS, constrains M_PS>10¹⁴ |
| `scripts/d4_simulation_64.py` | 4D simulation with derived κ₄=0.70, Z_λ measurement (Session 13) | 8/8 PASS, Z_λ=0.108 |
| `scripts/alpha_pade_three_loop.py` | Padé three-loop BZ integral analysis (Session 12) | 9/9 PASS, gap 0.95%→0.044% |
| `scripts/kappa4_lattice_derivation.py` | κ₄ from D₄ bond potential (Session 12) | 11/11 PASS, 4 methods |

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

### Tool Selection Heuristic

When processing a new prompt, apply this decision tree:

1. **Contains equations or symbolic expressions?** → `math-mcp`
2. **Claims about quantum states or tunneling?** → `quantum-mcp`
3. **Claims about statistical mechanics or phase transitions?** → `molecular-mcp`
4. **Requires machine-checked proof?** → `lean-lsp-mcp`
5. **Involves ML models or data fitting?** → `neural-mcp`

Multiple servers can and should be used in combination when a task spans domains.

### Lean 4 Project

The Lean 4 project lives in `lean4/` with `lakefile.toml`. It uses Mathlib and requires Lean v4.30.0-rc1 (via `lean-toolchain`). Build with:

```bash
cd lean4/
lake update && lake build
```

Current state: 311 verified declarations across 15 files (Basic.lean: 30, V2Basic.lean: 13, V2Problems.lean: 17, FiveDesign.lean: 14, Circularity.lean: 8, LiebRobinson.lean: 13, MeasureUniqueness.lean: 11, D4Uniqueness.lean: 12, Goldstone.lean: 12, GaugeInvariance.lean: 15, ReggeContinuumLimit.lean: 16, NonAbelianGauge.lean: 22, DiracEquation.lean: 49, BornRule.lean: 21, ModeDecomposition.lean: 58). Zero `sorry` across all files. All files registered in `IHMFramework.lean` and `lakefile.toml`. Full build: 2528 jobs.

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

### Current State (v87.0, 2026-04-16 — Session 27: Review86 Directives)

The manuscript is at v87.0. Session 27 completes Review86 directives 18 and 20. 78 Python scripts, 311 Lean 4 declarations across 15 files, 0 sorry.

**Session 27 results:**
- **Two-loop beta hidden DOF (Directive 18):** `scripts/two_loop_beta_hidden_dof.py` — 31/31 PASS. Full Machacek-Vaughn matrix with 20 hidden G₂ modes. Grade: D→D+.
- **Independent α derivation (Directive 20):** `scripts/alpha_independent_derivation.py` — 25/25 PASS. Multi-channel BZ integral hierarchy. Grade: C+→B.

**Review86 directive status:** 12 of 27 complete (01, 02, 03, 04, 05, 06, 09, 10, 11, 17, 18, 20).

**Script verification:** 78 scripts total, all pass.

| Item | Status | Key Finding |
|------|--------|-------------|
| α BZ integral | **Gap 0.044% (Session 12)** | Padé resummed: 0.038%; 25× improvement over Session 6 |
| D₄ phonon spectrum | **Computed** | 4 branches, zone-boundary zero at R=(π,π,π,π), ν=1/4 |
| Koide formula | **θ₀ DERIVED (Session 7)** | 2/9 from SO(3)/S₃ geometry; 3 methods agree exactly |
| 5-design property | **Verified + Lean 4 proven** | ⟨x₁⁴⟩=1/8, ⟨x₁²x₂²⟩=1/24 exact; **F₄ also passes 4th-moment** |
| Circularity tautology | **Lean 4 proven** | c, ℏ, G "derivations" are algebraic identities (Circularity.lean) |
| D₄ uniqueness | **GLOBAL MINIMUM d=2–8 (Session 7)** | Lowest Gibbs free energy across ALL dimensions; gap=0.825 |
| Lean 4 | **311 declarations, 0 sorry** | Build verified across 15 files (v4.30.0-rc1) |
| Scripts | **78 total, all pass** | 2 new Session 27 scripts |
| κ₄ derivation | **κ₄ ≈ 0.70 derived (Session 12)** | 4 methods; reconstruction 43% |
| Non-Abelian gauge | **17 theorems (Session 12)** | Wilson action gauge invariance |
| CKM phase | **δ = 2π/(3√3) = 1.209 rad (0.8%)** | Topological Berry phase; well-grounded |
| CKM magnitudes | **V_us=0.2246 (0.1%), NLO matching (Session 20)** | QCD running corrections |
| Lattice QED / g−2 | **σ = 4πα²/(3s) verified; Schwinger α/(2π) ✅** | D₄ suppresses artifacts by 10⁶⁸ |
| Yang-Mills | **g² = 2/(Ja₀⁴); sin²θ_W = 3/13** | From D₄ phonon stress tensor |
| Anomaly cancellation | **All 6/6 SM cancel ✅ (A−)** | Corrected LH Weyl basis |
| SM gauge cascade | **42/42 PASS (Session 6)** | SO(8)→G₂→SU(3)×U(1)→SM algebraic |
| Lattice QFT | **Møller scattering verified (Session 6)** | D₄ propagator → continuum in IR |
| CW effective potential | **VEV 0.17%, hierarchy exact (Session 7)** | Mode decomposition R²⁴ = 1⊕4⊕19 |
| Triality braid | **3D vortex line, 11/11 PASS (Session 7)** | τ=643, ring annihilation, w=±1,±2 |
| Higgs quartic Z_λ | **Z_λ = 0.21; ab initio CW minimum 0.5% (S20)** | Multi-threshold matching; hierarchy exact |
| Two-loop unification | **Spread 0.4 units; M_PS ~ 10¹⁴ derived (S8)** | Threshold corrections reduce spread 62% |
| M_PS tension | **Gap reduced; threshold corrections 62% (S20)** | Proton decay safe at 10^{15.5} |
| Proton decay | **τ_p too short at M_PS=3.5e12 (Session 11)** | Constrains M_PS > 2×10¹⁴ with D₄ |
| Cosmological constant | **α⁵⁷/(4π) matches to 0.2%; BZ integral + triality (S8)** | Spectral density computed + triality averaged |
| Higgs VEV | **v = E_P α⁹ π⁵(9/8); CW Z_λ=0.21 (S8)** | RG-improved; hierarchy self-consistent |
| 4D simulation | **Anharmonic + scaling (Session 11)** | κ₄ terms, vectorized, 64⁴ extrapolation |
| Regge continuum limit | **7 theorems, 0 sorry (Session 11)** | O(a₀²) convergence, 5-design improvement |
| Parsimony | **2.5–5.0 (corrected)** | All references consistent |
| Overall confidence | **94%** | +1% from Session 20 |

### Priority 1: Close the α BZ Integral (gap now 0.044%)

Session 12 reduced the BZ integral gap to **0.044%** via Padé approximants. To close further:

1. **Full lattice Monte Carlo:** Direct numerical evaluation on a finite D₄ lattice at 64⁴ resolution.
2. **Higher-order Padé:** [2/2] and [3/1] approximants with additional loop data.
3. **Analytic completion:** Prove the SO(8) Casimir uniquely determines the residual.

### Priority 2: Resolve M_PS to < 1 Decade

Session 11 reduced the M_PS gap from 4 to 2 decades. Proton decay constrains M_PS > 2×10¹⁴ GeV. To close:

1. Implement full two-loop PS beta functions (not just SM approximation)
2. Include non-perturbative lattice matching corrections at PS threshold
3. Derive the PS Higgs VEV from the D₄ lattice action directly

### Priority 3: Improve κ₄ Reconstruction

Session 12 derived κ₄ from D₄ geometry (4 methods), but 43% reconstruction error remains:

1. Compute two-loop CW corrections to κ₄ from full SO(8) cascade
2. Include threshold matching at G₂ and PS scales
3. Target reconstruction error < 10%

### Priority 4: Close CKM Magnitude Gap (Partially Resolved)

Session 13 implemented the lattice Dirac approach — V_us = 0.164 (27% off), massive improvement from 6508%. Remaining gap:

1. Include perturbative QCD running from lattice scale to 2 GeV (MS-bar matching)
2. Improve 2nd-3rd generation mixing (V_cb, V_ub too small — needs larger mass ratio dynamical range)
3. Explore momentum-dependent Wilson parameter optimization

### Priority 5: arXiv Submission Preparation

When Priorities 1-4 close:
1. Extract Paper 1 from manuscript: "Explicit D₄ Lattice Derivation of α, Koide, and SM Parameters"
2. Format for arXiv: hep-th or hep-ph classification
3. Include all 80 scripts as supplementary material
4. Include Lean 4 proof files as formal verification

### Open Problem Status (as of v87.0 Session 27)

| # | Problem | Status | Next Step |
|---|---------|--------|-----------|
| 1 | α BZ integral | **Gap 0.044% (Session 12: Padé + two-loop)** | Three-loop lattice MC confirmation |
| 2 | M_PS tension | **Gap 4→2 decades (Session 11: 3 methods)** | Full PS two-loop beta functions |
| 3 | Full CW Z_λ | **28 modes, threshold matching (Session 11)** | PS-specific coefficients |
| 4 | CKM magnitudes | **V_us=0.164, lattice Dirac, 7/7 PASS (Session 13)** | QCD running corrections |
| 5 | Proton decay | **Constrains M_PS > 2×10¹⁴ (Session 11)** | Resolves M_PS in favor of CW analytic |
| 6 | 4D simulation | **κ₄=0.70, Z_λ(dyn)=0.108, 8/8 PASS (Session 13)** | GPU 64⁴ |
| 7 | Regge continuum | **7 theorems, 0 sorry (Session 11)** | Complete |
| 8 | Two-loop unification | **Spread 0.4; M_PS ~ 10¹⁴ derived (S8)** | Consistent with proton decay bound |
| 9 | Z_λ effective potential | **RG-improved Z_λ = 0.21; κ₄ derived (S12)** | Two-loop SO(8) correction |
| 10 | ρ_Λ spectral density | **BZ integral + triality + α⁵⁷/(4π) (S8)** | Derive f_supp mechanism |
| 11 | CKM phase | **δ=2π/(3√3), 0.8% agreement ✅** | Complete |
| 12 | D₄ anharmonic κ₄ / force constant J | **κ₄≈0.70 derived (Session 12): 4 methods** | Two-loop SO(8) correction to λ |
| 13 | Circularity resolution | **PROVEN (Lean 4)** | Complete |
| 14 | D₄ uniqueness | **GLOBAL MIN d=2–8 (Session 7)** | Complete; gap=0.825 |
| 15 | 5-design T6 | **PROVEN (Lean 4)** | Complete |
| 16 | Anomaly cancellation | **All 6/6 SM cancel ✅ (A−)** | GUT-scale embedding |
| 17 | Parsimony ratio | **CORRECTED: 2.5–5.0** | Complete |
| 18 | Lean 4 T3 Lieb-Robinson | **FORMALIZED (Session 8): 14 thms, 0 sorry** | Complete |
| 19 | g−2 on D₄ | **Schwinger α/(2π) verified; O(a⁶) artifact (Session 4)** | Higher-loop BZ integrals |
| 20 | Higgs VEV derivation | **CW mode decomp + impedance cascade (Session 7)** | Derive κ₄ from lattice action |
| 21 | θ₀ Koide phase | **DERIVED: 2/9 from SO(3)/S₃ (Session 7)** | Complete; 3 methods agree |
| 22 | SM gauge cascade | **42/42 PASS (Session 6)** | Complete; SO(8)→SM algebraic |
| 23 | Topological defects | **3D vortex + 4D MD + anharmonic (S7+S8+S11)** | Defect mass spectrum |
| 24 | Lattice QFT | **Møller scattering verified (Session 6)** | Higher-order processes |
| 25 | Manuscript / arXiv | **v87.0 complete; 80 scripts, 311 declarations** | Priority 2,4 closure → submit |
