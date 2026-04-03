#!/usr/bin/env python3
"""
Academic Research Assistant - Main Orchestration Script

This script provides a unified interface for:
1. Running AI agents (Expert, Lean 4, HLRE, Meta)
2. Executing computational scripts
3. Performing formal verification
4. Querying MCP servers
5. Analyzing research documents

Usage:
    python run_research_assistant.py --help
    python run_research_assistant.py verify-environment
    python run_research_assistant.py run-computation bz_integral
    python run_research_assistant.py analyze-document 82.0theaceinthehole.md
"""

import argparse
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional

# Color output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def log(msg: str, color: str = Colors.GREEN):
    print(f"{color}{msg}{Colors.NC}")

def error(msg: str):
    print(f"{Colors.RED}[ERROR] {msg}{Colors.NC}", file=sys.stderr)
    sys.exit(1)

def warn(msg: str):
    print(f"{Colors.YELLOW}[WARNING] {msg}{Colors.NC}")

def info(msg: str):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.NC}")

class ResearchAssistant:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.scripts_dir = self.root_dir / "scripts"
        self.lean4_dir = self.root_dir / "lean4"
        self.agents_dir = self.root_dir / "agents"
        self.mcp_config = self.root_dir / "mcp-servers" / "all-servers.json"
    
    def verify_environment(self) -> bool:
        """Verify all dependencies are installed."""
        log("\n" + "="*70)
        log("  Academic Research Assistant - Environment Verification")
        log("="*70 + "\n")
        
        checks = []
        
        # Python
        try:
            result = subprocess.run(["python3", "--version"], 
                                   capture_output=True, text=True)
            info(f"✓ Python: {result.stdout.strip()}")
            checks.append(True)
        except:
            error("✗ Python not found")
            checks.append(False)
        
        # Conda
        try:
            result = subprocess.run(["conda", "--version"], 
                                   capture_output=True, text=True)
            info(f"✓ Conda: {result.stdout.strip()}")
            checks.append(True)
        except:
            warn("✗ Conda not found (optional but recommended)")
            checks.append(False)
        
        # Lean 4
        try:
            result = subprocess.run(["lean", "--version"], 
                                   capture_output=True, text=True)
            info(f"✓ Lean: {result.stdout.strip()}")
            checks.append(True)
        except:
            warn("✗ Lean not found (run setup_environment.sh)")
            checks.append(False)
        
        # Node.js
        try:
            result = subprocess.run(["node", "--version"], 
                                   capture_output=True, text=True)
            info(f"✓ Node.js: {result.stdout.strip()}")
            checks.append(True)
        except:
            warn("✗ Node.js not found (needed for scite, context7)")
            checks.append(False)
        
        # Check MCP configuration
        if self.mcp_config.exists():
            with open(self.mcp_config) as f:
                config = json.load(f)
                num_servers = len(config.get("mcpServers", {}))
                info(f"✓ MCP Configuration: {num_servers} servers configured")
                for name in config.get("mcpServers", {}).keys():
                    info(f"    - {name}")
                checks.append(True)
        else:
            error("✗ MCP configuration not found")
            checks.append(False)
        
        # Check scripts
        scripts = list(self.scripts_dir.glob("*.py"))
        info(f"✓ Computational Scripts: {len(scripts)} scripts found")
        for script in scripts:
            info(f"    - {script.name}")
        
        # Check Lean 4 project
        if (self.lean4_dir / "lakefile.toml").exists():
            info("✓ Lean 4 Project: lakefile.toml found")
            checks.append(True)
        else:
            warn("✗ Lean 4 project not properly configured")
            checks.append(False)
        
        # Check agents
        agents = list(self.agents_dir.glob("*.AGENTS.md"))
        info(f"✓ AI Agents: {len(agents)} agents configured")
        for agent in agents:
            info(f"    - {agent.stem}")
        
        log("\n" + "="*70)
        if all(checks):
            log("✅ All critical components verified successfully!")
            return True
        else:
            warn("⚠️  Some components missing. Run: ./setup_environment.sh")
            return False
    
    def run_computation(self, script_name: str, args: list = None):
        """Run a computational script."""
        script_path = self.scripts_dir / f"{script_name}.py"
        
        if not script_path.exists():
            error(f"Script not found: {script_path}")
        
        log(f"\nRunning computation: {script_name}")
        log("="*70)
        
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            subprocess.run(cmd, check=True)
            log("\n✅ Computation completed successfully")
        except subprocess.CalledProcessError as e:
            error(f"Computation failed with exit code {e.returncode}")
    
    def build_lean_project(self):
        """Build Lean 4 project."""
        log("\nBuilding Lean 4 project...")
        log("="*70)
        
        try:
            subprocess.run(["lake", "update"], cwd=self.lean4_dir, check=True)
            subprocess.run(["lake", "build"], cwd=self.lean4_dir, check=True)
            log("\n✅ Lean 4 project built successfully")
        except subprocess.CalledProcessError as e:
            error(f"Lean build failed with exit code {e.returncode}")
    
    def list_capabilities(self):
        """List all available capabilities."""
        log("\n" + "="*70)
        log("  Academic Research Assistant - Capabilities")
        log("="*70 + "\n")
        
        info("AI Agents:")
        for agent in self.agents_dir.glob("*.AGENTS.md"):
            info(f"  • {agent.stem.replace('_', ' ').title()}")
        
        info("\nComputational Scripts:")
        for script in self.scripts_dir.glob("*.py"):
            info(f"  • {script.stem}")
        
        info("\nMCP Servers:")
        if self.mcp_config.exists():
            with open(self.mcp_config) as f:
                config = json.load(f)
                for name, server in config.get("mcpServers", {}).items():
                    desc = server.get("description", "No description")
                    info(f"  • {name}: {desc}")
        
        info("\nLean 4 Formal Verification:")
        if (self.lean4_dir / "IHMFramework").exists():
            lean_files = list((self.lean4_dir / "IHMFramework").glob("*.lean"))
            info(f"  • {len(lean_files)} formal proof files")
        
        log("\n" + "="*70)

def main():
    parser = argparse.ArgumentParser(
        description="Academic Research Assistant - Main Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s verify-environment
  %(prog)s run-computation bz_integral --samples 100000
  %(prog)s run-computation d4_phonon_spectrum
  %(prog)s build-lean
  %(prog)s list-capabilities
        """
    )
    
    parser.add_argument(
        "command",
        choices=["verify-environment", "run-computation", "build-lean", 
                "list-capabilities"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "args",
        nargs="*",
        help="Additional arguments for the command"
    )
    
    args = parser.parse_args()
    
    assistant = ResearchAssistant()
    
    if args.command == "verify-environment":
        success = assistant.verify_environment()
        sys.exit(0 if success else 1)
    
    elif args.command == "run-computation":
        if not args.args:
            error("Please specify a script name (e.g., bz_integral)")
        script_name = args.args[0]
        script_args = args.args[1:]
        assistant.run_computation(script_name, script_args)
    
    elif args.command == "build-lean":
        assistant.build_lean_project()
    
    elif args.command == "list-capabilities":
        assistant.list_capabilities()

if __name__ == "__main__":
    main()
