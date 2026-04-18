# Deep Research Prompt: Building the Ultimate Frontier Mathematics & Physics AI Agent

---

## OBJECTIVE

Design and specify the architecture, capabilities, knowledge base, tool integrations, reasoning protocols, and evaluation criteria for a cutting-edge AI agent system purpose-built for **frontier research in theoretical mathematics and physics**. This agent should be capable of:

1. **Discovering new theorems** — not just verifying known ones
2. **Deriving physical predictions from first principles** — not just fitting data
3. **Rigorously self-auditing** — distinguishing derivation from conjecture from calibration from tautology
4. **Interfacing with formal proof assistants** — machine-checking every claimed result
5. **Running numerical simulations** — validating theoretical predictions against computation
6. **Honestly assessing empirical grounding** — rating whether physics makes contact with reality

---

## PART I: COGNITIVE ARCHITECTURE

### 1.1 Multi-Modal Reasoning Pipeline

The agent should implement a **four-phase reasoning protocol** for every theoretical claim:

```
Phase 1: COMPREHENSION
  → Parse the mathematical structure completely
  → Identify all assumptions (stated and implicit)
  → Map dependencies: what does this result depend on?
  → Classify: axiom / definition / theorem / conjecture / heuristic

Phase 2: VERIFICATION
  → Formal proof (Lean 4 / Coq / Isabelle)
  → Numerical cross-check (independent computation)
  → Dimensional analysis (units consistency)
  → Limiting cases (known physics recovered?)
  → Alternative derivation (multiple paths to same result?)

Phase 3: GROUNDING
  → Empirical comparison (does it match experiment?)
  → Precision assessment (how closely? systematic errors?)
  → Calibration audit (what experimental inputs were used?)
  → Falsifiability check (can it be disproved?)
  → Classification: DERIVATION / PREDICTION / POSTDICTION / CALIBRATION / TAUTOLOGY

Phase 4: SYNTHESIS
  → Integrate into theoretical framework
  → Identify consequences and corollaries
  → Generate new testable predictions
  → Assess parsimony (predictions per free parameter)
  → Grade overall confidence (A through F scale)
```

### 1.2 Epistemic Hygiene Module

The agent MUST maintain strict epistemic discipline:

- **Never claim a derivation that is actually a fit.** If a quantity is adjusted to match data, label it CALIBRATION.
- **Never claim a prediction that uses the observed value as input.** If the observed value enters anywhere in the derivation chain, label it POSTDICTION.
- **Never confuse algebraic identities with physical predictions.** If a result is true for any value of a parameter, it is a TAUTOLOGY, not a prediction.
- **Always report the look-elsewhere effect.** If you searched 10,000 formulas and found one that matches, report the search space.
- **Always distinguish the bare integer from the correction.** If α⁻¹ = 137 + small, state clearly whether 137 is derived or assumed.

### 1.3 Failure Mode Detection

The agent should actively detect and flag:

| Failure Mode | Detection Method |
|---|---|
| Circular reasoning | Trace derivation DAG; flag if output appears in input |
| Post-hoc rationalization | Check if formula was constructed knowing the answer |
| Dimensional inconsistency | Automated unit tracking on every equation |
| Sign errors | Compare with limiting cases and known special cases |
| Overcounting | Check for double-counting in sums, integrals, mode decompositions |
| Silent assumptions | Log every step that is "obvious" or "well-known" — verify each |
| Tautological derivations | Check if fundamental constants (c, ℏ, G) enter and exit without transformation |

---

## PART II: MATHEMATICAL CAPABILITIES

### 2.1 Core Symbolic Computation

**Required capabilities:**
- Symbolic algebra (SymPy-level + beyond): polynomials, transcendentals, special functions
- Group theory: Lie algebras, root systems, Weyl groups, representation theory, branching rules
- Differential geometry: manifolds, connections, curvature, fiber bundles, characteristic classes
- Topology: homotopy, homology, cohomology, index theorems, fiber bundle classification
- Number theory: algebraic integers, p-adic analysis, modular forms (for connections to physics)
- Category theory: functors, natural transformations, adjunctions (for structural coherence)

**Specific operations needed for lattice physics:**
```python
# Root system construction and analysis
def construct_root_system(type: str, rank: int) -> RootSystem:
    """E.g., D₄, E₈, F₄, G₂. Full root vectors, Weyl group, Dynkin diagram."""

# Brillouin zone integration
def bz_integral(integrand, lattice, method='monte_carlo', samples=10_000_000):
    """Monte Carlo or adaptive quadrature on the first BZ."""

# Representation theory
def branching_rule(G: LieGroup, H: LieGroup, rep: Representation):
    """Decompose representation of G into irreducibles of H."""

# Invariant theory
def compute_invariants(G: LieGroup, rep: Representation, degree: int):
    """All polynomial invariants up to given degree."""
```

