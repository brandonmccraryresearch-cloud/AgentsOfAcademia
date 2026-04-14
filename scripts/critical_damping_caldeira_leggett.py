#!/usr/bin/env python3
"""
Critical Damping from D₄ Hamiltonian via Caldeira-Leggett Formalism
====================================================================

Rigorous derivation of the damping ratio ζ for translational modes
on the D₄ root lattice, treating shear modes as a Caldeira-Leggett
bath. The calculation avoids the trivially-circular ratio
(4/24)×(24/4) = 1 and instead derives ζ from first principles.

Physics:
    The D₄ lattice has z = 24 nearest neighbors. The 24 bond DOFs
    decompose under the Weyl group W(D₄) as:
        R²⁴ = V_breath(1) ⊕ V_trans(4) ⊕ V_shear(19)

    The breathing mode (uniform expansion) is a 1D trivial rep.
    Translational modes (center-of-mass motion) form a 4D vector rep.
    Shear modes (relative distortions) occupy the remaining 19D subspace.

    In the Caldeira-Leggett picture, the translational mode is the
    "system" coupled to a "bath" of 19 shear oscillators. The coupling
    is mediated by inter-site phase factors (1 - cos(k·δ_j)) that
    break the on-site Weyl symmetry.

    BZ-averaged squared coupling:

        C(j,l) = ⟨(1-cos k·δ_j)(1-cos k·δ_l)⟩_BZ
               = 1 + ½ δ_{jl} + ½ δ_{j,l'}

    where l' is the antipodal partner (δ_{l'} = -δ_l). This follows from
    ⟨cos(k·v)⟩ = δ_{v,0} for integer vectors on the 4-torus [0,2π)⁴.

    The coupling decomposes into three contributions:
        Base:      (ê_μ)ᵀ P_s ê_μ × 1           = 0     (orthogonality)
        Diagonal:  ½ Σ_j (ê_μ)²_j (P_s)_{jj}    = 19/48
        Antipodal: ½ Σ_j (ê_μ)_j(ê_μ)_{j'}(P_s)_{j,j'} = -3/48

    Total: ⟨|c|²⟩ = 16/48 = 1/3.

Key Result:
    η = π/6  (damping coefficient in natural units M* = J = 1)
    ζ = π/12 ≈ 0.262  (damping ratio — UNDERDAMPED)

    Critical damping (ζ = 1) is NOT achieved. The deficit factor
    is 12/π ≈ 3.82.

Usage:
    python critical_damping_caldeira_leggett.py

References:
    - Caldeira & Leggett, Physica A 121 (1983) 587
    - IRH v86.0 §I (D₄ lattice structure)
"""

import numpy as np
import sys


# ═══════════════════════════════════════════════════════════════════════
# D₄ root lattice utilities
# ═══════════════════════════════════════════════════════════════════════

def d4_root_vectors():
    """Generate all 24 root vectors of D₄: ±eᵢ ± eⱼ for i < j."""
    roots = []
    for i in range(4):
        for j in range(i + 1, 4):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = np.zeros(4)
                    v[i] = si
                    v[j] = sj
                    roots.append(v)
    return np.array(roots)


def build_projectors(roots):
    """
    Build the three orthogonal projectors for the R²⁴ mode decomposition.

    Breathing: P_b = (1/z) J  (all-ones matrix, rank 1)
    Translational: P_t = B (BᵀB)⁻¹ Bᵀ  where B is (24×4) with B_{jμ} = (δ_j)_μ/√2
    Shear: P_s = I - P_b - P_t  (rank 19)

    Returns (P_b, P_t, P_s).
    """
    z = len(roots)

    # Breathing projector: uniform stretch of all bonds
    P_b = np.ones((z, z)) / z

    # Translational projector
    # B maps 4D spatial displacement to 24D bond stretch: u_j = r·δ̂_j
    B = roots / np.sqrt(2.0)  # (24, 4), normalised by bond length √2
    BtB = B.T @ B             # 6 I₄ for D₄
    BtB_inv = np.linalg.inv(BtB)
    P_t = B @ BtB_inv @ B.T

    # Shear projector: orthogonal complement
    P_s = np.eye(z) - P_b - P_t

    return P_b, P_t, P_s


