#!/usr/bin/env python3
"""
Circularity Analysis: Tautological vs Genuine Predictions in the IHM Framework

Formally demonstrates that the derivation of c, ℏ, G from lattice primitives
(a₀, M*, Ω_P) is tautological — all √24 factors cancel exactly. This addresses
Error 1 (FATAL) in audit_results/v82_critical_review_and_schematic.md.

Then identifies what the framework *genuinely* derives: dimensionless ratios
from D₄ geometry (α, sin²θ_W, Koide masses, etc.), which require only ONE
dimensionful input (e.g. the Planck mass) rather than zero.

Usage:
    python circularity_analysis.py            # Default analysis
    python circularity_analysis.py --strict   # CI mode: exit non-zero on failure
"""

import argparse
import numpy as np
import sys

try:
    import sympy as sp
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


# ==================== CODATA 2018 constants ====================
c_SI = 299792458.0             # m/s (exact)
hbar_SI = 1.054571817e-34      # J·s
G_SI = 6.67430e-11             # m³/(kg·s²)
L_P = 1.616255e-35             # Planck length (m)
M_P_kg = 2.176434e-8           # Planck mass (kg)
E_P_GeV = 1.220890e19          # Planck energy (GeV)
alpha_inv_exp = 137.035999206  # CODATA 2018


PASS = 0
FAIL = 0


def check(name, value, expected, tol_pct):
    """Verify a numerical result against expected value."""
    global PASS, FAIL
    if expected == 0:
        diff_pct = abs(value) * 100
    else:
        diff_pct = abs(value - expected) / abs(expected) * 100
    ok = diff_pct <= tol_pct
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {name}: {value:.10g} vs {expected:.10g} "
          f"(diff={diff_pct:.2e}%, tol={tol_pct}%)")
    return ok


def symbolic_circularity_proof():
    """
    Prove symbolically that c, ℏ, G derived from lattice primitives
    are identically equal to the input values. All √24 factors cancel.
    """
    print("PART 1: SYMBOLIC CIRCULARITY PROOF (SymPy)")
    print("=" * 72)
    print()

    if not HAS_SYMPY:
        print("  [SKIP] SymPy not available — falling back to numerical only")
        print()
        return True

    c, hbar, G_sym = sp.symbols('c hbar G', positive=True)
    L_P_sym = sp.sqrt(hbar * G_sym / c**3)
    M_P_sym = sp.sqrt(hbar * c / G_sym)

    # Lattice primitives defined in terms of Planck units
    a0 = L_P_sym / sp.sqrt(24)
    Mstar = sp.sqrt(sp.Integer(24)) * M_P_sym
    Omega_P = sp.sqrt(sp.Integer(24)) * c / L_P_sym

    print("  Lattice primitives:")
    print(f"    a₀   = L_P / √24")
    print(f"    M*   = √24 · M_P")
    print(f"    Ω_P  = √24 · c / L_P")
    print()

    # Derive c from lattice primitives
    c_derived = sp.simplify(a0 * Omega_P)
    ratio_c = sp.simplify(c_derived / c)
    print(f"  c_derived  = a₀ · Ω_P")
    print(f"             = (L_P/√24) · (√24·c/L_P)")
    print(f"             = {c_derived}")
    print(f"    ratio c_derived/c = {ratio_c}  ← TAUTOLOGY")
    print()

    # Derive ℏ from lattice primitives
    hbar_derived = sp.simplify(Mstar * Omega_P * a0**2)
    ratio_hbar = sp.simplify(hbar_derived / hbar)
    print(f"  ℏ_derived  = M* · Ω_P · a₀²")
    print(f"             = √24·M_P · (√24·c/L_P) · (L_P²/24)")
    print(f"             = {hbar_derived}")
    print(f"    ratio ℏ_derived/ℏ = {ratio_hbar}  ← TAUTOLOGY")
    print()

    # Derive G from lattice primitives
    G_derived = sp.simplify(24 * c**2 * a0 / Mstar)
    ratio_G = sp.simplify(G_derived / G_sym)
    print(f"  G_derived  = 24 · c² · a₀ / M*")
    print(f"             = 24·c² · (L_P/√24) / (√24·M_P)")
    print(f"             = {G_derived}")
    print(f"    ratio G_derived/G = {ratio_G}  ← TAUTOLOGY")
    print()

    all_tautological = (ratio_c == 1) and (ratio_hbar == 1) and (ratio_G == 1)

    print("  SYMBOLIC RESULT:")
    if all_tautological:
        print("    All three ratios equal 1 identically.")
        print("    The √24 factors cancel in every case.")
        print("    The derivation is TAUTOLOGICAL — no new information is generated.")
    else:
        print(f"    UNEXPECTED: ratios are c={ratio_c}, ℏ={ratio_hbar}, G={ratio_G}")
    print()

    return all_tautological


