#!/usr/bin/env python3
"""
CKM Matrix Analysis v2: Triality Berry Phase + Mass Hierarchy (Tier 2, Task 2.2)

The v1 script correctly derived the CP-violating phase δ_CKM = 2π/(3√3) ≈ 1.209 rad
(0.8% agreement), but the Cabibbo angle sin θ_C = 0.439 was 93.7% off.

This v2 script investigates WHY the topology gives the phase correctly but not the
mixing magnitudes, and explores proper quark mass-ratio approaches:

1. Gatto-Sartori-Tonin (GST) relation: sin θ_C ≈ √(m_d/m_s)
   → Tests whether the D₄ geometry can predict m_d/m_s

2. Wolfenstein parametrization from mass ratios:
   → λ ≈ √(m_d/m_s), A ≈ (m_s/m_b)^(1/2), etc.

3. Honest assessment of what the triality model actually predicts vs. what
   requires additional structure (mass matrix texture).

Key finding: The triality Berry phase gives a TOPOLOGICAL invariant (the CP phase),
which is protected against continuous deformations and hence naturally geometric.
The mixing MAGNITUDES depend on the quark mass HIERARCHY, which is a dynamical
quantity requiring the Yukawa couplings — not just topology.
"""
import numpy as np
import sys


def ckm_phase_from_berry():
    """
    CKM CP phase from Berry holonomy on triality orbifold.

    δ_CKM = Φ × √(Ω_fund / 2π) = (2π/3) × 1/√3 = 2π/(3√3)
    """
    Phi = 2 * np.pi / 3
    Omega_fund = 2 * np.pi / 3
    delta_CKM = Phi * np.sqrt(Omega_fund / (2 * np.pi))
    return delta_CKM


def gst_relation():
    """
    Gatto-Sartori-Tonin relation: sin θ_C ≈ √(m_d/m_s).

    Using PDG 2024 running masses at 2 GeV (MS-bar):
      m_d = 4.7 ± 0.5 MeV
      m_s = 93.4 ± 8.6 MeV

    This gives sin θ_C = √(4.7/93.4) ≈ 0.224, within 1% of experiment.
    """
    m_d = 4.7e-3   # GeV (MS-bar at 2 GeV)
    m_s = 93.4e-3  # GeV
    m_b = 4.18     # GeV (MS-bar at m_b)
    m_u = 2.16e-3  # GeV
    m_c = 1.27     # GeV (MS-bar at m_c)
    m_t = 172.69   # GeV (pole mass)

    sin_theta_C = np.sqrt(m_d / m_s)
    theta_C = np.arcsin(sin_theta_C)

    return {
        'sin_theta_C': sin_theta_C,
        'theta_C_deg': np.degrees(theta_C),
        'm_d': m_d, 'm_s': m_s, 'm_b': m_b,
        'm_u': m_u, 'm_c': m_c, 'm_t': m_t,
    }


def wolfenstein_from_mass_ratios():
    """
    Derive Wolfenstein parameters from quark mass ratios.

    The "texture zero" ansatz (Fritzsch) gives:
      λ ≈ √(m_d/m_s)
      A ≈ (m_s/m_b) / λ²
      ρ, η from CP phase

    For the D₄ lattice, the quark mass ratios would need to come from
    the Yukawa couplings, which are related to the overlap integrals
    of wavefunctions on the triality orbifold.
    """
    gst = gst_relation()
    m_d, m_s, m_b = gst['m_d'], gst['m_s'], gst['m_b']
    m_u, m_c, m_t = gst['m_u'], gst['m_c'], gst['m_t']

    # Wolfenstein λ from GST
    lam = np.sqrt(m_d / m_s)

    # A from V_cb ≈ m_s/m_b (Fritzsch texture)
    V_cb = np.sqrt(m_s / m_b) * lam  # ≈ A λ²
    A = V_cb / lam**2

    # V_ub from up-sector
    V_ub = np.sqrt(m_u / m_t) * lam  # very rough
    rho_eta_sq = (V_ub / (A * lam**3))**2

    # CP phase
    delta = ckm_phase_from_berry()

    # Construct approximate CKM
    rho_bar = np.sqrt(rho_eta_sq) * np.cos(delta) if rho_eta_sq > 0 else 0
    eta_bar = np.sqrt(rho_eta_sq) * np.sin(delta) if rho_eta_sq > 0 else 0

    return lam, A, rho_bar, eta_bar, delta


