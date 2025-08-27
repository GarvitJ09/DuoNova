#!/usr/bin/env python3
"""
DuoNova Comprehensive Test Runner
Executes all test suites in organized modules with detailed reporting.
"""

import asyncio
import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

async def run_unit_tests():
    """Run all unit tests."""
    print("📋 Unit Tests")
    print("-" * 20)
    
    unit_tests = [
        "tests/unit/test_s3_client.py",
        "tests/unit/test_processing_switches.py", 
        "tests/unit/test_mongodb_connection.py"
    ]
    
    results = []
    for test_file in unit_tests:
        if Path(test_file).exists():
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=30)
                success = result.returncode == 0
                results.append(success)
                
                if success:
                    print(f"✅ {test_file.split('/')[-1]}")
                else:
                    print(f"❌ {test_file.split('/')[-1]}")
                    if result.stderr:
                        print(f"   Error: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file.split('/')[-1]} (timeout)")
                results.append(False)
            except Exception as e:
                print(f"❌ {test_file.split('/')[-1]} ({e})")
                results.append(False)
        else:
            print(f"⚠️ {test_file.split('/')[-1]} (not found)")
            results.append(False)
    
    return results

async def run_integration_tests():
    """Run all integration tests."""
    print("\n⚙️ Integration Tests")
    print("-" * 25)
    
    integration_tests = [
        "tests/integration/test_s3_upload_flow.py",
        "tests/integration/test_resume_processing.py"
    ]
    
    results = []
    for test_file in integration_tests:
        if Path(test_file).exists():
            try:
                result = subprocess.run([sys.executable, test_file],
                                      capture_output=True, text=True, timeout=60)
                success = result.returncode == 0
                results.append(success)
                
                if success:
                    print(f"✅ {test_file.split('/')[-1]}")
                else:
                    print(f"❌ {test_file.split('/')[-1]}")
                    if result.stderr:
                        print(f"   Error: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file.split('/')[-1]} (timeout)")
                results.append(False)
            except Exception as e:
                print(f"❌ {test_file.split('/')[-1]} ({e})")
                results.append(False)
        else:
            print(f"⚠️ {test_file.split('/')[-1]} (not found)")
            results.append(False)
    
    return results

async def run_api_tests():
    """Run all API tests."""
    print("\n🚀 API Tests")
    print("-" * 15)
    
    api_tests = [
        "tests/api/test_resume_endpoints.py",
        "tests/api/test_s3_endpoints.py"
    ]
    
    results = []
    for test_file in api_tests:
        if Path(test_file).exists():
            try:
                result = subprocess.run([sys.executable, test_file],
                                      capture_output=True, text=True, timeout=45)
                success = result.returncode == 0
                results.append(success)
                
                if success:
                    print(f"✅ {test_file.split('/')[-1]}")
                else:
                    print(f"❌ {test_file.split('/')[-1]}")
                    if result.stderr:
                        print(f"   Error: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file.split('/')[-1]} (timeout)")
                results.append(False)
            except Exception as e:
                print(f"❌ {test_file.split('/')[-1]} ({e})")
                results.append(False)
        else:
            print(f"⚠️ {test_file.split('/')[-1]} (not found)")
            results.append(False)
    
    return results

async def run_diagnostic_checks():
    """Run system diagnostic checks."""
    print("\n🏥 System Health Checks")
    print("-" * 25)
    
    diagnostic_script = "scripts/diagnostics/system_health_check.py"
    
    if Path(diagnostic_script).exists():
        try:
            print("🔍 Running comprehensive health check...")
            result = subprocess.run([sys.executable, diagnostic_script],
                                  capture_output=True, text=True, timeout=120)
            success = result.returncode == 0
            
            if success:
                print("✅ System health check passed")
                # Print summary from health check
                lines = result.stdout.split('\n')
                for line in lines:
                    if '🎉' in line or '⚠️' in line or '❌' in line or '📊' in line:
                        print(f"   {line}")
            else:
                print("❌ System health check failed")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
            
            return [success]
            
        except subprocess.TimeoutExpired:
            print("⏰ System health check timeout")
            return [False]
        except Exception as e:
            print(f"❌ System health check error: {e}")
            return [False]
    else:
        print(f"⚠️ Health check script not found")
        return [False]

async def main():
    """Run comprehensive test suite."""
    print("🧪 Running DuoNova Test Suite")
    print("=" * 50)
    
    # Run all test categories
    unit_results = await run_unit_tests()
    integration_results = await run_integration_tests()
    api_results = await run_api_tests()
    diagnostic_results = await run_diagnostic_checks()
    
    # Calculate summary
    all_results = unit_results + integration_results + api_results + diagnostic_results
    passed_tests = sum(1 for result in all_results if result)
    total_tests = len(all_results)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("-" * 15)
    
    # Category summaries
    unit_passed = sum(unit_results)
    unit_total = len(unit_results)
    print(f"📋 Unit Tests: {unit_passed}/{unit_total}")
    
    integration_passed = sum(integration_results)
    integration_total = len(integration_results)
    print(f"⚙️ Integration Tests: {integration_passed}/{integration_total}")
    
    api_passed = sum(api_results)
    api_total = len(api_results)
    print(f"🚀 API Tests: {api_passed}/{api_total}")
    
    diagnostic_passed = sum(diagnostic_results)
    diagnostic_total = len(diagnostic_results)
    print(f"🏥 Health Checks: {diagnostic_passed}/{diagnostic_total}")
    
    print("-" * 15)
    
    # Overall result
    if passed_tests == total_tests:
        print(f"✅ All test suites passed ({passed_tests}/{total_tests})")
        print("🎉 Test run completed successfully!")
        return True
    elif passed_tests > total_tests // 2:
        print(f"⚠️ Partial success ({passed_tests}/{total_tests})")
        print("🔧 Some components need attention")
        return False
    else:
        print(f"❌ Multiple test failures ({passed_tests}/{total_tests})")
        print("🚨 Critical issues need to be resolved")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
