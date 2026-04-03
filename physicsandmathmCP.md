PsiAnimator: Quantum Physics Simulation & Animation Tool
PsiAnimator-MCP
Quantum Physics Simulation and Animation Server

A Model Context Protocol (MCP) server that integrates QuTip (Quantum Toolbox in Python) for quantum physics computations with Manim (Mathematical Animation Engine) for visualization.

Features
🔬 Quantum Physics Engine: Complete state management, time evolution, and measurement tools
🎬 Manim Animations: Publication-quality visualizations with quantum-specific scenes
🔌 MCP Integration: Seamless integration with MCP-compatible clients
🧮 Scientific Computing: Built on NumPy, SciPy, and QuTip for accuracy
📊 Visualization Types: Bloch spheres, Wigner functions, state tomography, circuits
🎓 Educational Focus: Perfect for quantum mechanics education and research
Installation
Quick Install
Option 1: One-line install (Unix/macOS)
curl -fsSL https://raw.githubusercontent.com/username/PsiAnimator-MCP/main/scripts/install.sh | bash
Option 2: PowerShell (Windows)
iwr https://raw.githubusercontent.com/username/PsiAnimator-MCP/main/scripts/install.ps1 | iex
Option 3: pip (when available on PyPI)
# Core installation (quantum computation only)
pip install psianimator-mcp

# Full installation with animation support
pip install "psianimator-mcp[animation]"

# Development installation
pip install "psianimator-mcp[dev,animation]"
Option 4: From source
git clone https://github.com/username/PsiAnimator-MCP.git
cd PsiAnimator-MCP
./scripts/install.sh --from-source
Prerequisites
Python ≥ 3.10
Git (for development installation)
For animation features:

LaTeX (for advanced mathematical rendering)
FFmpeg (for video generation)
Cairo graphics library (for high-quality rendering)
Installation Options Explained
🚀 Core Installation (Recommended for most users)

pip install psianimator-mcp
Includes all quantum computation features
MCP server functionality
QuTip, NumPy, SciPy for quantum physics
Works immediately without system dependencies
🎬 Animation Installation (For visualization)

pip install "psianimator-mcp[animation]"
Everything from core installation
Manim for generating animations
Requires system dependencies (LaTeX, FFmpeg)
Larger download and installation time
🔧 Development Installation

git clone https://github.com/username/PsiAnimator-MCP.git
cd PsiAnimator-MCP
pip install -e ".[dev,animation]"
Why Animation is Optional
Animation features (Manim) are kept optional because:

Heavy Dependencies: Manim requires LaTeX, FFmpeg, and Cairo which can be several GB
Installation Complexity: System dependencies can fail on different platforms
Use Case Separation: Many users only need quantum computation, not visualization
CI/Testing Reliability: Core features can be tested without system dependencies
Disk Space: Core installation is ~100MB vs ~2GB+ with full animation stack
Dependencies
Core dependencies (automatically installed):

QuTip ≥ 4.7.0 (quantum physics computations)
MCP ≥ 1.0.0 (Model Context Protocol)
NumPy, SciPy, matplotlib (scientific computing)
Pydantic, aiohttp (async web framework)
Animation dependencies (optional extras):

Manim ≥ 0.18.0 (mathematical animations)
h5py ≥ 3.9.0 (data storage)
pandas ≥ 2.0.0 (data analysis)
Post-Installation Setup
After installation, run the setup command:

psianimator-mcp setup
This will:

Create configuration directory (~/.config/psianimator-mcp/)
Copy example configuration file
Test installation and show feature availability
Provide Claude Desktop integration instructions
Verifying Installation
Check your installation status:

python -c "import psianimator_mcp; print(f'✅ Core: OK, Animation: {psianimator_mcp.is_animation_available()}')"
Expected outputs:

✅ Core: OK, Animation: True - Full installation with animations
✅ Core: OK, Animation: False - Core installation only
Troubleshooting
Import Errors

# If you get "No module named 'psianimator_mcp'"
pip install psianimator-mcp

# If you get animation-related errors
pip install "psianimator-mcp[animation]"
Animation Dependencies

