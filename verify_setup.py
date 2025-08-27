#!/usr/bin/env python3
"""
DuoNova Setup Verification Script
Checks if all requirements are properly installed and configured.
"""

import sys
import os
import asyncio
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    required = (3, 12)
    
    if version >= required:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (required: {required[0]}.{required[1]}+)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (required: {required[0]}.{required[1]}+)")
        return False

def check_packages():
    """Check if all required packages are installed."""
    print("\n📦 Checking required packages...")
    
    required_packages = {
        'fastapi': '0.116.1',
        'uvicorn': '0.35.0',
        'motor': '3.7.1',
        'openai': '1.102.0',
        'groq': '0.31.0',
        'pydantic': '2.11.7',
        'python-dotenv': '1.1.1'
    }
    
    all_good = True
    for package, expected_version in required_packages.items():
        try:
            if package == 'python-dotenv':
                import dotenv
                version = dotenv.__version__
                package_name = 'python-dotenv'
            elif package == 'motor':
                import motor
                version = motor.version
                package_name = package
            elif package == 'fastapi':
                import fastapi
                version = fastapi.__version__
                package_name = package
            elif package == 'uvicorn':
                import uvicorn
                version = uvicorn.__version__
                package_name = package
            elif package == 'openai':
                import openai
                version = openai.__version__
                package_name = package
            elif package == 'groq':
                import groq
                # Groq might not have __version__
                version = "installed"
                package_name = package
            elif package == 'pydantic':
                import pydantic
                version = pydantic.__version__
                package_name = package
            else:
                # Generic import
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                package_name = package
                
            print(f"   ✅ {package_name}: {version}")
            
        except ImportError:
            print(f"   ❌ {package}: Not installed")
            all_good = False
        except Exception as e:
            print(f"   ⚠️  {package}: Error checking version - {e}")
            
    return all_good

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n🔧 Checking environment configuration...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("   ❌ .env file not found")
        print("   💡 Copy env.template to .env and configure with your values")
        return False
    
    print("   ✅ .env file exists")
    
    # Load and check environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'MONGODB_URL',
            'MONGODB_DATABASE'
        ]
        
        optional_vars = [
            'OPENAI_API_KEY',
            'GROQ_API_KEY',
            'DEFAULT_PROCESSING_MODE',
            'PROVIDER_PRIORITY'
        ]
        
        missing_required = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith('your_') or value == '':
                missing_required.append(var)
            else:
                print(f"   ✅ {var}: Configured")
        
        if missing_required:
            print(f"   ❌ Missing required variables: {', '.join(missing_required)}")
            return False
        
        # Check LLM providers
        llm_providers = []
        for var in ['OPENAI_API_KEY', 'GROQ_API_KEY', 'ANTHROPIC_API_KEY']:
            value = os.getenv(var)
            if value and not value.startswith('your_') and value != '':
                provider = var.replace('_API_KEY', '').lower()
                llm_providers.append(provider)
                print(f"   ✅ {var}: Configured")
        
        if not llm_providers:
            print("   ❌ No LLM provider API keys configured")
            print("   💡 Configure at least OPENAI_API_KEY or GROQ_API_KEY")
            return False
        else:
            print(f"   ✅ LLM providers available: {', '.join(llm_providers)}")
        
        # Check processing configuration
        mode = os.getenv('DEFAULT_PROCESSING_MODE', 'hybrid')
        priority = os.getenv('PROVIDER_PRIORITY', 'groq,openai,anthropic')
        print(f"   ✅ Processing mode: {mode}")
        print(f"   ✅ Provider priority: {priority}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error loading .env file: {e}")
        return False

async def check_mongodb_connection():
    """Check MongoDB connection."""
    print("\n🍃 Checking MongoDB connection...")
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from dotenv import load_dotenv
        load_dotenv()
        
        mongodb_url = os.getenv('MONGODB_URL')
        if not mongodb_url or mongodb_url.startswith('mongodb+srv://username:password'):
            print("   ❌ MongoDB URL not properly configured")
            return False
            
        # Test connection
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("   ✅ MongoDB connection successful")
        client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ MongoDB connection failed: {e}")
        print("   💡 Check your MONGODB_URL and network connectivity")
        return False

def check_file_structure():
    """Check if required files exist."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'app/__init__.py',
        'app/api/resume.py',
        'app/services/resume_processing.py'
    ]
    
    all_good = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} not found")
            all_good = False
            
    return all_good

async def test_server_start():
    """Test if server can start (quick test)."""
    print("\n🚀 Testing server startup...")
    
    try:
        # Import main components
        from main import app
        print("   ✅ Main application imports successfully")
        
        # Test basic FastAPI functionality
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test health endpoint if it exists
        try:
            response = client.get("/health")
            if response.status_code == 200:
                print("   ✅ Health endpoint working")
            else:
                print(f"   ⚠️  Health endpoint returned {response.status_code}")
        except:
            print("   ⚠️  Health endpoint not available (this is okay)")
            
        print("   ✅ Server components load successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Server startup test failed: {e}")
        return False

def print_summary(results):
    """Print setup verification summary."""
    print("\n" + "="*60)
    print("📊 SETUP VERIFICATION SUMMARY")
    print("="*60)
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check}")
    
    print(f"\nScore: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n🎉 SETUP COMPLETE! Your DuoNova installation is ready to use.")
        print("\nNext steps:")
        print("1. Start the server: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Visit API docs: http://localhost:8000/docs")
        print("3. Test resume upload using Postman or curl")
    else:
        print(f"\n⚠️  SETUP INCOMPLETE! Please fix the failing checks above.")
        print("\nFor help:")
        print("- Check SETUP_GUIDE.md for detailed instructions")
        print("- Verify your .env file configuration")
        print("- Make sure all dependencies are installed")

async def main():
    """Run all setup verification checks."""
    print("🔍 DuoNova Setup Verification")
    print("="*60)
    
    # Run all checks
    results = {
        "Python Version": check_python_version(),
        "Required Packages": check_packages(),
        "Environment Configuration": check_env_file(),
        "Project Structure": check_file_structure(),
        "Server Components": await test_server_start(),
        "MongoDB Connection": await check_mongodb_connection()
    }
    
    print_summary(results)

if __name__ == "__main__":
    asyncio.run(main())
