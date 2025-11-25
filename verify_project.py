#!/usr/bin/env python
"""
TalentScout Project Verification Script
Verifies all project files are present and properly structured.
"""

import os
import sys
from pathlib import Path


class ProjectVerifier:
    """Verify project structure and files."""
    
    def __init__(self, project_root: str = "."):
        """Initialize verifier."""
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.success = []
    
    def verify_all(self):
        """Run all verification checks."""
        print("\n" + "="*60)
        print("  TalentScout Project Verification")
        print("="*60 + "\n")
        
        self.verify_core_files()
        self.verify_documentation()
        self.verify_configuration()
        self.verify_utils()
        self.verify_data_directories()
        self.verify_dependencies()
        self.verify_code_quality()
        
        self.print_results()
        return len(self.errors) == 0
    
    def verify_core_files(self):
        """Verify core Python files."""
        print("Checking core files...")
        
        core_files = [
            "core.py",
            "main.py",
            "streamlit_app.py",
            "config.py"
        ]
        
        for file in core_files:
            path = self.project_root / file
            if path.exists():
                self.success.append(f"✓ Core file found: {file}")
            else:
                self.errors.append(f"✗ Missing core file: {file}")
    
    def verify_documentation(self):
        """Verify documentation files."""
        print("Checking documentation...")
        
        doc_files = [
            "README.md",
            "QUICKSTART.md",
            "CONTRIBUTING.md",
            "DEPLOYMENT.md",
            "DEMO.md",
            "PROJECT_SUMMARY.md",
            "FILE_INDEX.md"
        ]
        
        for file in doc_files:
            path = self.project_root / file
            if path.exists():
                size = path.stat().st_size
                if size > 100:  # Sanity check: file has content
                    self.success.append(f"✓ Documentation: {file} ({size} bytes)")
                else:
                    self.warnings.append(f"⚠ Documentation {file} is very small")
            else:
                self.errors.append(f"✗ Missing documentation: {file}")
    
    def verify_configuration(self):
        """Verify configuration files."""
        print("Checking configuration...")
        
        config_files = [
            ("requirements.txt", True),
            (".env.example", True),
            (".gitignore", True),
            ("setup.bat", True),
            ("setup.sh", True)
        ]
        
        for file, required in config_files:
            path = self.project_root / file
            if path.exists():
                self.success.append(f"✓ Configuration: {file}")
            elif required:
                self.errors.append(f"✗ Missing required: {file}")
            else:
                self.warnings.append(f"⚠ Optional file missing: {file}")
    
    def verify_utils(self):
        """Verify utils package."""
        print("Checking utils package...")
        
        utils_dir = self.project_root / "utils"
        if utils_dir.exists() and utils_dir.is_dir():
            self.success.append(f"✓ Utils directory exists")
            
            # Check for __init__.py
            init_file = utils_dir / "__init__.py"
            if init_file.exists():
                self.success.append(f"✓ Utils __init__.py exists")
            else:
                self.warnings.append("⚠ Utils __init__.py missing")
            
            # Check for data_handler.py
            handler_file = utils_dir / "data_handler.py"
            if handler_file.exists():
                size = handler_file.stat().st_size
                self.success.append(f"✓ Utils data_handler.py ({size} bytes)")
            else:
                self.errors.append("✗ Utils data_handler.py missing")
        else:
            self.errors.append("✗ Utils directory missing")
    
    def verify_data_directories(self):
        """Verify data directories."""
        print("Checking data directories...")
        
        data_dir = self.project_root / "data"
        if data_dir.exists():
            self.success.append("✓ Data directory exists")
        else:
            self.warnings.append("⚠ Data directory missing (will be created on first run)")
        
        prompts_dir = self.project_root / "prompts"
        if prompts_dir.exists():
            self.success.append("✓ Prompts directory exists")
        else:
            self.warnings.append("⚠ Prompts directory missing (optional)")
    
    def verify_dependencies(self):
        """Verify dependencies file."""
        print("Checking dependencies...")
        
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            deps = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
            if len(deps) >= 10:
                self.success.append(f"✓ Requirements.txt has {len(deps)} packages")
            else:
                self.warnings.append(f"⚠ Only {len(deps)} packages in requirements.txt")
            
            # Check for critical packages
            critical_packages = ['streamlit', 'openai', 'pydantic']
            for pkg in critical_packages:
                if any(pkg.lower() in line.lower() for line in lines):
                    self.success.append(f"✓ Critical package found: {pkg}")
                else:
                    self.errors.append(f"✗ Critical package missing: {pkg}")
    
    def verify_code_quality(self):
        """Verify code quality features."""
        print("Checking code quality...")
        
        py_files = list(self.project_root.glob("*.py")) + \
                   list((self.project_root / "utils").glob("*.py"))
        
        for py_file in py_files:
            if py_file.name.startswith("__"):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(py_file, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # Check for docstrings
            if '"""' in content or "'''" in content:
                self.success.append(f"✓ {py_file.name} has docstrings")
            else:
                self.warnings.append(f"⚠ {py_file.name} lacks docstrings")
            
            # Check for type hints
            if "->" in content or ": " in content:
                self.success.append(f"✓ {py_file.name} has type hints")
            else:
                self.warnings.append(f"⚠ {py_file.name} lacks type hints")
    
    def print_results(self):
        """Print verification results."""
        print("\n" + "="*60)
        print("  Verification Results")
        print("="*60 + "\n")
        
        if self.success:
            print("✓ PASSED CHECKS:")
            for msg in self.success[:10]:  # Show first 10
                print(f"  {msg}")
            if len(self.success) > 10:
                print(f"  ... and {len(self.success) - 10} more checks")
        
        if self.warnings:
            print("\n⚠ WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print("\n✗ ERRORS:")
            for msg in self.errors:
                print(f"  {msg}")
        
        print("\n" + "="*60)
        if not self.errors:
            print("✓ Project verification PASSED!")
            print(f"  - {len(self.success)} checks passed")
            print(f"  - {len(self.warnings)} warnings")
            print("\n  Ready for:")
            print("    • Local testing")
            print("    • Cloud deployment")
            print("    • Code review")
            print("    • Production use")
        else:
            print("✗ Project verification FAILED!")
            print(f"  - {len(self.errors)} errors found")
            print(f"  - {len(self.warnings)} warnings")
            print("\n  Please fix errors before proceeding.")
        
        print("="*60 + "\n")


def main():
    """Main verification entry point."""
    verifier = ProjectVerifier()
    success = verifier.verify_all()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
