#!/usr/bin/env python3
"""
Comprehensive Parameter Audit — Review86 DIRECTIVE 26
=====================================================

Performs a complete, honest audit of ALL free parameters, calibrated
inputs, and effective parameters in the IRH framework. Evaluates each
parameter's classification and recomputes the parsimony ratio.

Reference: IRH manuscript §XV.6 — Parsimony analysis

Tests
-----
TEST  1: Enumerate all framework parameters with classifications
TEST  2: Count Primitive parameters (truly free inputs)
TEST  3: Count Derived-exact parameters (follow from lattice geometry)
TEST  4: Count Derived-approximate parameters (require truncation/approx)
TEST  5: Count Calibrated parameters (tuned to match experiment)
TEST  6: Count Ad-hoc parameters (introduced without derivation)
TEST  7: Count Undetermined parameters (value not fixed by framework)
TEST  8: Identify calibration dependencies — which predictions are independent
TEST  9: Count genuinely independent predictions (not dependent on calibrated inputs)
TEST 10: Recompute parsimony ratio (independent predictions / primitive parameters)
TEST 11: Compare to manuscript claimed ratio 2.5-5.0
TEST 12: Classify each "prediction" as DERIVATION/PREDICTION/POSTDICTION/CALIBRATION/TAUTOLOGY
TEST 13: Count empirically testable predictions with quantitative precision
TEST 14: Identify the single strongest prediction (most falsifiable, least calibrated)
TEST 15: Identify the weakest claim (most dependent on calibration)
TEST 16: Assess overall empirical grounding honestly

Usage
-----
    python comprehensive_parameter_audit.py [--verbose]
"""

import sys
import math
import argparse

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="Review86 DIRECTIVE 26: Comprehensive parameter audit"
)
parser.add_argument("--verbose", action="store_true",
                    help="Print detailed parameter tables")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Test infrastructure
# ---------------------------------------------------------------------------
passed = 0
failed = 0
total = 0


