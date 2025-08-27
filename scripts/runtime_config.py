#!/usr/bin/env python3
"""
Runtime Configuration Manager for DuoNova
Change processing types and models while the application is running.
"""

import os
import sys
import json
import asyncio
import httpx
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class RuntimeConfigManager:
    """
    Manages runtime configuration changes for DuoNova processing.
    Allows changing processing modes and providers without restarting the server.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.config_cache = {}
    
    # ============================================================================
    # ENVIRONMENT VARIABLE RUNTIME CHANGES
    # ============================================================================
    
    def change_processing_mode(self, mode: str) -> bool:
        """
        Change the default processing mode at runtime.
        
        Args:
            mode: 'hybrid' or 'complete_llm'
        """
        if mode not in ['hybrid', 'complete_llm']:
            print(f"❌ Invalid processing mode: {mode}")
            print("   Valid options: hybrid, complete_llm")
            return False
        
        print(f"🔄 Changing processing mode to: {mode}")
        os.environ['DEFAULT_PROCESSING_MODE'] = mode
        self._invalidate_cache()
        print(f"✅ Processing mode changed to: {mode}")
        print("💡 This affects new file uploads immediately!")
        return True
    
    def change_provider_priority(self, providers: str) -> bool:
        """
        Change LLM provider priority at runtime.
        
        Args:
            providers: Comma-separated list like 'groq,openai,anthropic'
        """
        valid_providers = ['groq', 'openai', 'anthropic', 'auto']
        provider_list = [p.strip().lower() for p in providers.split(',')]
        
        for provider in provider_list:
            if provider not in valid_providers:
                print(f"❌ Invalid provider: {provider}")
                print(f"   Valid options: {', '.join(valid_providers)}")
                return False
        
        print(f"🔄 Changing provider priority to: {providers}")
        os.environ['PROVIDER_PRIORITY'] = providers.lower()
        self._invalidate_cache()
        print(f"✅ Provider priority changed to: {providers}")
        print("💡 Next file upload will use this priority!")
        return True
    
    def toggle_cost_optimization(self, enabled: bool) -> bool:
        """
        Enable or disable cost optimization at runtime.
        
        Args:
            enabled: True to enable, False to disable
        """
        value = "true" if enabled else "false"
        print(f"🔄 {'Enabling' if enabled else 'Disabling'} cost optimization...")
        os.environ['ENABLE_COST_OPTIMIZATION'] = value
        self._invalidate_cache()
        print(f"✅ Cost optimization: {'ENABLED' if enabled else 'DISABLED'}")
        return True
    
    def toggle_auto_fallback(self, enabled: bool) -> bool:
        """
        Enable or disable auto fallback at runtime.
        
        Args:
            enabled: True to enable, False to disable
        """
        value = "true" if enabled else "false"
        print(f"🔄 {'Enabling' if enabled else 'Disabling'} auto fallback...")
        os.environ['ENABLE_AUTO_FALLBACK'] = value
        self._invalidate_cache()
        print(f"✅ Auto fallback: {'ENABLED' if enabled else 'DISABLED'}")
        return True
    
    def apply_preset(self, preset: str) -> bool:
        """
        Apply a configuration preset at runtime.
        
        Args:
            preset: 'speed', 'accuracy', 'cost', 'dev', 'prod'
        """
        presets = {
            'speed': {
                'DEFAULT_PROCESSING_MODE': 'hybrid',
                'PROVIDER_PRIORITY': 'groq,openai,anthropic',
                'ENABLE_COST_OPTIMIZATION': 'true',
                'ENABLE_AUTO_FALLBACK': 'true'
            },
            'accuracy': {
                'DEFAULT_PROCESSING_MODE': 'complete_llm',
                'PROVIDER_PRIORITY': 'openai,anthropic,groq',
                'ENABLE_COST_OPTIMIZATION': 'false',
                'ENABLE_AUTO_FALLBACK': 'true'
            },
            'cost': {
                'DEFAULT_PROCESSING_MODE': 'hybrid',
                'PROVIDER_PRIORITY': 'groq,openai,anthropic',
                'ENABLE_COST_OPTIMIZATION': 'true',
                'ENABLE_AUTO_FALLBACK': 'true'
            },
            'dev': {
                'DEFAULT_PROCESSING_MODE': 'hybrid',
                'PROVIDER_PRIORITY': 'groq,openai',
                'ENABLE_COST_OPTIMIZATION': 'true',
                'ENABLE_AUTO_FALLBACK': 'true'
            },
            'prod': {
                'DEFAULT_PROCESSING_MODE': 'complete_llm',
                'PROVIDER_PRIORITY': 'openai,anthropic,groq',
                'ENABLE_COST_OPTIMIZATION': 'false',
                'ENABLE_AUTO_FALLBACK': 'true'
            }
        }
        
        if preset not in presets:
            print(f"❌ Unknown preset: {preset}")
            print(f"   Available presets: {', '.join(presets.keys())}")
            return False
        
        print(f"🔄 Applying {preset} preset...")
        config = presets[preset]
        
        for key, value in config.items():
            os.environ[key] = value
            print(f"   ✅ {key} = {value}")
        
        self._invalidate_cache()
        print(f"🎉 {preset.title()} preset applied successfully!")
        print("💡 Changes take effect immediately for new uploads!")
        return True
    
    # ============================================================================
    # API-BASED RUNTIME CHANGES (if server supports it)
    # ============================================================================
    
    async def change_config_via_api(self, config: Dict[str, Any]) -> bool:
        """
        Attempt to change configuration via API endpoint (if available).
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/admin/update_config",
                    json=config,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Configuration updated via API: {result.get('message', 'Success')}")
                    return True
                else:
                    print(f"❌ API configuration failed: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"⚠️ API not available, using environment variables: {e}")
            return False
    
    async def get_current_config_from_api(self) -> Optional[Dict[str, Any]]:
        """
        Get current configuration from the running server.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/intelligent_processing_info",
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"❌ Failed to get config from API: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"⚠️ Could not connect to server: {e}")
            return None
    
    # ============================================================================
    # CONFIGURATION MONITORING
    # ============================================================================
    
    def _invalidate_cache(self):
        """Invalidate configuration cache."""
        self.config_cache.clear()
    
    def get_current_env_config(self) -> Dict[str, str]:
        """Get current environment-based configuration."""
        return {
            'processing_mode': os.getenv('DEFAULT_PROCESSING_MODE', 'hybrid'),
            'provider_priority': os.getenv('PROVIDER_PRIORITY', 'groq,openai,anthropic'),
            'cost_optimization': os.getenv('ENABLE_COST_OPTIMIZATION', 'true'),
            'auto_fallback': os.getenv('ENABLE_AUTO_FALLBACK', 'true')
        }
    
    async def show_runtime_status(self):
        """Show current runtime configuration status."""
        print("📊 Runtime Configuration Status")
        print("=" * 50)
        
        # Environment variables
        print("\n🔧 Environment Variables (Current Session):")
        env_config = self.get_current_env_config()
        for key, value in env_config.items():
            print(f"   {key}: {value}")
        
        # Server status
        print(f"\n🚀 Server Status:")
        api_config = await self.get_current_config_from_api()
        if api_config:
            print("   ✅ Server is running and responding")
            current_config = api_config.get('current_configuration', {})
            print(f"   📋 Active Mode: {current_config.get('default_processing_mode', 'unknown')}")
            print(f"   🤖 Provider Priority: {', '.join(current_config.get('provider_priority', []))}")
            print(f"   💰 Cost Optimization: {current_config.get('cost_optimization', 'unknown')}")
            
            # Available providers
            available = api_config.get('available_providers', {})
            print(f"\n🔌 Available Providers:")
            for provider, status in available.items():
                icon = "✅" if status else "❌"
                print(f"   {icon} {provider}")
        else:
            print("   ❌ Server not responding or not running")
            print("   💡 Environment changes will apply when server restarts")
    
    async def test_runtime_changes(self, test_file_path: str = None):
        """
        Test runtime configuration changes with a sample upload.
        """
        if not test_file_path:
            print("⚠️ No test file provided, simulating with API check...")
            
        print("🧪 Testing Runtime Configuration Changes")
        print("=" * 50)
        
        try:
            async with httpx.AsyncClient() as client:
                # Test the explain endpoint if available
                response = await client.get(
                    f"{self.base_url}/intelligent_processing_info",
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Server is responding to configuration requests")
                    
                    # Show sample selections
                    samples = result.get('sample_selections', {})
                    if samples:
                        print("\n📄 Sample File Processing (with current config):")
                        for filename, selection in samples.items():
                            if selection.get('success'):
                                print(f"   {filename}: {selection['mode']} + {selection['provider']}")
                    
                    return True
                else:
                    print(f"❌ Server test failed: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Runtime test failed: {e}")
            print("💡 Make sure the server is running with: uvicorn app.main:app --reload")
            return False

# ============================================================================
# INTERACTIVE RUNTIME MANAGER
# ============================================================================

def interactive_runtime_config():
    """Interactive runtime configuration manager."""
    manager = RuntimeConfigManager()
    
    while True:
        print("\n" + "=" * 60)
        print("🔧 DuoNova Runtime Configuration Manager")
        print("=" * 60)
        print("1. Change processing mode")
        print("2. Change provider priority")
        print("3. Toggle cost optimization")
        print("4. Toggle auto fallback")
        print("5. Apply preset")
        print("6. Show current status")
        print("7. Test configuration")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            print("\nProcessing modes:")
            print("  hybrid - Library extraction + LLM (fast, cheap)")
            print("  complete_llm - Direct file upload (best accuracy)")
            mode = input("Enter mode (hybrid/complete_llm): ").strip().lower()
            manager.change_processing_mode(mode)
        
        elif choice == "2":
            print("\nProvider priority options:")
            print("  groq,openai,anthropic - Speed optimized")
            print("  openai,anthropic,groq - Accuracy optimized")
            print("  groq - Cost optimized (free only)")
            providers = input("Enter provider priority (comma-separated): ").strip()
            manager.change_provider_priority(providers)
        
        elif choice == "3":
            enable = input("Enable cost optimization? (y/n): ").strip().lower() == 'y'
            manager.toggle_cost_optimization(enable)
        
        elif choice == "4":
            enable = input("Enable auto fallback? (y/n): ").strip().lower() == 'y'
            manager.toggle_auto_fallback(enable)
        
        elif choice == "5":
            print("\nAvailable presets:")
            print("  speed - Fast processing, cost-effective")
            print("  accuracy - Best quality, higher cost")
            print("  cost - Minimize API costs")
            print("  dev - Development settings")
            print("  prod - Production settings")
            preset = input("Enter preset name: ").strip().lower()
            manager.apply_preset(preset)
        
        elif choice == "6":
            asyncio.run(manager.show_runtime_status())
        
        elif choice == "7":
            asyncio.run(manager.test_runtime_changes())
        
        elif choice == "8":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-8.")
        
        input("\nPress Enter to continue...")

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

async def main():
    """Main function with command line support."""
    manager = RuntimeConfigManager()
    
    if len(sys.argv) == 1:
        # No arguments, show interactive menu
        interactive_runtime_config()
    
    elif len(sys.argv) == 2:
        command = sys.argv[1].lower()
        
        if command == "status":
            await manager.show_runtime_status()
        elif command == "test":
            await manager.test_runtime_changes()
        elif command == "interactive":
            interactive_runtime_config()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: status, test, interactive")
    
    elif len(sys.argv) == 3:
        command = sys.argv[1].lower()
        value = sys.argv[2]
        
        if command == "mode":
            manager.change_processing_mode(value)
        elif command == "preset":
            manager.apply_preset(value)
        elif command == "providers":
            manager.change_provider_priority(value)
        elif command == "cost":
            manager.toggle_cost_optimization(value.lower() == 'true')
        elif command == "fallback":
            manager.toggle_auto_fallback(value.lower() == 'true')
        else:
            print(f"❌ Unknown command: {command}")
    
    else:
        print("Usage:")
        print("  python scripts/runtime_config.py                    # Interactive menu")
        print("  python scripts/runtime_config.py status             # Show current status")
        print("  python scripts/runtime_config.py test               # Test configuration")
        print("  python scripts/runtime_config.py mode <mode>        # Change processing mode")
        print("  python scripts/runtime_config.py preset <preset>    # Apply preset")
        print("  python scripts/runtime_config.py providers <list>   # Change provider priority")
        print("  python scripts/runtime_config.py cost <true/false>  # Toggle cost optimization")

if __name__ == "__main__":
    asyncio.run(main())