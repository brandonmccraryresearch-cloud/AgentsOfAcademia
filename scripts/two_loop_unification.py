#!/usr/bin/env python3
"""
Priority 4: Two-Loop Gauge Unification with Hidden-Sector Threshold Corrections

Implements the full two-loop RG running of SM gauge couplings from M_Z to
M_lattice = M_P/√24, including threshold corrections from the 20 hidden
D₄ phonon modes with representations determined by the SO(8) → G₂ → SM
symmetry breaking cascade.

The SO(8) adjoint (28-dim) decomposes as:
  28 → 14(G₂) ⊕ 7(G₂) ⊕ 7(G₂)

Under SM embedding: 14(G₂) → 8(SU3) ⊕ 3(SU3) ⊕ 3̄(SU3)
                     7(G₂)  → 3(SU3) ⊕ 3̄(SU3) ⊕ 1(SU3)

Hidden DOF threshold masses from dimensional scaling:
  M_G₂ = M_lattice/√7 ≈ 9.4 × 10¹⁷ GeV
  M_EW = M_lattice/√14 ≈ 6.7 × 10¹⁷ GeV
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


def hidden_sector_beta_coefficients():
    """
    One-loop beta coefficient contributions from hidden D₄ modes.
    
    The SO(8) → G₂ decomposition gives:
    - 14(G₂) at M_G₂: contains octet (8,1)₀ + triplets (3+3̄,1)_Y
    - 7(G₂) ×2 at M_EW: contains (3+3̄+1,1)_Y'
    
    Hypercharge assignments from G₂ embedding:
      For 14: Y = ±1/3 for the triplets (same as d_R quarks)
      For 7:  Y = ±1/3 for triplets, 0 for singlet
    """
    # Hidden multiplets: (name, SU3_dim, SU2_dim, Y, N_copies, mass_label)
    multiplets = [
        # From 14(G₂)
        ("14_octet", 8, 1, 0.0, 1, "M_G2"),          # Color octet, EW singlet
        ("14_triplet", 3, 1, 1.0/3, 2, "M_G2"),       # Color triplet pair (3 + 3̄)
        # From 7(G₂) × 2
        ("7_triplet", 3, 1, 1.0/3, 4, "M_EW"),        # 2×(3 + 3̄)
        ("7_singlet", 1, 1, 0.0, 2, "M_EW"),           # 2×(1)
    ]
    
    delta_b = {"M_G2": np.zeros(3), "M_EW": np.zeros(3)}
    
    for name, su3, su2, Y, N, mass_label in multiplets:
        # SU(3) contribution: (2/3) × T(R) × d(SU2) × N for real scalars
        if su3 == 8:
            T3 = 3.0  # Dynkin index of adjoint
        elif su3 == 3:
            T3 = 0.5  # Dynkin index of fundamental
        else:
            T3 = 0.0
        
        # SU(2) contribution
        if su2 == 2:
            T2 = 0.5
        else:
            T2 = 0.0
        
        # U(1) contribution: (2/3) × Y² × d(SU3) × d(SU2) × N for real scalars
        db1 = (2.0/3) * Y**2 * su3 * su2 * N
        db2 = (2.0/3) * T2 * su3 * N
        db3 = (2.0/3) * T3 * su2 * N
        
        delta_b[mass_label] += np.array([db1, db2, db3])
    
    return delta_b, multiplets


def run_couplings_two_loop(alpha_inv_MZ, M_Z, M_lattice, M_thresholds, 
                            delta_b_thresholds, n_steps=10000):
    """
    Run gauge couplings from M_Z to M_lattice at two-loop order.
    
    Uses step-wise integration with threshold corrections.
    """
    b_sm = sm_beta_coefficients()
    b2_sm = sm_two_loop_matrix()
    
    t_start = np.log(M_Z)
    t_end = np.log(M_lattice)
    dt = (t_end - t_start) / n_steps
    
    alpha_inv = alpha_inv_MZ.copy()
    
    # Sort thresholds
    sorted_thresholds = sorted(M_thresholds.items(), key=lambda x: x[1])
    
    for step in range(n_steps):
        t = t_start + step * dt
        mu = np.exp(t)
        
        # Determine active beta coefficients
        b_total = b_sm.copy()
        for label, M_th in sorted_thresholds:
            if mu > M_th:
                b_total += delta_b_thresholds[label]
        
        # Current couplings
        alpha = 1.0 / alpha_inv
        
        # One-loop
        dalpha_inv = -b_total / (2 * np.pi) * dt
        
        # Two-loop
        for i in range(3):
            for j in range(3):
                dalpha_inv[i] -= b2_sm[i, j] / (8 * np.pi**2) * alpha[j] * dt
        
        alpha_inv += dalpha_inv
    
    return alpha_inv


def main():
    print("=" * 72)
    print("TWO-LOOP GAUGE UNIFICATION WITH HIDDEN-SECTOR THRESHOLDS (v83.0)")
    print("=" * 72)
    print()
    
    # Experimental inputs at M_Z
    M_Z = 91.1876  # GeV
    alpha_em_inv_MZ = 127.951
    sin2_theta_W = 0.23122
    alpha_s_MZ = 0.1179
    
    # GUT-normalized couplings
    alpha1_inv = alpha_em_inv_MZ * (1 - sin2_theta_W) * 5.0/3
    alpha2_inv = alpha_em_inv_MZ * sin2_theta_W
    alpha3_inv = 1.0 / alpha_s_MZ
    
    alpha_inv_MZ = np.array([alpha1_inv, alpha2_inv, alpha3_inv])
    
    print("Experimental Inputs at M_Z:")
    print(f"  α₁⁻¹(M_Z) = {alpha1_inv:.2f} (GUT-normalized)")
    print(f"  α₂⁻¹(M_Z) = {alpha2_inv:.2f}")
    print(f"  α₃⁻¹(M_Z) = {alpha3_inv:.2f}")
    print()
    
    # Lattice scale
    M_P = 1.22e19  # GeV (Planck mass)
    M_lattice = M_P / np.sqrt(24)
    
    print(f"  M_lattice = M_P/√24 = {M_lattice:.3e} GeV")
    print()
    
    # Part 1: SM-only one-loop running
    print("Part 1: SM-Only One-Loop Running to M_lattice")
    print("-" * 50)
    b_sm = sm_beta_coefficients()
    t = np.log(M_lattice / M_Z)
    alpha_inv_1loop = alpha_inv_MZ - b_sm / (2 * np.pi) * t
    print(f"  α₁⁻¹(M_lattice) = {alpha_inv_1loop[0]:.2f}")
    print(f"  α₂⁻¹(M_lattice) = {alpha_inv_1loop[1]:.2f}")
    print(f"  α₃⁻¹(M_lattice) = {alpha_inv_1loop[2]:.2f}")
    spread_1loop = alpha_inv_1loop[2] - alpha_inv_1loop[0]
    print(f"  Spread Δ(α₃⁻¹ - α₁⁻¹) = {spread_1loop:.1f} units")
    print(f"  IRH prediction (6:4:3 ratio): α_U⁻¹ would need ≈ {alpha_inv_1loop.mean():.1f}")
    print()
    
    # Part 2: SM two-loop running
    print("Part 2: SM Two-Loop Running to M_lattice")
    print("-" * 50)
    alpha_inv_2loop = run_couplings_two_loop(
        alpha_inv_MZ, M_Z, M_lattice, {}, {}, n_steps=5000
    )
    print(f"  α₁⁻¹(M_lattice) = {alpha_inv_2loop[0]:.2f}")
    print(f"  α₂⁻¹(M_lattice) = {alpha_inv_2loop[1]:.2f}")
    print(f"  α₃⁻¹(M_lattice) = {alpha_inv_2loop[2]:.2f}")
    spread_2loop = alpha_inv_2loop[2] - alpha_inv_2loop[0]
    print(f"  Spread = {spread_2loop:.1f} units (SM two-loop)")
    print()
    
    # Part 3: Hidden-sector threshold corrections
    print("Part 3: SO(8) Hidden-Sector Threshold Corrections")
    print("-" * 50)
    
    delta_b, multiplets = hidden_sector_beta_coefficients()
    
    # Threshold masses from dimensional scaling
    M_G2 = M_lattice / np.sqrt(7)
    M_EW_hidden = M_lattice / np.sqrt(14)
    
    M_thresholds = {"M_G2": M_G2, "M_EW": M_EW_hidden}
    
    print(f"  M_G₂ = M_lattice/√7 = {M_G2:.3e} GeV")
    print(f"  M_EW = M_lattice/√14 = {M_EW_hidden:.3e} GeV")
    print()
    print("  Hidden multiplet contributions:")
    for label, db in delta_b.items():
        print(f"    Δb at {label}: ({db[0]:.3f}, {db[1]:.3f}, {db[2]:.3f})")
    print()
    
    # Part 4: Full two-loop + threshold running
    print("Part 4: Full Two-Loop + Threshold Running")
    print("-" * 50)
    alpha_inv_full = run_couplings_two_loop(
        alpha_inv_MZ, M_Z, M_lattice, M_thresholds, delta_b, n_steps=10000
    )
    print(f"  α₁⁻¹(M_lattice) = {alpha_inv_full[0]:.2f}")
    print(f"  α₂⁻¹(M_lattice) = {alpha_inv_full[1]:.2f}")
    print(f"  α₃⁻¹(M_lattice) = {alpha_inv_full[2]:.2f}")
    spread_full = alpha_inv_full[2] - alpha_inv_full[0]
    print(f"  Spread = {spread_full:.1f} units (full two-loop + thresholds)")
    print()
    
    # Part 5: Check 6:4:3 embedding index ratios
    print("Part 5: SO(8) Embedding Index Ratios at M_lattice")
    print("-" * 50)
    mean_alpha_inv = alpha_inv_full.mean()
    predicted_643 = np.array([6, 4, 3]) * mean_alpha_inv / np.mean([6, 4, 3])
    print(f"  Mean α_U⁻¹ = {mean_alpha_inv:.2f}")
    print(f"  Predicted 6:4:3 → ({predicted_643[0]:.2f}, {predicted_643[1]:.2f}, {predicted_643[2]:.2f})")
    print(f"  Actual:         ({alpha_inv_full[0]:.2f}, {alpha_inv_full[1]:.2f}, {alpha_inv_full[2]:.2f})")
    ratios_actual = alpha_inv_full / alpha_inv_full[2]
    print(f"  Ratios: {ratios_actual[0]:.2f} : {ratios_actual[1]:.2f} : {ratios_actual[2]:.2f}")
    print(f"  Expected: 6/3 : 4/3 : 1 = 2.00 : 1.33 : 1.00")
    print()
    
    # Summary
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  SM one-loop spread:              {spread_1loop:.1f} units")
    print(f"  SM two-loop spread:              {spread_2loop:.1f} units")
    print(f"  Full (two-loop + thresholds):    {spread_full:.1f} units")
    improvement = abs(spread_2loop) - abs(spread_full)
    print(f"  Improvement from thresholds:     {improvement:.1f} units")
    print()
    
    if abs(spread_full) < abs(spread_2loop):
        print(f"  ✅ Hidden-sector thresholds REDUCE unification gap")
        print(f"     (from {abs(spread_2loop):.1f} to {abs(spread_full):.1f} units)")
    else:
        print(f"  ⚠️ Threshold corrections do not close the gap")
    
    if abs(spread_full) < 5:
        print(f"  ✅ NEAR UNIFICATION: spread < 5 units")
    elif abs(spread_full) < 10:
        print(f"  ⚠️ APPROACHING: spread = {abs(spread_full):.1f} units (< 10)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
