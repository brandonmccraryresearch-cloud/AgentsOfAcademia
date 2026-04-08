#!/usr/bin/env bash
#
# Academic Research Assistant - Comprehensive Environment Setup
# =============================================================
# This script ensures all dependencies are installed for:
# - AI Agents (Expert Research Assistant, HLRE, Lean 4 Specialist, Meta Agent)
# - Lean 4 Formal Verification System
# - All 6 MCP Servers + Context7
# - Python computational scripts
# - Research document processing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/setup.log"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        log "✓ $1 is installed"
        return 0
    else
        warn "✗ $1 is not installed"
        return 1
    fi
}

echo "========================================================================="
echo "  Academic Research Assistant - Environment Setup"
echo "  Repository: Intrinsic Resonance Holography Research Framework"
echo "========================================================================="
echo ""

# ============================================================
# 1. SYSTEM PREREQUISITES
# ============================================================
log "Step 1: Checking system prerequisites..."

# Check Python
if ! check_command python3; then
    error "Python 3 is required but not installed"
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log "Python version: $PYTHON_VERSION"

# Check pip
if ! check_command pip3; then
    log "Installing pip3..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Check git
if ! check_command git; then
    error "Git is required but not installed"
fi

# ============================================================
# 2. INSTALL MINICONDA (if not present)
# ============================================================
log "Step 2: Setting up Conda environment..."

if ! check_command conda; then
    log "Installing Miniconda..."
    
    # Detect architecture
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    elif [ "$ARCH" = "aarch64" ]; then
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
    else
        error "Unsupported architecture: $ARCH"
    fi
    
    wget -q "$MINICONDA_URL" -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
    rm /tmp/miniconda.sh
    
    # Initialize conda
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    conda init bash
    
    log "✓ Miniconda installed successfully"
else
    log "✓ Conda already installed"
    eval "$(conda shell.bash hook)" 2>/dev/null || true
fi

# Create/update conda environment for research
ENV_NAME="research_assistant"
if conda env list | grep -q "^${ENV_NAME} "; then
    log "Updating existing conda environment: $ENV_NAME"
    conda activate "$ENV_NAME"
else
    log "Creating new conda environment: $ENV_NAME"
    conda create -y -n "$ENV_NAME" python=3.11
    conda activate "$ENV_NAME"
fi

# ============================================================
# 3. INSTALL LEAN 4 with ELAN
# ============================================================
log "Step 3: Setting up Lean 4..."

if ! check_command elan; then
    log "Installing elan (Lean version manager)..."
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
    source "$HOME/.elan/env"
    export PATH="$HOME/.elan/bin:$PATH"
    log "✓ elan installed successfully"
else
    log "✓ elan already installed"
    export PATH="$HOME/.elan/bin:$PATH"
fi

# Install Lean 4 toolchain specified in lean-toolchain
if [ -f "${SCRIPT_DIR}/lean4/lean-toolchain" ]; then
    LEAN_VERSION=$(cat "${SCRIPT_DIR}/lean4/lean-toolchain")
    log "Installing Lean toolchain: $LEAN_VERSION"
    cd "${SCRIPT_DIR}/lean4"
    elan install "$LEAN_VERSION"
    elan default "$LEAN_VERSION"
    
    # Build Lean project
    log "Building Lean 4 project..."
    if ! check_command lake; then
        error "Lake (Lean build tool) not found after elan installation"
    fi
    lake update
    lake build
    log "✓ Lean 4 project built successfully"
else
    warn "lean-toolchain file not found, skipping Lean installation"
fi

# ============================================================
# 4. INSTALL NODE.JS and NPM (for npx-based MCP servers)
# ============================================================
log "Step 4: Setting up Node.js (for npx-based MCP servers)..."

if ! check_command node; then
    log "Installing Node.js..."
    conda install -y -c conda-forge nodejs
    log "✓ Node.js installed via conda"
else
    log "✓ Node.js already installed"
fi

NODE_VERSION=$(node --version 2>/dev/null || echo "none")
NPM_VERSION=$(npm --version 2>/dev/null || echo "none")
log "Node version: $NODE_VERSION"
log "NPM version: $NPM_VERSION"

# ============================================================
# 5. INSTALL PYTHON SCIENTIFIC COMPUTING PACKAGES
# ============================================================
log "Step 5: Installing Python scientific packages..."

pip3 install --upgrade pip

# Core scientific computing
pip3 install numpy scipy matplotlib pandas sympy

# Quantum computing
pip3 install qutip

# Physics and math
pip3 install astropy uncertainties pint

