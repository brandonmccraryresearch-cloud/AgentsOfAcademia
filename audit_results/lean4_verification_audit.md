# Lean 4 Formal Verification Specialist — Derivation Audit

**Subject:** Intrinsic Resonance Holography (IRH), Version 73.1.1  
**Author Under Review:** Brandon D. McCrary  
**Audit Date:** March 2026  
**Auditor Persona:** MATH_PHYSICS_REASONER_V1 (v1.0.0)

---

## Protocol

Every derivation below is processed through the mandatory Four-Phase Reasoning Protocol:
1. **Phase 1 — Structural Decomposition:** Formally rephrase; identify domain; list axioms; declare strategy.
2. **Phase 2 — Tool-Integrated Thinking:** Dimensional analysis; pseudo-Lean 4 tactic states; numerical verification.
3. **Phase 3 — Recursive Critique:** Review for unproven lemmas; issue [BACKTRACK] if needed.
4. **Phase 4 — Final Synthesis:** LaTeX output; Confidence Score; Verification Method.

---

## Derivation 1: Fine-Structure Constant Formula

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify whether $\alpha^{-1} = 137 + \frac{1}{28 - \pi/14}$ follows from any action principle or constitutes an empirical observation.

**Domain:** Lie algebra representation theory, number theory.

**Axioms Invoked:**
- $\dim(\mathrm{SO}(8)) = 8 \times 7 / 2 = 28$ (standard Lie group dimension formula)
- $\dim(G_2) = 14$ (exceptional Lie group)
- $\pi = 3.14159265...$

**Strategy:** Direct numerical verification + logical analysis of derivation chain.

### Phase 2 — Tool-Integrated Thinking

```lean
-- Tactic state: ⊢ α⁻¹ = 137 + 1/(28 - π/14)
-- Numerical verification:
theorem alpha_inv_numerical : 
  137 + 1/(28 - Real.pi/14) ≈ 137.0360028 := by
  -- dim_SO8 := 28
  -- dim_G2 := 14
  -- correction := 1/(28 - π/14) = 1/27.7756 = 0.03600282
  -- α⁻¹ = 137.0360028
  norm_num
  -- tactic state: verified numerically ✓
```

**Dimensional Analysis:** $\alpha$ is dimensionless. $\dim(\mathrm{SO}(8)) = 28$ is dimensionless (an integer). $\pi/14$ is dimensionless. The formula is dimensionally consistent. ✓

**Numerical Computation:**
```
28 - π/14 = 28 - 0.22440 = 27.77560
1/27.77560 = 0.036003
137 + 0.036003 = 137.036003

Experimental: α⁻¹ = 137.0359990840(21)
|Theory - Experiment| = 3.74 × 10⁻⁶
Relative discrepancy = 27.3 ppb
```

### Phase 3 — Recursive Critique

**[BACKTRACK]** — The numerical agreement is verified, but the logical chain from the $D_4$ lattice action to this specific combination of Lie group dimensions is missing. The paper's argument proceeds:

1. The integer 137 = $2 \times 8^2 + 8 + 1$ — a representation decomposition. ✓ (algebraically true)
2. The correction $1/(28 - \pi/14)$ encodes "triality breaking" — but no Lagrangian or action principle produces this specific functional form.
3. The paper itself (§II.3) acknowledges these are "empirical conjectures."

Returning to Phase 2 with revised assessment: the formula is a numerical observation, not a theorem.

### Phase 4 — Final Synthesis

The formula $\alpha^{-1} = 137 + 1/(28 - \pi/14)$ achieves 27 ppb agreement with experiment. The constituent integers (28, 14) are genuine Lie group dimensions of $\mathrm{SO}(8)$ and $G_2$. However, no derivation from a Lagrangian, path integral, or action principle has been provided. The formula is an empirical conjecture with suggestive group-theoretic content.

```
Confidence Score: 95% (numerical verification)
                  15% (derivational completeness)
Verification Method: Independent numerical computation
```

---

## Derivation 2: Koide Lepton Mass Formula

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify the mass formula $m_n = M_\text{scale}[1 + \sqrt{2}\cos(\theta_0 + 2\pi n/3)]^2$ with $\theta_0 = 2/9$, and test the paper's claim that $Q[\theta] = 2/3$ for all $\theta$.

