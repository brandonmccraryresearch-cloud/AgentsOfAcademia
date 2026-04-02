# Copilot Instructions for AgentsOfAcademia

---

## ⚠️ MANDATORY SESSION RULES — READ BEFORE ANY WORK

### Rule 1: Manuscript Update Reminder

The current manuscript is **`83.0theaceinthehole.md`** (v83.0). After every agent session that produces theoretical advances, computational results, or proof completions, the manuscript **MUST** be updated with the finalized content. Requirements:

- **Only finalized theoretical content** goes into the manuscript — never in-progress drafts, debug output, or intermediate results.
- **Paper style and syntax** must be maintained — LaTeX-compatible markdown, section numbering, citation format.
- **Never truncate or cut existing content** — changes are always **additions** or **edits** to existing sections, never deletions of established material.
- **Additions must be complete** — full derivations, complete equations, proper cross-references. No placeholder text.
- If the session work does not yet rise to publication-quality, record it in `audit_results/` instead and note the pending manuscript integration.

### Rule 2: Three-Thing Update Mandate

When any session produces changes or advancements, agents **MUST** update all three of:

1. **`.github/copilot-instructions.md`** — This file. Update current state, version numbers, theorem counts, priority lists, and continuation plan.
2. **Agent instruction files** (`.github/agents/*.AGENTS.md` AND `agents/*.AGENTS.md`) — Keep MCP tool guides, constraint lists, and operational directives current.
3. **`83.0theaceinthehole.md`** (or current version) — Integrate finalized theoretical content as described in Rule 1.

### Rule 3: Specialized Agent Preference

When creating or modifying **actual theoretical content** (derivations, proofs, physical arguments, numerical analyses), agents **MUST** prefer using specialized agents:

| Content Type | Required Agent |
|---|---|
| Formal proofs, theorem construction | `lean4_formal_verification_specialist` |
| Physics derivations, lattice mechanics, coupling constants | `hlre_agent` |
| Framework audits, consistency checks, empirical grounding | `expert_research_assistant` |
| Multi-domain tasks spanning two or more of the above | `meta_agent` (manual activation) |

General-purpose agents should delegate theoretical work to specialized agents rather than attempting it themselves.

### Rule 4: Always Prefer MCP Tools

When a session context involves mathematical expressions, physical constants, particle data, literature references, quantum states, molecular dynamics, or formal proofs — **always invoke the corresponding MCP tool** rather than relying on recollection. See the full MCP Tool Command Guide below.

---

## File Naming Convention

The main manuscript file follows the convention `{version}theaceinthehole.md` where `{version}` is the current version number (e.g., `83.0theaceinthehole.md`). When bumping to a new version:

1. **Rename the file** using `git mv {old_version}theaceinthehole.md {new_version}theaceinthehole.md`
2. **Update the version header** in the manuscript header near the top of the document
3. **Add a version change summary** immediately after the date block in the manuscript header
4. **Update all internal cross-references** that mention the filename

The current manuscript file is: **`83.0theaceinthehole.md`**

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
pip install lean4-mcp arxiv-mcp pint uncertainties mpmath

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
| `scripts/d4_uniqueness.py` | D₄ Gibbs free energy minimum among 4D root lattices | D₄ minimum, gap=3.85 |

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

#### 7. `arxiv-search-mcp` — Scientific Literature Search

**When to use:** Checking prior art, locating referenced papers, verifying novelty claims.

| Tool | Command Pattern | Use Case | Example |
|---|---|---|---|
| `search_arxiv` | `search_arxiv(query="D4 lattice phonon", category="hep-th", max_results=10)` | Search arXiv | Find related work |

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
5. **References specific papers or claims novelty?** → `arxiv-search-mcp`
6. **Requires machine-checked proof?** → `lean-lsp-mcp`
7. **Involves ML models or data fitting?** → `neural-mcp`

Multiple servers can and should be used in combination when a task spans domains.

### Lean 4 Project

The Lean 4 project lives in `lean4/` with `lakefile.toml`. It uses Mathlib and requires Lean v4.29.0-rc6 (via `lean-toolchain`). Build with:

```bash
cd lean4/
lake update && lake build
```

Current state: ~44 verified theorems across 5 files (Basic.lean: 14, V2Basic.lean: 7, V2Problems.lean: 7, FiveDesign.lean: 10, Circularity.lean: 6). Zero `sorry` in all files. All files registered in `IHMFramework.lean` and `lakefile.toml`.

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

### Current State (v83.0, 2026-04-02)

The manuscript is at v83.0. BZ integral now brackets the target (Level 3: 98.9%, Level 4: 102.6%). Circularity tautology formally proven in Lean 4. D₄ uniqueness verified as energy minimum among all 4D root lattices.