### 2.2 Formal Proof System Integration

**Required:** Deep integration with Lean 4 (or equivalent) including:

1. **Proof search**: Given a goal, automatically try `simp`, `ring`, `omega`, `norm_num`, `aesop`, `decide`
2. **Tactic suggestion**: Given an incomplete proof state, suggest next steps
3. **Library search**: Find relevant lemmas in Mathlib by type signature (`loogle`) or natural language (`leansearch`)
4. **Proof refactoring**: Convert sorry-containing proofs to complete ones
5. **Counter-example generation**: When a theorem fails, construct explicit counter-examples
6. **Proof complexity analysis**: Estimate proof length and identify key lemmas

**Architecture pattern:**
```
Theorem claim → Lean 4 formalization → Tactic search → 
  If proved: Mark VERIFIED
  If stuck: Identify gap → Human-readable gap description
  If counterexample: Mark FALSIFIED → Report
```

### 2.3 Numerical Computation Engine

**Required capabilities:**
- GPU-accelerated lattice simulations (4D, up to 64⁴ sites)
- Monte Carlo integration with variance reduction (importance sampling, control variates, stratified sampling)
- Spectral methods (FFT, eigenvalue decomposition)
- ODE/PDE solvers (Runge-Kutta, symplectic integrators, spectral methods)
- Statistical analysis (bootstrap, jackknife, cross-validation)
- Convergence analysis (Richardson extrapolation, error scaling)

---

## PART III: PHYSICS KNOWLEDGE BASE

### 3.1 Required Physics Knowledge

The agent must have deep knowledge of:

**Quantum Mechanics:**
- Canonical quantization, path integrals, Feynman diagrams
- Lattice field theory (Wilson action, staggered fermions, domain wall fermions)
- Nielsen-Ninomiya theorem and its evasion strategies
- Anomaly cancellation (ABJ, gauge, gravitational, mixed)
- Spontaneous symmetry breaking (Goldstone theorem, Higgs mechanism)

**General Relativity:**
- Einstein field equations, Regge calculus, ADM formalism
- Black hole thermodynamics (Bekenstein-Hawking, information paradox)
- Cosmology (Friedmann equations, inflation, dark energy)
- Gravitational waves (polarizations, detectors)

**Standard Model:**
- Electroweak theory (SU(2)×U(1) breaking, W/Z masses)
- QCD (confinement, asymptotic freedom, chiral symmetry breaking)
- CKM matrix (CP violation, unitarity triangle)
- Neutrino masses (seesaw mechanism, PMNS matrix)
- BSM physics (GUTs, SUSY, extra dimensions, composite Higgs)

**Condensed Matter (for lattice analogies):**
- Phonon band structure, Bloch waves, tight-binding models
- Topological phases (topological insulators, Chern numbers)
- Critical phenomena (universality, renormalization group)
- Lattice dynamics (dynamical matrix, phonon dispersion, elastic constants)

### 3.2 Required Mathematical Knowledge for Physics

- **Lie groups and algebras**: SO(N), SU(N), Spin(N), exceptional groups (G₂, F₄, E₆, E₇, E₈)
- **Representation theory**: irreducible representations, tensor products, Clebsch-Gordan coefficients
- **Fiber bundles**: principal bundles, associated bundles, connections, curvature
- **Index theorems**: Atiyah-Singer, Atiyah-Patodi-Singer, family index theorem
- **Spectral theory**: functional determinants, zeta-function regularization, heat kernel

### 3.3 Experimental Data Interface

The agent should have access to:
- **PDG (Particle Data Group)**: All particle masses, lifetimes, branching ratios, coupling constants
- **CODATA**: Fundamental physical constants with uncertainties
- **Planck satellite data**: CMB parameters, cosmological constants
- **Gravitational wave data**: LIGO/Virgo/KAGRA event catalogs
- **Lattice QCD results**: FLAG averages for quark masses, decay constants

---

## PART IV: TOOL INTEGRATIONS

### 4.1 MCP Server Architecture

The agent should integrate with specialized computation servers via MCP (Model Context Protocol):

| Server | Purpose | Key Operations |
|---|---|---|
| `math-mcp` | Symbolic algebra | Solve, differentiate, integrate, simplify, FFT, optimize |
| `quantum-mcp` | Quantum simulation | Schrödinger evolution, wave packets, potentials |
| `molecular-mcp` | Classical MD | N-body simulation, thermodynamics, phase transitions |
| `neural-mcp` | Machine learning | Model training, evaluation, hyperparameter search |
| `lean-lsp-mcp` | Formal proofs | Lean 4 verification, tactic search, library search |
| `lattice-mcp` | Lattice field theory | Wilson loops, propagators, spectral functions |
| `group-theory-mcp` | Lie algebra computation | Root systems, Weyl groups, branching rules, Casimirs |
| `experimental-data-mcp` | Data access | PDG, CODATA, Planck, FLAG databases |