**Domain:** Spectral theory on compact manifolds; trigonometric identities.

**Axioms:**
- $\sum_{n=0}^{2} \cos(\theta + 2\pi n/3) = 0$ for all $\theta$ (trigonometric identity)
- $\sum_{n=0}^{2} \cos^2(\theta + 2\pi n/3) = 3/2$ for all $\theta$ (trigonometric identity)
- $Q = \sum m_n / (\sum \sqrt{m_n})^2$ (Koide ratio definition)

**Strategy:** Direct computation + algebraic analysis of Q universality.

### Phase 2 — Tool-Integrated Thinking

```lean
-- Tactic state: ⊢ Q[θ] = 2/3 for all θ
-- Define amplitude: amp_n(θ) := 1 + √2·cos(θ + 2πn/3)
-- mass: m_n = M·(amp_n)²
-- √m_n = √M·|amp_n|  (absolute value required since mass ≥ 0)
-- 
-- Numerator: Σ m_n = M·Σ amp_n²
-- Using identities: Σ amp_n² = Σ(1 + 2√2·cos + 2·cos²)
--   = 3 + 2√2·(Σcos) + 2·(Σcos²) = 3 + 0 + 2·(3/2) = 6
-- ∴ Numerator = 6M  ✓ (for all θ)
--
-- Denominator: (Σ √m_n)² = M·(Σ |amp_n|)²
-- Case 1: All amp_n > 0: Σ|amp_n| = Σ amp_n = 3 + √2·(Σcos) = 3
--   ∴ Q = 6M/(M·9) = 6/9 = 2/3 ✓
-- Case 2: Some amp_n < 0: Σ|amp_n| > Σ amp_n = 3
--   ∴ Q = 6/(Σ|amp_n|)² < 6/9 = 2/3 ✗
```

**[BACKTRACK]** — The claim Q = 2/3 for ALL θ is false. Q = 2/3 holds only when all three amplitudes are positive.

Returning to Phase 2 with corrected analysis:

**Boundary condition for Q = 2/3:**
```
amp_n > 0 ⟺ cos(θ + 2πn/3) > -1/√2
⟺ θ + 2πn/3 ∉ (3π/4, 5π/4)  [mod 2π]

For the most restrictive case (n=1):
θ + 2π/3 < 3π/4  ⟹  θ < 3π/4 - 2π/3 = π/12

∴ Q = 2/3 iff θ₀ ∈ [0, π/12) ≈ [0, 0.2618)
```

Since $\theta_0 = 2/9 \approx 0.2222 < \pi/12 \approx 0.2618$, the empirically relevant value is within the valid range.

**Numerical mass verification:**
```
M_scale = 313.84 MeV (from measured masses)

n=0 (τ):  θ = 0.2222, m = 1776.88 MeV  [expt: 1776.86, err: 0.001%]
n=1 (e):  θ = 2.3166, m = 0.5110 MeV   [expt: 0.51100, err: 0.006%]
n=2 (μ):  θ = 4.4110, m = 105.65 MeV   [expt: 105.658, err: 0.005%]
```

### Phase 3 — Recursive Critique

Two issues identified:

1. **Q universality claim is false.** The paper states (§III.6): "Q[θ] = 2/3 for all values of θ." This is mathematically incorrect. The correct statement is: Q[θ] = 2/3 for θ ∈ [0, π/12), where all three amplitudes remain positive.

2. **θ₀ = 2/9 is not derived from pure geometry.** The paper presents a geometric argument involving $\Omega_\text{fund} = 2\pi/3$ but then acknowledges that θ₀ is "fixed by any one of them [the measured masses]." This makes θ₀ a calibrated parameter, not a prediction.

### Phase 4 — Final Synthesis

The Koide parametrization $m_n = M[1 + \sqrt{2}\cos(\theta_0 + 2\pi n/3)]^2$ correctly reproduces the charged lepton masses to high precision with $\theta_0 = 2/9$ and $M = 313.84$ MeV. However:

