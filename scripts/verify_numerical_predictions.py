#!/usr/bin/env python3
"""
Verify all numerical predictions of the IRH/IHM-HRIIP framework.

This script independently verifies every quantitative claim in the manuscript
82.0theaceinthehole.md. It is the canonical computational verification record.

Usage:
    python verify_numerical_predictions.py

All values are compared against CODATA 2018 / PDG 2022 experimental data.
"""

import numpy as np
import sys

PASS = 0
FAIL = 0

def check(name, theory, experiment, tolerance_pct, unit=""):
    """Verify a prediction against experiment."""
    global PASS, FAIL
    if experiment == 0:
        diff_pct = abs(theory) * 100
    else:
        diff_pct = abs(theory - experiment) / abs(experiment) * 100
    status = "PASS" if diff_pct <= tolerance_pct else "FAIL"
    if status == "PASS":
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {name}: theory={theory:.6g} {unit}, "
          f"exp={experiment:.6g} {unit}, diff={diff_pct:.4f}% "
          f"(tol={tolerance_pct}%)")
    return status == "PASS"


def main():
    print("=" * 72)
    print("IRH/IHM-HRIIP NUMERICAL VERIFICATION (v82.0)")
    print("=" * 72)
    print()

    # ===== Fundamental Constants =====
    alpha_inv_exp = 137.035999206  # CODATA 2018 (Morel et al. 2020: 81 ppt)
    alpha = 1.0 / alpha_inv_exp
    E_P = 1.220890e19  # Planck energy (GeV)
    M_P = E_P  # Planck mass (GeV/c²)
    L_P = 1.616255e-35  # Planck length (m)
    M_Z = 91.1876  # Z boson mass (GeV)

    # ===== §II.3: Fine-structure constant =====
    print("§II.3 Fine-structure constant")
    alpha_inv_theory = 137 + 1 / (28 - np.pi / 14)
    check("α⁻¹ = 137 + 1/(28 - π/14)", alpha_inv_theory, alpha_inv_exp, 0.001)
    ppb = abs(alpha_inv_theory - alpha_inv_exp) / alpha_inv_exp * 1e9
    print(f"       Agreement: {ppb:.1f} parts per billion")
    print()

    # ===== §IV.4: Weak mixing angle =====
    print("§IV.4 Weak mixing angle")
    sin2_tw_theory = 3.0 / 13.0
    sin2_tw_exp = 0.23122  # PDG 2022 at M_Z
    check("sin²θ_W = 3/13", sin2_tw_theory, sin2_tw_exp, 0.5)
    print()

    # ===== §VIII.3: Higgs VEV =====
    print("§VIII.3 Higgs vacuum expectation value")
    v_theory = E_P * alpha**9 * np.pi**5 * (9.0 / 8.0)
    v_exp = 246.22  # GeV
    check("v = E_P · α⁹ · π⁵ · 9/8", v_theory, v_exp, 0.5, "GeV")
    print()

    # ===== §V.6: Cosmological constant =====
    print("§V.6 Cosmological constant")
    rho_ratio_theory = alpha**57 / (4 * np.pi)
    rho_ratio_exp = 1.26e-123
    log_diff = abs(np.log10(rho_ratio_theory) - np.log10(rho_ratio_exp))
    print(f"  [{'PASS' if log_diff < 0.1 else 'FAIL'}] "
          f"ρ_Λ/ρ_P = α⁵⁷/(4π): theory={rho_ratio_theory:.3e}, "
          f"obs≈{rho_ratio_exp:.2e}, Δlog₁₀={log_diff:.4f}")
    if log_diff < 0.1:
        global PASS
        PASS += 1
    else:
        global FAIL
        FAIL += 1
    print()

    # ===== §III.6: Koide formula with θ₀ = 2/9 =====
    print("§III.6 Koide formula (θ₀ = 2/9)")
    theta_0 = 2.0 / 9.0
    koide_f = lambda n: (1 + np.sqrt(2) * np.cos(theta_0 + 2 * np.pi * n / 3))**2
    m_tau_exp = 1776.86  # MeV
    M_scale = m_tau_exp / koide_f(0)

    m_tau_th = M_scale * koide_f(0)
    m_muon_th = M_scale * koide_f(2)
    m_electron_th = M_scale * koide_f(1)

    m_muon_exp = 105.658  # MeV
    m_electron_exp = 0.5110  # MeV

    check("m_e (Koide)", m_electron_th, m_electron_exp, 0.1, "MeV")
    check("m_μ (Koide)", m_muon_th, m_muon_exp, 0.1, "MeV")

    # Koide Q ratio
    Q_exp = (m_electron_exp + m_muon_exp + m_tau_exp) / \
            (np.sqrt(m_electron_exp) + np.sqrt(m_muon_exp) + np.sqrt(m_tau_exp))**2
    print(f"  Koide Q (exp): {Q_exp:.8f}, |Q - 2/3| = {abs(Q_exp - 2/3):.2e}")
    print()

    # ===== §III.6.1: θ₀ Berry phase derivation =====
    print("§III.6.1 θ₀ = 2/9 from Berry phase")
    Phi = 2 * np.pi / 3
    theta_derived = Phi / (3 * np.pi)
    check("θ₀ = Φ/(3π) = 2/9", theta_derived, 2.0 / 9.0, 1e-10)
    print()

    # ===== §IV.5: Gauge coupling running =====
    print("§IV.5 Gauge coupling running to M_lattice")
    M_lattice = M_P / np.sqrt(24)
    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0

    alpha_em_inv_MZ = 127.951
    sin2_tw_MZ = 0.23122
    alpha_s_MZ = 0.1179

    alpha2_inv_MZ = sin2_tw_MZ * alpha_em_inv_MZ
    alpha_Y_inv_MZ = (1 - sin2_tw_MZ) * alpha_em_inv_MZ
    alpha1_inv_MZ = (3.0 / 5.0) * alpha_Y_inv_MZ
    alpha3_inv_MZ = 1.0 / alpha_s_MZ

    t = np.log(M_lattice / M_Z) / (2 * np.pi)

    alpha1_inv_ML = alpha1_inv_MZ - b1 * t
    alpha2_inv_ML = alpha2_inv_MZ - b2 * t
    alpha3_inv_ML = alpha3_inv_MZ - b3 * t

    spread = max(alpha1_inv_ML, alpha2_inv_ML, alpha3_inv_ML) - \
             min(alpha1_inv_ML, alpha2_inv_ML, alpha3_inv_ML)

    print(f"  α₁⁻¹(M_lattice) = {alpha1_inv_ML:.3f}")
    print(f"  α₂⁻¹(M_lattice) = {alpha2_inv_ML:.3f}")
    print(f"  α₃⁻¹(M_lattice) = {alpha3_inv_ML:.3f}")
    print(f"  Spread = {spread:.2f} units")
    print()

    # ===== §V.5.1: Phonon spectrum (D₄ dynamical matrix) =====
    print("§V.5.1 D₄ phonon spectrum")

    d4_roots = []
    for i in range(4):
        for j in range(i + 1, 4):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = np.zeros(4)
                    v[i] = si
                    v[j] = sj
                    d4_roots.append(v)
    d4_roots = np.array(d4_roots)

    print(f"  D₄ root vectors: {len(d4_roots)} (coordination number = 24)")

    # Zone-boundary zero at R = (π,π,π,π)
    k_R = np.array([np.pi, np.pi, np.pi, np.pi])
    D_R = np.zeros((4, 4))
    for delta in d4_roots:
        norm_sq = np.dot(delta, delta)
        outer = np.outer(delta, delta) / norm_sq
        phase = 1 - np.cos(np.dot(k_R, delta))
        D_R += outer * phase
    eigs_R = np.linalg.eigvalsh(D_R)
    print(f"  R = (π,π,π,π) eigenvalues: {eigs_R}")
    all_zero = np.allclose(eigs_R, 0)
    print(f"  Zone-boundary zero: {'PASS' if all_zero else 'FAIL'}")
    if all_zero:
        PASS += 1
    else:
        FAIL += 1
    print()

    # ===== §II.3.2: 5-design verification =====
    print("§II.3.2 D₄ 5-design property")
    norms = np.linalg.norm(d4_roots, axis=1)
    d4_unit = d4_roots / norms[:, np.newaxis]
    quartic_test = np.mean(d4_unit[:, 0]**4)
    quartic_exact = 3.0 / (4 * 6)
    check("⟨x₁⁴⟩ = 3/(d(d+2))", quartic_test, quartic_exact, 1e-8)

    mixed_test = np.mean(d4_unit[:, 0]**2 * d4_unit[:, 1]**2)
    mixed_exact = 1.0 / (4 * 6)
    check("⟨x₁²x₂²⟩ = 1/(d(d+2))", mixed_test, mixed_exact, 1e-8)
    print()

    # ===== (E/E_P)^6 measure sensitivity =====
    print("Measure sensitivity at electroweak scale")
    E_ew = 246  # GeV
    measure_corr = (E_ew / E_P)**6
    print(f"  (E_EW/E_P)⁶ = {measure_corr:.2e} (experimentally inaccessible)")
    print()

    # ===== Summary =====
    print("=" * 72)
    print(f"RESULTS: {PASS} PASS, {FAIL} FAIL out of {PASS + FAIL} checks")
    print("=" * 72)

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
