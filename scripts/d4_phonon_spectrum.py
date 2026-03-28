#!/usr/bin/env python3
"""
D₄ Phonon Spectrum Computation

Computes the full phonon dispersion for the D₄ root lattice:
- Dynamical matrix at arbitrary wavevector k
- Eigenvalues at all high-symmetry points (Γ, X, M, R)
- Acoustic branch structure and sound velocities
- Zone-boundary topological degeneracy
- Spectral density integral (partial)

This directly addresses Review&Reconstruction §I.2 and §II.2.

Usage:
    python d4_phonon_spectrum.py                  # Default (fast, 10K samples)
    python d4_phonon_spectrum.py --samples 500000 # Full computation
    python d4_phonon_spectrum.py --strict          # CI mode: non-zero exit on failure
"""

import argparse
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


def dynamical_matrix(k, roots, J=1.0):
    """
    Compute 4×4 dynamical matrix at wavevector k.

    D_αβ(k) = J Σ_δ (δ_α δ_β / |δ|²) [1 - cos(k·δ)]

    Parameters:
        k: 4D wavevector
        roots: array of D₄ root vectors
        J: spring constant
    """
    D = np.zeros((4, 4))
    for delta in roots:
        norm_sq = np.dot(delta, delta)
        outer = np.outer(delta, delta) / norm_sq
        phase = 1 - np.cos(np.dot(k, delta))
        D += J * outer * phase
    return D


def dynamical_matrix_batch(k_batch, roots, J=1.0):
    """
    Vectorized dynamical matrix computation for a batch of wavevectors.

    Parameters:
        k_batch: (N, 4) array of wavevectors
        roots: (24, 4) array of D₄ root vectors
        J: spring constant

    Returns:
        (N, 4) array of eigenvalues at each k-point
    """
    N = k_batch.shape[0]
    # k_batch: (N, 4), roots: (24, 4)
    # k·δ for all k and all roots: (N, 24)
    kdot = k_batch @ roots.T
    # phase factors: 1 - cos(k·δ), shape (N, 24)
    phases = 1 - np.cos(kdot)

    norm_sq = np.sum(roots**2, axis=1)  # (24,)
    eigenvalues = np.zeros((N, 4))

    for idx in range(N):
        D = np.zeros((4, 4))
        for r, delta in enumerate(roots):
            outer = np.outer(delta, delta) / norm_sq[r]
            D += J * outer * phases[idx, r]
        eigenvalues[idx] = np.linalg.eigvalsh(D)

    return eigenvalues


def compute_dispersion(k_path, k_labels, roots, J=1.0):
    """Compute eigenvalues along a k-path."""
    nk = len(k_path)
    eigenvalues = np.zeros((nk, 4))
    for i, k in enumerate(k_path):
        D = dynamical_matrix(k, roots, J)
        eigenvalues[i] = np.linalg.eigvalsh(D)
    return eigenvalues


