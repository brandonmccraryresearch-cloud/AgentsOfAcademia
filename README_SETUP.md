# Academic Research Assistant - Setup Guide

## Overview

This repository is a comprehensive academic research assistant for solving frontier physics problems using:

- **AI Agents**: Expert Research Assistant, Lean 4 Specialist, HLRE Agent, Meta Agent
- **Lean 4**: Formal verification and theorem proving
- **MCP Servers**: 9 specialized servers for computations
- **Python Scripts**: Numerical verification and simulations
- **Research Framework**: Intrinsic Resonance Holography (IRH) theory

## Quick Start

### 1. Initial Setup (First Time Only)

```bash
cd /app
chmod +x setup_environment.sh
./setup_environment.sh
```

This will install:
- ✅ Miniconda (Python environment manager)
- ✅ Lean 4 with elan toolchain
- ✅ Node.js and NPM
- ✅ All Python scientific packages
- ✅ All 9 MCP servers
- ✅ Research computational scripts

### 2. Activate Environment (Each Session)

```bash
source /app/activate.sh
```

### 3. Verify Installation

```bash
# Check Python
python3 --version

# Check Lean 4
lean --version

# Check Node.js
node --version

# Test computational script
python scripts/bz_integral.py --samples 10000
```

## MCP Servers

The research assistant integrates 9 MCP (Model Context Protocol) servers:

### Scientific Computing
1. **math-mcp**: Symbolic algebra, numerical computing, optimization
2. **quantum-mcp**: Wave mechanics, Schrödinger simulations
3. **molecular-mcp**: Classical molecular dynamics
4. **neural-mcp**: Neural network training and evaluation
5. **psianimator-mcp**: Quantum state simulation and animation

### Research Tools
6. **scite**: Scientific literature search (citation intelligence)
7. **particlephysics-mcp**: Particle Data Group (PDG) data access
8. **lean-lsp-mcp**: Lean 4 theorem prover language server
9. **context7-mcp**: Real-time library documentation (NEW!)

Configuration: `/app/mcp-servers/all-servers.json`

## AI Agents

### 1. Expert Research Assistant
- **Purpose**: Axiomatic rigor, four pillars structural audit
- **File**: `/app/agents/expert_research_assistant.AGENTS.md`
- **Use**: Evaluating theoretical frameworks, identifying gaps

### 2. Lean 4 Formal Verification Specialist
- **Purpose**: Machine-checked proofs, MATH_PHYSICS_REASONER_V1
- **File**: `/app/agents/lean4_formal_verification_specialist.AGENTS.md`
- **Use**: Formal verification, preventing hallucinated steps

### 3. HLRE Agent
- **Purpose**: Hyper-literal reasoning, geometric realism
- **File**: `/app/agents/hlre_agent.AGENTS.md`
- **Use**: Mechanical interpretation, lattice-geometric structures

### 4. Meta Agent
- **Purpose**: Unified intelligence combining all three personas
- **File**: `/app/agents/meta_agent.AGENTS.md`
- **Use**: Full-spectrum analysis with all capabilities

## Research Framework

### Main Theory Document
- **File**: `84.0IRH.md` (v83.0, ~600 pages)
- **Topic**: Intrinsic Resonance Holography (IRH)
- **Focus**: Unified field theory deriving constants from D₄ lattice geometry

### Lean 4 Formal Proofs
- **Location**: `/app/lean4/`
- **Project**: IHMFramework
- **Build**: `cd lean4 && lake build`

### Computational Scripts

#### 1. BZ Integral Computation
```bash
python scripts/bz_integral.py --samples 2000000
```
Computes vacuum polarization on D₄ Brillouin zone.

#### 2. D₄ Phonon Spectrum
```bash
python scripts/d4_phonon_spectrum.py
```
Computes phonon dispersion relations.

#### 3. Numerical Predictions Verification
```bash
python scripts/verify_numerical_predictions.py
```
Verifies all numerical predictions against experimental data.

## Context7 Integration

### What is Context7?
Context7 provides real-time, version-specific documentation for libraries and frameworks, preventing outdated or hallucinated information in AI responses.

### Setup (Optional)
1. Sign up at [context7.com](https://context7.com) (free basic tier)
2. Get API key from dashboard
3. Set environment variable:
   ```bash
   export CONTEXT7_API_KEY="your-key-here"
   ```
4. Add to `/app/mcp-servers/all-servers.json` (already configured)

### Usage
Context7 automatically provides documentation when AI agents query about:
- Python libraries (NumPy, SciPy, SymPy, etc.)
- Physics packages (QuTip, AstroPy, etc.)
- Machine learning frameworks (PyTorch, etc.)
- Any supported library (thousands available)

## Typical Workflows

### 1. Verify Theory Predictions
```bash
source activate.sh
python scripts/verify_numerical_predictions.py
```

### 2. Run Formal Verification
```bash
cd lean4
lake update
lake build
```

### 3. Perform BZ Integral Computation
```bash
python scripts/bz_integral.py --samples 2000000 > results/bz_integral_results.txt
```

### 4. Launch Interactive Research
```bash
jupyter lab
# Create new notebook
# Import agents, run computations, analyze results
```

### 5. Critical Theory Review
Use the meta-agent to perform comprehensive analysis:
1. Load theory document
2. Apply Four Pillars audit
3. Verify mathematical claims with Lean 4
4. Cross-check with MCP computational tools
5. Generate detailed report

## Troubleshooting

### Conda not found
```bash
export PATH="$HOME/miniconda3/bin:$PATH"
eval "$(conda shell.bash hook)"
```

### Lean not found
```bash
export PATH="$HOME/.elan/bin:$PATH"
source $HOME/.elan/env
```

### MCP server fails
```bash
# For uvx-based servers
uvx --version  # Check uvx is installed

# For npx-based servers (scite, context7)
npm --version  # Check npm is installed
```

### Lake build errors
```bash
cd lean4
lake clean
lake update
lake build
```

## Advanced Configuration

### GPU Support (Optional)
For faster computations with GPU acceleration:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Custom MCP Servers
Add new servers to `/app/mcp-servers/all-servers.json`:
```json
{
  "your-server": {
    "type": "stdio",
    "command": "your-command",
    "args": ["arg1", "arg2"],
    "tools": ["*"]
  }
}
```

## Documentation

- **Agent Specifications**: `/app/agents/*.AGENTS.md`
- **MCP Configurations**: `/app/mcp-servers/*.json`
- **Research Documents**: `/app/*.md`
- **Audit Results**: `/app/audit_results/*.md`
- **Lean 4 Proofs**: `/app/lean4/IHMFramework/*.lean`

## Support & Resources

- **Lean 4 Docs**: https://lean-lang.org/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Context7**: https://context7.com/
- **QuTip**: https://qutip.org/
- **SymPy**: https://www.sympy.org/

## Citation

If you use this research framework, please cite:

```
Intrinsic Resonance Holography: A Unified Field Theory via D₄ Spectral Geometry
Version 82.0, March 2026
```

## License

Research and educational use. See individual component licenses.