# Ubuntu/Debian
sudo apt-get install texlive-latex-base ffmpeg libcairo2-dev

# macOS
brew install mactex ffmpeg cairo

# Windows
# Install MiKTeX, FFmpeg from official websites
Claude Desktop Integration
Automatic Configuration
Generate Claude Desktop configuration:

psianimator-mcp claude-config
Manual Configuration
Add to your Claude Desktop configuration file:

Windows: %USERPROFILE%\AppData\Roaming\Claude\claude_desktop_config.json macOS: ~/Library/Application Support/Claude/claude_desktop_config.json Linux: ~/.config/claude-desktop/claude_desktop_config.json

{
  "mcpServers": {
    "psianimator-mcp": {
      "command": "python3",
      "args": ["-m", "psianimator_mcp.cli", "serve"],
      "env": {
        "PSIANIMATOR_CONFIG": "~/.config/psianimator-mcp/config.json"
      }
    }
  }
}
Note: Restart Claude Desktop after configuration changes.

Quick Start
1. Start the Server
Default (serves via MCP protocol):

psianimator-mcp
Stdio transport explicitly:

psianimator-mcp serve --transport stdio
WebSocket transport:

psianimator-mcp serve --transport websocket --port 3000
2. Test Installation
psianimator-mcp test
3. Basic Usage Example
import asyncio
from psianimator_mcp.tools.quantum_state_tools import create_quantum_state
from psianimator_mcp.tools.measurement_tools import measure_observable
from psianimator_mcp.server.config import MCPConfig

async def basic_example():
    config = MCPConfig()
    
    # Create a qubit in |0⟩ state
    result = await create_quantum_state({
        'state_type': 'pure',
        'system_dims': [2],
        'parameters': {'state_indices': [0]},
        'basis': 'computational'
    }, config)
    
    state_id = result['state_id']
    
    # Measure ⟨σz⟩
    measurement = await measure_observable({
        'state_id': state_id,
        'observable': 'sigmaz',
        'measurement_type': 'expectation'
    }, config)
    
    print(f"⟨σz⟩ = {measurement['measurement_results']['expectation_value']}")

asyncio.run(basic_example())
MCP Tools
1. create_quantum_state
Create quantum states of various types:

Pure states: |ψ⟩ (ket vectors)
Mixed states: ρ (density matrices)
Coherent states: |α⟩ (harmonic oscillator)
Squeezed states: reduced uncertainty
Thermal states: finite temperature
Fock states: definite photon number
2. evolve_quantum_system
Time evolution with multiple methods:

Unitary: Schrödinger equation (closed systems)
Master equation: Lindblad form (open systems)
Monte Carlo: Quantum trajectories
Stochastic: Continuous measurement
3. measure_observable
Quantum measurements and analysis:

Expectation values: ⟨O⟩
Variances: Δ²O
Probability distributions: P(outcome)
Correlation functions: ⟨A⟩⟨B⟩
4. animate_quantum_process
Generate Manim animations:

Bloch sphere evolution: Qubit dynamics
Wigner functions: Phase space representation
State tomography: Density matrix visualization
Circuit execution: Gate sequence animation
Energy levels: Population dynamics
5. quantum_gate_sequence
Apply quantum gates with visualization:

Single-qubit gates: Pauli, Hadamard, rotations
Two-qubit gates: CNOT, CZ, SWAP
Parameterized gates: RX, RY, RZ with custom angles
Circuit visualization: Step-by-step animation
6. calculate_entanglement
Compute entanglement measures:

Von Neumann entropy: S(ρ) = -Tr(ρ log ρ)
Concurrence: Two-qubit entanglement measure
Negativity: Partial transpose criterion
Mutual information: I(A:B)
Configuration
Configure via environment variables or MCPConfig:

from psianimator_mcp.server.config import MCPConfig

config = MCPConfig(
    quantum_precision=1e-12,
    max_hilbert_dimension=1024,
    animation_cache_size=100,
    output_directory="./output",
    render_backend="cairo"
)
Environment Variables
Configure PsiAnimator-MCP via environment variables:

