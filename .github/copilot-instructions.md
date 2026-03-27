# Copilot Instructions for AgentsOfAcademia

## File Naming Convention

The main manuscript file follows the convention `{version}theaceinthehole.md` where `{version}` is the current version number (e.g., `81.0theaceinthehole.md`). When bumping to a new version:

1. **Rename the file** using `git mv {old_version}theaceinthehole.md {new_version}theaceinthehole.md`
2. **Update the version header** on line 7 of the document
3. **Add a version change summary** starting at line 20
4. **Update all internal cross-references** that mention the filename

The current manuscript file is: **`81.0theaceinthehole.md`**

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
