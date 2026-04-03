/-
  IHM-HRIIP: Moment Equalities for D₄ Root Vectors

  Derives the required 4th-order moment equalities from known D₄ root
  counting facts. The 24 D₄ root vectors (±eᵢ ± eⱼ for i<j in ℝ⁴) satisfy:

    (1) ⟨x₁⁴⟩ = (1/24) Σᵣ (r₁/|r|)⁴ = 1/8 = 3/(d(d+2)) for d=4
    (2) ⟨x₁²x₂²⟩ = (1/24) Σᵣ (r₁/|r|)²(r₂/|r|)² = 1/24 = 1/(d(d+2))

  These are the independent 4th-order moment conditions required for a
  spherical 5-design on S³. The proofs here verify these identities from
  hard-coded root counts (d4RootsPerComponent, d4RootsPerPair), not from
  an explicit enumeration of the root set in ℝ⁴. A full formalization
  would define the 24 roots as a finite subset of S³ and prove the moment
  sums over that set directly.

  These identities guarantee elastic isotropy of the D₄ lattice and are
  essential for emergent Lorentz invariance in the continuum limit.
-/

import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Fin.Basic

open Real

/-! ## D₄ Root System Properties

  The D₄ root system consists of 24 vectors in ℝ⁴ of the form ±eᵢ ± eⱼ
  for 0 ≤ i < j ≤ 3. Key structural properties:

  - 24 roots = C(4,2) × 2² = 6 × 4
  - Each root has norm √2
  - 12 roots have nonzero first component (3 partner indices × 4 signs)
  - 4 roots have nonzero first AND second components (4 sign combinations)
-/

/-- The D₄ coordination number: 24 nearest neighbors. -/
def d4CoordinationNumber : ℕ := 24

/-- The D₄ root norm squared: each root ±eᵢ ± eⱼ has |r|² = 2. -/
def d4RootNormSq : ℝ := 2

/-- Number of D₄ roots with nonzero component in any given direction.
    For any fixed index i, there are 3 choices of partner j and 4 sign
    combinations, giving 12 roots with rᵢ ≠ 0. -/
def d4RootsPerComponent : ℕ := 12

/-- Number of D₄ roots with nonzero components in both of two given directions.
    For fixed indices i, j with i ≠ j, only the 4 roots ±eᵢ ± eⱼ have
    both components nonzero. -/
def d4RootsPerPair : ℕ := 4

/-! ## Quartic Moment (⟨x₁⁴⟩ = 1/8)

  For a unit-normalized D₄ root r/|r|, each nonzero component is ±1/√2.
  The fourth power of ±1/√2 is 1/4.

  Sum of x₁⁴ over all 24 roots:
    - 12 roots with x₁ ≠ 0: contribute 12 × (1/√2)⁴ = 12 × 1/4 = 3
    - 12 roots with x₁ = 0: contribute 0
    Total sum = 3
    Average = 3/24 = 1/8 = 3/(d(d+2)) for d = 4   ✓
-/

/-- The quartic sum: Σᵣ (r₁/|r|)⁴ = 3 for the 24 D₄ roots. -/
theorem d4_quartic_sum :
    (d4RootsPerComponent : ℝ) * (1 / d4RootNormSq) ^ 2 = 3 := by
  simp [d4RootsPerComponent, d4RootNormSq]
  norm_num

/-- The quartic average (5-design condition 1):
    ⟨x₁⁴⟩ = (1/24) Σᵣ (r₁/|r|)⁴ = 1/8 -/
theorem d4_five_design_quartic :
    (d4RootsPerComponent : ℝ) * (1 / d4RootNormSq) ^ 2 /
    (d4CoordinationNumber : ℝ) = 1 / 8 := by
  simp [d4RootsPerComponent, d4RootNormSq, d4CoordinationNumber]
  norm_num

/-! ## Mixed Moment (⟨x₁²x₂²⟩ = 1/24)

  For unit-normalized D₄ roots, (rᵢ/|r|)² = 1/2 when rᵢ ≠ 0.

  Sum of x₁²x₂² over all 24 roots:
    - 4 roots of form ±e₁ ± e₂: contribute 4 × (1/2)(1/2) = 1
    - 20 other roots: at least one of x₁, x₂ is zero → contribute 0
    Total sum = 1
    Average = 1/24 = 1/(d(d+2)) for d = 4   ✓