### 4.2 Workflow Orchestration

```
User query → 
  Classification (math / physics / computation / proof) →
  Route to specialized sub-agent →
    Phase 1: Comprehension (parse, identify dependencies)
    Phase 2: Computation (MCP tools for numerical/symbolic work)
    Phase 3: Verification (Lean 4 for formal proofs, cross-checks)
    Phase 4: Assessment (empirical grounding, grade assignment)
  → Synthesis and response
```

---

## PART V: EVALUATION CRITERIA

### 5.1 Benchmark Tasks

The agent should be evaluated on:

1. **Derivation quality**: Can it derive known results (e.g., Schwarzschild metric from Einstein equations)?
2. **Novel theorem discovery**: Can it find new mathematical relationships in lattice systems?
3. **Empirical grounding**: Does it correctly distinguish derivation from fit?
4. **Proof verification**: Can it formalize physics arguments in Lean 4?
5. **Numerical accuracy**: Does it achieve correct precision in lattice computations?
6. **Self-correction**: Does it catch its own errors (sign errors, dimensional errors, circular reasoning)?
7. **Honest assessment**: Does it correctly identify failures and limitations?

### 5.2 Scoring Rubric

For each theoretical claim produced by the agent:

| Criterion | A (3 pts) | B (2 pts) | C (1 pt) | F (0 pts) |
|---|---|---|---|---|
| Derivation | Complete from axioms | Sketch with gaps | Motivated conjecture | Ad hoc assertion |
| Verification | Lean 4 proof + numerics | Numerical only | Dimensional check | None |
| Precision | < 0.1% of experiment | < 1% | < 10% | > 10% or wrong sign |
| Falsifiability | Precise quantitative | Semi-quantitative | Qualitative only | Unfalsifiable |
| Honesty | All caveats stated | Most caveats | Some caveats | Overclaiming |

### 5.3 Anti-Patterns to Detect and Penalize

The evaluation should penalize:
- **Overclaiming**: Stating a result is "derived" when it is actually "fitted" (-3 pts)
- **Tautology smuggling**: Claiming to "derive" c, ℏ, G from a framework that uses them as input (-3 pts)
- **Look-elsewhere blindness**: Finding one formula match without reporting search space (-2 pts)
- **Precision inflation**: Quoting 0.2% when the actual match is 11% (-3 pts)
- **Silent calibration**: Using experimental data as input without disclosure (-3 pts)

---

## PART VI: RESEARCH WORKFLOW

### 6.1 For a New Theoretical Framework

When asked to evaluate a new theoretical framework, the agent should:

1. **Enumerate ALL free parameters** — including those disguised as "derived from geometry"
2. **Classify ALL predictions** — DERIVATION / PREDICTION / POSTDICTION / CALIBRATION / TAUTOLOGY
3. **Compute parsimony** — (calibration-free predictions) / (effective free parameters)
4. **Identify tautologies** — derivations that are algebraic identities in disguise
5. **Test uniqueness** — are the claimed formulas unique or do alternatives exist?
6. **Assess falsifiability** — can the framework be disproved by experiment?
7. **Grade overall** — using the rubric above, grade on structural/mathematical/empirical axes

### 6.2 For a Novel Computation

When performing a new computation, the agent should:

1. **State all assumptions** before computing
2. **Implement the computation** in Python with full error handling
3. **Cross-check** with at least one independent method
4. **Verify limiting cases** (known physics limits must be recovered)
5. **Report uncertainty** — statistical error, systematic error, truncation error
6. **Compare to experiment** — if applicable, with honest precision claims
7. **Classify the result** — was it derived or fitted?

### 6.3 For Formal Proof Construction

When building a formal proof, the agent should:

1. **Formalize definitions** in Lean 4 with proper type classes
2. **State the theorem** precisely (every variable typed, every condition explicit)
3. **Construct the proof** using available Mathlib lemmas
4. **Eliminate ALL sorry** — no proof gaps allowed
5. **Verify the build** — `lake build` must succeed with zero errors
6. **Document** — every theorem should have a docstring explaining its physical meaning

---

## PART VII: FRONTIER RESEARCH DIRECTIONS

The agent should be prepared to investigate:

### 7.1 Lattice Approaches to Quantum Gravity
- D₄ and other root lattice dynamics as models for emergent spacetime
- Regge calculus convergence theorems with sharp error bounds
- Phonon-gravity correspondence: elastic waves ↔ gravitational waves
- Causal set theory intersection with lattice dynamics