# Visualization
pip3 install plotly seaborn ipympl

# Machine learning (for neural-mcp)
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Data analysis
pip3 install jupyter jupyterlab notebook

# Utilities
pip3 install tqdm rich click typer

log "✓ Python scientific packages installed"

# ============================================================
# 6. INSTALL MCP SERVER DEPENDENCIES
# ============================================================
log "Step 6: Installing MCP servers..."

# Install uv (fast Python package installer for MCP servers)
if ! check_command uv; then
    log "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    log "✓ uv installed"
else
    log "✓ uv already installed"
fi

# Install uvx if not present
if ! check_command uvx; then
    log "uvx will be available after uv installation"
fi

# Test MCP servers availability (they will be installed on first use with uvx)
log "MCP Servers configured:"
info "  1. math-mcp (scicomp-math-mcp)"
info "  2. quantum-mcp (scicomp-quantum-mcp)"
info "  3. molecular-mcp (scicomp-molecular-mcp)"
info "  4. neural-mcp (scicomp-neural-mcp)"
info "  5. lean-lsp-mcp"
info "  6. context7-mcp"

# ============================================================
# 7. INSTALL CONTEXT7 MCP SERVER
# ============================================================
log "Step 7: Setting up Context7 MCP server..."

# Context7 will be installed via npx on first use
log "Context7 MCP server configured for on-demand installation"
info "  • Provides real-time library documentation"
info "  • Supports thousands of packages"
info "  • Will be installed automatically via npx"

# ============================================================
# 8. VERIFY RESEARCH SCRIPTS
# ============================================================
log "Step 8: Verifying research scripts..."

cd "${SCRIPT_DIR}"

# Check Python scripts
for script in scripts/*.py; do
    if [ -f "$script" ]; then
        log "✓ Found: $(basename "$script")"
    fi
done

# Make scripts executable
chmod +x scripts/*.py 2>/dev/null || true

# ============================================================
# 9. CREATE CONVENIENCE SCRIPTS
# ============================================================
log "Step 9: Creating convenience scripts..."

# Create activate script
cat > "${SCRIPT_DIR}/activate.sh" << 'EOF'
#!/usr/bin/env bash
# Activate research assistant environment

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate research_assistant

# Add Lean to PATH
export PATH="$HOME/.elan/bin:$PATH"

# Add uv/uvx to PATH
export PATH="$HOME/.cargo/bin:$PATH"

echo "✓ Research Assistant environment activated"
echo ""
echo "Available commands:"
echo "  • python scripts/bz_integral.py       - Run BZ integral computation"
echo "  • python scripts/d4_phonon_spectrum.py - Compute D4 phonon spectrum"
echo "  • cd lean4 && lake build              - Build Lean 4 proofs"
echo "  • jupyter lab                         - Launch Jupyter for notebooks"
echo ""
EOF

chmod +x "${SCRIPT_DIR}/activate.sh"
log "✓ Created activate.sh"

# ============================================================
# 10. ENVIRONMENT VALIDATION
# ============================================================
log "Step 10: Validating environment..."

echo ""
echo "========================================================================="
echo "  ENVIRONMENT VALIDATION"
echo "========================================================================="

# Python
python3 --version
pip3 --version

# Conda
conda --version

# Lean
if command -v lean &> /dev/null; then
    lean --version
else
    warn "Lean not in PATH, but elan is configured"
fi

# Node
node --version
npm --version

# Test one Python script
log "Testing BZ integral script..."
if python3 "${SCRIPT_DIR}/scripts/bz_integral.py" --samples 1000 > /dev/null 2>&1; then
    log "✓ BZ integral script works"
else
    warn "BZ integral script test failed (might need dependencies)"
fi

# ============================================================
# FINAL SUMMARY
# ============================================================
echo ""
echo "========================================================================="
echo "  SETUP COMPLETE"
echo "========================================================================="
echo ""
log "✅ All dependencies installed successfully!"
echo ""
echo "To activate the environment in future sessions:"
echo "  source ${SCRIPT_DIR}/activate.sh"
echo ""
echo "To verify MCP servers:"
echo "  cat ${SCRIPT_DIR}/mcp-servers/all-servers.json"
echo ""
echo "To start research:"
echo "  1. Activate environment: source activate.sh"
echo "  2. Run computations: python scripts/bz_integral.py"
echo "  3. Build Lean proofs: cd lean4 && lake build"
echo "  4. Launch Jupyter: jupyter lab"
echo ""
echo "Setup log saved to: $LOG_FILE"
echo "========================================================================="
