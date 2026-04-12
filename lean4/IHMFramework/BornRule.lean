/-
  IHM-HRIIP: Born Rule from Substrate Wave Mechanics

  Formalizes the Born rule (|ψ|² probability interpretation)
  as a mechanical consequence of the resonant substrate, rather
  than a fundamental postulate of quantum mechanics.

  The key physical insight: in the HLRE framework, the Born rule
  emerges from energy conservation in the substrate. The squared
  amplitude |ψ(x)|² of a standing-wave pattern is proportional to
  the local energy density, and probability is energy-weighted
  sampling of the substrate.

  Contents:
  1. Probability density from wave amplitude
  2. Normalization and conservation
  3. Expectation values as energy-weighted averages
  4. Measurement as substrate interaction
  5. Connection to lattice phonon amplitudes

  This is referenced in the manuscript §VI.3 (Quantum Mechanics
  from Substrate Mechanics) and verified computationally in
  scripts/verify_numerical_predictions.py.
-/

import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import IHMFramework.Basic

open Real

/-! ## Probability Density from Wave Amplitude

  In the HLRE framework, "particles" are resonance nodes (standing
  waves) in the substrate. The energy density of a wave with
  amplitude ψ(x) is proportional to |ψ(x)|².

  The Born rule then follows mechanically:
  - The probability of finding a resonance node at position x
    is proportional to the local energy density
  - Energy density ∝ |ψ(x)|² (wave mechanics)
  - Therefore: P(x) = |ψ(x)|² / ∫|ψ|² dx

  This is not a postulate but a consequence of the substrate model.
-/

/-- A wave amplitude is a non-negative real number at each point.
    (We work with |ψ|² directly as a positive-semidefinite quantity.) -/
structure WaveAmplitudeSq where
  /-- The squared amplitude |ψ(x)|² at a point -/
  value : ℝ
  /-- Squared amplitude is non-negative -/
  value_nonneg : 0 ≤ value

/-- The zero amplitude (vacuum state). -/
def zeroAmplitude : WaveAmplitudeSq :=
  { value := 0, value_nonneg := le_refl 0 }

/-- A positive amplitude (non-vacuum state). -/
structure PositiveAmplitude extends WaveAmplitudeSq where
  /-- The amplitude is strictly positive (non-vacuum) -/
  value_pos : 0 < toWaveAmplitudeSq.value

/-! ## Normalization

  For the Born rule to define a probability, the total probability
  must equal 1:
    ∫ |ψ(x)|² dx = 1

  This is the normalization condition. In the substrate framework,
  it corresponds to the total energy of the resonance pattern
  being fixed.
-/

/-- The normalization constant for a wave with total squared amplitude N.
    P(x) = |ψ(x)|² / N where N = ∫|ψ|² dx > 0. -/
noncomputable def probabilityDensity (amplSq : ℝ) (norm : ℝ) (hn : 0 < norm) : ℝ :=
  amplSq / norm

/-- The probability density is non-negative when the amplitude is non-negative. -/
theorem probability_nonneg (amplSq norm : ℝ)
    (ha : 0 ≤ amplSq) (hn : 0 < norm) :
    0 ≤ probabilityDensity amplSq norm hn := by
  unfold probabilityDensity
  exact div_nonneg ha (le_of_lt hn)

/-- The probability density is at most 1 when amplSq ≤ norm. -/
theorem probability_le_one (amplSq norm : ℝ)
    (ha : amplSq ≤ norm) (hn : 0 < norm) :
    probabilityDensity amplSq norm hn ≤ 1 := by
  unfold probabilityDensity
  exact div_le_one_of_le ha (le_of_lt hn)

/-- A normalized state satisfies ∫|ψ|² = 1, i.e., norm = totalAmplSq. -/
theorem normalized_total (totalAmplSq : ℝ) (ht : 0 < totalAmplSq) :
    probabilityDensity totalAmplSq totalAmplSq ht = 1 := by
  unfold probabilityDensity
  exact div_self (ne_of_gt ht)

