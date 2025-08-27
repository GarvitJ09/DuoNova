#!/usr/bin/env python3
"""
Intelligent Processing Selection Service
Handles automatic selection of processing modes and LLM providers based on configuration.
"""

from typing import Dict, Any, Tuple, Optional
from app.config.processing_config import ProcessingConfig, ProcessingMode, LLMProvider, ProcessingRule
from app.services.resume_processing import ResumeProcessingService

class ProcessingSelectionService:
    """
    Service that intelligently selects processing mode and LLM provider
    based on file characteristics and configuration rules.
    """
    
    def __init__(self):
        self.config = ProcessingConfig()
        self.resume_service = ResumeProcessingService()
    
    def select_processing_strategy(
        self, 
        file_name: str, 
        file_size_bytes: int,
        user_level: str = "mid"
    ) -> Tuple[ProcessingMode, LLMProvider, str]:
        """
        Select the optimal processing strategy based on file characteristics.
        
        Args:
            file_name: Name of the uploaded file
            file_size_bytes: Size of the file in bytes
            user_level: User experience level (entry, mid, senior)
            
        Returns:
            Tuple of (processing_mode, selected_provider, reasoning)
        """
        print(f"🤖 Selecting processing strategy for {file_name} ({file_size_bytes} bytes)")
        
        # Step 1: Check if rules should be applied or if explicit config takes precedence
        explicit_config_mode = self.config.get_default_processing_mode()
        
        # Check if user has explicitly configured processing mode via environment
        import os
        has_explicit_config = os.getenv("DEFAULT_PROCESSING_MODE") is not None
        
        if has_explicit_config:
            # Respect explicit configuration - don't apply automatic rules
            selected_mode = explicit_config_mode
            preferred_providers = self.config.get_provider_priority()
            reasoning = f"Explicit configuration: {selected_mode.value} mode (rules bypassed)"
            print(f"⚙️ Using explicit configuration: {selected_mode.value} mode")
        else:
            # Apply automatic rules for intelligent selection
            applicable_rule = self.config.evaluate_file_rules(file_name, file_size_bytes)
            
            if applicable_rule:
                # Use rule-based selection
                selected_mode = applicable_rule.mode
                preferred_providers = applicable_rule.preferred_providers
                reasoning = f"Rule-based: {applicable_rule.description}"
            else:
                # Use default configuration
                selected_mode = explicit_config_mode
                preferred_providers = self.config.get_provider_priority()
                reasoning = "Default configuration applied"
        
        # Step 2: Select available provider from preferred list
        available_providers = self.resume_service.get_available_providers()
        selected_provider = self._select_best_provider(
            preferred_providers, 
            available_providers, 
            selected_mode
        )
        
        # Step 3: Apply cost optimization if enabled
        if self.config.is_cost_optimization_enabled():
            selected_provider, cost_reasoning = self._apply_cost_optimization(
                selected_provider, 
                available_providers, 
                selected_mode
            )
            reasoning += f" | {cost_reasoning}"
        
        print(f"✅ Selected: {selected_mode.value} mode with {selected_provider.value} provider")
        print(f"💡 Reasoning: {reasoning}")
        
        return selected_mode, selected_provider, reasoning
    
    def _select_best_provider(
        self, 
        preferred_providers: list, 
        available_providers: Dict[str, bool],
        processing_mode: ProcessingMode
    ) -> LLMProvider:
        """Select the best available provider from preferred list."""
        
        # Filter to only available providers
        available_preferred = []
        for provider in preferred_providers:
            provider_key = provider.value if hasattr(provider, 'value') else str(provider)
            if provider_key in available_providers and available_providers[provider_key]:
                available_preferred.append(provider)
        
        if not available_preferred:
            # Fallback to any available provider
            for provider_key, is_available in available_providers.items():
                if is_available:
                    try:
                        return LLMProvider(provider_key)
                    except ValueError:
                        continue
            
            raise Exception("No LLM providers are currently available")
        
        # Return the highest priority available provider
        return available_preferred[0]
    
    def _apply_cost_optimization(
        self, 
        current_provider: LLMProvider, 
        available_providers: Dict[str, bool],
        processing_mode: ProcessingMode
    ) -> Tuple[LLMProvider, str]:
        """Apply cost optimization rules."""
        
        provider_configs = self.config.PROVIDER_CONFIGS
        current_cost_tier = provider_configs[current_provider]["cost_tier"]
        
        # If current provider is already free/low cost, keep it
        if current_cost_tier == "free":
            return current_provider, "Already using cost-effective provider"
        
        # Look for cheaper alternatives that are available
        for provider, config in provider_configs.items():
            provider_key = provider.value
            if (provider_key in available_providers and 
                available_providers[provider_key] and 
                config["cost_tier"] == "free"):
                
                # Check if cheaper provider is suitable for the mode
                if processing_mode == ProcessingMode.HYBRID or "text_processing" in config["strengths"]:
                    return provider, f"Cost optimization: switched to {config['name']}"
        
        return current_provider, "No cost-effective alternatives available"
    
    def get_processing_explanation(
        self, 
        file_name: str, 
        file_size_bytes: int
    ) -> Dict[str, Any]:
        """
        Get detailed explanation of why certain processing options were chosen.
        """
        mode, provider, reasoning = self.select_processing_strategy(file_name, file_size_bytes)
        
        # Get provider capabilities
        provider_config = self.config.PROVIDER_CONFIGS[provider]
        
        # Check what rules were applied
        applicable_rule = self.config.evaluate_file_rules(file_name, file_size_bytes)
        
        return {
            "selected_strategy": {
                "processing_mode": mode.value,
                "llm_provider": provider.value,
                "provider_name": provider_config["name"]
            },
            "reasoning": reasoning,
            "rule_applied": {
                "name": "file_characteristics" if applicable_rule else "default",
                "description": applicable_rule.description if applicable_rule else "No specific rule matched, using defaults"
            },
            "provider_capabilities": {
                "strengths": provider_config["strengths"],
                "best_for": provider_config["best_for"],
                "cost_tier": provider_config["cost_tier"]
            },
            "file_analysis": {
                "name": file_name,
                "size_mb": round(file_size_bytes / (1024 * 1024), 2),
                "extension": file_name.split('.')[-1].lower(),
                "estimated_complexity": self._estimate_file_complexity(file_name, file_size_bytes)
            },
            "configuration": {
                "cost_optimization": self.config.is_cost_optimization_enabled(),
                "auto_fallback": self.config.is_auto_fallback_enabled(),
                "default_mode": self.config.get_default_processing_mode().value
            }
        }
    
    def _estimate_file_complexity(self, file_name: str, file_size_bytes: int) -> str:
        """Estimate file complexity based on size and type."""
        size_mb = file_size_bytes / (1024 * 1024)
        extension = file_name.split('.')[-1].lower()
        
        if size_mb > 5:
            return "high"
        elif size_mb > 2:
            return "medium"
        elif extension == "pdf":
            return "medium"  # PDFs often have complex layouts
        else:
            return "low"
    
    def test_configuration(self) -> Dict[str, Any]:
        """Test current configuration with sample files."""
        test_files = [
            ("small_resume.docx", 1024 * 500),  # 500KB DOCX
            ("large_resume.pdf", 1024 * 1024 * 6),  # 6MB PDF
            ("simple_resume.txt", 1024 * 50),  # 50KB TXT
            ("complex_resume.pdf", 1024 * 1024 * 2),  # 2MB PDF
        ]
        
        results = {}
        for file_name, file_size in test_files:
            try:
                mode, provider, reasoning = self.select_processing_strategy(file_name, file_size)
                results[file_name] = {
                    "mode": mode.value,
                    "provider": provider.value,
                    "reasoning": reasoning,
                    "success": True
                }
            except Exception as e:
                results[file_name] = {
                    "error": str(e),
                    "success": False
                }
        
        return {
            "test_results": results,
            "configuration": self.config.get_current_config(),
            "available_providers": self.resume_service.get_available_providers()
        }
