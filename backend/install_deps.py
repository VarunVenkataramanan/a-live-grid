#!/usr/bin/env python3
"""
Simple dependency installer for A-Live-Grid Backend
Installs packages one by one to avoid conflicts
"""

import subprocess
import sys

def install_package(package):
    """Install a single package"""
    print(f"🔄 Installing {package}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e.stderr}")
        return False

def main():
    print("🚀 Installing A-Live-Grid Backend Dependencies...")
    
    # Core packages needed for the app to run
    packages = [
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0", 
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-multipart>=0.0.6",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
        "geopy>=2.3.0"
    ]
    
    failed_packages = []
    
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install {len(failed_packages)} packages:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\n💡 Try installing them manually or check your Python/pip installation.")
        return False
    else:
        print("\n🎉 All dependencies installed successfully!")
        print("\n📋 Next steps:")
        print("1. Copy env.example to .env")
        print("2. Run: python run.py")
        print("3. Visit http://localhost:8000/docs for API documentation")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 