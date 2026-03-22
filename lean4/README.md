# IHM-HRIIP Formal Verification Framework

Lean 4 formalization of **Intrinsic Harmonic Motion: Holographic-like, Resonance Induced Interference Projection** (IHM-HRIIP).

## Verification Status

**14 theorems verified** — zero `sorry` placeholders, zero errors.

| Category | Theorems | Status |
|:---------|:---------|:-------|
| Substrate mechanics | `luminalSpeed_pos`, `luminalSpeed_sq` | ✓ |
| Wave compression | `lorentzFactorSqInv_pos`, `forwardWavelength_nonneg`, `forwardWavelength_le_rest` | ✓ |
| Mass-energy | `trappedEnergy_eq`, `trappedEnergy_pos` | ✓ |
| Holographic bound | `maxNodalCount_pos` | ✓ |
| Gravity | `flat_vacuum`, `attractive_gravity` | ✓ |
| Speed limit | `no_superluminal`, `velocity_sq_lt_c_sq` | ✓ |
| Conservation | `totalEnergy_nonneg` | ✓ |
| D₄ connection | `latticeSpacing_lt_planck` | ✓ |

## Building

```bash
lake update
lake build
```

Requires Lean 4 v4.29.0-rc6 (managed by `lean-toolchain`).