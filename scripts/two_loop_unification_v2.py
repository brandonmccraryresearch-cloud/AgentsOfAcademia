#!/usr/bin/env python3
"""
Gauge Unification Analysis v2: Alternative Embeddings (Tier 2, Task 2.3)

The v1 script showed that the SO(8) → G₂ → SM breaking cascade with
hidden scalar threshold corrections reduces the unification gap by only
0.1 units (17.0 → 16.9), far less than needed. This v2 script:

1. Diagnoses WHY the threshold corrections are so small
2. Tests alternative breaking chains and representations
3. Investigates whether the embedding indices can be modified
4. Provides an honest assessment of what is needed

Key finding: The fundamental issue is that the hidden multiplets are
color-charged scalars with SU(2) singlet quantum numbers. They affect
α₃ and α₁ but NOT α₂, which means they cannot reduce the spread
between all three couplings simultaneously. A successful unification
requires either:
  (a) Hidden multiplets with SU(2) quantum numbers (doublets)
  (b) A different embedding where the unification condition is NOT
      α₁ = α₂ = α₃ but rather a different relation (e.g., weighted sum)
  (c) A non-perturbative matching condition at M_lattice
"""
import numpy as np
import sys


def sm_beta_coefficients():
    """One-loop SM beta function coefficients b_i."""
    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0
    return np.array([b1, b2, b3])


def sm_two_loop_matrix():
    """Two-loop SM Machacek-Vaughn beta function matrix b_ij."""
    return np.array([
        [199.0/50, 27.0/10, 44.0/5],
        [9.0/10, 35.0/6, 12.0],
        [11.0/10, 9.0/2, -26.0]
    ])


def run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lattice, thresholds, n_steps=10000):
    """Run gauge couplings from M_Z to M_lattice at two-loop order."""
    b_sm = sm_beta_coefficients()
    b2_sm = sm_two_loop_matrix()

    t_start = np.log(M_Z)
    t_end = np.log(M_lattice)
    dt = (t_end - t_start) / n_steps

    alpha_inv = alpha_inv_MZ.copy()

    for step in range(n_steps):
        t = t_start + step * dt
        mu = np.exp(t)

        b_total = b_sm.copy()
        for M_th, db in thresholds:
            if mu > M_th:
                b_total += db

        alpha = 1.0 / alpha_inv
        dalpha_inv = -b_total / (2 * np.pi) * dt
        for i in range(3):
            for j in range(3):
                dalpha_inv[i] -= b2_sm[i, j] / (8 * np.pi**2) * alpha[j] * dt

        alpha_inv += dalpha_inv

    return alpha_inv


def threshold_contribution(su3_dim, su2_dim, Y, N_copies, is_fermion=False):
    """Compute beta coefficient contribution from a multiplet."""
    if su3_dim == 8:
        T3 = 3.0
    elif su3_dim == 3:
        T3 = 0.5
    else:
        T3 = 0.0

    if su2_dim == 2:
        T2 = 0.5
    elif su2_dim == 3:
        T2 = 2.0
    else:
        T2 = 0.0

    # Prefactor: 2/3 for Weyl fermion, 1/6 for real scalar, 1/3 for complex scalar
    if is_fermion:
        pf = 2.0 / 3.0
    else:
        pf = 1.0 / 6.0  # real scalar (conservative)

    db1 = pf * Y**2 * su3_dim * su2_dim * N_copies
    db2 = pf * T2 * su3_dim * N_copies
    db3 = pf * T3 * su2_dim * N_copies

    return np.array([db1, db2, db3])