Server Configuration:

PSIANIMATOR_CONFIG - Path to configuration file
PSIANIMATOR_TRANSPORT - Transport protocol (stdio/websocket)
PSIANIMATOR_HOST - Host for WebSocket transport
PSIANIMATOR_PORT - Port for WebSocket transport
Quantum Settings:

PSIANIMATOR_QUANTUM_PRECISION - Quantum computation precision
PSIANIMATOR_MAX_HILBERT_DIM - Maximum Hilbert space dimension
PSIANIMATOR_OUTPUT_DIR - Output directory for animations
Example:

export PSIANIMATOR_TRANSPORT=websocket
export PSIANIMATOR_PORT=3001
psianimator-mcp
CLI Commands
PsiAnimator-MCP provides several CLI commands:

psianimator-mcp                    # Start server (default: stdio)
psianimator-mcp serve              # Start server with options
psianimator-mcp config             # Show current configuration
psianimator-mcp setup              # Run post-installation setup
psianimator-mcp test               # Test installation
psianimator-mcp claude-config      # Generate Claude Desktop config
psianimator-mcp examples           # Show usage examples
psianimator-mcp version            # Show version
psianimator-mcp --help             # Show help
Command Examples
Start with custom config:

psianimator-mcp serve --config /path/to/config.json
WebSocket mode:

psianimator-mcp serve --transport websocket --host 0.0.0.0 --port 8080
Verbose logging:

psianimator-mcp serve -vvv
Examples
Comprehensive examples are provided in the examples/ directory:

basic_usage.py - Core functionality walkthrough
Bell state creation and entanglement analysis
Harmonic oscillator coherent state evolution
Multi-qubit quantum circuits
Run examples:

python examples/basic_usage.py
Development
Setup Development Environment
git clone https://github.com/username/PsiAnimator-MCP.git
cd PsiAnimator-MCP
pip install -e ".[dev]"
pre-commit install
Run Tests
pytest tests/
Code Quality
black src/ tests/
isort src/ tests/
mypy src/
Architecture
PsiAnimator-MCP/
├── src/psianimator_mcp/
│   ├── server/          # MCP server implementation
│   ├── quantum/         # Quantum physics engine
│   ├── animation/       # Manim visualization components
│   └── tools/           # MCP tool implementations
├── tests/               # Comprehensive test suite
├── examples/            # Usage examples
└── docs/               # Documentation
Limitations
Animation rendering requires sufficient system resources
Large Hilbert spaces (>1024 dimensions) may impact performance
Some advanced quantum error correction features are not yet implemented
License
MIT License - see LICENSE for details.

Contributing
We welcome contributions! Please see CONTRIBUTING.md for:

Development guidelines
Code standards
Testing requirements
Pull request process
Support
Documentation: See docs/API_REFERENCE.md
Examples: Check examples/ directory
Issues: Report bugs via GitHub issues

-----

Scite: Find Scientific Papers with Citation Intelligence
scite MCP Server
An MCP server that provides tools to search scientific literature via scite.ai, returning papers with citation context (supporting, contrasting, or mentioning citations).

Features
Search papers by keyword or topic
Citation intelligence — see how each paper is cited (supporting/contrasting/mentioning)
Formatted output with title, authors, abstract, and citation counts
Integration
Add the following configuration to your MCP client config:

{
  "mcpServers": {
    "scite": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.scite.ai/mcp"]
    }
  }
}

Usage
The server provides a tool named `search` that accepts a query string:

{
  "query": string  // Search terms, e.g. "D4 lattice phonon fine structure constant"
}
Example
Request:

{
  "query": "D4 root lattice phonon dispersion"
}
This will return matching papers with citation context indicating whether other works support, contrast, or merely mention each result.

License
See the scite.ai terms of service at https://scite.ai

----

Particle Physics: PDG Data API for AI Assistants & Apps
ParticlePhysics MCP Server
A Model Context Protocol (MCP) server that provides seamless access to particle physics data from the Particle Data Group (PDG). This production-ready server enables AI assistants and applications to query comprehensive particle physics information.