def d4_mass_ratio_prediction():
    """
    Test whether D₄ geometry predicts m_d/m_s.

    The triality group Z₃ maps between generations. If the mass hierarchy
    follows from the D₄ lattice geometry, the ratio m_d/m_s should be
    related to a geometric invariant.

    Candidate: m_d/m_s = sin²(θ₀) where θ₀ = 2/9 (Koide phase)
    → sin²(2/9) = 0.0486 → √(0.0486) = 0.220 ← close to 0.224!

    Alternative: m_d/m_s = θ₀² = (2/9)² = 0.0494 → √(0.0494) = 0.222
    → Also close!

    These are numerically suggestive but require a derivation linking
    the Koide phase to the down-type quark mass hierarchy.
    """
    theta_0 = 2.0 / 9.0

    candidates = [
        ("sin²(θ₀)", np.sin(theta_0)**2),
        ("θ₀²", theta_0**2),
        ("θ₀ × sin(π/3)", theta_0 * np.sin(np.pi / 3)),
        ("1/20 (= 1/z_D₄ × 24/24)", 1.0 / 20.0),
        ("θ₀/√(4.5)", theta_0 / np.sqrt(4.5)),
    ]

    m_d_over_m_s_exp = 4.7 / 93.4

    results = []
    for name, ratio in candidates:
        sin_tc = np.sqrt(ratio)
        agreement = abs(sin_tc - 0.2265) / 0.2265 * 100
        results.append((name, ratio, sin_tc, agreement))

    return results, m_d_over_m_s_exp


def ckm_matrix_from_wolfenstein(lam, A, rho_bar, eta_bar):
    """Construct CKM matrix from Wolfenstein parameters to O(λ⁵)."""
    s12 = lam
    s23 = A * lam**2
    s13 = A * lam**3 * np.sqrt(rho_bar**2 + eta_bar**2) if (rho_bar**2 + eta_bar**2) > 0 else 0
    delta = np.arctan2(eta_bar, rho_bar) if (rho_bar != 0 or eta_bar != 0) else 0

    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(max(0, 1 - s13**2))

    V = np.array([
        [c12*c13, s12*c13, s13*np.exp(-1j*delta)],
        [-s12*c23 - c12*s23*s13*np.exp(1j*delta),
         c12*c23 - s12*s23*s13*np.exp(1j*delta),
         s23*c13],
        [s12*s23 - c12*c23*s13*np.exp(1j*delta),
         -c12*s23 - s12*c23*s13*np.exp(1j*delta),
         c23*c13]
    ])
    return V


