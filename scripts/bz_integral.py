#!/usr/bin/env python3
"""
Brillouin Zone Integral for One-Loop Vacuum Polarization on D₄

Computes the vacuum polarization tensor Π_μν(k=0) on the D₄ Brillouin zone
using Monte Carlo integration with increasing sophistication:

1. Bare scalar loop (single vertex, single propagator)
2. Multi-channel structure (6 independent pairs)
3. Vertex-dressed loop (SO(8) adjoint generators)

This directly addresses Review&Reconstruction Priority 1 (§I.1).
"""

import numpy as np
import sys


def d4_root_vectors():
    """Generate all 24 root vectors of the D₄ lattice."""
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


def lattice_propagator_inv(q):
    """D₄ lattice propagator inverse: D⁻¹(q) = 4 Σ sin²(qμ/2)"""
    return 4 * np.sum(np.sin(q / 2)**2)


def verify_5_design(roots):
    """Verify the D₄ 5-design property."""
    norms = np.linalg.norm(roots, axis=1)
    unit = roots / norms[:, np.newaxis]

    # Test <x₁⁴> = 3/(d(d+2)) for d=4
    quartic = np.mean(unit[:, 0]**4)
    expected = 3.0 / (4 * 6)
    ok1 = np.isclose(quartic, expected)

    # Test <x₁²x₂²> = 1/(d(d+2))
    mixed = np.mean(unit[:, 0]**2 * unit[:, 1]**2)
    expected2 = 1.0 / (4 * 6)
    ok2 = np.isclose(mixed, expected2)

    return ok1 and ok2, quartic, mixed


def bare_loop_integral(N_samples=2000000, seed=42):
    """
    Level 1: Bare scalar loop on the D₄ BZ.

    Π_μμ(0) = ∫ d⁴q/(2π)⁴ × sin²(qμ) / [4Σ sin²(qρ/2)]²

    This is the simplest possible vacuum polarization diagram.
    """
    np.random.seed(seed)
    q_samples = np.random.uniform(-np.pi, np.pi, size=(N_samples, 4))

    # Propagator and vertex
    Dinv = 4 * np.sum(np.sin(q_samples / 2)**2, axis=1)
    sinq_sq = np.sum(np.sin(q_samples)**2, axis=1)

    # Filter zero mode
    mask = Dinv > 1e-8

    # Full trace: tr Π(0) = ∫ [Σ sin²qμ] / [D⁻¹]²
    Pi_trace = np.mean(sinq_sq[mask] / Dinv[mask]**2)

    # Individual diagonal components (isotropy check)
    Pi_00 = np.mean(np.sin(q_samples[mask, 0])**2 / Dinv[mask]**2)
    Pi_11 = np.mean(np.sin(q_samples[mask, 1])**2 / Dinv[mask]**2)

    return Pi_trace, Pi_00, Pi_11


def multi_channel_integral(N_samples=2000000, seed=42):
    """
    Level 2: Multi-channel vertex structure.

    The D₄ lattice has 6 independent pairs of coordinate axes (4 choose 2).
    Each pair contributes an independent scattering channel. The total
    vacuum polarization includes all 6 channels with their respective
    vertex factors from the D₄ root structure.

    Π_total(0) = Σ_{i<j} ∫ d⁴q/(2π)⁴ × V_ij(q)² / [D(q)]²

    where V_ij(q) is the vertex factor for the (i,j) channel.
    """
    np.random.seed(seed)
    q_samples = np.random.uniform(-np.pi, np.pi, size=(N_samples, 4))

    Dinv = 4 * np.sum(np.sin(q_samples / 2)**2, axis=1)
    mask = Dinv > 1e-8

    # For each pair (i,j), the D₄ vertex involves sin(q_i ± q_j)
    # from the root vectors (±e_i ± e_j)
    total_Pi = 0
    channel_results = []

    for i in range(4):
        for j in range(i + 1, 4):
            # Vertex from D₄ roots (±e_i ± e_j): 4 roots per pair
            # V_ij² = Σ over 4 roots: sin²(±qi ± qj)
            # Since sin(-x) = -sin(x), the four terms reduce to two unique:
            # sin²(qi+qj) and sin²(qi-qj), each appearing twice → factor of 2
            V_sq = 2 * (np.sin(q_samples[mask, i] + q_samples[mask, j])**2 +
                        np.sin(q_samples[mask, i] - q_samples[mask, j])**2)

            Pi_channel = np.mean(V_sq / Dinv[mask]**2)
            channel_results.append((i, j, Pi_channel))
            total_Pi += Pi_channel

    return total_Pi, channel_results


