#!/usr/bin/env python3
"""
System Health Diagnostic Tool
Comprehensive system health check for DuoNova application.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

async def check_environment_variables():
    """Check if all required environment variables are set."""
    print("🔧 Checking Environment Variables...")
    
    required_vars = {
        'AWS_ACCESS_KEY_ID': 'AWS Access Key',
        'AWS_SECRET_ACCESS_KEY': 'AWS Secret Key',
        'AWS_REGION': 'AWS Region',
        'S3_BUCKET_NAME': 'S3 Bucket Name',
        'MONGODB_URL': 'MongoDB Connection URL',
        'MONGODB_DATABASE': 'MongoDB Database Name'
    }
    
    optional_vars = {
        'GROQ_API_KEY': 'Groq API Key',
        'OPENAI_API_KEY': 'OpenAI API Key',
        'ANTHROPIC_API_KEY': 'Anthropic API Key'
    }
    
    all_good = True
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {description}: {'*' * min(len(value), 20)}...")
        else:
            print(f"   ❌ {description}: NOT SET")
            all_good = False
    
    # Check optional variables
    llm_providers = 0
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {description}: {'*' * min(len(value), 20)}...")
            llm_providers += 1
        else:
            print(f"   ⚠️ {description}: NOT SET (optional)")
    
    if llm_providers == 0:
        print("   ⚠️ No LLM provider API keys found - resume processing will be limited")
        all_good = False
    
    return all_good

async def check_aws_connectivity():
    """Test AWS S3 connectivity and permissions."""
    print("☁️ Testing AWS S3 Connectivity...")
    
    try:
        from app.core.s3 import S3Client
        
        s3_client = S3Client()
        
        # Test bucket access
        print("   - Bucket access: ", end="")
        try:
            bucket_exists = await s3_client.check_bucket_exists()
            if bucket_exists:
                print("✅")
            else:
                print("❌ (Bucket not accessible)")
                return False
        except Exception as e:
            print(f"❌ ({e})")
            return False
        
        # Test list permissions
        print("   - List permissions: ", end="")
        try:
            files = await s3_client.list_files()
            print("✅")
        except Exception as e:
            print(f"❌ ({e})")
            return False
        
        # Test upload permissions (with test file)
        print("   - Upload permissions: ", end="")
        try:
            test_content = b"Health check test file"
            test_filename = "health_check_test.txt"
            upload_result = await s3_client.upload_file_bytes(
                test_content, 
                test_filename,
                content_type="text/plain"
            )
            
            if upload_result and upload_result.get('success'):
                print("✅")
                # Clean up test file
                try:
                    await s3_client.delete_file(test_filename)
                except:
                    pass
            else:
                print("❌ (Upload failed)")
                return False
        except Exception as e:
            print(f"❌ ({e})")
            return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ S3 client import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ S3 connectivity test failed: {e}")
        return False

async def check_mongodb_connectivity():
    """Test MongoDB connectivity."""
    print("🍃 Testing MongoDB Connectivity...")
    
    try:
        from app.core.database import get_database
        
        # Test database connection
        print("   - Database connection: ", end="")
        try:
            db = await get_database()
            if db:
                print("✅")
            else:
                print("❌")
                return False
        except Exception as e:
            print(f"❌ ({e})")
            return False
        
        # Test collection access
        print("   - Collection access: ", end="")
        try:
            collection = db["resumes"]
            # Try to count documents (should work even with 0 documents)
            count = await collection.count_documents({})
            print(f"✅ ({count} documents)")
        except Exception as e:
            print(f"❌ ({e})")
            return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Database import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ MongoDB connectivity test failed: {e}")
        return False

async def check_llm_providers():
    """Test LLM provider connectivity."""
    print("🤖 Testing LLM Providers...")
    
    try:
        from app.services.resume_processing import ResumeProcessingService
        
        service = ResumeProcessingService()
        providers = service.get_available_providers()
        
        if not providers:
            print("   ❌ No LLM providers available")
            return False
        
        for provider, status in providers.items():
            status_icon = "✅" if status else "❌"
            print(f"   - {provider.title()}: {status_icon}")
        
        available_count = sum(1 for status in providers.values() if status)
        if available_count > 0:
            print(f"   ✅ {available_count} provider(s) available")
            return True
        else:
            print("   ❌ No providers are functional")
            return False
            
    except ImportError as e:
        print(f"   ❌ LLM service import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ LLM provider test failed: {e}")
        return False

async def check_file_system():
    """Check file system permissions and directories."""
    print("📁 Checking File System...")
    
    directories_to_check = [
        "logs",
        "uploads/temp",
        "app",
        "tests"
    ]
    
    all_good = True
    
    for directory in directories_to_check:
        dir_path = Path(directory)
        if dir_path.exists():
            if dir_path.is_dir():
                # Test write permissions
                try:
                    test_file = dir_path / "health_check_test.tmp"
                    test_file.write_text("test")
                    test_file.unlink()
                    print(f"   ✅ {directory}: Accessible and writable")
                except Exception as e:
                    print(f"   ❌ {directory}: Not writable ({e})")
                    all_good = False
            else:
                print(f"   ❌ {directory}: Exists but not a directory")
                all_good = False
        else:
            print(f"   ⚠️ {directory}: Does not exist")
            # Try to create it
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ {directory}: Created successfully")
            except Exception as e:
                print(f"   ❌ {directory}: Cannot create ({e})")
                all_good = False
    
    return all_good

async def main():
    """Run comprehensive health check."""
    print("🏥 DuoNova System Health Check")
    print("=" * 50)
    
    checks = []
    
    # Run all health checks
    checks.append(await check_environment_variables())
    checks.append(await check_file_system())
    checks.append(await check_mongodb_connectivity())
    checks.append(await check_aws_connectivity())
    checks.append(await check_llm_providers())
    
    print("\n" + "=" * 50)
    
    # Summary
    passed_checks = sum(1 for check in checks if check)
    total_checks = len(checks)
    
    if all(checks):
        print("🎉 All health checks passed!")
        print("✅ System is ready for operation")
    elif passed_checks > total_checks // 2:
        print(f"⚠️ {passed_checks}/{total_checks} health checks passed")
        print("🔧 Some components need attention but basic functionality should work")
    else:
        print(f"❌ {passed_checks}/{total_checks} health checks passed")
        print("🚨 System has critical issues that need to be resolved")
    
    print(f"\n📊 Health Score: {passed_checks}/{total_checks} ({(passed_checks/total_checks)*100:.1f}%)")
    
    return all(checks)

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
