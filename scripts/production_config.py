#!/usr/bin/env python3
"""
Production Configuration Manager
Secure configuration management for production environments.
"""

import os
import sys
import requests
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import time

class ProductionConfigManager:
    """Production-ready configuration manager with security and logging."""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("CONFIG_API_KEY")
        self.session = requests.Session()
        
        # Set up headers for authentication
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log configuration changes for audit trail."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "user": os.getenv("USER", "unknown")
        }
        
        # Log to file for audit trail
        log_file = Path("config_changes.log")
        with open(log_file, "a") as f:
            f.write(f"{json.dumps(log_entry)}\n")
        
        print(f"[{timestamp}] {action}: {details}")
    
    def switch_processing_mode(self, mode: str) -> bool:
        """Switch processing mode in production."""
        valid_modes = ["hybrid", "complete_llm"]
        if mode not in valid_modes:
            print(f"❌ Invalid mode. Valid options: {', '.join(valid_modes)}")
            return False
        
        try:
            # Method 1: Environment variable (immediate effect)
            old_mode = os.getenv("DEFAULT_PROCESSING_MODE", "hybrid")
            os.environ["DEFAULT_PROCESSING_MODE"] = mode
            
            # Method 2: API call (if server is running)
            if self._is_server_running():
                response = self.session.post(
                    f"{self.base_url}/api/v1/admin/update_config",
                    json={"processing_mode": mode},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_action("processing_mode_change", {
                        "old_mode": old_mode,
                        "new_mode": mode,
                        "method": "api",
                        "status": "success"
                    })
                    print(f"✅ Processing mode changed: {old_mode} → {mode}")
                    return True
                else:
                    print(f"❌ API call failed: {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                # Server not running - environment variable change will take effect on restart
                self.log_action("processing_mode_change", {
                    "old_mode": old_mode,
                    "new_mode": mode,
                    "method": "environment",
                    "status": "pending_restart"
                })
                print(f"✅ Processing mode set to: {mode}")
                print("💡 Change will take effect when server restarts")
                return True
                
        except Exception as e:
            self.log_action("processing_mode_change", {
                "mode": mode,
                "error": str(e),
                "status": "failed"
            })
            print(f"❌ Failed to change processing mode: {e}")
            return False
    
    def apply_production_preset(self, environment: str = "prod") -> bool:
        """Apply production-optimized preset."""
        presets = {
            "prod": {
                "processing_mode": "complete_llm",
                "provider_priority": "openai,anthropic,groq",
                "cost_optimization": False,
                "auto_fallback": True,
                "description": "Production: High accuracy, reliable processing"
            },
            "staging": {
                "processing_mode": "hybrid",
                "provider_priority": "groq,openai,anthropic",
                "cost_optimization": True,
                "auto_fallback": True,
                "description": "Staging: Balanced speed and accuracy"
            },
            "dev": {
                "processing_mode": "hybrid", 
                "provider_priority": "groq,openai",
                "cost_optimization": True,
                "auto_fallback": True,
                "description": "Development: Fast iteration"
            }
        }
        
        if environment not in presets:
            print(f"❌ Invalid environment. Valid options: {', '.join(presets.keys())}")
            return False
        
        preset = presets[environment]
        
        try:
            # Apply environment variables
            os.environ["DEFAULT_PROCESSING_MODE"] = preset["processing_mode"]
            os.environ["PROVIDER_PRIORITY"] = preset["provider_priority"]
            os.environ["ENABLE_COST_OPTIMIZATION"] = str(preset["cost_optimization"]).lower()
            os.environ["ENABLE_AUTO_FALLBACK"] = str(preset["auto_fallback"]).lower()
            
            # Apply via API if server is running
            if self._is_server_running():
                response = self.session.post(
                    f"{self.base_url}/api/v1/admin/apply_preset",
                    json={"preset": environment},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_action("preset_applied", {
                        "environment": environment,
                        "preset": preset,
                        "method": "api",
                        "status": "success"
                    })
                    print(f"✅ {environment.upper()} preset applied successfully")
                    print(f"📋 {preset['description']}")
                    return True
            else:
                self.log_action("preset_applied", {
                    "environment": environment,
                    "preset": preset,
                    "method": "environment", 
                    "status": "pending_restart"
                })
                print(f"✅ {environment.upper()} preset configured")
                print(f"📋 {preset['description']}")
                print("💡 Changes will take effect when server restarts")
                return True
                
        except Exception as e:
            self.log_action("preset_application", {
                "environment": environment,
                "error": str(e),
                "status": "failed"
            })
            print(f"❌ Failed to apply {environment} preset: {e}")
            return False
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current configuration status."""
        try:
            # Check environment variables
            env_config = {
                "processing_mode": os.getenv("DEFAULT_PROCESSING_MODE", "hybrid"),
                "provider_priority": os.getenv("PROVIDER_PRIORITY", "groq,openai,anthropic"),
                "cost_optimization": os.getenv("ENABLE_COST_OPTIMIZATION", "true"),
                "auto_fallback": os.getenv("ENABLE_AUTO_FALLBACK", "true")
            }
            
            # Check server status
            server_status = "running" if self._is_server_running() else "stopped"
            
            # Get API status if server is running
            api_config = None
            if server_status == "running":
                try:
                    response = self.session.get(
                        f"{self.base_url}/api/v1/admin/current_config",
                        timeout=5
                    )
                    if response.status_code == 200:
                        api_config = response.json()
                except:
                    pass
            
            return {
                "server_status": server_status,
                "environment_config": env_config,
                "api_config": api_config,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _is_server_running(self) -> bool:
        """Check if the server is running."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def emergency_reset(self):
        """Emergency reset to safe defaults."""
        safe_defaults = {
            "DEFAULT_PROCESSING_MODE": "hybrid",
            "PROVIDER_PRIORITY": "groq,openai,anthropic", 
            "ENABLE_COST_OPTIMIZATION": "true",
            "ENABLE_AUTO_FALLBACK": "true"
        }
        
        print("🚨 Performing emergency reset to safe defaults...")
        
        for key, value in safe_defaults.items():
            os.environ[key] = value
        
        self.log_action("emergency_reset", {
            "defaults": safe_defaults,
            "reason": "manual_reset"
        })
        
        print("✅ Emergency reset completed")
        print("🔄 Restart server to apply changes")

def main():
    parser = argparse.ArgumentParser(description="Production Configuration Manager")
    parser.add_argument("action", choices=[
        "switch-mode", "apply-preset", "status", "emergency-reset"
    ], help="Action to perform")
    parser.add_argument("--mode", choices=["hybrid", "complete_llm"], 
                       help="Processing mode for switch-mode action")
    parser.add_argument("--environment", choices=["prod", "staging", "dev"],
                       default="prod", help="Environment preset to apply")
    parser.add_argument("--api-url", help="API base URL")
    parser.add_argument("--api-key", help="API key for authentication")
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = ProductionConfigManager(
        base_url=args.api_url,
        api_key=args.api_key
    )
    
    if args.action == "switch-mode":
        if not args.mode:
            print("❌ --mode required for switch-mode action")
            sys.exit(1)
        manager.switch_processing_mode(args.mode)
        
    elif args.action == "apply-preset":
        manager.apply_production_preset(args.environment)
        
    elif args.action == "status":
        status = manager.get_current_status()
        print(json.dumps(status, indent=2))
        
    elif args.action == "emergency-reset":
        manager.emergency_reset()

if __name__ == "__main__":
    main()