- $Q = 2/3$ is NOT universal — it requires $\theta_0 \in [0, \pi/12)$
- $\theta_0$ is calibrated from experiment, not derived from $D_4$ geometry
- $M_\text{scale}$ is defined from measured masses

```
Confidence Score: 98% (numerical mass predictions)
                  30% (claim that θ₀ is derived from D₄)
                   0% (claim that Q = 2/3 for all θ)
Verification Method: Independent numerical computation + algebraic proof of Q universality failure
```

---

## Derivation 3: Higgs VEV Formula

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify $v = E_P \times \alpha^9 \times \pi^5 \times 9/8$ and assess whether the two VEV formulas (A and B) are consistent.

**Domain:** Dimensional analysis; renormalization group theory.

**Strategy:** Direct computation of both formulas; consistency analysis.

### Phase 2 — Tool-Integrated Thinking

**Dimensional Analysis:**
```
[E_P] = GeV
[α⁹] = dimensionless
[π⁵] = dimensionless
[9/8] = dimensionless
∴ [v] = GeV ✓
```

**Numerical Computation:**
```
Formula A: v = 1.22089 × 10¹⁹ × (1/137.036)⁹ × π⁵ × 9/8
         = 1.22089 × 10¹⁹ × 5.868 × 10⁻²⁰ × 306.02 × 1.125
         = 246.64 GeV

Formula B: v_bare = E_P × α⁸ × π² × 9/8
         = 1.22089 × 10¹⁹ × 8.038 × 10⁻¹⁸ × 9.870 × 1.125
         = 1090.1 GeV

Ratio: v_A/v_B = α × π³ = (1/137.036) × 31.006 = 0.2263
```

### Phase 3 — Recursive Critique

**[BACKTRACK]** — The two formulas differ by a factor $\alpha \pi^3 \approx 0.226$. The paper claims this difference is due to "renormalization effects" but provides no renormalization calculation. Without a concrete RG flow computation, this is an ad hoc adjustment, not a derivation.

Additionally, the exponent $n = 9$ is obtained by rounding $\ln(E_P/v)/\ln(\alpha^{-1}) \approx 7.8$ up to 9. The "+5.5 threshold correction" invoked in Appendix E (§E.1) is stated but not derived from the lattice dynamics.

### Phase 4 — Final Synthesis

Formula A achieves 0.17% agreement with the measured Higgs VEV. Formula B gives 1090 GeV, off by a factor of ~4.4. The two formulas are inconsistent, and the "renormalization" bridging them is not computed. The exponent 9 is semi-empirically determined.

```
Confidence Score: 90% (Formula A numerical agreement)
                  10% (derivational chain from lattice action to VEV)
                   5% (Formula A/B consistency)
Verification Method: Independent numerical computation
```

---

## Derivation 4: Cosmological Constant

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify $\rho_\Lambda/\rho_P = \alpha^{57}/(4\pi)$ and assess the derivation.

**Domain:** Statistical mechanics; lattice field theory.

**Strategy:** Numerical verification + logical assessment of the 57 = 3 × 19 argument.

### Phase 2 — Tool-Integrated Thinking

**Dimensional Analysis:**
```
[ρ_Λ/ρ_P] = dimensionless
[α⁵⁷] = dimensionless
[4π] = dimensionless ✓
```

**Numerical Computation:**
```
α = 1/137.036003
α⁵⁷ = (7.297 × 10⁻³)⁵⁷ = 1.585 × 10⁻¹²²
α⁵⁷/(4π) = 1.262 × 10⁻¹²³

ρ_Λ = 1.262 × 10⁻¹²³ × 2.22 × 10⁷⁶ GeV⁴ = 2.80 × 10⁻⁴⁷ GeV⁴
Experimental: 2.846 × 10⁻⁴⁷ GeV⁴
Discrepancy: 1.5%
```

### Phase 3 — Recursive Critique

The agreement across 123 orders of magnitude is remarkable. However:

1. **The exponent 57 = 3 × 19 is a product of integers chosen post hoc.** The factorization "triality (3) × shear modes (19)" is suggestive but not derived from a partition function or path integral.
2. **Why α as the transmission coefficient?** The paper asserts that α represents the "impedance matching" between lattice levels, but this is not demonstrated from the lattice Hamiltonian.
3. **The factor $4\pi$ is a conventional geometric factor** that could easily absorb small numerical discrepancies.
4. **Alternative exponents:** $\alpha^{56}/(4\pi) \approx 1.73 \times 10^{-121}$ and $\alpha^{58}/(4\pi) \approx 9.21 \times 10^{-126}$ would not match as well, but this sensitivity to the exponent means the agreement is only valid if 57 is correct.

### Phase 4 — Final Synthesis

The formula $\rho_\Lambda/\rho_P = \alpha^{57}/(4\pi)$ achieves 1.5% agreement with the observed cosmological constant, spanning 123 orders of magnitude. The factorization 57 = 3 × 19 is numerologically appealing but not derived. The use of α as the transmission coefficient is assumed, not proven.

```
Confidence Score: 95% (numerical computation)
                  20% (derivational completeness)
Verification Method: Independent numerical computation
```

---

## Derivation 5: Appendix D Algebra

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify $137 = 2n^2 + n + 1$ for $n = 8$ and check the alternative form $(2n+1)^2 - 1)/2 + 1$.

**Strategy:** Direct computation.

### Phase 2 — Tool-Integrated Thinking

```
2n² + n + 1 (n=8):
  2(64) + 8 + 1 = 128 + 8 + 1 = 137 ✓

[(2n+1)² - 1]/2 + 1 (n=8):
  (17² - 1)/2 + 1 = (289 - 1)/2 + 1 = 144 + 1 = 145 ≠ 137 ✗

Note: (2n+1)² - 1 = 4n² + 4n = 4n(n+1)
  so [(2n+1)² - 1]/2 + 1 = 2n² + 2n + 1 ≠ 2n² + n + 1
  The difference is n = 8.
```

### Phase 4 — Final Synthesis

Version 73.1.1 correctly identifies and fixes this algebraic error. The correct identity is $137 = 2 \times 8^2 + 8 + 1 = 128 + 8 + 1$.

```
Confidence Score: 100%
Verification Method: Direct algebraic computation
```

---

## Derivation 6: Weak Mixing Angle

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify $\sin^2\theta_W = 3/13$ from the dimension ratio $\dim(\mathfrak{su}(2))/[\dim(\mathfrak{so}(8)) - \dim(\mathfrak{su}(4))]$.

**Domain:** Lie algebra; electroweak theory.

### Phase 2 — Tool-Integrated Thinking

```
dim(so(8)) = 28  ✓ [8×7/2]
dim(su(4)) = 15  ✓ [4²-1]
dim(su(2)) = 3   ✓ [2²-1]

Residual dimension: 28 - 15 = 13
Ratio: 3/13 = 0.23077

Experimental: sin²θ_W(M_Z) = 0.23122 ± 0.00004
Discrepancy: 0.19%
```

### Phase 3 — Recursive Critique

The formula is dimensionally consistent and uses correct Lie group dimensions. However, the interpretation of $\sin^2\theta_W$ as the ratio $\dim(\mathfrak{su}(2))/[\dim(\mathfrak{so}(8)) - \dim(\mathfrak{su}(4))]$ is non-standard. In GUT approaches, $\sin^2\theta_W$ at unification is typically $3/8$ (for $\mathrm{SU}(5)$) or other values depending on the GUT group. The ratio 3/13 does not correspond to any standard embedding index calculation.

The 0.19% discrepancy is claimed to arise from radiative corrections (RG running from the unification scale to $M_Z$), which is plausible but not computed.

### Phase 4 — Final Synthesis

The formula $\sin^2\theta_W = 3/13$ gives 0.19% agreement with experiment. The group-theoretic motivation is creative but non-standard. The specific ratio of $\dim(\mathfrak{su}(2)_L)$ to the "electroweak residual" $\dim(\mathfrak{so}(8)) - \dim(\mathfrak{su}(4))$ is asserted without derivation from a branching rule or representation decomposition.

```
Confidence Score: 95% (numerical verification)
                  25% (group-theoretic derivation)
Verification Method: Lie algebra dimension computation
```

---

