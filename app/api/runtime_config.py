#!/usr/bin/env python3
"""
Runtime Configuration API Endpoints
Allows changing processing configuration via API calls.
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel
import os
import re

def update_env_file(key: str, value: str):
    """
    Update or add a key-value pair in the .env file.
    """
    env_file_path = ".env"
    
    # Read current .env file
    try:
        with open(env_file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    
    # Find and update existing key or add new one
    key_updated = False
    updated_lines = []
    
    for line in lines:
        # Skip empty lines and comments
        if line.strip() == '' or line.strip().startswith('#'):
            updated_lines.append(line)
            continue
            
        # Check if this line contains our key
        if '=' in line:
            env_key = line.split('=')[0].strip()
            if env_key == key:
                updated_lines.append(f"{key}={value}\n")
                key_updated = True
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    # Add new key if it wasn't found
    if not key_updated:
        # Add to processing configuration section or at the end
        processing_section_found = False
        for i, line in enumerate(updated_lines):
            if "# Processing Configuration" in line:
                processing_section_found = True
                # Insert after this section header
                updated_lines.insert(i + 1, f"{key}={value}\n")
                break
        
        if not processing_section_found:
            # Add processing section and the key
            updated_lines.extend([
                "\n# Processing Configuration\n",
                f"{key}={value}\n"
            ])
    
    # Write back to .env file
    with open(env_file_path, 'w') as f:
        f.writelines(updated_lines)

# Import authentication for production
try:
    from ..core.auth import verify_admin_token, verify_api_key
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False
    # Fallback for development - no auth required
    def verify_admin_token():
        return True
    def verify_api_key():
        return True

router = APIRouter(prefix="/admin", tags=["configuration"])

class ConfigUpdateRequest(BaseModel):
    """Request model for configuration updates."""
    processing_mode: Optional[Literal["hybrid", "complete_llm"]] = None
    provider_priority: Optional[str] = None  # comma-separated
    cost_optimization: Optional[bool] = None
    auto_fallback: Optional[bool] = None

class PresetRequest(BaseModel):
    """Request model for applying presets."""
    preset: Literal["speed", "accuracy", "cost", "dev", "prod"]

@router.post("/update_config")
async def update_runtime_config(
    config: ConfigUpdateRequest,
    auth: bool = Depends(verify_api_key)
):
    """
    Update processing configuration at runtime.
    Changes take effect immediately for new file uploads.
    """
    try:
        changes_made = []
        
        # Update processing mode
        if config.processing_mode:
            os.environ['DEFAULT_PROCESSING_MODE'] = config.processing_mode
            update_env_file('DEFAULT_PROCESSING_MODE', config.processing_mode)
            changes_made.append(f"processing_mode → {config.processing_mode}")
        
        # Update provider priority
        if config.provider_priority:
            # Validate providers
            valid_providers = ['groq', 'openai', 'anthropic', 'auto']
            providers = [p.strip().lower() for p in config.provider_priority.split(',')]
            
            for provider in providers:
                if provider not in valid_providers:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid provider '{provider}'. Valid options: {', '.join(valid_providers)}"
                    )
            
            os.environ['PROVIDER_PRIORITY'] = config.provider_priority.lower()
            update_env_file('PROVIDER_PRIORITY', config.provider_priority.lower())
            changes_made.append(f"provider_priority → {config.provider_priority}")
        
        # Update cost optimization
        if config.cost_optimization is not None:
            os.environ['ENABLE_COST_OPTIMIZATION'] = str(config.cost_optimization).lower()
            update_env_file('ENABLE_COST_OPTIMIZATION', str(config.cost_optimization).lower())
            changes_made.append(f"cost_optimization → {config.cost_optimization}")
        
        # Update auto fallback
        if config.auto_fallback is not None:
            os.environ['ENABLE_AUTO_FALLBACK'] = str(config.auto_fallback).lower()
            update_env_file('ENABLE_AUTO_FALLBACK', str(config.auto_fallback).lower())
            changes_made.append(f"auto_fallback → {config.auto_fallback}")
        
        if not changes_made:
            raise HTTPException(status_code=400, detail="No configuration changes provided")
        
        return {
            "status": "success",
            "message": "Configuration updated successfully",
            "changes": changes_made,
            "note": "Changes take effect immediately for new uploads and are persisted to .env file"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")

@router.post("/apply_preset")
async def apply_configuration_preset(preset_request: PresetRequest):
    """
    Apply a configuration preset at runtime.
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
    
    try:
        preset_config = presets[preset_request.preset]
        
        # Apply all preset settings
        changes = []
        for key, value in preset_config.items():
            os.environ[key] = value
            changes.append(f"{key} → {value}")
        
        return {
            "status": "success",
            "message": f"{preset_request.preset.title()} preset applied successfully",
            "preset": preset_request.preset,
            "changes": changes,
            "note": "Configuration changes take effect immediately"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preset application failed: {str(e)}")

@router.get("/current_config")
async def get_current_runtime_config():
    """
    Get current runtime configuration.
    """
    try:
        from ..config.processing_config import ProcessingConfig
        from ..services.processing_selection import ProcessingSelectionService
        
        # Get current configuration
        config = ProcessingConfig()
        current_config = config.get_current_config()
        
        # Get provider availability
        try:
            selection_service = ProcessingSelectionService()
            test_results = selection_service.test_configuration()
            available_providers = test_results.get("available_providers", {})
        except Exception as e:
            available_providers = {"error": f"Could not check providers: {str(e)}"}
        
        # Get environment variables
        env_config = {
            'DEFAULT_PROCESSING_MODE': os.getenv('DEFAULT_PROCESSING_MODE', 'hybrid'),
            'PROVIDER_PRIORITY': os.getenv('PROVIDER_PRIORITY', 'groq,openai,anthropic'),
            'ENABLE_COST_OPTIMIZATION': os.getenv('ENABLE_COST_OPTIMIZATION', 'true'),
            'ENABLE_AUTO_FALLBACK': os.getenv('ENABLE_AUTO_FALLBACK', 'true')
        }
        
        return {
            "status": "success",
            "runtime_config": current_config,
            "environment_variables": env_config,
            "available_providers": available_providers,
            "update_methods": {
                "api": "POST /admin/update_config",
                "preset": "POST /admin/apply_preset",
                "script": "python scripts/runtime_config.py"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get configuration: {str(e)}")

@router.post("/test_config")
async def test_runtime_configuration():
    """
    Test current runtime configuration with sample files.
    """
    try:
        from ..services.processing_selection import ProcessingSelectionService
        
        selection_service = ProcessingSelectionService()
        test_results = selection_service.test_configuration()
        
        return {
            "status": "success",
            "message": "Configuration test completed",
            "test_results": test_results["test_results"],
            "configuration": test_results["configuration"],
            "available_providers": test_results["available_providers"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration test failed: {str(e)}")

@router.post("/force_provider/{provider}")
async def force_provider_for_session(
    provider: Literal["groq", "openai", "anthropic"],
    request: Request
):
    """
    Force a specific provider for the current session (temporary override).
    This creates a session-specific override that lasts until server restart.
    """
    try:
        # Store in a session-specific way (you might want to use Redis or similar for production)
        session_id = request.headers.get("session-id", "default")
        
        # For demonstration, we'll use environment variables with session prefix
        session_key = f"SESSION_{session_id}_FORCED_PROVIDER"
        os.environ[session_key] = provider
        
        return {
            "status": "success",
            "message": f"Provider '{provider}' forced for session {session_id}",
            "provider": provider,
            "session_id": session_id,
            "note": "This override lasts until server restart"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to force provider: {str(e)}")

@router.delete("/clear_session_overrides")
async def clear_session_overrides(request: Request):
    """
    Clear any session-specific configuration overrides.
    """
    try:
        session_id = request.headers.get("session-id", "default")
        session_keys = [key for key in os.environ.keys() if key.startswith(f"SESSION_{session_id}_")]
        
        cleared = []
        for key in session_keys:
            value = os.environ.pop(key, None)
            if value:
                cleared.append(key)
        
        return {
            "status": "success",
            "message": f"Cleared {len(cleared)} session overrides",
            "cleared_keys": cleared,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear overrides: {str(e)}")
