# IHM-HRIIP Formal Verification Framework

Lean 4 formalization of **Intrinsic Harmonic Motion: Holographic-like, Resonance Induced Interference Projection** (IHM-HRIIP).

## Verification Status

**311 declarations verified** across 16 files — zero `sorry` placeholders, zero errors.

See the [**Formal Verification Registry**](IHMFramework/FormalVerificationRegistry.lean) for the complete mapping between manuscript claims and Lean 4 theorems, and the [**Markdown Registry**](../docs/LeanRegistry.md) for a human-readable version.

| File | Declarations | Key Content |
|:-----|:------------|:------------|
| Basic.lean | 30 | Core IRH: c > 0, Lorentz, E=mc², gravity, speed limit |
| V2Basic.lean | 13 | IVT stability, D₄ phonon, mass gap |
| V2Problems.lean | 17 | Holographic projection, dispersion relations |
| FiveDesign.lean | 14 | 5-design moment identities, elastic isotropy |
| Circularity.lean | 8 | Circularity tautology (c, ℏ, G) |
| LiebRobinson.lean | 13 | Lieb-Robinson bound, causal cone |
| MeasureUniqueness.lean | 11 | Moment uniqueness, elastic reduction |
| D4Uniqueness.lean | 12 | D₄ global free energy minimum |
| Goldstone.lean | 12 | 4 massless Goldstone modes |
| GaugeInvariance.lean | 15 | U(1) plaquette gauge invariance |
| ReggeContinuumLimit.lean | 16 | O(a₀²) convergence |
| NonAbelianGauge.lean | 22 | SU(N) Wilson action |
| DiracEquation.lean | 49 | Lattice Dirac, Clifford, Wilson fermions |
| BornRule.lean | 21 | Born rule, measurement, Gleason |
| ModeDecomposition.lean | 58 | Irrep decomposition, Schur, branching |
| FormalVerificationRegistry.lean | — | Registry table + C/D+ stub axioms |

## Building

```bash
lake update
lake build
```

Requires Lean 4 v4.30.0-rc1 (managed by `lean-toolchain`).