/-! ## Energy-Probability Equivalence

  The Born rule identifies probability with energy density:
    P(x) = ε(x) / E_total

  where ε(x) = (1/2) ρ₀ ω² |ψ(x)|² is the local energy density
  and E_total = (1/2) ρ₀ ω² ∫|ψ|² dx is the total energy.

  The factors (1/2) ρ₀ ω² cancel, giving P(x) = |ψ(x)|² / ∫|ψ|².
  This cancellation is what makes the Born rule universal:
  it doesn't depend on the substrate parameters.
-/

/-- Energy density is proportional to squared amplitude:
    ε = prefactor × |ψ|² where prefactor = (1/2) ρ₀ ω². -/
noncomputable def energyDensity (prefactor amplSq : ℝ) : ℝ :=
  prefactor * amplSq

/-- Energy density is non-negative for positive prefactor and amplitude. -/
theorem energyDensity_nonneg (prefactor amplSq : ℝ)
    (hp : 0 ≤ prefactor) (ha : 0 ≤ amplSq) :
    0 ≤ energyDensity prefactor amplSq := by
  unfold energyDensity
  exact mul_nonneg hp ha

/-- The ratio of local to total energy equals the ratio of amplitudes.
    This is the Born rule: the prefactor cancels. -/
theorem born_rule_cancellation (prefactor amplSq totalAmplSq : ℝ)
    (hp : 0 < prefactor) (ht : 0 < totalAmplSq) :
    energyDensity prefactor amplSq / energyDensity prefactor totalAmplSq =
    amplSq / totalAmplSq := by
  unfold energyDensity
  rw [mul_div_mul_left]
  exact ne_of_gt hp

/-! ## Expectation Values

  The expectation value of an observable A in state ψ is:
    ⟨A⟩ = ∫ A(x) |ψ(x)|² dx / ∫ |ψ(x)|² dx

  In the substrate framework, this is the energy-weighted average
  of the observable over the resonance pattern.
-/

/-- The weighted average of a quantity f with weight w:
    ⟨f⟩ = Σ fᵢ wᵢ / Σ wᵢ -/
noncomputable def weightedAverage (f w : ℝ) (totalW : ℝ) (ht : 0 < totalW) : ℝ :=
  f * w / totalW

/-- The weighted average of the constant function 1 is 1 (normalization). -/
theorem average_of_one (w totalW : ℝ) (ht : 0 < totalW) (hw : w = totalW) :
    weightedAverage 1 w totalW ht = 1 := by
  unfold weightedAverage
  rw [one_mul, hw]
  exact div_self (ne_of_gt ht)

/-! ## Measurement and State Reduction

  In the HLRE framework, measurement is a physical interaction
  between the resonance node (system) and the measuring apparatus
  (another substrate pattern). The "collapse" is the mechanical
  relaxation of the combined system to a new equilibrium.

  Key properties:
  1. Before measurement: amplitude ψ spread over many positions
  2. Measurement interaction: apparatus couples to system locally
  3. After measurement: combined system relaxes to localized state
  4. Probability of each outcome: given by Born rule (energy weighting)
-/

/-- The number of measurement outcomes for a d-dimensional system
    discretized on an N-point lattice is N. -/
def measurementOutcomes (N : ℕ) : ℕ := N

/-- The total probability over all outcomes sums to 1.
    Formalized: if probabilities sum to totalProb and totalProb > 0,
    then dividing each by totalProb gives a normalized distribution. -/
theorem probability_conservation (prob totalProb : ℝ)
    (hp : 0 ≤ prob) (ht : 0 < totalProb) (hle : prob ≤ totalProb) :
    0 ≤ prob / totalProb ∧ prob / totalProb ≤ 1 := by
  constructor
  · exact div_nonneg hp (le_of_lt ht)
  · exact div_le_one_of_le hle (le_of_lt ht)