def numerical_circularity_proof():
    """
    Verify numerically using CODATA values that √24 cancels exactly.
    """
    print("PART 2: NUMERICAL VERIFICATION (CODATA 2018)")
    print("=" * 72)
    print()

    sqrt24 = np.sqrt(24)

    # Lattice primitives
    a0 = L_P / sqrt24
    Mstar = sqrt24 * M_P_kg
    Omega_P = sqrt24 * c_SI / L_P

    print(f"  Lattice primitives (SI units):")
    print(f"    a₀   = {a0:.6e} m")
    print(f"    M*   = {Mstar:.6e} kg")
    print(f"    Ω_P  = {Omega_P:.6e} s⁻¹")
    print()

    # Derive c
    c_derived = a0 * Omega_P
    ratio_c = c_derived / c_SI

    # Derive ℏ
    hbar_derived = Mstar * Omega_P * a0**2
    ratio_hbar = hbar_derived / hbar_SI

    # Derive G
    G_derived = 24 * c_SI**2 * a0 / Mstar
    ratio_G = G_derived / G_SI

    print(f"  Derived constants:")
    print(f"    c_derived   = {c_derived:.10e} m/s")
    print(f"    c_CODATA    = {c_SI:.10e} m/s")
    print(f"    ratio       = {ratio_c:.16f}")
    print()
    print(f"    ℏ_derived   = {hbar_derived:.10e} J·s")
    print(f"    ℏ_CODATA    = {hbar_SI:.10e} J·s")
    print(f"    ratio       = {ratio_hbar:.16f}")
    print()
    print(f"    G_derived   = {G_derived:.10e} m³/(kg·s²)")
    print(f"    G_CODATA    = {G_SI:.10e} m³/(kg·s²)")
    print(f"    ratio       = {ratio_G:.16f}")
    print()

    ok = True
    # Tolerance accounts for limited precision of CODATA input constants.
    # The symbolic proof (Part 1) shows exact cancellation; here we just
    # confirm that the numerical residuals are below measurement precision.
    ok &= check("c_derived / c = 1", ratio_c, 1.0, 1e-3)
    ok &= check("ℏ_derived / ℏ = 1", ratio_hbar, 1.0, 1e-3)
    ok &= check("G_derived / G = 1", ratio_G, 1.0, 1e-3)
    print()

    # Show the cancellation mechanism explicitly
    print("  Cancellation mechanism:")
    print(f"    √24 appears {3} times in numerator, {3} times in denominator")
    print(f"    For c:  (1/√24) × (√24)         = 1")
    print(f"    For ℏ:  (√24) × (√24) × (1/24)  = 24/24 = 1")
    print(f"    For G:  24 × (1/√24) × (1/√24)  = 24/24 = 1")
    print(f"    The rescaling a₀ = L_P/√24 is purely cosmetic.")
    print()

    return ok


