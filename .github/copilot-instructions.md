# Copilot Instructions for AgentsOfAcademia

## File Naming Convention

The main manuscript file follows the convention `{version}theaceinthehole.md` where `{version}` is the current version number (e.g., `82.0theaceinthehole.md`). When bumping to a new version:

1. **Rename the file** using `git mv {old_version}theaceinthehole.md {new_version}theaceinthehole.md`
2. **Update the version header** in the manuscript header near the top of the document
3. **Add a version change summary** immediately after the date block in the manuscript header
4. **Update all internal cross-references** that mention the filename

The current manuscript file is: **`82.0theaceinthehole.md`**

## Environment Setup

A GitHub Action (`.github/workflows/env_setup.yml`) automatically installs the required environment on session start:

- **Python 3.11+** with NumPy, SciPy, SymPy, Matplotlib
- **Lean 4** (v4.29.0-rc6 via elan) with Mathlib
- **Verification scripts** in `scripts/`

### Quick Setup (manual session)

```bash
# Python scientific stack
pip install numpy scipy sympy matplotlib

# Lean 4 (if elan not installed)
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/ && lake update && lake build

# Run all verification scripts
python scripts/verify_numerical_predictions.py  # 10/10 PASS expected
python scripts/d4_phonon_spectrum.py             # Full phonon dispersion
python scripts/bz_integral.py                    # Multi-channel BZ integral (93.2%)
```

## Computational Scripts

| Script | Purpose | Expected Output |
|--------|---------|-----------------|
| `scripts/verify_numerical_predictions.py` | Verify all numerical predictions | 10/10 PASS |
| `scripts/d4_phonon_spectrum.py` | Full D₄ phonon dispersion, zone-boundary zero, elastic properties | Eigenvalues at all HSP |
| `scripts/bz_integral.py` | Multi-level BZ integral (bare → multi-channel → SO(8)) | Level 2: 93.2% of target |

## MCP Server Usage

This repository uses multiple Model Context Protocol (MCP) servers for scientific computation, simulation, and formal verification. Server configurations are in `mcp-servers/`.

### Available MCP Servers

| Server | Purpose | Tools |
|--------|---------|-------|
| **math-mcp** | Symbolic math (SymPy), linear algebra, FFT, optimization | `symbolic_solve`, `symbolic_diff`, `symbolic_integrate`, `symbolic_simplify`, `matrix_multiply`, `solve_linear_system`, `fft`, `optimize_function`, `find_roots` |
| **quantum-mcp** | Quantum simulation (Schrödinger equation, wave packets, lattice potentials) | `create_lattice_potential`, `create_gaussian_wavepacket`, `solve_schrodinger_2d`, `render_video`, `visualize_potential`, `analyze_wavefunction` |
| **molecular-mcp** | Molecular dynamics (Lennard-Jones, NVT/NPT, phase transitions) | `create_particles`, `add_potential`, `run_md`, `run_nvt`, `compute_rdf`, `detect_phase_transition`, `render_trajectory` |
| **neural-mcp** | Neural networks (PyTorch, training, evaluation) | `define_model`, `load_dataset`, `train_model`, `evaluate_model`, `confusion_matrix`, `export_model` |
| **lean-lsp-mcp** | Lean 4 formal verification (proof goals, diagnostics, search) | `lean_goal`, `lean_verify`, `lean_diagnostic_messages`, `lean_multi_attempt`, `lean_leansearch`, `lean_loogle`, `lean_state_search`, `lean_hammer_premise`, `lean_code_actions`, `lean_build` |
| **psianimator-mcp** | QuTiP quantum physics + Manim visualization | Bloch spheres, Wigner functions, state tomography |
| **arxiv-search-mcp** | arXiv paper search | Literature search and retrieval |
| **particlephysics-mcp** | Particle physics data and calculations | PDG data, cross-sections, decay rates |

### Usage Guidelines

1. **For numerical verification** of manuscript claims (e.g., α⁻¹ ≈ 137.036, (E/E_P)^6 bounds): use `math-mcp` symbolic tools
2. **For quantum simulations** (D₄ lattice wave packet propagation, BZ integrals): use `quantum-mcp`
3. **For Lean 4 theorem verification** (28 existing theorems + T1–T10 roadmap): use `lean-lsp-mcp`
4. **For lattice phonon dynamics**: use `molecular-mcp` with custom potentials
5. **For literature cross-checks**: use `arxiv-search-mcp`

### Lean 4 Project

The Lean 4 project lives in `lean4/` with `lakefile.toml`. It uses Mathlib and requires Lean v4.29.0-rc6 (via `lean-toolchain`). Build with:

```bash
cd lean4/
lake update && lake build
```

Current state: 28 verified theorems across 3 files (Basic.lean: 14, V2Basic.lean: 7, V2Problems.lean: 7). Zero `sorry` in all files.

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

### Current State (v82.0, 2026-03-27)