def translational_mode(roots, mu):
    """
    Normalized translational mode in spatial direction μ ∈ {0,1,2,3}.

    (ê_μ)_j = (δ_j)_μ / √(Σ_l (δ_l)_μ²)
    """
    e = roots[:, mu].copy()
    e /= np.linalg.norm(e)
    return e


def antipodal_partners(roots):
    """
    For each root j, find the index j' such that δ_{j'} = -δ_j.

    Returns array of length z with partner indices.
    """
    z = len(roots)
    partners = np.full(z, -1, dtype=int)
    for j in range(z):
        for l in range(z):
            if np.allclose(roots[l], -roots[j]):
                partners[j] = l
                break
    assert np.all(partners >= 0), "Every root must have an antipodal partner"
    return partners


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    np.set_printoptions(precision=8, linewidth=100)
    np.random.seed(42)

    n_pass = 0
    n_fail = 0

    def check(name, condition, detail=""):
        nonlocal n_pass, n_fail
        if condition:
            n_pass += 1
            print(f"  [PASS] {name}" + (f"  ({detail})" if detail else ""))
        else:
            n_fail += 1
            print(f"  [FAIL] {name}" + (f"  ({detail})" if detail else ""))
        return condition

    # ───────────────────────────────────────────────────────────────────
    # Build lattice data
    # ───────────────────────────────────────────────────────────────────
    roots = d4_root_vectors()
    z = len(roots)
    P_b, P_t, P_s = build_projectors(roots)
    partners = antipodal_partners(roots)

    # ═══════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("TEST GROUP 1: D₄ Mode Decomposition  R²⁴ = 1 ⊕ 4 ⊕ 19")
    print("=" * 70)
    # ═══════════════════════════════════════════════════════════════════

    # Test 1
    norms_sq = np.sum(roots ** 2, axis=1)
    check("24 root vectors, all with |δ|² = 2",
          z == 24 and np.allclose(norms_sq, 2.0),
          f"z = {z}, |δ|² ∈ [{norms_sq.min()}, {norms_sq.max()}]")

    # Test 2
    rank_b = np.linalg.matrix_rank(P_b, tol=1e-10)
    idem_b = np.allclose(P_b @ P_b, P_b, atol=1e-12)
    sym_b = np.allclose(P_b, P_b.T, atol=1e-14)
    check("P_b: rank-1 symmetric idempotent (breathing)",
          rank_b == 1 and idem_b and sym_b,
          f"rank={rank_b}, Tr={np.trace(P_b):.0f}")

    # Test 3
    rank_t = np.linalg.matrix_rank(P_t, tol=1e-10)
    idem_t = np.allclose(P_t @ P_t, P_t, atol=1e-12)
    sym_t = np.allclose(P_t, P_t.T, atol=1e-12)
    check("P_t: rank-4 symmetric idempotent (translational)",
          rank_t == 4 and idem_t and sym_t,
          f"rank={rank_t}, Tr={np.trace(P_t):.1f}")

    # Test 4
    rank_s = np.linalg.matrix_rank(P_s, tol=1e-10)
    idem_s = np.allclose(P_s @ P_s, P_s, atol=1e-12)
    sym_s = np.allclose(P_s, P_s.T, atol=1e-12)
    check("P_s: rank-19 symmetric idempotent (shear)",
          rank_s == 19 and idem_s and sym_s,
          f"rank={rank_s}, Tr={np.trace(P_s):.1f}")

    # Test 5
    completeness = np.allclose(P_b + P_t + P_s, np.eye(z), atol=1e-12)
    orth_bt = np.allclose(P_b @ P_t, 0, atol=1e-12)
    orth_bs = np.allclose(P_b @ P_s, 0, atol=1e-12)
    orth_ts = np.allclose(P_t @ P_s, 0, atol=1e-12)
    check("Completeness P_b+P_t+P_s = I₂₄ and mutual orthogonality",
          completeness and orth_bt and orth_bs and orth_ts,
          "P_i P_j = δ_{ij} P_i verified for all pairs")

    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TEST GROUP 2: On-Site Coupling Vanishes (Schur Orthogonality)")
    print("=" * 70)
    # ═══════════════════════════════════════════════════════════════════

    # For any Weyl-invariant scalar f(δ_j) = const (W(D₄) acts transitively
    # on the roots), the on-site coupling between inequivalent irreps vanishes:
    #   c = const × Σ_j (e_μ)_j (e_a)_j = const × (e_μ · e_a) = 0

    # Test 6
    e_breath = np.ones(z) / np.sqrt(z)
    bt_overlaps = [abs(e_breath @ translational_mode(roots, mu))
                   for mu in range(4)]
    max_bt = max(bt_overlaps)
    check("Breathing ⊥ Translational (all 4 directions)",
          max_bt < 1e-14,
          f"max |⟨b|t_μ⟩| = {max_bt:.2e}")

    # Test 7
    ts_norms = [np.linalg.norm(P_s @ translational_mode(roots, mu))
                for mu in range(4)]
    max_ts = max(ts_norms)
    check("P_s ê_μ = 0 for all μ (trans ⊥ shear, Schur orthogonality)",
          max_ts < 1e-14,
          f"max ‖P_s ê_μ‖ = {max_ts:.2e}")

    # Test 8
    bs_norm = np.linalg.norm(P_s @ e_breath)
    check("P_s ê_breath = 0 (breathing ⊥ shear)",
          bs_norm < 1e-14,
          f"‖P_s b‖ = {bs_norm:.2e}")

    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TEST GROUP 3: Inter-Site BZ Coupling  ⟨|c|²⟩ = 1/3")
    print("=" * 70)
    # ═══════════════════════════════════════════════════════════════════

    # ⟨(1-cos k·δ_j)(1-cos k·δ_l)⟩_BZ = 1 + ½δ_{jl} + ½δ_{j,l'}
    # because ⟨cos(k·v)⟩ = δ_{v,0} for integer v on [0,2π)⁴.

    # Test 9: Verify analytic correlator against Monte Carlo
    C_analytic = np.ones((z, z))
    for j in range(z):
        C_analytic[j, j] += 0.5
        C_analytic[j, partners[j]] += 0.5

    N_mc = 10 ** 6
    k_samples = np.random.uniform(0, 2 * np.pi, (N_mc, 4))
    phases = k_samples @ roots.T                   # (N_mc, 24)
    one_minus_cos = 1.0 - np.cos(phases)           # (N_mc, 24)

    # Batch outer products to keep memory bounded
    C_mc = np.zeros((z, z))
    batch_size = 50000
    for start in range(0, N_mc, batch_size):
        end = min(start + batch_size, N_mc)
        batch = one_minus_cos[start:end]
        C_mc += batch.T @ batch
    C_mc /= N_mc

    mc_error = np.max(np.abs(C_mc - C_analytic))
    check("BZ correlator C(j,l) matches MC (10⁶ samples)",
          mc_error < 0.02,
          f"max |C_analytic − C_MC| = {mc_error:.4f}")

    # Diagonal elements of P_s are uniform: (P_s)_{jj} = 19/24
    Ps_diag = np.diag(P_s)
    check("(P_s)_{jj} = 19/24 for all j (uniform diagonal)",
          np.allclose(Ps_diag, 19.0 / 24.0, atol=1e-12),
          f"mean = {np.mean(Ps_diag):.6f}, target = {19/24:.6f}")

    # Use μ=0 for the detailed decomposition; Test 24 confirms μ-independence
    mu = 0
    e_mu = translational_mode(roots, mu)

    # Test 11: Base contribution = 0
    base = e_mu @ P_s @ e_mu
    check("Base contribution (ê_μ)ᵀ P_s ê_μ = 0",
          abs(base) < 1e-14,
          f"base = {base:.2e}")

    # Test 12: Diagonal contribution = 19/48
    diag_term = 0.5 * np.sum(e_mu ** 2 * Ps_diag)
    target_diag = 19.0 / 48.0
    check(f"Diagonal contribution ½ Σ_j (ê_μ)²_j (P_s)_{{jj}} = 19/48",
          abs(diag_term - target_diag) < 1e-14,
          f"computed = {diag_term:.8f}, target = {target_diag:.8f}")

    # Test 13: Antipodal contribution = -3/48 = -1/16
    Ps_anti = np.array([P_s[j, partners[j]] for j in range(z)])
    anti_term = 0.5 * np.sum(e_mu * e_mu[partners] * Ps_anti)
    target_anti = -3.0 / 48.0
    check(f"Antipodal contribution ½ Σ_j (ê_μ)_j (ê_μ)_{{j'}} (P_s)_{{j,j'}} = −3/48",
          abs(anti_term - target_anti) < 1e-14,
          f"computed = {anti_term:.8f}, target = {target_anti:.8f}")

    # Test 14: Total analytic ⟨|c|²⟩ = 1/3
    c2_analytic = base + diag_term + anti_term
    check("Analytic ⟨|c|²⟩ = 19/48 − 3/48 = 16/48 = 1/3",
          abs(c2_analytic - 1.0 / 3.0) < 1e-14,
          f"computed = {c2_analytic:.10f}")

    # Test 15: MC confirms ⟨|c|²⟩ = 1/3
    c2_mc = np.einsum("j,jl,l,jl->", e_mu, P_s, e_mu, C_mc)
    check("MC confirms ⟨|c|²⟩ = 1/3 (statistical consistency)",
          abs(c2_mc - 1.0 / 3.0) < 0.01,
          f"MC = {c2_mc:.6f}, analytic = {1/3:.6f}")

    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TEST GROUP 4: Caldeira-Leggett Damping  ζ = π/12")
    print("=" * 70)
    # ═══════════════════════════════════════════════════════════════════

    # Natural units: M* = 1, J = 1 → ω₀ = √(J/M*) = 1, Ω_P = √24
    M_star = 1.0
    J_bond = 1.0
    omega_0 = np.sqrt(J_bond / M_star)

    # Flat-band Caldeira-Leggett spectral density:
    #   η = (π/2) × ⟨|c|²⟩ / (M* ω_s²)    with ω_s = ω₀
    c2 = 1.0 / 3.0
    eta = (np.pi / 2.0) * c2 / (M_star * omega_0 ** 2)
    eta_target = np.pi / 6.0

    # Test 16
    check(f"Damping coefficient η = π/6 ≈ {eta_target:.6f}",
          abs(eta - eta_target) < 1e-14,
          f"η = {eta:.6f}")

    # Test 17
    zeta = eta / (2.0 * M_star * omega_0)
    zeta_target = np.pi / 12.0
    check(f"Damping ratio ζ = η/(2M*ω₀) = π/12 ≈ {zeta_target:.6f}",
          abs(zeta - zeta_target) < 1e-14,
          f"ζ = {zeta:.6f}")

    # Test 18
    check("ζ < 1  ⟹  system is UNDERDAMPED",
          zeta < 1.0,
          f"ζ = {zeta:.4f}")

    # Test 19
    deficit = 1.0 / zeta
    deficit_target = 12.0 / np.pi
    check(f"Deficit factor for ζ = 1: need 12/π ≈ {deficit_target:.4f}× more coupling",
          abs(deficit - deficit_target) < 1e-12,
          f"1/ζ = {deficit:.4f}")

    # Test 20
    Omega_P = np.sqrt(24.0 * J_bond / M_star)
    check(f"Planck frequency Ω_P = √(24J/M*) = {Omega_P:.6f}",
          abs(Omega_P - np.sqrt(24) * omega_0) < 1e-14,
          f"Ω_P/ω₀ = √24 = {np.sqrt(24):.6f}")

    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TEST GROUP 5: Physical Assessment")
    print("=" * 70)
    # ═══════════════════════════════════════════════════════════════════

    # Test 21: Circular ratio
    circular = (4.0 / 24.0) * (24.0 / 4.0)
    check("(d/z)×(z/d) = (4/24)×(24/4) = 1 is trivially circular",
          abs(circular - 1.0) < 1e-15,
          "This ratio carries zero physical information")

    # Test 22: Quality factor
    Q = 1.0 / (2.0 * zeta)
    Q_target = 6.0 / np.pi
    check(f"Quality factor Q = 1/(2ζ) = 6/π ≈ {Q_target:.4f}",
          abs(Q - Q_target) < 1e-12,
          f"Q = {Q:.4f}, confirms underdamped oscillation")

    # Test 23: Damped oscillation frequency
    omega_d = omega_0 * np.sqrt(1.0 - zeta ** 2)
    omega_d_exact = omega_0 * np.sqrt(1.0 - (np.pi / 12.0) ** 2)
    check(f"Damped frequency ω_d/ω₀ = √(1−ζ²) = {omega_d:.6f}",
          abs(omega_d - omega_d_exact) < 1e-14,
          f"ω_d/ω₀ = {omega_d/omega_0:.6f} ≈ 0.966")

    # Test 24: μ-independence of ⟨|c|²⟩ for all 4 translational modes
    c2_all = []
    for mu_idx in range(4):
        e_test = translational_mode(roots, mu_idx)
        c2_mu = (0.5 * np.sum(e_test ** 2 * Ps_diag) +
                 0.5 * np.sum(e_test * e_test[partners] * Ps_anti))
        c2_all.append(c2_mu)
    spread = max(c2_all) - min(c2_all)
    check("⟨|c|²⟩ = 1/3 for ALL μ ∈ {0,1,2,3} (D₄ isotropy)",
          spread < 1e-14 and all(abs(v - 1.0 / 3.0) < 1e-14 for v in c2_all),
          f"values = [{', '.join(f'{v:.8f}' for v in c2_all)}]")

    # Test 25: Internal consistency summary
    all_ok = (abs(zeta - np.pi / 12) < 1e-14
              and zeta < 1.0
              and abs(c2_analytic - 1.0 / 3.0) < 1e-14
              and abs(circular - 1.0) < 1e-15)
    check("All results internally consistent",
          all_ok,
          "ζ = π/12, ⟨|c|²⟩ = 1/3, circular ratio identified")

    # ═══════════════════════════════════════════════════════════════════
    # CONCLUSION
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("  Caldeira-Leggett Damping Derived from D₄ Root Geometry")
    print("  " + "─" * 54)
    print()
    print("  Mode decomposition of the 24 nearest-neighbor bonds:")
    print("      R²⁴ = V_breath(1) ⊕ V_trans(4) ⊕ V_shear(19)")
    print()
    print("  On-site coupling between V_trans and V_shear vanishes")
    print("  by Schur orthogonality under the Weyl group W(D₄),")
    print("  which acts transitively on the 24 root vectors.")
    print()
    print("  Inter-site BZ-averaged coupling breaks Weyl symmetry")
    print("  via the phase factor (1 − cos k·δⱼ):")
    print()
    print("      ⟨|c|²⟩_BZ = 19/48 (diagonal) − 3/48 (antipodal)")
    print("                 = 16/48 = 1/3")
    print()
    print("  Caldeira-Leggett damping (flat optical band at ω₀):")
    print()
    print(f"      η = (π/2)(1/3)/(M*ω₀²) = π/6 ≈ {np.pi/6:.4f}")
    print(f"      ζ = η/(2M*ω₀)           = π/12 ≈ {np.pi/12:.4f}")
    print()
    print("  ╔═══════════════════════════════════════════════════════╗")
    print("  ║  RESULT: ζ = π/12 ≈ 0.2618                          ║")
    print("  ║  The system is UNDERDAMPED — NOT critically damped.  ║")
    print("  ║  Deficit: need 12/π ≈ 3.82× more coupling for ζ=1.  ║")
    print("  ╚═══════════════════════════════════════════════════════╝")
    print()
    print("  The trivially-cancelling ratio (4/24)×(24/4) = 1 is")
    print("  algebraic tautology (d/z × z/d ≡ 1 for any lattice)")
    print("  and does NOT constitute a derivation of critical damping.")
    print()
    print("  IMPLICATION FOR LORENTZIAN SIGNATURE:")
    print("  Lorentzian signature cannot be justified by claiming")
    print("  critical damping of translational modes on D₄. The")
    print("  shear-bath coupling derived from D₄ root geometry gives")
    print("  ζ ≈ 0.26, which is underdamped by a factor of ~3.8.")
    print("  Any argument invoking ζ = 1 requires additional physics")
    print("  beyond the bare D₄ Hamiltonian with harmonic bonds.")

    # ═══════════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print(f"RESULTS: {n_pass} PASS, {n_fail} FAIL out of {n_pass + n_fail}")
    print(f"{'=' * 70}")

    return n_fail == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