### 7.2 Lie Group Structure of the Standard Model
- Why SU(3)×SU(2)×U(1)? Derivation from larger symmetry principles
- Grand unification in exceptional groups (E₆, E₈, SO(10))
- Anomaly cancellation as a constraint on the fermion spectrum
- Gauge coupling unification: precision two-loop analysis

### 7.3 Mass Generation Mechanisms
- Koide formula: is Q=2/3 an exact identity or approximate rule?
- Geometric phase angles as mass parameters
- Coleman-Weinberg mechanism on lattice backgrounds
- Neutrino mass generation (seesaw, inverse seesaw, radiative)

### 7.4 Cosmological Constant Problem
- Why ρ_Λ/ρ_P ~ 10⁻¹²³? Can lattice dynamics explain this?
- Spectral density approaches to vacuum energy
- Cancellation mechanisms (SUSY, sequestering, relaxion)

### 7.5 Information Theory and Quantum Foundations
- Holographic principle on lattice backgrounds
- Black hole information paradox resolution
- Born rule derivation from decoherence
- Measurement problem and collapse interpretations

---

## PART VIII: IMPLEMENTATION SPECIFICATIONS

### 8.1 Agent Configuration

```yaml
agent:
  name: "Frontier Physics Research Agent"
  version: "1.0"
  model: "claude-opus-4.6 or equivalent frontier model"
  context_window: "200K+ tokens"
  
  reasoning:
    protocol: "four_phase"  # comprehension → verification → grounding → synthesis
    epistemic_hygiene: true
    failure_detection: true
    self_correction: true
    
  tools:
    symbolic: ["sympy", "sage", "mathematica_kernel"]
    numerical: ["numpy", "scipy", "jax", "cupy"]
    formal_proof: ["lean4", "lean-lsp-mcp"]
    visualization: ["matplotlib", "plotly"]
    data: ["pdg_api", "codata_api", "planck_data"]
    mcp_servers: ["math-mcp", "quantum-mcp", "molecular-mcp", "neural-mcp"]
    
  knowledge:
    physics: ["qft", "gr", "sm", "cosmology", "condensed_matter"]
    mathematics: ["lie_theory", "topology", "differential_geometry", "number_theory"]
    experimental: ["pdg_2024", "codata_2018", "planck_2018"]
    
  evaluation:
    auto_grade: true
    detect_tautology: true
    calibration_tracking: true
    parsimony_computation: true
    falsifiability_assessment: true
```

### 8.2 Session Protocol

Every research session should follow this protocol:

1. **Read the current manuscript** — full comprehension before any changes
2. **Identify the specific task** — what directive or question is being addressed
3. **Select appropriate tools** — MCP servers, proof assistants, numerical codes
4. **Execute the computation** — with full error handling and logging
5. **Verify the result** — cross-check, limiting cases, formal proof if possible
6. **Classify the finding** — derivation / prediction / postdiction / calibration / tautology
7. **Grade honestly** — using the standard rubric
8. **Update the manuscript** — integrate findings into the appropriate section
9. **Store key facts** — for future session continuity
10. **Report progress** — with checklist of completed and remaining items

### 8.3 Quality Gates

Before any result is reported, it must pass:

- [ ] **Dimensional consistency**: All equations have correct units
- [ ] **Limiting cases**: Known physics recovered in appropriate limits
- [ ] **Numerical stability**: Result does not change qualitatively with grid resolution
- [ ] **Statistical significance**: Error bars computed and reported
- [ ] **Independence verification**: At least one alternative computation method
- [ ] **Honesty check**: No overclaiming; all caveats stated
- [ ] **Classification**: Properly labeled as derivation/prediction/postdiction/calibration/tautology

---

## PART IX: SUCCESS CRITERIA

The frontier physics AI agent is successful if it can:

1. **Produce a novel, verifiable theorem** in lattice physics or related areas (machine-checked in Lean 4)
2. **Derive a previously unknown numerical prediction** from first principles (not fitted to data)
3. **Correctly identify a flaw** in an existing derivation that humans missed
4. **Compute a lattice integral** to higher precision than existing literature
5. **Generate a falsifiable prediction** that distinguishes the theory from alternatives
6. **Honestly assess** its own uncertainty and limitations without external prompting
7. **Maintain epistemic integrity** — never confuse derivation with fit, prediction with postdiction

The ultimate test: **Can the agent produce a publishable physics paper (or substantial contribution to one) that passes peer review?**

---

*This prompt was generated from the experience of building and auditing the IRH (Intrinsic Harmonic Resonance) theoretical framework across 31 agent sessions, producing 86 verification scripts, 311 Lean 4 declarations, and a comprehensive empirical grounding assessment. The key lesson: the most scientifically valuable work an AI agent does is NOT producing impressive-sounding derivations — it is honestly identifying where claimed derivations are actually fits, where predictions are actually postdictions, and where the framework makes genuine contact with reality versus where it departs from it.*
