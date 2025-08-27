#!/usr/bin/env python3
"""
Configuration Management Script for DuoNova
Easy way to view and change processing configuration.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.config.processing_config import ProcessingConfig, ConfigPresets
from app.services.processing_selection import ProcessingSelectionService

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🔧 {title}")
    print("=" * 60)

def print_section(title):
    """Print a section header."""
    print(f"\n📋 {title}")
    print("-" * 40)

def show_current_configuration():
    """Display current configuration."""
    print_header("Current Configuration")
    ProcessingConfig.print_configuration()

def show_available_presets():
    """Show available configuration presets."""
    print_section("Available Configuration Presets")
    
    presets = {
        "speed": ("Speed Optimized", ConfigPresets.SPEED_OPTIMIZED),
        "accuracy": ("Accuracy Optimized", ConfigPresets.ACCURACY_OPTIMIZED),
        "cost": ("Cost Optimized", ConfigPresets.COST_OPTIMIZED),
        "dev": ("Development", ConfigPresets.DEVELOPMENT),
        "prod": ("Production", ConfigPresets.PRODUCTION)
    }
    
    for key, (name, config) in presets.items():
        print(f"\n🎯 {name} ({key}):")
        for setting, value in config.items():
            print(f"   {setting}: {value}")

def apply_preset(preset_name: str):
    """Apply a configuration preset."""
    presets = {
        "speed": ConfigPresets.SPEED_OPTIMIZED,
        "accuracy": ConfigPresets.ACCURACY_OPTIMIZED,
        "cost": ConfigPresets.COST_OPTIMIZED,
        "dev": ConfigPresets.DEVELOPMENT,
        "prod": ConfigPresets.PRODUCTION
    }
    
    if preset_name not in presets:
        print(f"❌ Unknown preset: {preset_name}")
        print(f"Available presets: {', '.join(presets.keys())}")
        return False
    
    preset = presets[preset_name]
    
    print(f"🔄 Applying {preset_name} preset...")
    
    # Apply to environment (for current session)
    for key, value in preset.items():
        os.environ[key] = value
        print(f"   ✅ {key} = {value}")
    
    print(f"\n✅ Preset '{preset_name}' applied for current session!")
    print("💡 To make permanent, add these to your .env file:")
    
    for key, value in preset.items():
        print(f"   {key}={value}")
    
    return True

def test_configuration():
    """Test current configuration with sample files."""
    print_header("Configuration Testing")
    
    try:
        service = ProcessingSelectionService()
        results = service.test_configuration()
        
        print("📊 Test Results:")
        for file_name, result in results["test_results"].items():
            if result["success"]:
                print(f"   ✅ {file_name}: {result['mode']} + {result['provider']}")
                print(f"      💡 {result['reasoning']}")
            else:
                print(f"   ❌ {file_name}: {result['error']}")
        
        print(f"\n🤖 Available Providers:")
        for provider, available in results["available_providers"].items():
            status = "✅" if available else "❌"
            print(f"   {status} {provider}")
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")

def change_setting(setting_name: str, setting_value: str):
    """Change a specific configuration setting."""
    valid_settings = {
        "mode": "DEFAULT_PROCESSING_MODE",
        "providers": "PROVIDER_PRIORITY", 
        "cost": "ENABLE_COST_OPTIMIZATION",
        "fallback": "ENABLE_AUTO_FALLBACK"
    }
    
    if setting_name not in valid_settings:
        print(f"❌ Unknown setting: {setting_name}")
        print(f"Available settings: {', '.join(valid_settings.keys())}")
        return False
    
    env_key = valid_settings[setting_name]
    
    # Validate values
    if setting_name == "mode" and setting_value not in ["hybrid", "complete_llm"]:
        print(f"❌ Invalid mode: {setting_value}. Use 'hybrid' or 'complete_llm'")
        return False
    
    if setting_name == "providers":
        valid_providers = ["groq", "openai", "anthropic", "auto"]
        providers = [p.strip() for p in setting_value.split(",")]
        for provider in providers:
            if provider not in valid_providers:
                print(f"❌ Invalid provider: {provider}. Use: {', '.join(valid_providers)}")
                return False
    
    if setting_name in ["cost", "fallback"] and setting_value not in ["true", "false"]:
        print(f"❌ Invalid boolean: {setting_value}. Use 'true' or 'false'")
        return False
    
    # Apply setting
    os.environ[env_key] = setting_value
    print(f"✅ {env_key} = {setting_value}")
    print("💡 Add to .env file to make permanent:")
    print(f"   {env_key}={setting_value}")
    
    return True

def interactive_menu():
    """Interactive configuration menu."""
    while True:
        print_header("DuoNova Configuration Manager")
        print("1. Show current configuration")
        print("2. Show available presets") 
        print("3. Apply preset")
        print("4. Change specific setting")
        print("5. Test configuration")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            show_current_configuration()
        
        elif choice == "2":
            show_available_presets()
        
        elif choice == "3":
            print("\nAvailable presets: speed, accuracy, cost, dev, prod")
            preset = input("Enter preset name: ").strip().lower()
            apply_preset(preset)
        
        elif choice == "4":
            print("\nAvailable settings:")
            print("  mode - Processing mode (hybrid/complete_llm)")
            print("  providers - Provider priority (comma-separated)")
            print("  cost - Cost optimization (true/false)")
            print("  fallback - Auto fallback (true/false)")
            
            setting = input("Enter setting name: ").strip().lower()
            value = input("Enter setting value: ").strip()
            change_setting(setting, value)
        
        elif choice == "5":
            test_configuration()
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-6.")
        
        input("\nPress Enter to continue...")

def main():
    """Main function with command line argument support."""
    if len(sys.argv) == 1:
        # No arguments, show interactive menu
        interactive_menu()
    
    elif len(sys.argv) == 2:
        command = sys.argv[1].lower()
        
        if command == "show":
            show_current_configuration()
        elif command == "presets":
            show_available_presets()
        elif command == "test":
            test_configuration()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: show, presets, test")
    
    elif len(sys.argv) == 3:
        command = sys.argv[1].lower()
        
        if command == "preset":
            apply_preset(sys.argv[2])
        else:
            print(f"❌ Unknown command: {command}")
    
    elif len(sys.argv) == 4:
        command = sys.argv[1].lower()
        
        if command == "set":
            change_setting(sys.argv[2], sys.argv[3])
        else:
            print(f"❌ Unknown command: {command}")
    
    else:
        print("❌ Too many arguments")
        print("\nUsage:")
        print("  python config_manager.py                    # Interactive menu")
        print("  python config_manager.py show               # Show current config")
        print("  python config_manager.py presets            # Show presets")
        print("  python config_manager.py test               # Test configuration")
        print("  python config_manager.py preset <name>      # Apply preset")
        print("  python config_manager.py set <key> <value>  # Change setting")

if __name__ == "__main__":
    main()