Latest Updates
Natural Language Particle Names and Simplified Tools
Added support for plain English particle names
Over 400 internal name translations
Improved fuzzy matching and normalization
Streamlined tool usage
Installation
For Claude Desktop/IDE Users:
Simply add this to your claude_desktop_config.json:

{
  "mcpServers": {
    "particlephysics": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "--from",
        "git+https://github.com/uzerone/ParticlePhysics-MCP-Server.git",
        "pp-mcp-server"
      ]
    }
  }
}
That's it! No local installation needed. The server will be automatically downloaded and run when needed.

Available Tools (Hotfixing 24/7)
search_particle

Unified particle search and data retrieval tool - handles ALL particle searches, property lookups, database info, Monte Carlo ID lookups, canonical names, PDG editions, identifier operations, PDG identifier parsing, base identifier extraction, identifier creation, and best property finding.
get_data

Unified data tool - handles ALL data operations including mass/lifetime/width measurements, summary values, particle text, property details, PDG database keys, measurement details, measurement values, references, footnotes, measurement error analysis, particle quantum numbers, particle properties/classification, particle lists by criteria, detailed particle analysis, mass/lifetime/width details, particle error information, linked data retrieval, data normalization, and raw PDG table access.
decay_analysis

Unified decay analysis tool - handles ALL decay operations including branching fractions with uncertainty analysis, decay products with subdecay analysis, branching ratios with correlations, decay mode details with classification, hierarchical decay structure analysis with visualization data, and PDG rounding rules for decay values with detailed formatting.
error_analysis

Unified error analysis tool - handles ALL error operations including PDG identifier validation with enhanced error analysis and suggestions, PDG API error type information and meanings, diagnosis of common particle/data lookup issues with solutions, and safe particle lookup with comprehensive error handling.
Maintainers
This project is maintained by:

@uzerone
@bee4come
License
MIT License - see LICENSE file for details.

----

Math MCP: GPU Scientific Computing for AI & Simulations
Math-Physics-ML MCP System
PyPI - Math MCP PyPI - Quantum MCP PyPI - Molecular MCP PyPI - Neural MCP Documentation License: MIT

GPU-accelerated Model Context Protocol servers for computational mathematics, physics simulations, and machine learning.

📚 Documentation
View Full Documentation →

Guide	Description
Installation	Setup instructions for pip, uv, and uvx
Configuration	Claude Desktop & Claude Code setup
Quick Start	Get running in 5 minutes
API Reference	Complete tool documentation
Visual Demos	Interactive physics simulations
About
This system enables AI assistants to perform real scientific computing — from solving differential equations to running molecular dynamics simulations.

Overview
This system provides 4 specialized MCP servers that bring scientific computing capabilities to AI assistants like Claude:

Server	Description	Tools
Math MCP	Symbolic algebra (SymPy) + numerical computing	14
Quantum MCP	Wave mechanics & Schrodinger simulations	12
Molecular MCP	Classical molecular dynamics	15
Neural MCP	Neural network training & evaluation	16
Key Features:

GPU acceleration with automatic CUDA detection (10-100x speedup)
Async task support for long-running simulations
Cross-MCP workflows via URI-based data sharing
Progressive discovery for efficient tool exploration
Quick Start
Installation with uvx (Recommended)
Run any MCP server directly without installation:

# Run individual servers
uvx scicomp-math-mcp
uvx scicomp-quantum-mcp
uvx scicomp-molecular-mcp
uvx scicomp-neural-mcp
Installation with pip/uv
# Install individual servers
pip install scicomp-math-mcp
pip install scicomp-quantum-mcp
pip install scicomp-molecular-mcp
pip install scicomp-neural-mcp

# Or install all at once
pip install scicomp-math-mcp scicomp-quantum-mcp scicomp-molecular-mcp scicomp-neural-mcp

# With GPU support (requires CUDA)
pip install scicomp-math-mcp[gpu] scicomp-quantum-mcp[gpu] scicomp-molecular-mcp[gpu] scicomp-neural-mcp[gpu]
Configuration
Claude Desktop
Add to your Claude Desktop configuration file:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json Windows: %APPDATA%\Claude\claude_desktop_config.json