def genuine_predictions():
    """
    Identify and verify what the framework genuinely predicts:
    dimensionless ratios from D₄ geometry.
    """
    print("PART 3: GENUINE PREDICTIONS (Dimensionless Ratios from D₄)")
    print("=" * 72)
    print()

    alpha = 1.0 / alpha_inv_exp

    # --- α⁻¹ = 137 + 1/(28 - π/14) ---
    print("  A. Fine-structure constant")
    print("  " + "-" * 50)
    alpha_inv_theory = 137 + 1 / (28 - np.pi / 14)
    ppb = abs(alpha_inv_theory - alpha_inv_exp) / alpha_inv_exp * 1e9
    check("α⁻¹ = 137 + 1/(28 - π/14)", alpha_inv_theory, alpha_inv_exp, 0.001)
    print(f"    Agreement: {ppb:.1f} ppb")
    print(f"    Origin: 28 = dim SO(8) adjoint, π/14 from BZ curvature")
    print(f"    Status: GENUINE if BZ integral converges to 1/(28-π/14)")
    print()

    # --- sin²θ_W = 3/13 ---
    print("  B. Weak mixing angle")
    print("  " + "-" * 50)
    sin2_tw_theory = 3.0 / 13.0
    sin2_tw_exp = 0.23122  # PDG 2022 at M_Z
    check("sin²θ_W = 3/13", sin2_tw_theory, sin2_tw_exp, 0.5)
    print(f"    Origin: 13 = 1 + 12 (D₄ has 12 positive roots)")
    print(f"    Status: GENUINE ratio from D₄ root counting")
    print()

    # --- Koide formula with θ₀ = 2/9 ---
    print("  C. Koide formula (charged lepton mass ratios)")
    print("  " + "-" * 50)
    theta_0 = 2.0 / 9.0
    koide_f = lambda n: (1 + np.sqrt(2) * np.cos(theta_0 + 2 * np.pi * n / 3))**2

    m_tau_exp = 1776.86   # MeV
    m_muon_exp = 105.658  # MeV
    m_e_exp = 0.5110      # MeV

    M_scale = m_tau_exp / koide_f(0)
    m_e_th = M_scale * koide_f(1)
    m_mu_th = M_scale * koide_f(2)

    check("m_e (Koide, θ₀=2/9)", m_e_th, m_e_exp, 0.1, )
    check("m_μ (Koide, θ₀=2/9)", m_mu_th, m_muon_exp, 0.1)
    print(f"    Origin: θ₀ = 2/9 from Berry phase Φ/(3π) on D₄ triality cycle")
    print(f"    Status: GENUINE — predicts mass ratios from one geometric parameter")
    print()

    # --- Cosmological constant ---
    print("  D. Cosmological constant")
    print("  " + "-" * 50)
    rho_ratio_theory = alpha**57 / (4 * np.pi)
    rho_ratio_exp = 1.26e-123
    log_diff = abs(np.log10(rho_ratio_theory) - np.log10(rho_ratio_exp))
    print(f"    ρ_Λ/ρ_P = α⁵⁷/(4π) = {rho_ratio_theory:.3e}")
    print(f"    Observed: ≈ {rho_ratio_exp:.2e}")
    print(f"    Δlog₁₀ = {log_diff:.4f}")
    print(f"    Status: SUGGESTIVE — exponent 57 needs derivation from phonon spectrum")
    print()

    # --- Higgs VEV ---
    print("  E. Higgs vacuum expectation value")
    print("  " + "-" * 50)
    v_theory = E_P_GeV * alpha**9 * np.pi**5 * (9.0 / 8.0)
    v_exp = 246.22  # GeV
    diff_pct = abs(v_theory - v_exp) / v_exp * 100
    check("v = E_P · α⁹ · π⁵ · 9/8", v_theory, v_exp, 0.5, )
    print(f"    Status: MIXED — requires ONE dimensionful input (E_P or M_P)")
    print()

    # --- 5-design property ---
    print("  F. D₄ 5-design property")
    print("  " + "-" * 50)
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
    norms = np.linalg.norm(d4_roots, axis=1)
    d4_unit = d4_roots / norms[:, np.newaxis]
    quartic = np.mean(d4_unit[:, 0]**4)
    mixed = np.mean(d4_unit[:, 0]**2 * d4_unit[:, 1]**2)
    check("⟨x₁⁴⟩ = 1/8 (5-design)", quartic, 3.0 / 24, 1e-8)
    check("⟨x₁²x₂²⟩ = 1/24 (5-design)", mixed, 1.0 / 24, 1e-8)
    print(f"    Status: GENUINE — pure geometry of D₄ root system")
    print()


