#!/usr/bin/env python3
"""
Processing Configuration for DuoNova Resume Processing
Handles intelligent selection of processing modes and LLM providers.
"""

import os
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass
from enum import Enum

class ProcessingMode(str, Enum):
    """Available processing modes."""
    HYBRID = "hybrid"
    COMPLETE_LLM = "complete_llm"

class LLMProvider(str, Enum):
    """Available LLM providers."""
    AUTO = "auto"
    OPENAI = "openai"
    GROQ = "groq"
    ANTHROPIC = "anthropic"

@dataclass
class ProcessingRule:
    """Configuration rule for processing selection."""
    mode: ProcessingMode
    preferred_providers: List[LLMProvider]
    description: str
    conditions: Dict[str, Any]

class ProcessingConfig:
    """
    Central configuration for processing modes and LLM provider selection.
    
    Configuration hierarchy (highest to lowest priority):
    1. Environment variables
    2. Configuration file settings
    3. Default values
    """
    
    # ============================================================================
    # DEFAULT CONFIGURATION
    # ============================================================================
    
    # Global defaults (can be overridden by environment variables)
    DEFAULT_PROCESSING_MODE = ProcessingMode.HYBRID
    DEFAULT_PROVIDER_PRIORITY = [LLMProvider.GROQ, LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
    
    # ============================================================================
    # INTELLIGENT PROCESSING RULES
    # ============================================================================
    
    PROCESSING_RULES = {
        "large_files": ProcessingRule(
            mode=ProcessingMode.COMPLETE_LLM,
            preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
            description="Large files (>5MB) benefit from direct LLM processing",
            conditions={"file_size_mb": ">5"}
        ),
        
        "pdf_files": ProcessingRule(
            mode=ProcessingMode.COMPLETE_LLM,
            preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
            description="PDF files often need OCR capabilities of advanced LLMs",
            conditions={"file_extension": [".pdf"]}
        ),
        
        "docx_files": ProcessingRule(
            mode=ProcessingMode.HYBRID,
            preferred_providers=[LLMProvider.GROQ, LLMProvider.OPENAI],
            description="DOCX files extract well with libraries, hybrid is efficient",
            conditions={"file_extension": [".docx"]}
        ),
        
        "small_text_files": ProcessingRule(
            mode=ProcessingMode.HYBRID,
            preferred_providers=[LLMProvider.GROQ],
            description="Small text files are perfect for fast hybrid processing",
            conditions={"file_size_mb": "<1", "file_extension": [".txt"]}
        ),
        
        "complex_resumes": ProcessingRule(
            mode=ProcessingMode.COMPLETE_LLM,
            preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
            description="Complex layouts need advanced LLM understanding",
            conditions={"complexity": "high"}
        )
    }
    
    # ============================================================================
    # PROVIDER-SPECIFIC SETTINGS
    # ============================================================================
    
    PROVIDER_CONFIGS = {
        LLMProvider.GROQ: {
            "name": "Groq",
            "strengths": ["speed", "cost_effective", "text_processing"],
            "limitations": ["no_file_upload", "rate_limits"],
            "best_for": ["hybrid_mode", "text_extraction", "quick_processing"],
            "cost_tier": "free"
        },
        
        LLMProvider.OPENAI: {
            "name": "OpenAI GPT-4",
            "strengths": ["file_upload", "comprehensive_analysis", "accuracy"],
            "limitations": ["cost", "rate_limits"],
            "best_for": ["complete_llm", "pdf_processing", "complex_analysis"],
            "cost_tier": "premium"
        },
        
        LLMProvider.ANTHROPIC: {
            "name": "Claude",
            "strengths": ["large_context", "detailed_analysis", "file_upload"],
            "limitations": ["cost", "availability"],
            "best_for": ["complete_llm", "detailed_extraction", "large_documents"],
            "cost_tier": "premium"
        }
    }
    
    # ============================================================================
    # ENVIRONMENT-BASED OVERRIDES
    # ============================================================================
    
    @classmethod
    def get_default_processing_mode(cls) -> ProcessingMode:
        """Get default processing mode from environment or config."""
        env_mode = os.getenv("DEFAULT_PROCESSING_MODE", cls.DEFAULT_PROCESSING_MODE.value)
        try:
            return ProcessingMode(env_mode.lower())
        except ValueError:
            print(f"⚠️ Invalid processing mode in environment: {env_mode}, using default: {cls.DEFAULT_PROCESSING_MODE.value}")
            return cls.DEFAULT_PROCESSING_MODE
    
    @classmethod
    def get_provider_priority(cls) -> List[LLMProvider]:
        """Get provider priority from environment or config."""
        env_priority = os.getenv("PROVIDER_PRIORITY")
        if env_priority:
            try:
                providers = [LLMProvider(p.strip().lower()) for p in env_priority.split(",")]
                return providers
            except ValueError as e:
                print(f"⚠️ Invalid provider in environment priority: {e}, using default")
        
        return cls.DEFAULT_PROVIDER_PRIORITY
    
    @classmethod
    def is_cost_optimization_enabled(cls) -> bool:
        """Check if cost optimization is enabled."""
        return os.getenv("ENABLE_COST_OPTIMIZATION", "true").lower() == "true"
    
    @classmethod
    def is_auto_fallback_enabled(cls) -> bool:
        """Check if automatic fallback between modes is enabled."""
        return os.getenv("ENABLE_AUTO_FALLBACK", "true").lower() == "true"
    
    # ============================================================================
    # RULE EVALUATION METHODS
    # ============================================================================
    
    @classmethod
    def evaluate_file_rules(cls, file_name: str, file_size_bytes: int) -> Optional[ProcessingRule]:
        """
        Evaluate processing rules based on file characteristics.
        
        Args:
            file_name: Name of the file
            file_size_bytes: Size of the file in bytes
            
        Returns:
            ProcessingRule if a rule matches, None otherwise
        """
        file_extension = os.path.splitext(file_name.lower())[1]
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        # Check each rule
        for rule_name, rule in cls.PROCESSING_RULES.items():
            if cls._matches_conditions(rule.conditions, file_extension, file_size_mb):
                print(f"📋 Applied rule '{rule_name}': {rule.description}")
                return rule
        
        return None
    
    @classmethod
    def _matches_conditions(cls, conditions: Dict[str, Any], file_extension: str, file_size_mb: float) -> bool:
        """Check if file matches rule conditions."""
        
        # Check file extension conditions
        if "file_extension" in conditions:
            if file_extension not in conditions["file_extension"]:
                return False
        
        # Check file size conditions
        if "file_size_mb" in conditions:
            size_condition = conditions["file_size_mb"]
            if isinstance(size_condition, str):
                if size_condition.startswith(">"):
                    threshold = float(size_condition[1:])
                    if file_size_mb <= threshold:
                        return False
                elif size_condition.startswith("<"):
                    threshold = float(size_condition[1:])
                    if file_size_mb >= threshold:
                        return False
        
        return True
    
    # ============================================================================
    # CONFIGURATION DISPLAY METHODS
    # ============================================================================
    
    @classmethod
    def get_current_config(cls) -> Dict[str, Any]:
        """Get current configuration summary."""
        return {
            "default_processing_mode": cls.get_default_processing_mode().value,
            "provider_priority": [p.value for p in cls.get_provider_priority()],
            "cost_optimization": cls.is_cost_optimization_enabled(),
            "auto_fallback": cls.is_auto_fallback_enabled(),
            "available_rules": list(cls.PROCESSING_RULES.keys()),
            "provider_configs": {
                provider.value: config["name"] 
                for provider, config in cls.PROVIDER_CONFIGS.items()
            }
        }
    
    @classmethod
    def print_configuration(cls):
        """Print current configuration in a readable format."""
        print("🔧 DuoNova Processing Configuration")
        print("=" * 50)
        
        config = cls.get_current_config()
        
        print(f"📋 Default Processing Mode: {config['default_processing_mode']}")
        print(f"🤖 Provider Priority: {' → '.join(config['provider_priority'])}")
        print(f"💰 Cost Optimization: {'✅' if config['cost_optimization'] else '❌'}")
        print(f"🔄 Auto Fallback: {'✅' if config['auto_fallback'] else '❌'}")
        
        print(f"\n📏 Available Rules:")
        for rule_name, rule in cls.PROCESSING_RULES.items():
            print(f"   • {rule_name}: {rule.description}")
        
        print(f"\n🤖 Provider Capabilities:")
        for provider, config_data in cls.PROVIDER_CONFIGS.items():
            print(f"   • {config_data['name']}: {', '.join(config_data['strengths'])}")

# ============================================================================
# CONFIGURATION PRESETS
# ============================================================================

class ConfigPresets:
    """Predefined configuration presets for different scenarios."""
    
    SPEED_OPTIMIZED = {
        "DEFAULT_PROCESSING_MODE": "hybrid",
        "PROVIDER_PRIORITY": "groq,openai,anthropic",
        "ENABLE_COST_OPTIMIZATION": "true"
    }
    
    ACCURACY_OPTIMIZED = {
        "DEFAULT_PROCESSING_MODE": "complete_llm",
        "PROVIDER_PRIORITY": "openai,anthropic,groq",
        "ENABLE_COST_OPTIMIZATION": "false"
    }
    
    COST_OPTIMIZED = {
        "DEFAULT_PROCESSING_MODE": "hybrid",
        "PROVIDER_PRIORITY": "groq,openai,anthropic",
        "ENABLE_COST_OPTIMIZATION": "true"
    }
    
    DEVELOPMENT = {
        "DEFAULT_PROCESSING_MODE": "hybrid",
        "PROVIDER_PRIORITY": "groq,openai",
        "ENABLE_COST_OPTIMIZATION": "true",
        "ENABLE_AUTO_FALLBACK": "true"
    }
    
    PRODUCTION = {
        "DEFAULT_PROCESSING_MODE": "complete_llm",
        "PROVIDER_PRIORITY": "openai,anthropic,groq",
        "ENABLE_COST_OPTIMIZATION": "false",
        "ENABLE_AUTO_FALLBACK": "true"
    }
