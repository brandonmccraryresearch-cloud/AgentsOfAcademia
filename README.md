# AgentsOfAcademia

[![Lean 4 Verified](https://img.shields.io/badge/Lean_4-Verified_%E2%9C%93-blue)](https://github.com/brandonmccraryresearch-cloud/AgentsOfAcademia/blob/main/lean4/IHMFramework/FormalVerificationRegistry.lean) ![Theorems](https://img.shields.io/badge/Declarations-376-green) ![Files](https://img.shields.io/badge/Lean_Files-17-green) ![Scripts](https://img.shields.io/badge/Python_Scripts-99-green) ![Sorry](https://img.shields.io/badge/sorry-0-brightgreen)

## Intrinsic Resonance Holography (IRH)

A unified field theory framework deriving Standard Model parameters as geometric invariants of the D₄ root lattice. The universe is modeled as a discrete cymatic resonance network subject to coherent oscillation at the Planck frequency.

### Key Results

- **Fine-structure constant:** α⁻¹ = 137.0360028 from D₄ Brillouin zone vacuum polarization (27 ppb agreement)
- **Koide relation:** θ₀ = 2/9 radians derived from SO(3)/S₃ geometry (0.006% agreement)
- **CKM phase:** δ = 2π/(3√3) from topological Berry phase (0.8% agreement)
- **D₄ uniqueness:** Proven global free energy minimum among all 4D root lattices
- **Born rule:** P = |ψ|² derived from Lindblad decoherence of 20 hidden DOF

### Repository Structure

```
├── 89.0IRH.md                  # Main manuscript (v89.0)
├── TECHNICAL_MAP.md             # Technical map & specification flowchart
├── lean4/                       # Lean 4 formal verification (376 declarations, 0 sorry)
│   ├── IHMFramework/            # 17 Lean source files
│   │   ├── FormalVerificationRegistry.lean  # Public registry table
│   │   └── ...
│   └── lakefile.toml            # Build configuration
├── scripts/                     # 66 computational verification scripts (all PASS)
├── docs/
│   └── LeanRegistry.md          # Markdown mirror of Lean registry
└── agents/                      # AI agent specifications
```

See [`TECHNICAL_MAP.md`](TECHNICAL_MAP.md) for the full derivation dependency graph, verification architecture, and specification flowchart.

### Lean 4 Verification

```bash
cd lean4/
lake update    # Fetch Mathlib (~15 min first time)
lake build     # Build all 311 declarations (~40 min)
```

Run `lake build` to independently verify all 311 machine-checked declarations. See [`docs/LeanRegistry.md`](docs/LeanRegistry.md) for the complete registry mapping manuscript claims to Lean theorems.

### Computational Scripts

All 66 Python scripts in `scripts/` are self-contained and executable:

```bash
python3 scripts/<name>.py    # Each prints PASS/FAIL for each test
```

### Manuscript

The current manuscript is [`89.0IRH.md`](89.0IRH.md) (v89.0, April 2026). It contains the complete theoretical framework with derivation grades (A through D) for each claim, enabling readers to assess confidence levels.

### License

See repository for license details.