## Derivation 7: SVEA → Schrödinger Equation

### Phase 1 — Structural Decomposition

**Problem Statement:** Verify that the SVEA applied to the Klein-Gordon equation on the $D_4$ lattice yields the Schrödinger equation.

**Domain:** Wave mechanics; asymptotic analysis.

**Strategy:** Direct algebraic verification of the SVEA substitution.

### Phase 2 — Tool-Integrated Thinking

Starting from the Klein-Gordon equation:
$$\frac{1}{c^2}\frac{\partial^2\Phi}{\partial t^2} - \nabla^2\Phi + \frac{m^2c^2}{\hbar^2}\Phi = 0$$

SVEA ansatz: $\Phi = \psi \cdot e^{-i\Omega_P t}$ where $\Omega_P = M_P c^2/\hbar$.

Time derivatives:
$$\frac{\partial\Phi}{\partial t} = (\dot\psi - i\Omega_P\psi)e^{-i\Omega_P t}$$
$$\frac{\partial^2\Phi}{\partial t^2} = (\ddot\psi - 2i\Omega_P\dot\psi - \Omega_P^2\psi)e^{-i\Omega_P t}$$

SVEA: drop $\ddot\psi$ (slowly varying). Substituting:
$$\frac{1}{c^2}(-2i\Omega_P\dot\psi - \Omega_P^2\psi) - \nabla^2\psi + \frac{M_P^2c^2}{\hbar^2}\psi + \frac{2M_Pm_\text{eff}c^2}{\hbar^2}\psi = 0$$

The $-\Omega_P^2/c^2$ and $+M_P^2c^2/\hbar^2$ terms cancel (since $\Omega_P = M_Pc^2/\hbar$).

Remaining:
$$-\frac{2i\Omega_P}{c^2}\dot\psi - \nabla^2\psi + \frac{2M_Pm_\text{eff}c^2}{\hbar^2}\psi = 0$$

Multiply by $-\hbar^2/(2M_P)$:
$$i\hbar\dot\psi = -\frac{\hbar^2}{2M_P}\nabla^2\psi + m_\text{eff}c^2\psi$$

### Phase 3 — Recursive Critique

The algebra is correct ✓. However, there is a critical issue: the kinetic mass in the result is $M_P$ (the Planck mass), not the particle mass $m$. The paper invokes "effective mass theory" to replace $M_P \to m$, but this requires:

1. A band structure calculation on the $D_4$ lattice showing that excitations near a triality defect have effective mass $m \ll M_P$.
2. This effective mass theory is standard in condensed matter physics but has not been explicitly computed for the $D_4$ lattice.

Without this calculation, the SVEA derivation produces a Schrödinger equation with the wrong mass.

### Phase 4 — Final Synthesis

The SVEA derivation from Klein-Gordon to Schrödinger is algebraically correct. The cancellation of rest-mass terms and the SVEA approximation are standard techniques. However, the resulting kinetic mass is $M_P$, not the particle mass $m$. The bridge from $M_P$ to $m$ via effective mass theory is invoked but not computed.

```
Confidence Score: 95% (algebraic correctness of SVEA)
                  30% (completeness of derivation including mass identification)
Verification Method: Step-by-step algebraic verification
```

---

## Summary Table

| Derivation | Numerical | Derivational | Key Issue |
|:-----------|:----------|:-------------|:----------|
| 1. α⁻¹ formula | ✅ 27 ppb | ⚠ Conjecture | No Lagrangian derivation |
| 2. Koide masses | ✅ 0.006% | ⚠ Calibrated | Q=2/3 universality FALSE |
| 3. Higgs VEV | ✅ 0.17% | ⚠ Semi-fitted | Two formulas inconsistent |
| 4. Cosmo. const. | ✅ 1.5% | ⚠ Numerology | Exponent 57 not derived |
| 5. Appendix D | ✅ Fixed | ✅ Correct | Error properly corrected |
| 6. sin²θ_W | ✅ 0.19% | ⚠ Non-standard | No branching rule derivation |
| 7. SVEA→Schrödinger | ✅ Algebraic | ⚠ Mass gap | Kinetic mass = M_P, not m |