def main():
    print("=" * 72)
    print("CKM ANALYSIS v2 — TRIALITY PHASE + MASS HIERARCHY (v83.0 Session 3)")
    print("=" * 72)
    print()

    # ===== Part 1: Berry phase (reproduced from v1) =====
    print("Part 1: CKM CP Phase from Berry Holonomy (CONFIRMED)")
    print("-" * 60)
    delta = ckm_phase_from_berry()
    delta_exp = 1.20
    print(f"  δ_CKM = 2π/(3√3) = {delta:.4f} rad")
    print(f"  Experiment:         {delta_exp:.2f} ± 0.08 rad")
    print(f"  Agreement:          {abs(delta - delta_exp)/delta_exp*100:.1f}%  ← CONFIRMED")
    print()

    # ===== Part 2: Cabibbo angle diagnosis =====
    print("Part 2: Cabibbo Angle — Diagnosis of 93.7% Failure")
    print("-" * 60)
    # v1 formula
    theta_0 = 2.0 / 9.0
    sin_tc_v1 = np.sqrt(theta_0 * np.sin(2 * np.pi / 3))
    sin_tc_exp = 0.22650
    print(f"  v1 formula: sin θ_C = √(θ₀ × sin(2π/3)) = {sin_tc_v1:.4f}")
    print(f"  Experiment: sin θ_C = {sin_tc_exp:.5f}")
    print(f"  Discrepancy: {abs(sin_tc_v1 - sin_tc_exp)/sin_tc_exp*100:.1f}%")
    print()
    print("  DIAGNOSIS: The v1 formula is an ad hoc geometric-mean construction")
    print("  with no derivation from the D₄ orbifold. The factor sin(2π/3) = √3/2")
    print("  was chosen to get a number in the right ballpark, but it misses by")
    print("  nearly 2× because it conflates the TOPOLOGICAL Berry phase (which")
    print("  gives δ_CKM correctly) with the DYNAMICAL mass mixing (which requires")
    print("  knowledge of quark mass ratios).")
    print()

    # ===== Part 3: GST relation =====
    print("Part 3: Gatto-Sartori-Tonin Relation")
    print("-" * 60)
    gst = gst_relation()
    print(f"  sin θ_C ≈ √(m_d/m_s) = √({gst['m_d']*1e3:.1f}/{gst['m_s']*1e3:.1f} MeV)")
    print(f"  = √({gst['m_d']/gst['m_s']:.5f}) = {gst['sin_theta_C']:.5f}")
    print(f"  Experiment:                        {sin_tc_exp:.5f}")
    print(f"  Agreement:                         {abs(gst['sin_theta_C'] - sin_tc_exp)/sin_tc_exp*100:.1f}%")
    print()
    print("  The GST relation is a well-known result from Fritzsch texture-zero")
    print("  mass matrices. It succeeds because the Cabibbo angle is determined")
    print("  by the down-type quark mass RATIO, not by the topology.")
    print()

    # ===== Part 4: Can D₄ predict m_d/m_s? =====
    print("Part 4: D₄ Geometric Candidates for m_d/m_s")
    print("-" * 60)
    candidates, md_ms_exp = d4_mass_ratio_prediction()
    print(f"  Experimental m_d/m_s = {md_ms_exp:.5f}")
    print(f"  Need: sin θ_C = √(m_d/m_s) ≈ {sin_tc_exp}")
    print()
    print(f"  {'Candidate':30s} {'m_d/m_s':>10s} {'sin θ_C':>10s} {'Off':>8s}")
    print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*8}")
    for name, ratio, sin_tc, off in candidates:
        print(f"  {name:30s} {ratio:10.5f} {sin_tc:10.5f} {off:7.1f}%")
    print()

    # Highlight the best
    best = min(candidates, key=lambda x: x[3])
    print(f"  Best candidate: {best[0]}")
    print(f"  → sin θ_C = {best[2]:.5f} ({best[3]:.1f}% off)")
    print()
    print("  NOTE: sin²(θ₀) and θ₀² are numerically close to m_d/m_s, but")
    print("  this is a NUMERICAL COINCIDENCE unless a derivation is provided")
    print("  linking the Koide phase to the down-type quark mass hierarchy.")
    print("  The IRH framework does not currently provide this link.")
    print()

    # ===== Part 5: Full CKM from Wolfenstein =====
    print("Part 5: Full CKM Matrix (GST + Berry Phase)")
    print("-" * 60)
    lam, A, rho_bar, eta_bar, delta = wolfenstein_from_mass_ratios()
    V = ckm_matrix_from_wolfenstein(lam, A, rho_bar, eta_bar)
    V_abs = np.abs(V)

    print(f"  Wolfenstein parameters:")
    print(f"    λ = {lam:.4f}  (exp: 0.2265, {abs(lam-0.2265)/0.2265*100:.1f}%)")
    print(f"    A = {A:.4f}  (exp: 0.790, {abs(A-0.790)/0.790*100:.1f}%)")
    print(f"    ρ̄ = {rho_bar:.4f}  (exp: 0.141)")
    print(f"    η̄ = {eta_bar:.4f}  (exp: 0.357)")
    print(f"    δ = {delta:.4f} rad (from Berry holonomy)")
    print()

    labels_u = ['u', 'c', 't']
    labels_d = ['d', 's', 'b']
    print("  |V_CKM| (GST + Berry phase):")
    print(f"         {'d':>10s} {'s':>10s} {'b':>10s}")
    for i in range(3):
        print(f"    {labels_u[i]:2s}: {V_abs[i,0]:10.4f} {V_abs[i,1]:10.4f} {V_abs[i,2]:10.4f}")
    print()

    V_exp = np.array([
        [0.97370, 0.2245, 0.00382],
        [0.2244, 0.9730, 0.0422],
        [0.0086, 0.0414, 0.9991]
    ])
    print("  |V_CKM| (experimental PDG):")
    print(f"         {'d':>10s} {'s':>10s} {'b':>10s}")
    for i in range(3):
        print(f"    {labels_u[i]:2s}: {V_exp[i,0]:10.4f} {V_exp[i,1]:10.4f} {V_exp[i,2]:10.4f}")
    print()

    # Element-by-element comparison
    print("  Element-by-element agreement:")
    for i in range(3):
        for j in range(3):
            if V_exp[i, j] > 0.001:
                pct = abs(V_abs[i, j] - V_exp[i, j]) / V_exp[i, j] * 100
                status = "✅" if pct < 10 else ("⚠️" if pct < 50 else "❌")
                print(f"    |V_{labels_u[i]}{labels_d[j]}| = {V_abs[i,j]:.4f} (exp: {V_exp[i,j]:.4f}, {pct:.1f}%) {status}")
    print()

    # Unitarity
    VVd = V @ V.conj().T
    unitarity = np.max(np.abs(VVd - np.eye(3)))
    print(f"  Unitarity: max|VV† - I| = {unitarity:.2e} {'PASS ✅' if unitarity < 1e-10 else 'CHECK'}")
    print()

    # ===== Summary =====
    print("=" * 72)
    print("SUMMARY — CKM ANALYSIS")
    print("=" * 72)
    print()
    print("  What the D₄ triality DOES predict:")
    print("    ✅ CP phase δ_CKM = 2π/(3√3) = 1.209 rad (0.8% agreement)")
    print("       → TOPOLOGICAL invariant of the triality orbifold")
    print("       → Protected against continuous deformations")
    print()
    print("  What the D₄ triality does NOT yet predict:")
    print("    ❌ Cabibbo angle (mixing magnitude)")
    print("       → Requires quark mass ratios m_d/m_s (DYNAMICAL, not topological)")
    print("       → GST relation sin θ_C ≈ √(m_d/m_s) works at 1% but needs")
    print("         the mass ratio as input")
    print("    ❌ Full CKM matrix (V_cb, V_ub magnitudes)")
    print("       → Requires all 6 quark masses or Yukawa texture structure")
    print()
    print("  Physical insight: The CP phase is a TOPOLOGICAL quantity (Berry phase)")
    print("  while the mixing magnitudes are DYNAMICAL quantities (mass ratios).")
    print("  The D₄ lattice naturally provides topological invariants but does")
    print("  not yet derive the Yukawa coupling hierarchy from geometry.")
    print()
    print("  Possible path forward:")
    print("    • Derive m_d/m_s from Koide-like relation for down quarks")
    print("    • Connect quark mass hierarchy to D₄ phonon spectrum structure")
    print("    • Use texture-zero ansatz constrained by triality symmetry")
    print()

    # Cabibbo angle with best D₄ candidate
    best_sin_tc = np.sqrt(np.sin(theta_0)**2)  # sin²(θ₀) candidate
    print(f"  Speculative: If m_d/m_s = sin²(θ₀) = {np.sin(theta_0)**2:.5f}")
    print(f"    → sin θ_C = sin(θ₀) = {np.sin(theta_0):.5f}")
    print(f"    → Agreement: {abs(np.sin(theta_0) - 0.2265)/0.2265*100:.1f}%")
    print(f"    → This would be a genuine prediction IF derivable from D₄.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