The manuscript is at v82.0. The Review&Reconstruction closure audit has been executed with the following key results:

| Item | Status | Key Finding |
|------|--------|-------------|
| Multi-channel BZ integral | **93.2% of target** | 6 coordinate-pair channels account for bulk of α⁻¹ fractional correction |
| D₄ phonon spectrum | **Computed** | 4 branches, zone-boundary zero at R=(π,π,π,π), ν=1/4 |
| Koide formula | **Verified** | m_e: 0.01%, m_μ: 0.006%, θ₀=2/9 from Berry phase |
| 5-design property | **Verified** | ⟨x₁⁴⟩=1/8, ⟨x₁²x₂²⟩=1/24 exact |
| Lean 4 | **28 theorems, 0 sorry** | Build verified |
| Defects | **5 resolved, 3 addressed, 4 open** | Out of 12 Review&Reconstruction defects |

### Priority 1: Close the α BZ Integral (93.2% → 100%)

The multi-channel integral is at 93.2%. Three approaches to close the remaining 6.8%:

1. **SO(8) Cartan subalgebra contribution:** The 6 coordinate pairs give 24 of 28 root vectors. The 4 Cartan generators should provide the missing contribution. Implement in `scripts/bz_integral.py` as Level 3.

2. **Ward identity constraint:** The transversality condition k_μ Π^μν(k) = 0 constrains the form of vertex corrections. This may fix the residual uniquely.

3. **Self-energy resummation:** The geometric series α⁻¹ = α₀⁻¹/(1 - Π_self) can enhance the bare value.

**Action:** Extend `scripts/bz_integral.py` with Level 3 (full SO(8) vertex) and Level 4 (Ward identity + resummation).

### Priority 2: T6 — 24-Cell 5-Design Lean 4 Proof

This is the highest-priority Lean 4 formalization target. The proof is purely combinatorial:

1. Define the 24 root vectors of D₄ in Lean 4
2. Compute ⟨x₁^n x₂^m⟩ for all monomials up to degree 5
3. Show equality with the continuous spherical integral formula 

**Action:** Create `lean4/IHMFramework/FiveDesign.lean` with the T6 theorem. Use `lean_leansearch` and `lean_loogle` to find relevant Mathlib lemmas for finite sums and spherical integrals.

### Priority 3: Cosmological Constant Spectral Density

The phonon spectrum is now computed (§V.5.1). The next step is:

1. Compute the full BZ integral of the zero-point energy: ∫ Σ ℏω(k) d⁴k/(2π)⁴
2. Determine the suppression function f(k) from triality phase averaging
3. Show the result matches α⁵⁷/(4π)

**Action:** Extend `scripts/d4_phonon_spectrum.py` with the spectral density integral and suppression function.

### Priority 4: Higgs Effective Potential

Compute the lattice free energy F(φ) as a function of the order parameter:

1. Set up the D₄ lattice partition function with an external field φ
2. Evaluate F(φ) = -T ln Z numerically via Monte Carlo
3. Minimize F(φ) to find v = √(-a/2b)

**Action:** Create `scripts/higgs_effective_potential.py`.

### Priority 5: Full QFT Construction

Build the lattice field theory from the phonon spectrum:

1. Quantize the phonon field: â(k), â†(k) with [â, â†] = δ
2. Construct the Hamiltonian H = Σ ω(k) â†â
3. Compute propagators G(x-y) = ⟨T â(x)â†(y)⟩
4. Define scattering amplitudes via LSZ reduction

**Action:** Create `scripts/lattice_qft.py` with the field theory construction.

### Priority 6: Additional Lean 4 Theorems (T3, T7)

After T6, formalize:
- **T3:** Lieb-Robinson bound (finite propagation speed on D₄ lattice)
- **T7:** Measure uniqueness from 5-design property (follows from T6)

### Priority 7: 4D D₄ Simulation

Create the GPU simulation infrastructure:
- Initialize 64³×64 lattice with D₄ connectivity
- Implement phonon dynamics with the computed dispersion
- Run NVE/NVT ensembles to extract thermodynamic properties

**Action:** Create `scripts/d4_simulation_4d.py` using molecular-mcp or custom code.

### Open Problem Status (as of v82.0)

| # | Problem | Status | Next Step |
|---|---------|--------|-----------|
| 1 | α BZ integral | **93.2%** | SO(8) Cartan completion |
| 2 | Two-loop threshold corrections | One-loop: 16.32 spread | Hidden-sector corrections |
| 3 | 4D simulation | Plan specified | GPU infrastructure |
| 4 | Z_λ effective potential | CW structure identified | Lattice free energy |
| 5 | ρ_Λ spectral density | Phonon spectrum computed | Suppression function |
| 6 | CKM/PMNS matrices | CKM phase derived | Full matrix elements |
| 7 | D₄ anharmonic κ₄ | Open | Lattice perturbation theory |
| 8 | SO(8) Cartan for α | NEW — identified by v82.0 | Complete Level 3 integral |