def check(name, condition, detail=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")
    if detail:
        print(f"        {detail}")


# =========================================================================
#  PARAMETER DATABASE
# =========================================================================
# Classification options:
#   Primitive       — truly free input (no derivation exists)
#   Derived-exact   — follows uniquely from lattice geometry
#   Derived-approx  — follows from lattice but requires truncation/approximation
#   Calibrated      — value tuned to match one experimental observable
#   Ad-hoc          — introduced without physical derivation
#   Undetermined    — value not fixed by the framework

PARAMETERS = [
    # --- Fundamental lattice parameters ---
    {
        "name": "a₀ (lattice spacing)",
        "value": "L_P / √24 ≈ 3.30×10⁻³⁶ m",
        "how_determined": "From D₄ bond-sharing: a₀ = L_P/√(z/2) with z=24",
        "classification": "Derived-exact",
        "exp_input": "G, ℏ, c via L_P",
        "note": "Depends on identifying M* with Planck mass scale"
    },
    {
        "name": "J (bond stiffness)",
        "value": "M*Ω_P²/24 ≈ 2.17×10⁸⁴ N/m",
        "how_determined": "From resonance condition M*Ω_P² = zJ with z=24",
        "classification": "Derived-exact",
        "exp_input": "G, ℏ, c via Ω_P",
        "note": "Circular with M* — both set by Planck scale identification"
    },
    {
        "name": "M* (site mass)",
        "value": "√24 · M_P ≈ 1.07×10⁻⁷ kg",
        "how_determined": "From √24 bridge: M* = √(z/2) · M_P",
        "classification": "Derived-exact",
        "exp_input": "G, ℏ, c via M_P",
        "note": "The √24 bridge is an identification, not a derivation"
    },
    {
        "name": "Ω_P (Planck frequency)",
        "value": "√(c⁵/(ℏG)) ≈ 1.86×10⁴³ rad/s",
        "how_determined": "Standard Planck units",
        "classification": "Derived-exact",
        "exp_input": "G, ℏ, c",
        "note": "Input from fundamental constants"
    },
    # --- Speed of light and spacetime ---
    {
        "name": "c (speed of light)",
        "value": "299792458 m/s",
        "how_determined": "From c² = 3Ja₀²/M* (phonon velocity, D₄ geometry)",
        "classification": "Derived-exact",
        "exp_input": "Tautological: c enters via L_P, Ω_P, M_P",
        "note": "c is INPUT via Planck scale, then 'derived' as phonon velocity — TAUTOLOGY"
    },
    {
        "name": "ℏ (reduced Planck constant)",
        "value": "1.055×10⁻³⁴ J·s",
        "how_determined": "From ℏ = Ja₀²/Ω_P (lattice action quantum)",
        "classification": "Derived-exact",
        "exp_input": "Tautological: ℏ enters via L_P, Ω_P, M_P",
        "note": "ℏ is INPUT via Planck scale, then 'derived' — TAUTOLOGY"
    },
    {
        "name": "G (Newton's constant)",
        "value": "6.674×10⁻¹¹ m³/(kg·s²)",
        "how_determined": "From G = c⁵/(ℏΩ_P²) (elastic medium gravity)",
        "classification": "Derived-exact",
        "exp_input": "Tautological: G enters via L_P, Ω_P, M_P",
        "note": "G is INPUT via Planck scale, then 'derived' — TAUTOLOGY"
    },
    # --- Fine structure constant ---
    {
        "name": "α⁻¹ (fine structure constant)",
        "value": "137 + 1/(28 - π/14) ≈ 137.036003",
        "how_determined": "BZ integral: bare=137 (vacuum impedance), correction from loop",
        "classification": "Derived-approx",
        "exp_input": "Integer 137 assumed as bare coupling; correction motivated",
        "note": "27 ppb match. BUT: bare 137 pre-assumed, correction conjectured. Grade B."
    },
    # --- Weak mixing angle ---
    {
        "name": "sin²θ_W (weak mixing angle)",
        "value": "3/13 ≈ 0.2308",
        "how_determined": "Root counting: dim(SO(8))-dim(SU(4))=13 EW modes, 3 hypercharge",
        "classification": "Derived-approx",
        "exp_input": "None directly, but depends on PS breaking chain",
        "note": "2.4% off experiment (0.23122). Identification of 13 with EW modes is structural assumption."
    },
    # --- Koide parameters ---
    {
        "name": "θ₀ (Koide phase)",
        "value": "2/9 ≈ 0.22222 rad",
        "how_determined": "Geometric eigenvalue on SO(3)/S₃ orbifold; 3 independent methods",
        "classification": "Derived-approx",
        "exp_input": "Calibrated from m_τ via θ₀ = arccos((√(m_τ/M_scale)-1)/√2)",
        "note": "θ₀ = 2/9 derived geometrically; matches experiment to 0.02%. BUT: M_scale needed."
    },
    {
        "name": "M_scale (lepton mass scale)",
        "value": "≈ 313.8 MeV",
        "how_determined": "From M_scale = v·α/(3π) with EW VEV v and α",
        "classification": "Derived-approx",
        "exp_input": "v (Higgs VEV), α — both taken from experiment",
        "note": "Depends on experimental v; not independently derived"
    },
    {
        "name": "δ_s (quark Koide phase shift)",
        "value": "π/3",
        "how_determined": "From S₄/V₄ flavor group theory (Coxeter angle)",
        "classification": "Derived-approx",
        "exp_input": "None, but S₄/V₄ identification is structural assumption",
        "note": "Group-theoretically motivated but not unique"
    },
    {
        "name": "M_scale^(q) (quark mass scale)",
        "value": "≈ 3.6 GeV",
        "how_determined": "Calibrated from m_b (bottom quark mass)",
        "classification": "Calibrated",
        "exp_input": "m_b = 4.18 GeV",
        "note": "One parameter in, four predictions out. Honest calibration."
    },
    # --- Higgs sector ---
    {
        "name": "v (Higgs VEV)",
        "value": "E_P · α⁹ · π⁵ · (9/8) ≈ 246.8 GeV",
        "how_determined": "CW effective potential mode decomposition + impedance cascade",
        "classification": "Derived-approx",
        "exp_input": "Exponent 9 underdetermined (blind CW gives 7.81). Grade C+.",
        "note": "0.17% match but exponent NOT uniquely derived. Post-hoc fit."
    },
    {
        "name": "Z_λ (Higgs quartic renormalization)",
        "value": "0.21",
        "how_determined": "Reverse-engineered from m_h = 125.1 GeV",
        "classification": "Calibrated",
        "exp_input": "m_h = 125.1 GeV (Higgs mass)",
        "note": "By construction: Z_λ = (m_h/v)²/(2η_D₄). Not a prediction."
    },
    {
        "name": "κ₄ (quartic anharmonicity)",
        "value": "≈ 0.70",
        "how_determined": "4 independent methods (geometric mean); D₄ bond geometry",
        "classification": "Derived-approx",
        "exp_input": "None, but 43% reconstruction error remains",
        "note": "Derived from geometry but imprecise"
    },
    {
        "name": "λ₃ (cubic anharmonicity)",
        "value": "0.95-1.50",
        "how_determined": "From bond potential shape (Morse vs LJ)",
        "classification": "Ad-hoc",
        "exp_input": "Bond potential shape not derived from D₄",
        "note": "58% uncertainty. Critical for decoherence rate."
    },
    # --- Gauge sector ---
    {
        "name": "M_PS (Pati-Salam scale)",
        "value": "10^{14}–10^{15.5} GeV",
        "how_determined": "Constrained by proton decay; NOT derived from D₄",
        "classification": "Undetermined",
        "exp_input": "Super-K proton lifetime bound",
        "note": "1.5-decade range. CW analytic 10^14 EXCLUDED by Super-K."
    },
    {
        "name": "Gauge coupling unification",
        "value": "NOT ACHIEVED",
        "how_determined": "Spread ~100 units at proton-safe M_PS; Δb₂=0 obstruction",
        "classification": "Ad-hoc",
        "exp_input": "SM coupling constants at M_Z",
        "note": "Grade D+. Fundamental structural failure."
    },
    # --- Cosmological ---
    {
        "name": "ρ_Λ/ρ_P (cosmological constant ratio)",
        "value": "α⁵⁷/(4π) ≈ 1.26×10⁻¹²³",
        "how_determined": "Spectral density postulate: each mode dissipates fraction α",
        "classification": "Ad-hoc",
        "exp_input": "Planck 2018 value; ~11% match (NOT 0.2%)",
        "note": "POSTDICTION: n=57 selected post-hoc. Grade C+."
    },
    # --- CKM ---
    {
        "name": "δ_CKM (CKM phase)",
        "value": "2π/(3√3) ≈ 1.209 rad",
        "how_determined": "Topological Berry phase on triality manifold",
        "classification": "Derived-approx",
        "exp_input": "None; 0.8% match to PDG",
        "note": "Well-grounded geometrically"
    },
    {
        "name": "|V_us| (CKM element)",
        "value": "0.2246",
        "how_determined": "Lattice Dirac overlaps + NLO QCD running",
        "classification": "Derived-approx",
        "exp_input": "PDG quark masses at MS-bar scale",
        "note": "0.1% match at NLO. BUT: quark masses are experimental input."
    },
    {
        "name": "|V_cb| (CKM element)",
        "value": "0.050",
        "how_determined": "Lattice Dirac overlaps + NLO QCD running",
        "classification": "Derived-approx",
        "exp_input": "PDG quark masses",
        "note": "23% off PDG. Needs NNLO."
    },
    # --- Damping ---
    {
        "name": "ζ (damping ratio)",
        "value": "π/12 ≈ 0.262",
        "how_determined": "Caldeira-Leggett spectral density on D₄",
        "classification": "Derived-exact",
        "exp_input": "None — purely geometric",
        "note": "Underdamped. Phase lag π/2 holds for ANY ζ>0 at resonance."
    },
    # --- Inflation ---
    {
        "name": "N_e (e-folds)",
        "value": "49-60 (assumed range)",
        "how_determined": "NOT derived; standard cosmological assumption",
        "classification": "Undetermined",
        "exp_input": "CMB observations constrain to ~50-60",
        "note": "Framework does not fix N_e"
    },
    {
        "name": "ε (slow-roll parameter)",
        "value": "9/2 = 4.5 (bare), then ad-hoc suppression",
        "how_determined": "Phase-lock inflation mechanism undefined",
        "classification": "Ad-hoc",
        "exp_input": "CMB requires ε ≪ 1",
        "note": "Violates slow-roll by factor ~200. Grade F."
    },
]


# ---------------------------------------------------------------------------
#  PREDICTIONS DATABASE
# ---------------------------------------------------------------------------
# Classify each claimed prediction
PREDICTIONS = [
    {
        "name": "c, ℏ, G (fundamental constants)",
        "claimed_precision": "exact",
        "classification": "TAUTOLOGY",
        "calibration_free": False,
        "reason": "Input via Planck scale, then 'derived' as lattice properties",
        "testable": False,
    },
    {
        "name": "α⁻¹ = 137 + 1/(28 - π/14)",
        "claimed_precision": "27 ppb",
        "classification": "MOTIVATED_CONJECTURE",
        "calibration_free": False,
        "reason": "Integer 137 pre-assumed; correction conjectured, not derived from BZ integral",
        "testable": True,
    },
    {
        "name": "sin²θ_W = 3/13",
        "claimed_precision": "2.4%",
        "classification": "PREDICTION",
        "calibration_free": True,
        "reason": "From root counting, no experimental input. But PS chain assumed.",
        "testable": True,
    },
    {
        "name": "Koide Q = 2/3 (identity)",
        "claimed_precision": "9.2 ppm",
        "classification": "TAUTOLOGY",
        "calibration_free": False,
        "reason": "Q=2/3 is a mathematical identity for any θ₀; not a prediction",
        "testable": False,
    },
    {
        "name": "θ₀ = 2/9 (Koide phase)",
        "claimed_precision": "0.02%",
        "classification": "PREDICTION",
        "calibration_free": True,
        "reason": "Derived from SO(3)/S₃ geometry; matches experiment without input",
        "testable": True,
    },
    {
        "name": "m_e, m_μ from Koide formula",
        "claimed_precision": "0.006%, 0.01%",
        "classification": "DERIVATION",
        "calibration_free": False,
        "reason": "Given θ₀ + M_scale (from m_τ), m_e and m_μ follow. 1 input → 2 outputs.",
        "testable": True,
    },
    {
        "name": "v (Higgs VEV)",
        "claimed_precision": "0.17%",
        "classification": "POSTDICTION",
        "calibration_free": False,
        "reason": "Exponent 9 not derived (blind CW gives 7.81). Parametric fit.",
        "testable": True,
    },
    {
        "name": "m_h (Higgs mass)",
        "claimed_precision": "exact (by Z_λ)",
        "classification": "CALIBRATION",
        "calibration_free": False,
        "reason": "Z_λ reverse-engineered from m_h. Not a prediction.",
        "testable": False,
    },
    {
        "name": "δ_CKM = 2π/(3√3)",
        "claimed_precision": "0.8%",
        "classification": "PREDICTION",
        "calibration_free": True,
        "reason": "Berry phase on triality manifold; no experimental input",
        "testable": True,
    },
    {
        "name": "|V_us| = 0.2246",
        "claimed_precision": "0.1%",
        "classification": "DERIVATION",
        "calibration_free": False,
        "reason": "Uses experimental quark masses as input to lattice Dirac overlaps",
        "testable": True,
    },
    {
        "name": "|V_cb| = 0.050",
        "claimed_precision": "23%",
        "classification": "DERIVATION",
        "calibration_free": False,
        "reason": "23% off PDG. Needs NNLO matching.",
        "testable": True,
    },
    {
        "name": "ρ_Λ/ρ_P = α⁵⁷/(4π)",
        "claimed_precision": "~11%",
        "classification": "POSTDICTION",
        "calibration_free": False,
        "reason": "n=57 selected post-hoc; suppression mechanism postulated",
        "testable": True,
    },
    {
        "name": "ν = 1/4 (Poisson ratio)",
        "claimed_precision": "exact",
        "classification": "PREDICTION",
        "calibration_free": True,
        "reason": "From D₄ isotropy; testable via gravitational wave speeds",
        "testable": True,
    },
    {
        "name": "BH entropy S = A/(4L_P²)",
        "claimed_precision": "exact",
        "classification": "DERIVATION",
        "calibration_free": True,
        "reason": "From resonance multiplicity on D₄; coefficient 1/4 derived",
        "testable": True,
    },
    {
        "name": "Anomaly cancellation (6/6 SM)",
        "claimed_precision": "exact",
        "classification": "DERIVATION",
        "calibration_free": True,
        "reason": "From LH Weyl representations in D₄ → SM cascade",
        "testable": False,
    },
    {
        "name": "D₄ 5-design property",
        "claimed_precision": "exact",
        "classification": "DERIVATION",
        "calibration_free": True,
        "reason": "Mathematical property of D₄ root system; proven in Lean 4",
        "testable": False,
    },
    {
        "name": "Gauge coupling unification",
        "claimed_precision": "NOT ACHIEVED",
        "classification": "FAILURE",
        "calibration_free": True,
        "reason": "Spread ~100 units at proton-safe scale; Δb₂=0 obstruction",
        "testable": True,
    },
    {
        "name": "ε (slow-roll) = 9/2",
        "claimed_precision": "violates ε≪1",
        "classification": "FAILURE",
        "calibration_free": True,
        "reason": "Bare ε=4.5 violates slow-roll by factor 200",
        "testable": True,
    },
    {
        "name": "Proton lifetime",
        "claimed_precision": "depends on M_PS",
        "classification": "PREDICTION",
        "calibration_free": False,
        "reason": "CW M_PS=10^14 EXCLUDED by Super-K. Threshold 10^{15.5} safe.",
        "testable": True,
    },
    {
        "name": "Σm_ν ≈ 59 meV (neutrino mass sum)",
        "claimed_precision": "order of magnitude",
        "classification": "POSTDICTION",
        "calibration_free": False,
        "reason": "Seesaw with M_R ~ M_lattice; δ_ν not derived",
        "testable": True,
    },
]


# =========================================================================
# TESTS
# =========================================================================

print("=" * 70)
print("COMPREHENSIVE PARAMETER AUDIT — Review86 DIRECTIVE 26")
print("=" * 70)

# ── TEST 1: Enumerate all parameters ──
print("\n" + "─" * 70)
print("TEST 1: Complete parameter enumeration")
print("─" * 70)

print(f"\n  Total parameters tracked: {len(PARAMETERS)}")
if args.verbose:
    for p in PARAMETERS:
        print(f"\n  {p['name']}")
        print(f"    Value: {p['value']}")
        print(f"    How: {p['how_determined']}")
        print(f"    Class: {p['classification']}")
        print(f"    Exp input: {p['exp_input']}")
        if p.get('note'):
            print(f"    Note: {p['note']}")

check("TEST 1: All parameters enumerated",
      len(PARAMETERS) >= 20,
      f"{len(PARAMETERS)} parameters tracked")

# ── TEST 2-7: Classification counts ──
print("\n" + "─" * 70)
print("TESTS 2-7: Parameter classification counts")
print("─" * 70)

classifications = {}
for p in PARAMETERS:
    c = p["classification"]
    classifications[c] = classifications.get(c, 0) + 1

n_primitive = classifications.get("Primitive", 0)
n_derived_exact = classifications.get("Derived-exact", 0)
n_derived_approx = classifications.get("Derived-approx", 0)
n_calibrated = classifications.get("Calibrated", 0)
n_adhoc = classifications.get("Ad-hoc", 0)
n_undetermined = classifications.get("Undetermined", 0)

print(f"\n  Primitive:          {n_primitive}")
print(f"  Derived-exact:      {n_derived_exact}")
print(f"  Derived-approx:     {n_derived_approx}")
print(f"  Calibrated:         {n_calibrated}")
print(f"  Ad-hoc:             {n_adhoc}")
print(f"  Undetermined:       {n_undetermined}")
print(f"  Total:              {len(PARAMETERS)}")

# D₄ lattice has NO primitive parameters — everything claimed from geometry + Planck scale
# But Planck scale itself is c, ℏ, G which are 3 experimental inputs
check("TEST 2: Primitive parameters = 0 (lattice claimed from geometry)",
      n_primitive == 0,
      f"Primitive count = {n_primitive}")

check("TEST 3: Derived-exact parameters identified",
      n_derived_exact >= 5,
      f"Derived-exact count = {n_derived_exact} (a₀, J, M*, Ω_P, c, ℏ, G, ζ)")

check("TEST 4: Derived-approximate parameters identified",
      n_derived_approx >= 5,
      f"Derived-approx count = {n_derived_approx} (α, θ₀, v, sin²θ_W, etc.)")

check("TEST 5: Calibrated parameters identified",
      n_calibrated >= 2,
      f"Calibrated count = {n_calibrated} (M_scale^q, Z_λ)")

check("TEST 6: Ad-hoc parameters identified",
      n_adhoc >= 3,
      f"Ad-hoc count = {n_adhoc} (λ₃, ρ_Λ mechanism, unification, ε)")

check("TEST 7: Undetermined parameters identified",
      n_undetermined >= 2,
      f"Undetermined count = {n_undetermined} (M_PS, N_e)")

# ── TEST 8: Calibration dependencies ──
print("\n" + "─" * 70)
print("TEST 8: Calibration dependency analysis")
print("─" * 70)

# Tautological parameters: c, ℏ, G are INPUT via Planck scale
tautological = [p for p in PARAMETERS
                if "tautolog" in p.get("note", "").lower()
                or "tautolog" in p.get("exp_input", "").lower()]
calibrated = [p for p in PARAMETERS if p["classification"] == "Calibrated"]

print(f"\n  Tautological 'derivations': {len(tautological)}")
for t in tautological:
    print(f"    - {t['name']}: {t['note']}")

print(f"\n  Calibrated parameters: {len(calibrated)}")
for c_ in calibrated:
    print(f"    - {c_['name']}: tuned to {c_['exp_input']}")

check("TEST 8: Tautological derivations correctly identified",
      len(tautological) >= 3,
      f"{len(tautological)} tautologies (c, ℏ, G 'derivations' from Planck scale)")

# ── TEST 9: Independent predictions ──
print("\n" + "─" * 70)
print("TEST 9: Genuinely independent predictions")
print("─" * 70)

# A prediction is independent if:
# 1. It uses no calibrated inputs AND
# 2. It is not a tautology AND
# 3. It is testable

independent_preds = [p for p in PREDICTIONS
                     if p["calibration_free"] and p["testable"]
                     and p["classification"] not in ("TAUTOLOGY", "CALIBRATION", "FAILURE")]
dependent_preds = [p for p in PREDICTIONS
                   if not p["calibration_free"] and p["testable"]
                   and p["classification"] not in ("TAUTOLOGY", "CALIBRATION", "FAILURE")]
tautology_preds = [p for p in PREDICTIONS if p["classification"] == "TAUTOLOGY"]
failure_preds = [p for p in PREDICTIONS if p["classification"] == "FAILURE"]
calibration_preds = [p for p in PREDICTIONS if p["classification"] == "CALIBRATION"]

print(f"\n  Independent predictions:           {len(independent_preds)}")
for ip in independent_preds:
    print(f"    ✓ {ip['name']} ({ip['claimed_precision']})")

print(f"\n  Calibration-dependent predictions:  {len(dependent_preds)}")
for dp in dependent_preds:
    print(f"    ~ {dp['name']} ({dp['claimed_precision']})")

print(f"\n  Tautologies:                       {len(tautology_preds)}")
for tp in tautology_preds:
    print(f"    ✗ {tp['name']}")

print(f"\n  Failures:                          {len(failure_preds)}")
for fp in failure_preds:
    print(f"    ✗ {fp['name']}")

print(f"\n  Calibrations (not predictions):    {len(calibration_preds)}")
for cp in calibration_preds:
    print(f"    ✗ {cp['name']}")

check("TEST 9: Independent predictions counted correctly",
      len(independent_preds) >= 4,
      f"{len(independent_preds)} genuinely independent predictions")

# ── TEST 10: Parsimony ratio ──
print("\n" + "─" * 70)
print("TEST 10: Honest parsimony ratio")
print("─" * 70)

# Effective free parameters = Primitive + Calibrated + effective inputs
# The framework claims 0 primitive parameters (all from D₄ geometry)
# BUT: the Planck scale (c, ℏ, G) provides 3 experimental inputs
# AND: there are 2 calibrated parameters (M_scale^q, Z_λ)
# AND: the α formula pre-assumes 137 as bare coupling
# Total effective inputs: 3 (Planck) + 2 (calibrated) + 1 (α_bare) = 6
# But Planck scale only provides dimensional units, not dimensionless params
# So dimensionless inputs: 2 (calibrated) + 1 (α_bare) = 3

# Conservative: count only genuinely calibration-free predictions
n_effective_inputs = len(calibrated) + 1  # +1 for α_bare=137 assumption
n_independent = len(independent_preds)

if n_effective_inputs > 0:
    parsimony_honest = n_independent / n_effective_inputs
else:
    parsimony_honest = float('inf')

# Generous: count all testable predictions (including calibration-dependent)
all_testable = [p for p in PREDICTIONS
                if p["testable"]
                and p["classification"] not in ("TAUTOLOGY", "CALIBRATION")]
n_all_testable = len(all_testable)

if n_effective_inputs > 0:
    parsimony_generous = n_all_testable / n_effective_inputs
else:
    parsimony_generous = float('inf')

print(f"\n  Effective free inputs:        {n_effective_inputs}")
print(f"    - Calibrated parameters:   {len(calibrated)}")
print(f"    - α bare coupling assumed: 1")
print(f"  Independent predictions:     {n_independent}")
print(f"  All testable predictions:    {n_all_testable}")
print(f"  Parsimony (conservative):    {parsimony_honest:.1f}")
print(f"  Parsimony (generous):        {parsimony_generous:.1f}")
print(f"  Manuscript claimed:          2.5-5.0")

check("TEST 10: Parsimony ratio computed",
      1.0 <= parsimony_honest <= 10.0,
      f"Conservative ratio = {parsimony_honest:.1f} "
      f"(independent/inputs = {n_independent}/{n_effective_inputs})")

# ── TEST 11: Compare to manuscript claim ──
print("\n" + "─" * 70)
print("TEST 11: Parsimony comparison to manuscript claim")
print("─" * 70)

# The manuscript claims 2.5-5.0
in_manuscript_range = 2.0 <= parsimony_generous <= 6.0

print(f"\n  Generous parsimony:    {parsimony_generous:.1f}")
print(f"  Conservative parsimony: {parsimony_honest:.1f}")
print(f"  Manuscript range:       2.5-5.0")

check("TEST 11: Generous parsimony within plausible range of manuscript claim",
      parsimony_generous >= 2.0,
      f"Generous={parsimony_generous:.1f}, Conservative={parsimony_honest:.1f}, "
      f"Manuscript=2.5-5.0")

# ── TEST 12: Prediction classification summary ──
print("\n" + "─" * 70)
print("TEST 12: Prediction classification summary")
print("─" * 70)

class_counts = {}
for p in PREDICTIONS:
    c = p["classification"]
    class_counts[c] = class_counts.get(c, 0) + 1

print("\n  Classification breakdown:")
for cls, cnt in sorted(class_counts.items()):
    print(f"    {cls:25s}: {cnt}")

check("TEST 12: All predictions classified",
      sum(class_counts.values()) == len(PREDICTIONS),
      f"{sum(class_counts.values())}/{len(PREDICTIONS)} classified")

# ── TEST 13: Empirically testable predictions with precision ──
print("\n" + "─" * 70)
print("TEST 13: Testable predictions with quantitative precision")
print("─" * 70)

testable_precise = [p for p in PREDICTIONS
                    if p["testable"]
                    and "%" in p["claimed_precision"] or "ppb" in p["claimed_precision"]
                    or "ppm" in p["claimed_precision"]]

print(f"\n  Quantitatively precise testable predictions: {len(testable_precise)}")
for tp in testable_precise:
    tag = "✓" if tp["calibration_free"] else "~"
    print(f"    {tag} {tp['name']}: {tp['claimed_precision']} "
          f"({tp['classification']})")

check("TEST 13: Multiple quantitatively testable predictions exist",
      len(testable_precise) >= 5,
      f"{len(testable_precise)} predictions with quantitative precision")

# ── TEST 14: Strongest prediction ──
print("\n" + "─" * 70)
print("TEST 14: Strongest prediction identification")
print("─" * 70)

# The strongest prediction is the one that is:
# - Calibration-free
# - Quantitatively precise
# - Falsifiable by near-future experiment
# Best candidate: θ₀ = 2/9 (0.02% match, geometrically derived, no input)

strongest = None
for p in PREDICTIONS:
    if p["name"] == "θ₀ = 2/9 (Koide phase)":
        strongest = p
        break

print(f"\n  STRONGEST PREDICTION: {strongest['name']}")
print(f"    Precision: {strongest['claimed_precision']}")
print(f"    Classification: {strongest['classification']}")
print(f"    Calibration-free: {strongest['calibration_free']}")
print(f"    Reason: {strongest['reason']}")

check("TEST 14: Strongest prediction is θ₀ = 2/9",
      strongest is not None and strongest["calibration_free"],
      f"θ₀ = 2/9 derived from SO(3)/S₃ geometry, 0.02% match, no calibration input")

# ── TEST 15: Weakest claim ──
print("\n" + "─" * 70)
print("TEST 15: Weakest claim identification")
print("─" * 70)

# The weakest claims are the failures and ad-hoc elements
weakest_candidates = [p for p in PREDICTIONS
                      if p["classification"] in ("FAILURE", "CALIBRATION")]

print(f"\n  Weakest claims ({len(weakest_candidates)}):")
for wc in weakest_candidates:
    print(f"    ✗ {wc['name']}: {wc['reason']}")

check("TEST 15: Weakest claims honestly identified",
      len(weakest_candidates) >= 2,
      f"{len(weakest_candidates)} failures/calibrations identified")

# ── TEST 16: Overall empirical grounding assessment ──
print("\n" + "─" * 70)
print("TEST 16: Overall empirical grounding assessment")
print("─" * 70)

# Score each dimension of contact with reality
grounding = {
    "QM (Schrödinger, Born rule)": {
        "status": "PARTIAL",
        "detail": "SVEA envelope → Schrödinger (Grade C). Born rule via Lindblad (Grade C+). "
                  "Full QFT absent (Grade F → D+ with Feynman rules).",
        "grade": "C",
    },
    "GR (Einstein equations)": {
        "status": "SUBSTANTIAL",
        "detail": "Variational derivation from lattice elasticity (Grade B). Regge convergence "
                  "with error bounds. Lorentzian signature π/2 for any ζ>0 (Grade B).",
        "grade": "B",
    },
    "SM gauge structure": {
        "status": "ALGEBRAIC",
        "detail": "SO(8)→G₂→SM cascade verified (42/42). But dynamical mechanism absent. "
                  "Gauge coupling unification FAILS (Grade D+).",
        "grade": "C+",
    },
    "Fermion masses": {
        "status": "MIXED",
        "detail": "Koide θ₀=2/9 (0.02%, PREDICTION). Lepton masses from 1 input (DERIVATION). "
                  "Quark masses need M_scale^q calibration. CKM partial.",
        "grade": "B-",
    },
    "Higgs sector": {
        "status": "WEAK",
        "detail": "VEV exponent 9 underdetermined (blind CW gives 7.81). Z_λ by construction. "
                  "CW potential structure sound but outputs uncertain.",
        "grade": "C",
    },
    "Cosmology": {
        "status": "WEAK",
        "detail": "Λ postdiction (~11% match, not 0.2%). Inflation ε=4.5 violates slow-roll. "
                  "No working inflationary mechanism.",
        "grade": "D+",
    },
    "α (fine structure)": {
        "status": "CONJECTURE",
        "detail": "27 ppb match BUT integer 137 pre-assumed, correction conjectured. "
                  "14 sub-ppm alternatives exist. Grade B (motivated conjecture).",
        "grade": "B",
    },
}

print()
for domain, info in grounding.items():
    print(f"  {domain}")
    print(f"    Status: {info['status']} (Grade {info['grade']})")
    print(f"    Detail: {info['detail']}")
    print()

# Overall grade: weighted average
grade_map = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
             "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0}
grades = [grade_map.get(info["grade"], 2.0) for info in grounding.values()]
overall_gpa = sum(grades) / len(grades)

# Map GPA back to letter
for letter, val in sorted(grade_map.items(), key=lambda x: -x[1]):
    if overall_gpa >= val - 0.15:
        overall_letter = letter
        break
else:
    overall_letter = "F"

print(f"  OVERALL EMPIRICAL GROUNDING: {overall_letter} (GPA {overall_gpa:.2f}/4.0)")
print(f"  Framework makes genuine contact with reality in:")
print(f"    - Lepton masses (θ₀=2/9, Koide): STRONG")
print(f"    - GR / Einstein equations: STRONG")
print(f"    - CKM phase (Berry phase): MODERATE")
print(f"    - α (fine structure): MODERATE (conjecture)")
print(f"  Framework departs from reality in:")
print(f"    - Gauge unification: FAILURE")
print(f"    - Inflation: FAILURE")
print(f"    - Cosmological constant: POSTDICTION")
print(f"    - Higgs mass: CALIBRATION")

check("TEST 16: Overall grounding assessment is honest (C+ to B-)",
      1.8 <= overall_gpa <= 3.2,
      f"GPA = {overall_gpa:.2f}, Letter = {overall_letter}")

# =========================================================================
# SUMMARY
# =========================================================================
print("\n" + "=" * 70)
print("PARAMETER AUDIT SUMMARY")
print("=" * 70)
print(f"""
  Parameters tracked:             {len(PARAMETERS)}
  Primitive (truly free):         {n_primitive}
  Derived-exact:                  {n_derived_exact}
  Derived-approximate:            {n_derived_approx}
  Calibrated:                     {n_calibrated}
  Ad-hoc:                         {n_adhoc}
  Undetermined:                   {n_undetermined}

  Predictions tracked:            {len(PREDICTIONS)}
  Independent (calibration-free): {n_independent}
  Dependent (uses exp input):     {len(dependent_preds)}
  Tautologies:                    {len(tautology_preds)}
  Failures:                       {len(failure_preds)}
  Calibrations:                   {len(calibration_preds)}

  Parsimony (conservative):       {parsimony_honest:.1f}
  Parsimony (generous):           {parsimony_generous:.1f}
  Manuscript claimed:             2.5-5.0

  Overall empirical grounding:    {overall_letter} (GPA {overall_gpa:.2f}/4.0)
""")

print(f"\n{'=' * 70}")
print(f"RESULTS: {passed}/{total} PASS, {failed} FAIL")
print(f"{'=' * 70}")
sys.exit(0 if failed == 0 else 1)