def main():
    parser = argparse.ArgumentParser(description="D₄ phonon spectrum computation")
    parser.add_argument("--samples", type=int, default=10000,
                        help="Monte Carlo samples for spectral density (default: 10000)")
    parser.add_argument("--strict", action="store_true",
                        help="CI mode: exit non-zero if any invariant check fails")
    args = parser.parse_args()

    failures = []

    print("=" * 72)
    print("D₄ PHONON SPECTRUM COMPUTATION (v82.0)")
    print("=" * 72)
    print()

    roots = d4_root_vectors()
    print(f"D₄ root vectors: {len(roots)}")
    print(f"Coordination number: {len(roots)}")
    print()

    # ===== High-symmetry points =====
    hsp = {
        'Γ': np.array([0, 0, 0, 0], dtype=float),
        'X': np.array([np.pi, 0, 0, 0]),
        'M': np.array([np.pi, np.pi, 0, 0]),
        'R': np.array([np.pi, np.pi, np.pi, np.pi]),
    }

    print("Eigenvalues at high-symmetry points (ω²/J):")
    print("-" * 50)
    for name, k in hsp.items():
        D = dynamical_matrix(k, roots)
        eigs = np.linalg.eigvalsh(D)
        print(f"  {name:2s} = {k}:")
        print(f"       ω² = ({', '.join(f'{e:.4f}' for e in eigs)})")
    print()

    # ===== Zone-boundary zero proof =====
    print("Zone-boundary zero analysis:")
    k_R = hsp['R']
    D_R = dynamical_matrix(k_R, roots)
    eigs_R = np.linalg.eigvalsh(D_R)
    zone_zero = np.allclose(eigs_R, 0)
    for delta in roots[:3]:  # Show proof for first 3 roots
        kdot = np.dot(k_R, delta)
        print(f"  k·δ = {kdot:.4f} → cos(k·δ) = {np.cos(kdot):.6f}"
              f" → 1-cos = {1-np.cos(kdot):.2e}")
    print(f"  ... (all 24 roots give 1-cos = 0)")
    print(f"  D(R) = 0 identically: {'PASS' if zone_zero else 'FAIL'}")
    if not zone_zero:
        failures.append("zone-boundary zero")
    print()

    # ===== Sound velocities =====
    print("Sound velocities (small-k limit):")
    eps = 1e-6
    for direction, label in [
        (np.array([1, 0, 0, 0], dtype=float), "[1,0,0,0]"),
        (np.array([1, 1, 0, 0], dtype=float), "[1,1,0,0]"),
        (np.array([1, 1, 1, 1], dtype=float), "[1,1,1,1]"),
    ]:
        khat = direction / np.linalg.norm(direction)
        k = eps * khat
        D = dynamical_matrix(k, roots)
        eigs = np.linalg.eigvalsh(D)
        c_sq = eigs / (eps**2)
        print(f"  k̂ = {label}: c² = ({', '.join(f'{c:.4f}' for c in c_sq)})")
    print()

    # ===== Isotropy test =====
    print("Isotropy verification (5-design property):")
    eps = 0.01
    k1 = np.array([eps, 0, 0, 0])
    k2 = np.array([eps/2, eps/2, eps/2, eps/2]) * np.linalg.norm(k1) / \
         np.linalg.norm(np.array([eps/2]*4))

    D1 = dynamical_matrix(k1, roots)
    D2 = dynamical_matrix(k2, roots)
    eigs1 = np.linalg.eigvalsh(D1)
    eigs2 = np.linalg.eigvalsh(D2)
    max_diff = np.max(np.abs(eigs1 - eigs2))
    is_isotropic = max_diff < 1e-10
    print(f"  k₁ = ({eps},0,0,0): ω² = {eigs1}")
    print(f"  k₂ ∝ (1,1,1,1):    ω² = {eigs2}")
    print(f"  Max difference: {max_diff:.2e}")
    print(f"  Isotropic: {'PASS' if is_isotropic else 'FAIL'}")
    if not is_isotropic:
        failures.append("isotropy")
    print()

    # ===== Dispersion along Γ→X =====
    print("Dispersion along Γ→X:")
    print(f"  {'k/π':>8s}  {'ω₁²':>8s}  {'ω₂²':>8s}  {'ω₃²':>8s}  {'ω₄²':>8s}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}")
    for i in range(11):
        kval = np.pi * i / 10
        k = np.array([kval, 0, 0, 0])
        D = dynamical_matrix(k, roots)
        eigs = np.linalg.eigvalsh(D)
        print(f"  {i/10:>8.1f}  " +
              "  ".join(f"{e:>8.4f}" for e in eigs))
    print()

    # ===== Spectral density computation =====
    N = args.samples
    print(f"Vacuum energy spectral density (Monte Carlo, N={N}):")
    np.random.seed(42)

    # Process in batches to limit memory usage while staying vectorized
    batch_size = min(N, 5000)
    total_omega = 0.0
    processed = 0
    while processed < N:
        this_batch = min(batch_size, N - processed)
        k_batch = np.random.uniform(-np.pi, np.pi, size=(this_batch, 4))
        eigs = dynamical_matrix_batch(k_batch, roots)
        eigs = np.maximum(eigs, 0)
        total_omega += np.sum(np.sqrt(eigs))
        processed += this_batch

    avg_omega = total_omega / N  # average ω per k-point (sum of 4 branches)
    print(f"  ⟨Σ_b ω_b(k)⟩ = {avg_omega:.6f} (lattice units)")
    print(f"  Total BZ-averaged zero-point energy density ∝ ½ℏ × {avg_omega:.6f}")
    print()

    # ===== Poisson ratio =====
    eps = 1e-6
    k_small = np.array([eps, 0, 0, 0])
    D_small = dynamical_matrix(k_small, roots)
    eigs_small = np.linalg.eigvalsh(D_small)
    c_sq = eigs_small / eps**2
    c_T_sq = c_sq[0]  # transverse
    c_L_sq = c_sq[3]  # longitudinal
    nu = (c_L_sq - 2*c_T_sq) / (2*c_L_sq - 2*c_T_sq)
    poisson_ok = np.isclose(nu, 0.25, atol=1e-3)
    print(f"Elastic properties:")
    print(f"  c²_T = {c_T_sq:.6f}")
    print(f"  c²_L = {c_L_sq:.6f}")
    print(f"  c²_L / c²_T = {c_L_sq/c_T_sq:.6f}")
    print(f"  Poisson ratio ν = {nu:.6f} (= 1/4 for isotropic 4D): "
          f"{'PASS' if poisson_ok else 'FAIL'}")
    if not poisson_ok:
        failures.append("Poisson ratio")
    print()

    print("=" * 72)
    print("PHONON SPECTRUM COMPUTATION COMPLETE")
    print("=" * 72)

    if failures:
        print(f"\nFailed checks: {', '.join(failures)}")
        if args.strict:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