def main():
    print("=" * 72)
    print("GAUGE UNIFICATION v2 — ALTERNATIVE MECHANISMS (v83.0 Session 3)")
    print("=" * 72)
    print()

    # Experimental inputs
    M_Z = 91.1876
    alpha_em_inv = 127.951
    sin2_tw = 0.23122
    alpha_s = 0.1179
    M_P = 1.22e19
    M_lat = M_P / np.sqrt(24)

    alpha1_inv = alpha_em_inv * (1 - sin2_tw) * 3.0/5
    alpha2_inv = alpha_em_inv * sin2_tw
    alpha3_inv = 1.0 / alpha_s
    alpha_inv_MZ = np.array([alpha1_inv, alpha2_inv, alpha3_inv])

    # ===== Part 1: Reproduce baseline =====
    print("Part 1: SM Two-Loop Baseline (No Thresholds)")
    print("-" * 60)
    alpha_sm = run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lat, [])
    spread_sm = alpha_sm[2] - alpha_sm[0]
    print(f"  α₁⁻¹ = {alpha_sm[0]:.2f},  α₂⁻¹ = {alpha_sm[1]:.2f},  α₃⁻¹ = {alpha_sm[2]:.2f}")
    print(f"  Spread: {spread_sm:.1f} units")
    print()

    # ===== Part 2: Diagnosis of v1 failure =====
    print("Part 2: Why v1 Threshold Corrections Fail")
    print("-" * 60)
    M_G2 = M_lat / np.sqrt(7)
    M_EW = M_lat / np.sqrt(14)

    # v1 hidden sector (real scalars, SU(2) singlets)
    v1_thresholds = [
        (M_G2, threshold_contribution(8, 1, 0.0, 1)),      # octet
        (M_G2, threshold_contribution(3, 1, 1/3, 2)),       # triplet pair
        (M_EW, threshold_contribution(3, 1, 1/3, 4)),       # 2×(3+3̄)
        (M_EW, threshold_contribution(1, 1, 0.0, 2)),       # singlets
    ]

    alpha_v1 = run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lat, v1_thresholds)
    spread_v1 = alpha_v1[2] - alpha_v1[0]
    print(f"  v1 result: spread = {spread_v1:.1f} units (improvement: {abs(spread_sm) - abs(spread_v1):.1f})")
    print()
    print("  Diagnosis:")
    db_total = sum(db for _, db in v1_thresholds)
    print(f"    Total Δb = ({db_total[0]:.3f}, {db_total[1]:.3f}, {db_total[2]:.3f})")
    print(f"    Δb₂ = {db_total[1]:.3f} ← ZERO! SU(2) singlets don't affect α₂!")
    print(f"    Only Δb₁ and Δb₃ are nonzero, so the corrections push α₁ and α₃")
    print(f"    but NOT α₂. This cannot close a three-way spread.")
    print()

    # ===== Part 3: Scenario A — SU(2) doublet hidden matter =====
    print("Part 3A: Scenario A — Add SU(2) Doublets to Hidden Sector")
    print("-" * 60)
    print("  If G₂ decomposition includes SU(2) doublets, Δb₂ becomes nonzero.")
    print("  Test: Add Weyl fermion doublets at intermediate scale.")
    print()

    # What if some hidden modes are fermions (Weyl) with SU(2) charges?
    # The 7(G₂) → (3,1)_{1/3} + (1,2)_{1/2} + (1,1)_0 under SM
    # This alternative branching gives SU(2) doublets
    scenarioA_thresholds = [
        (M_G2, threshold_contribution(8, 1, 0.0, 1)),           # octet (scalar)
        (M_G2, threshold_contribution(3, 1, 1/3, 2)),           # triplet pair (scalar)
        (M_EW, threshold_contribution(3, 1, 1/3, 2)),           # triplets (scalar)
        (M_EW, threshold_contribution(1, 2, 1/2, 4)),           # SU(2) doublets
        (M_EW, threshold_contribution(1, 1, 0.0, 2)),           # singlets
    ]
    alpha_A = run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lat, scenarioA_thresholds)
    spread_A = alpha_A[2] - alpha_A[0]
    db_A = sum(db for _, db in scenarioA_thresholds)
    print(f"  Δb = ({db_A[0]:.3f}, {db_A[1]:.3f}, {db_A[2]:.3f})")
    print(f"  α₁⁻¹ = {alpha_A[0]:.2f},  α₂⁻¹ = {alpha_A[1]:.2f},  α₃⁻¹ = {alpha_A[2]:.2f}")
    print(f"  Spread: {spread_A:.1f} units (improvement: {abs(spread_sm) - abs(spread_A):.1f})")
    print()

    # ===== Part 4: Scenario B — Weyl fermion hidden sector =====
    print("Part 3B: Scenario B — Weyl Fermion Hidden Sector")
    print("-" * 60)
    print("  If hidden modes are Weyl fermions (not scalars), β-coefficients")
    print("  are 4× larger (prefactor 2/3 vs 1/6).")
    print()

    scenarioB_thresholds = [
        (M_G2, threshold_contribution(8, 1, 0.0, 1, is_fermion=True)),
        (M_G2, threshold_contribution(3, 1, 1/3, 2, is_fermion=True)),
        (M_EW, threshold_contribution(3, 1, 1/3, 4, is_fermion=True)),
        (M_EW, threshold_contribution(1, 1, 0.0, 2, is_fermion=True)),
    ]
    alpha_B = run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lat, scenarioB_thresholds)
    spread_B = alpha_B[2] - alpha_B[0]
    db_B = sum(db for _, db in scenarioB_thresholds)
    print(f"  Δb = ({db_B[0]:.3f}, {db_B[1]:.3f}, {db_B[2]:.3f})")
    print(f"  α₁⁻¹ = {alpha_B[0]:.2f},  α₂⁻¹ = {alpha_B[1]:.2f},  α₃⁻¹ = {alpha_B[2]:.2f}")
    print(f"  Spread: {spread_B:.1f} units (improvement: {abs(spread_sm) - abs(spread_B):.1f})")
    print()

    # ===== Part 5: Scenario C — Modified unification condition =====
    print("Part 3C: Scenario C — Non-Standard Unification Condition")
    print("-" * 60)
    print("  Instead of α₁ = α₂ = α₃, the D₄/SO(8) embedding may require:")
    print("    α₁/k₁ = α₂/k₂ = α₃/k₃")
    print("  where k_i are the embedding indices of the SM subgroups in SO(8).")
    print()
    print("  For SO(8) → SM, the embedding indices depend on the breaking chain:")
    print("    Standard GUT: k₁ = 5/3, k₂ = 1, k₃ = 1")
    print("    SO(8) direct: k₁ = 1, k₂ = 1, k₃ = 1 (different normalization)")
    print()

    # Check if any set of k_i makes the couplings unify
    # We need k₁α₁⁻¹ = k₂α₂⁻¹ = k₃α₃⁻¹ at M_lat
    # This means k_i = c × α_i(M_lat) for some constant c
    # Normalized: k_i = α_i(M_lat) / α₃(M_lat)
    k_needed = alpha_sm / alpha_sm[2]
    print(f"  Needed k_i for unification: k₁ = {k_needed[0]:.3f}, k₂ = {k_needed[1]:.3f}, k₃ = {k_needed[2]:.3f}")
    print(f"  Ratio pattern: {k_needed[0]/k_needed[2]:.2f} : {k_needed[1]/k_needed[2]:.2f} : 1.00")
    print()

    # Check if this is the 6:4:3 pattern from SO(8)
    so8_643 = np.array([6, 4, 3], dtype=float)
    so8_643_norm = so8_643 / so8_643[2]
    print(f"  SO(8) 6:4:3 prediction: {so8_643_norm[0]:.2f} : {so8_643_norm[1]:.2f} : 1.00")
    print(f"  Actual needed:           {k_needed[0]:.2f} : {k_needed[1]:.2f} : 1.00")
    print(f"  → 6:4:3 does NOT match the needed ratios")
    print()

    # What about sin²θ_W = 3/13?
    # This gives α₁⁻¹/α₂⁻¹ = sin²θ_W/(1-sin²θ_W) × 5/3
    # = 0.23077/0.76923 × 5/3 = 0.3 × 5/3 = 0.5
    # Hmm, at M_Z. At M_lat the ratio changes.
    ratio_12_Mlat = alpha_sm[0] / alpha_sm[1]
    print(f"  At M_lat: α₁⁻¹/α₂⁻¹ = {ratio_12_Mlat:.3f}")
    print(f"  For sin²θ_W = 3/13: would need ratio ≈ {(3/13)/(1-3/13)*3/5:.3f}")
    print()

    # ===== Part 6: Scenario D — Large hidden sector at lower scale =====
    print("Part 3D: Scenario D — Hidden Sector at Intermediate Scale")
    print("-" * 60)
    print("  If hidden modes have masses much below M_lat (say M_int ~ 10¹⁵ GeV),")
    print("  the log factor ln(M_lat/M_int) is larger, enhancing corrections.")
    print()

    M_int = 1e15  # GeV — intermediate scale
    scenarioD_thresholds = [
        (M_int, threshold_contribution(8, 1, 0.0, 1)),
        (M_int, threshold_contribution(3, 2, 1/6, 3)),   # (3,2) with Y=1/6
        (M_int, threshold_contribution(1, 2, 1/2, 3)),   # doublets
        (M_int, threshold_contribution(3, 1, 1/3, 2)),
    ]
    alpha_D = run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lat, scenarioD_thresholds)
    spread_D = alpha_D[2] - alpha_D[0]
    db_D = sum(db for _, db in scenarioD_thresholds)
    print(f"  M_int = {M_int:.0e} GeV")
    print(f"  Δb = ({db_D[0]:.3f}, {db_D[1]:.3f}, {db_D[2]:.3f})")
    print(f"  α₁⁻¹ = {alpha_D[0]:.2f},  α₂⁻¹ = {alpha_D[1]:.2f},  α₃⁻¹ = {alpha_D[2]:.2f}")
    print(f"  Spread: {spread_D:.1f} units (improvement: {abs(spread_sm) - abs(spread_D):.1f})")
    print()

    # ===== Summary =====
    print("=" * 72)
    print("SUMMARY — UNIFICATION MECHANISM ANALYSIS")
    print("=" * 72)
    print()
    print(f"  {'Scenario':45s} {'Spread':>8s} {'Impr.':>8s}")
    print(f"  {'-'*45} {'-'*8} {'-'*8}")
    print(f"  {'SM only (two-loop baseline)':45s} {abs(spread_sm):7.1f}u {'—':>8s}")
    print(f"  {'v1: Real scalars, SU(2) singlets':45s} {abs(spread_v1):7.1f}u {abs(spread_sm)-abs(spread_v1):7.1f}u")
    print(f"  {'A: Add SU(2) doublets':45s} {abs(spread_A):7.1f}u {abs(spread_sm)-abs(spread_A):7.1f}u")
    print(f"  {'B: Weyl fermion hidden sector':45s} {abs(spread_B):7.1f}u {abs(spread_sm)-abs(spread_B):7.1f}u")
    print(f"  {'D: Intermediate scale (10¹⁵ GeV)':45s} {abs(spread_D):7.1f}u {abs(spread_sm)-abs(spread_D):7.1f}u")
    print()

    print("  HONEST ASSESSMENT:")
    print()
    print("  The fundamental obstacles to gauge unification in IRH are:")
    print()
    print("  1. STRUCTURAL: The hidden SO(8) modes are SU(2) singlets in the")
    print("     minimal G₂ decomposition. Without Δb₂ ≠ 0, α₂ cannot be pushed")
    print("     to converge with α₁ and α₃.")
    print()
    print("  2. QUANTITATIVE: Even with SU(2) doublets (Scenario A), the")
    print("     corrections are O(1) units, insufficient for a 17-unit gap.")
    print("     Closing the gap requires either much larger representations")
    print("     or a fundamentally different unification condition.")
    print()
    print("  3. CONCEPTUAL: The standard unification condition α₁ = α₂ = α₃")
    print("     may not apply in the D₄ lattice theory. The lattice regulator")
    print("     may impose a different matching condition (e.g., involving the")
    print("     lattice spacing and coordination number) that does not require")
    print("     exact equality of the couplings at any single scale.")
    print()

    best_improvement = max(
        abs(spread_sm) - abs(spread_v1),
        abs(spread_sm) - abs(spread_A),
        abs(spread_sm) - abs(spread_B),
        abs(spread_sm) - abs(spread_D),
    )
    print(f"  Best improvement achieved: {best_improvement:.1f} units out of {abs(spread_sm):.1f} needed")
    print(f"  Fraction closed: {best_improvement/abs(spread_sm)*100:.1f}%")
    print()

    if best_improvement < abs(spread_sm) / 2:
        print("  ⚠️ CONCLUSION: The perturbative threshold correction mechanism")
        print("     as currently formulated is INSUFFICIENT for gauge unification.")
        print("     The IRH framework needs either:")
        print("       (a) A non-perturbative matching condition at the lattice scale")
        print("       (b) An intermediate symmetry breaking scale with large representations")
        print("       (c) An alternative unification paradigm (e.g., Pati-Salam)")
        grade = "D+"
    else:
        print("  ✅ Significant progress toward unification")
        grade = "C+"

    print()
    print(f"  GRADE: {grade}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