-/

/-- The mixed-moment sum: Σᵣ (r₁/|r|)²(r₂/|r|)² = 1 for D₄ roots. -/
theorem d4_mixed_sum :
    (d4RootsPerPair : ℝ) * (1 / d4RootNormSq) * (1 / d4RootNormSq) = 1 := by
  simp [d4RootsPerPair, d4RootNormSq]
  norm_num

/-- The mixed fourth-moment average:
    ⟨x₁²x₂²⟩ = (1/24) Σᵣ (r₁/|r|)²(r₂/|r|)² = 1/24 -/
theorem d4_fourth_moment_mixed :
    (d4RootsPerPair : ℝ) * (1 / d4RootNormSq) * (1 / d4RootNormSq) /
    (d4CoordinationNumber : ℝ) = 1 / 24 := by
  simp [d4RootsPerPair, d4RootNormSq, d4CoordinationNumber]
  norm_num

/-! ## Combined Fourth-Moment Statement

  The two quartic moment identities established above are:
    ⟨x₁⁴⟩ = 1/8
    ⟨x₁²x₂²⟩ = 1/24

  These are the fourth-order moment equalities derived here from the counting
  assumptions on D₄ roots. This theorem packages those two identities together;
  it does not by itself formalize the full spherical 5-design definition.
-/

/-- The D₄ counting assumptions imply the two fourth-moment identities:
    the quartic moment is 1/8 and the mixed quartic moment is 1/24. -/
theorem d4_fourth_moment_identities :
    (d4RootsPerComponent : ℝ) * (1 / d4RootNormSq) ^ 2 /
    (d4CoordinationNumber : ℝ) = 1 / 8 ∧
    (d4RootsPerPair : ℝ) * (1 / d4RootNormSq) * (1 / d4RootNormSq) /
    (d4CoordinationNumber : ℝ) = 1 / 24 := by
  constructor
  · exact d4_five_design_quartic
  · exact d4_fourth_moment_mixed

/-! ## Elastic Isotropy Consequence

  The 5-design property implies that the D₄ lattice dynamical matrix
  D_αβ(k) = Σ_δ (δ_α δ_β/|δ|²)(1 - cos(k·δ)) is isotropic at small |k|:

    D_αβ(k) ≈ c² k² δ_αβ   as |k| → 0

  with a single phonon velocity c = a₀ Ω_P. This isotropy is the geometric
  foundation for emergent Lorentz invariance in the continuum limit. Without
  the 5-design property, the lattice would have direction-dependent propagation
  speeds, breaking Lorentz symmetry even in the long-wavelength limit.
-/

/-- Isotropy condition: quadratic moment ⟨x₁²⟩ = 1/d = 1/4 for D₄.
    This ensures all four phonon branches have the same velocity at small k. -/
theorem d4_quadratic_moment :
    (d4RootsPerComponent : ℝ) * (1 / d4RootNormSq) /
    (d4CoordinationNumber : ℝ) = 1 / 4 := by
  simp [d4RootsPerComponent, d4RootNormSq, d4CoordinationNumber]
  norm_num

/-- The D₄ lattice dimension. -/
def d4Dimension : ℕ := 4

/-- The expected quartic moment for a 5-design on S^{d-1}: 3/(d(d+2)). -/
noncomputable def fiveDesignQuartic (d : ℕ) : ℝ :=
  3 / ((d : ℝ) * ((d : ℝ) + 2))

/-- The expected mixed moment for a 5-design on S^{d-1}: 1/(d(d+2)). -/
noncomputable def fiveDesignMixed (d : ℕ) : ℝ :=
  1 / ((d : ℝ) * ((d : ℝ) + 2))

/-- For d = 4: 3/(d(d+2)) = 3/24 = 1/8. -/
theorem fiveDesignQuartic_d4 : fiveDesignQuartic 4 = 1 / 8 := by
  simp [fiveDesignQuartic]
  norm_num

/-- For d = 4: 1/(d(d+2)) = 1/24. -/
theorem fiveDesignMixed_d4 : fiveDesignMixed 4 = 1 / 24 := by
  simp [fiveDesignMixed]
  norm_num