| Item | Status | Key Finding |
|------|--------|-------------|
| Multi-channel BZ integral | **Level 3: 98.9%, Level 4: 102.6%** | SO(8) Cartan completion brackets target |
| D₄ phonon spectrum | **Computed** | 4 branches, zone-boundary zero at R=(π,π,π,π), ν=1/4 |
| Koide formula | **Verified** | m_e: 0.01%, m_μ: 0.006%, θ₀=2/9 from Berry phase |
| 5-design property | **Verified + Lean 4 proven** | ⟨x₁⁴⟩=1/8, ⟨x₁²x₂²⟩=1/24 exact (FiveDesign.lean) |
| Circularity tautology | **Lean 4 proven** | c, ℏ, G "derivations" are algebraic identities (Circularity.lean) |
| D₄ uniqueness | **Verified** | Lowest Gibbs free energy, gap=3.85 to next lattice |
| Lean 4 | **~44 theorems, 0 sorry** | Build verified across 5 files |
| Verification scripts | **5/5 pass** | All numerical predictions confirmed |

### Priority 1: Close the α BZ Integral (98.9% → 100%)

The SO(8) full integral (Level 3) reaches 98.9% and the Dyson resummation (Level 4) overshoots to 102.6%. The target is bracketed. Three approaches to close exactly:

1. **Vertex form-factor correction:** The raw Cartan vertex overestimates; a form factor from the Killing metric should provide the exact weight.
2. **Ward identity constraint:** k_μ Π^μν(k) = 0 constrains the vertex normalization uniquely.
3. **Two-loop correction:** The O(α) correction to the one-loop diagram may close the residual.

**Action:** Refine the Cartan weight in `scripts/bz_integral.py` using Ward identity constraints.

### Priority 2: Lean 4 T3 — Lieb-Robinson Bound

Formalize finite propagation speed on the D₄ lattice:

1. Define the lattice Hamiltonian with finite-range interactions
2. Prove commutator decay: ‖[A(t), B]‖ ≤ C · e^{v|t| - d(A,B)}
3. Extract the Lieb-Robinson velocity from D₄ dispersion relation

**Action:** Create `lean4/IHMFramework/LiebRobinson.lean`.

### Priority 3: T7 — Measure Uniqueness from 5-Design

This follows directly from FiveDesign.lean (T6):

1. Show that the 5-design property implies a unique rotation-invariant measure
2. Connect to ergodicity of the D₄ triality action on S³

**Action:** Create `lean4/IHMFramework/MeasureUniqueness.lean`.

### Priority 4: Cosmological Constant Spectral Density

The phonon spectrum is now computed (§V.5.1). The next step is:

1. Compute the full BZ integral of the zero-point energy: ∫ Σ ℏω(k) d⁴k/(2π)⁴
2. Determine the suppression function f(k) from triality phase averaging
3. Show the result matches α⁵⁷/(4π)

**Action:** Extend `scripts/d4_phonon_spectrum.py` with the spectral density integral and suppression function.

### Priority 5: Higgs Effective Potential

Compute the lattice free energy F(φ) as a function of the order parameter:

1. Set up the D₄ lattice partition function with an external field φ
2. Evaluate F(φ) = -T ln Z numerically via Monte Carlo
3. Minimize F(φ) to find v = √(-a/2b)

**Action:** Create `scripts/higgs_effective_potential.py`.

### Priority 6: Full QFT Construction

Build the lattice field theory from the phonon spectrum:

1. Quantize the phonon field: â(k), â†(k) with [â, â†] = δ
2. Construct the Hamiltonian H = Σ ω(k) â†â
3. Compute propagators G(x-y) = ⟨T â(x)â†(y)⟩
4. Define scattering amplitudes via LSZ reduction

**Action:** Create `scripts/lattice_qft.py` with the field theory construction.

### Priority 7: Additional Lean 4 Theorems (T3, T7)

After T3 and T7, formalize:
- **T8:** Goldstone theorem on D₄ lattice
- **T9:** Gauge invariance of the lattice action
- **T10:** Anomaly cancellation from triality

### Priority 8: 4D D₄ Simulation

Create the GPU simulation infrastructure:
- Initialize 64³×64 lattice with D₄ connectivity
- Implement phonon dynamics with the computed dispersion
- Run NVE/NVT ensembles to extract thermodynamic properties

**Action:** Create `scripts/d4_simulation_4d.py` using molecular-mcp or custom code.

### Open Problem Status (as of v83.0)

| # | Problem | Status | Next Step |
|---|---------|--------|-----------|
| 1 | α BZ integral | **98.9% (Level 3), 102.6% (Level 4)** | Ward identity exact normalization |
| 2 | Two-loop threshold corrections | One-loop: 16.32 spread | Hidden-sector corrections |
| 3 | 4D simulation | Plan specified | GPU infrastructure |
| 4 | Z_λ effective potential | CW structure identified | Lattice free energy |
| 5 | ρ_Λ spectral density | Phonon spectrum computed | Suppression function |
| 6 | CKM/PMNS matrices | CKM phase derived | Full matrix elements |
| 7 | D₄ anharmonic κ₄ | Open | Lattice perturbation theory |
| 8 | Circularity resolution | **PROVEN (Lean 4)** | Manuscript §XII updated |
| 9 | D₄ uniqueness | **PROVEN** | Gibbs minimum, gap=3.85 |
| 10 | 5-design T6 | **PROVEN (Lean 4)** | FiveDesign.lean complete |