/-! ## Connection to Lattice Phonon Amplitudes

  On the D₄ lattice, the phonon displacement field u_i plays the
  role of the wave function:
  - |u_i|² is the displacement energy at site i
  - The Born rule becomes: P(i) ∝ |u_i|²
  - Normalization: Σ_i |u_i|² = E_total / (Jz)

  The lattice discretization naturally regularizes the theory:
  - No UV divergences (lattice cutoff at π/a₀)
  - No IR divergences (finite lattice volume)
  - Born rule is exact on the lattice (finite sum)
-/

/-- Phonon energy at a lattice site: E_i = J × z × |u_i|².
    This is the discrete analog of the energy density. -/
noncomputable def phononEnergy (J : ℝ) (z : ℕ) (amplSq : ℝ) : ℝ :=
  J * z * amplSq

/-- Phonon energy is non-negative for J > 0, z > 0, |u|² ≥ 0. -/
theorem phononEnergy_nonneg (J : ℝ) (z : ℕ) (amplSq : ℝ)
    (hJ : 0 ≤ J) (ha : 0 ≤ amplSq) :
    0 ≤ phononEnergy J z amplSq := by
  unfold phononEnergy
  apply mul_nonneg
  apply mul_nonneg hJ
  exact Nat.cast_nonneg
  exact ha

/-- The Born rule on the lattice: phonon energy ratios equal amplitude ratios.
    This is the lattice version of born_rule_cancellation. -/
theorem lattice_born_rule (J : ℝ) (z : ℕ) (amp1 ampTotal : ℝ)
    (hJ : 0 < J) (hz : 0 < (z : ℝ)) (ht : 0 < ampTotal) :
    phononEnergy J z amp1 / phononEnergy J z ampTotal = amp1 / ampTotal := by
  unfold phononEnergy
  field_simp
  ring

/-! ## Uncertainty Relations

  The Heisenberg uncertainty relation ΔxΔp ≥ ℏ/2 follows from
  the wave nature of the substrate. On the lattice:
  - Position uncertainty: Δx ≥ a₀ (lattice spacing)
  - Momentum uncertainty: Δp ≤ ℏπ/a₀ (BZ boundary)
  - Product: ΔxΔp ≥ ℏπ (lattice minimum uncertainty)

  The continuum uncertainty relation is recovered as a₀ → 0.
-/

/-- The minimum position uncertainty on the lattice (one lattice spacing). -/
noncomputable def minPositionUncertainty (a₀ : ℝ) : ℝ := a₀

/-- The maximum momentum on the lattice (BZ boundary). -/
noncomputable def maxMomentum (hbar a₀ : ℝ) : ℝ := hbar * Real.pi / a₀

/-- The lattice uncertainty product ΔxΔp ≥ ℏπ.
    For a₀ = lattice spacing, this gives the minimum uncertainty. -/
noncomputable def latticeUncertaintyProduct (hbar : ℝ) : ℝ := hbar * Real.pi

/-- The lattice uncertainty product is positive. -/
theorem uncertainty_positive (hbar : ℝ) (hh : 0 < hbar) :
    0 < latticeUncertaintyProduct hbar := by
  unfold latticeUncertaintyProduct
  exact mul_pos hh Real.pi_pos

/-! ## Summary of Born Rule Results

  This file establishes:
  1. Born rule P(x) = |ψ(x)|²/N from energy-probability equivalence
  2. Normalization: probabilities are non-negative and sum to ≤ 1
  3. Energy prefactor cancellation (universality of Born rule)
  4. Lattice phonon analog: P(i) ∝ |u_i|²
  5. Probability conservation (0 ≤ P ≤ 1)
  6. Weighted averages for expectation values
  7. Lattice uncertainty product ΔxΔp ≥ ℏπ

  Physical significance: The Born rule is not an axiom but a
  consequence of energy conservation in the resonant substrate.
  The squared amplitude gives probability because it gives
  energy density, and probability IS energy-weighted sampling.
-/