{
  "mcpServers": {
    "math-mcp": {
      "command": "uvx",
      "args": ["scicomp-math-mcp"]
    },
    "quantum-mcp": {
      "command": "uvx",
      "args": ["scicomp-quantum-mcp"]
    },
    "molecular-mcp": {
      "command": "uvx",
      "args": ["scicomp-molecular-mcp"]
    },
    "neural-mcp": {
      "command": "uvx",
      "args": ["scicomp-neural-mcp"]
    }
  }
}
Claude Code
Add to your project's .mcp.json:

{
  "mcpServers": {
    "math-mcp": {
      "command": "uvx",
      "args": ["scicomp-math-mcp"]
    },
    "quantum-mcp": {
      "command": "uvx",
      "args": ["scicomp-quantum-mcp"]
    }
  }
}
Or configure globally in ~/.claude/settings.json.

Usage Examples
Math MCP
# Solve equations symbolically
symbolic_solve(equations="x**3 - 6*x**2 + 11*x - 6")
# Result: [1, 2, 3]

# Compute derivatives
symbolic_diff(expression="sin(x)*exp(-x**2)", variable="x")
# Result: cos(x)*exp(-x**2) - 2*x*sin(x)*exp(-x**2)

# GPU-accelerated matrix operations
result = matrix_multiply(a=matrix_a, b=matrix_b, use_gpu=True)
Quantum MCP
# Create a Gaussian wave packet
psi = create_gaussian_wavepacket(
    grid_size=[256],
    position=[64],
    momentum=[2.0],
    width=5.0
)

# Solve time-dependent Schrodinger equation
simulation = solve_schrodinger(
    potential=barrier_potential,
    initial_state=psi,
    time_steps=1000,
    dt=0.1,
    use_gpu=True
)
Molecular MCP
# Create particle system
system = create_particles(
    n_particles=1000,
    box_size=[20, 20, 20],
    temperature=1.5
)

# Add Lennard-Jones potential
add_potential(system_id=system, potential_type="lennard_jones")

# Run MD simulation
trajectory = run_nvt(system_id=system, n_steps=100000, temperature=1.0)

# Analyze diffusion
msd = compute_msd(trajectory_id=trajectory)
Neural MCP
# Define model
model = define_model(architecture="resnet18", num_classes=10, pretrained=True)

# Load dataset
dataset = load_dataset(dataset_name="CIFAR10", split="train")

# Train
experiment = train_model(
    model_id=model,
    dataset_id=dataset,
    epochs=50,
    batch_size=128,
    use_gpu=True
)

# Export for deployment
export_model(model_id=model, format="onnx", output_path="model.onnx")
Development
# Clone the repository
git clone https://github.com/andylbrummer/math-mcp.git
cd math-mcp

# Install dependencies
uv sync --all-extras

# Install MCP servers in editable mode (required for entry points)
uv pip install --python .venv/bin/python \
  -e servers/math-mcp \
  -e servers/quantum-mcp \
  -e servers/molecular-mcp \
  -e servers/neural-mcp

# Run tests
uv run pytest -m "not gpu"  # CPU only
uv run pytest               # All tests (requires CUDA)

# Run with coverage
uv run pytest --cov=shared --cov=servers
Note: The editable install step is required because uv sync doesn't install entry point scripts for workspace packages. After this step, you can run servers directly with uv run scicomp-math-mcp.

See CONTRIBUTING.md for development guidelines.

Performance
GPU acceleration provides significant speedups for compute-intensive operations:

MCP	Operation	CPU	GPU	Speedup
Math	Matrix multiply (4096x4096)	2.1s	35ms	60x
Quantum	2D Schrodinger (512x512, 1000 steps)	2h	2min	60x
Molecular	MD (100k particles, 10k steps)	1h	30s	120x
Neural	ResNet18 training (1 epoch)	45min	30s	90x
Architecture
For technical details about the system architecture, see ARCHITECTURE.md.

License
MIT License - see LICENSE for details.

Contributing
Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

---