def resolution_proposal():
    """
    Propose the resolution: reframe in terms of dimensionless ratios.
    """
    print("PART 4: PROPOSED RESOLUTION")
    print("=" * 72)
    print()
    print("  The framework should be reframed as follows:")
    print()
    print("  TAUTOLOGICAL (must be dropped as 'derivations'):")
    print("    • c  = a₀ · Ω_P         — circular by construction")
    print("    • ℏ  = M* · Ω_P · a₀²   — circular by construction")
    print("    • G  = 24c²a₀ / M*      — circular by construction")
    print("    These are DEFINITIONS of the lattice primitives in Planck units,")
    print("    not derivations of physics from the lattice.")
    print()
    print("  GENUINE (dimensionless ratios from D₄ geometry):")
    print("    • α⁻¹ = 137 + 1/(28-π/14)  — from BZ integral + SO(8) structure")
    print("    • sin²θ_W = 3/13            — from D₄ root counting")
    print("    • Koide θ₀ = 2/9            — from Berry phase on triality cycle")
    print("    • ⟨x₁⁴⟩ = 1/8              — 5-design (isotropy)")
    print("    • ν = 1/4                   — Poisson ratio (elastic isotropy)")
    print()
    print("  REQUIRES ONE DIMENSIONFUL INPUT:")
    print("    • The framework needs ONE dimensionful constant (e.g. M_P or L_P)")
    print("      to set the overall scale. All other dimensionful quantities then")
    print("      follow from the dimensionless ratios above.")
    print("    • This is analogous to QCD, which needs Λ_QCD as input but")
    print("      predicts all hadron mass RATIOS from the theory.")
    print()
    print("  The honest claim is:")
    print('    "Given the D₄ lattice at Planck scale, derive dimensionless')
    print('     coupling constants and mass ratios from pure geometry."')
    print("    This is still highly non-trivial if the BZ integral works.")
    print()


def summary():
    """Print the final classification summary."""
    global PASS, FAIL
    print("=" * 72)
    print("CLASSIFICATION SUMMARY")
    print("=" * 72)
    print()
    print("  ┌─────────────────────────────────────┬──────────────────────┐")
    print("  │ Claim                                │ Status               │")
    print("  ├─────────────────────────────────────┼──────────────────────┤")
    print("  │ c  derived from (a₀, Ω_P)           │ TAUTOLOGICAL         │")
    print("  │ ℏ  derived from (M*, Ω_P, a₀)       │ TAUTOLOGICAL         │")
    print("  │ G  derived from (c, a₀, M*)          │ TAUTOLOGICAL         │")
    print("  ├─────────────────────────────────────┼──────────────────────┤")
    print("  │ α⁻¹ = 137 + 1/(28-π/14)            │ GENUINE (if BZ ✓)    │")
    print("  │ sin²θ_W = 3/13                      │ GENUINE              │")
    print("  │ Koide θ₀ = 2/9                      │ GENUINE              │")
    print("  │ D₄ 5-design                         │ GENUINE (proven)     │")
    print("  │ Poisson ratio ν = 1/4               │ GENUINE (proven)     │")
    print("  ├─────────────────────────────────────┼──────────────────────┤")
    print("  │ ρ_Λ/ρ_P = α⁵⁷/(4π)                 │ SUGGESTIVE           │")
    print("  │ v = E_P·α⁹·π⁵·(9/8)               │ MIXED (needs E_P)    │")
    print("  │ 137 = 128 + 8 + 1                   │ NUMEROLOGICAL        │")
    print("  └─────────────────────────────────────┴──────────────────────┘")
    print()
    print(f"  Numerical checks: {PASS} PASS, {FAIL} FAIL out of {PASS+FAIL}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Circularity analysis: tautological vs genuine predictions")
    parser.add_argument("--strict", action="store_true",
                        help="CI mode: exit non-zero if any check fails")
    args = parser.parse_args()

    print("=" * 72)
    print("CIRCULARITY ANALYSIS — TAUTOLOGICAL vs GENUINE PREDICTIONS (v83.0)")
    print("=" * 72)
    print()
    print("  Reference: audit_results/v82_critical_review_and_schematic.md")
    print("  Error 1 (FATAL): derivation of c, ℏ, G from lattice primitives")
    print()

    sym_ok = symbolic_circularity_proof()
    num_ok = numerical_circularity_proof()
    genuine_predictions()
    resolution_proposal()
    summary()

    if args.strict and FAIL > 0:
        print(f"[STRICT] {FAIL} check(s) failed.", file=sys.stderr)
        return 1

    if not sym_ok or not num_ok:
        print("WARNING: circularity proof did not verify — check SymPy output.",
              file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