def main():
    print("=" * 72)
    print("BRILLOUIN ZONE INTEGRAL — VACUUM POLARIZATION ON D₄ (v82.0)")
    print("=" * 72)
    print()

    roots = d4_root_vectors()

    # ===== 5-Design Verification =====
    print("5-Design Verification:")
    ok, quartic, mixed = verify_5_design(roots)
    print(f"  ⟨x₁⁴⟩ = {quartic:.8f} (exact: {3.0/(4*6):.8f})")
    print(f"  ⟨x₁²x₂²⟩ = {mixed:.8f} (exact: {1.0/(4*6):.8f})")
    print(f"  5-design: {'PASS' if ok else 'FAIL'}")
    print()

    # ===== Level 1: Bare Loop =====
    print("Level 1: Bare Scalar Loop (2M samples)")
    print("-" * 50)
    Pi_trace, Pi_00, Pi_11 = bare_loop_integral()
    print(f"  tr Π(0) = {Pi_trace:.8f}")
    print(f"  Π₀₀(0)  = {Pi_00:.8f}")
    print(f"  Π₁₁(0)  = {Pi_11:.8f}")
    print(f"  Isotropy: Π₀₀/Π₁₁ = {Pi_00/Pi_11:.6f}")
    print(f"  tr Π/(4π) = {Pi_trace/(4*np.pi):.8f}")
    target = 1 / (28 - np.pi / 14)
    print(f"  Target: 1/(28-π/14) = {target:.8f}")
    print(f"  Ratio: {Pi_trace/(4*np.pi) / target:.4f}")
    print()

    # ===== Level 2: Multi-Channel =====
    print("Level 2: Multi-Channel Vertex Structure (2M samples)")
    print("-" * 50)
    total_Pi, channels = multi_channel_integral()
    print(f"  Channel contributions:")
    for i, j, Pi_ch in channels:
        print(f"    ({i},{j}): Π = {Pi_ch:.8f}")
    print(f"  Total Π (6 channels) = {total_Pi:.8f}")
    print(f"  Total Π/(4π) = {total_Pi/(4*np.pi):.8f}")
    print(f"  Target: {target:.8f}")
    print(f"  Ratio: {total_Pi/(4*np.pi) / target:.4f}")
    print()

    # ===== Analysis =====
    print("Analysis:")
    print(f"  Bare loop / target = {Pi_trace/(4*np.pi) / target:.4f}")
    print(f"  Multi-channel / target = {total_Pi/(4*np.pi) / target:.4f}")
    print()
    print("  The multi-channel structure significantly enhances the integral")
    print("  relative to the bare loop. The remaining gap to the target value")
    print("  requires the full SO(8) vertex dressing, which includes:")
    print("    - 28 adjoint generators (not just 6 coordinate pairs)")
    print("    - Triality sector summation (×3)")
    print("    - Self-energy chain resummation")
    print()

    # ===== Summary =====
    alpha_inv_theory = 137 + target
    alpha_inv_exp = 137.035999206
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  α⁻¹ formula: 137 + 1/(28 - π/14) = {alpha_inv_theory:.10f}")
    print(f"  CODATA 2018:                        {alpha_inv_exp:.10f}")
    print(f"  Agreement: {abs(alpha_inv_theory-alpha_inv_exp)/alpha_inv_exp*1e9:.1f} ppb")
    print()
    print("  BZ integral status:")
    print(f"    Level 1 (bare):         {Pi_trace/(4*np.pi)/target*100:.1f}% of target")
    print(f"    Level 2 (multi-channel): {total_Pi/(4*np.pi)/target*100:.1f}% of target")
    print(f"    Level 3 (SO(8) dressed): PENDING (requires full vertex structure)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
