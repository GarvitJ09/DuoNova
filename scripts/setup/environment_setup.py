#!/usr/bin/env python3
"""
Setup Script for DuoNova Environment
Configures the development environment and validates setup.
"""

import os
import sys
from pathlib import Path

def create_env_template():
    """Create .env template file with all required variables."""
    print("📝 Creating .env template...")
    
    env_template = """# DuoNova Environment Configuration
# Copy this file to .env and fill in your actual values

# === AWS S3 Configuration ===
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=eu-north-1
S3_BUCKET_NAME=s3-bucket-resumes

# === MongoDB Configuration ===
MONGODB_URL=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/
MONGODB_DATABASE=duonova_db

# === LLM Provider Configurations ===

# Groq Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192

# OpenAI Configuration (optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Configuration (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# === Application Configuration ===
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=INFO

# === Processing Configuration ===
DEFAULT_PROCESSING_MODE=hybrid
DEFAULT_LLM_PROVIDER=groq
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,doc,docx,txt

# === Security ===
SECRET_KEY=your_secret_key_for_sessions_here
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(env_template)
        print("   ✅ .env.template created successfully")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create .env.template: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version >= min_version:
        print(f"   ✅ Python {current_version[0]}.{current_version[1]} (minimum 3.8 required)")
        return True
    else:
        print(f"   ❌ Python {current_version[0]}.{current_version[1]} (minimum 3.8 required)")
        return False

def create_project_directories():
    """Create necessary project directories."""
    print("📁 Creating project directories...")
    
    directories = [
        "app/api",
        "app/core", 
        "app/services",
        "app/models",
        "app/utils",
        "tests/unit",
        "tests/integration", 
        "tests/api",
        "scripts/setup",
        "scripts/diagnostics",
        "logs",
        "uploads/temp"
    ]
    
    success = True
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}")
        except Exception as e:
            print(f"   ❌ {directory}: {e}")
            success = False
    
    return success

def create_init_files():
    """Create __init__.py files for Python packages."""
    print("🔧 Creating Python package files...")
    
    init_files = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/core/__init__.py",
        "app/services/__init__.py", 
        "app/models/__init__.py",
        "app/utils/__init__.py",
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/api/__init__.py"
    ]
    
    success = True
    for init_file in init_files:
        try:
            if not Path(init_file).exists():
                Path(init_file).touch()
                print(f"   ✅ {init_file}")
            else:
                print(f"   ↩️ {init_file} (already exists)")
        except Exception as e:
            print(f"   ❌ {init_file}: {e}")
            success = False
    
    return success

def check_requirements():
    """Check if requirements.txt exists and suggest installation."""
    print("📦 Checking requirements...")
    
    if Path("requirements.txt").exists():
        print("   ✅ requirements.txt found")
        print("   💡 Run: pip install -r requirements.txt")
        return True
    else:
        print("   ❌ requirements.txt not found")
        print("   💡 Create requirements.txt with necessary dependencies")
        return False

def main():
    """Main setup function."""
    print("🚀 DuoNova Environment Setup")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        create_project_directories(),
        create_init_files(),
        create_env_template(),
        check_requirements()
    ]
    
    print("\n" + "=" * 40)
    if all(checks):
        print("✅ Setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Copy .env.template to .env and fill in your credentials")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run tests: python tests/run_all_tests.py")
        print("4. Start the application: uvicorn app.main:app --reload")
    else:
        print("❌ Setup completed with errors!")
        print("Please resolve the issues above before proceeding.")
    
    return all(checks)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
