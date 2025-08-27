# Runtime Configuration Guide

## Overview

This guide explains how to change processing types and models **at runtime** without restarting the server. The configuration system supports multiple methods for live updates.

## Quick Start

### 1. Check Current Configuration

**Via API:**
```bash
curl -X GET "http://localhost:8000/api/v1/admin/current_config"
```

**Via Script:**
```bash
python scripts/runtime_config.py status
```

### 2. Change Processing Mode

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/v1/admin/update_config" \
     -H "Content-Type: application/json" \
     -d '{"processing_mode": "complete_llm"}'
```

**Via Script:**
```bash
python scripts/runtime_config.py change-mode complete_llm
```

**Via Environment Variable:**
```bash
export DEFAULT_PROCESSING_MODE=complete_llm
```

### 3. Change Provider Priority

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/v1/admin/update_config" \
     -H "Content-Type: application/json" \
     -d '{"provider_priority": "openai,anthropic,groq"}'
```

**Via Script:**
```bash
python scripts/runtime_config.py change-priority openai,anthropic,groq
```

## Configuration Methods

### Method 1: API Endpoints

The server provides REST API endpoints for runtime configuration:

#### Available Endpoints:

- `GET /api/v1/admin/current_config` - Get current configuration
- `POST /api/v1/admin/update_config` - Update specific settings
- `POST /api/v1/admin/apply_preset` - Apply configuration presets
- `POST /api/v1/admin/test_config` - Test current configuration
- `POST /api/v1/admin/force_provider/{provider}` - Force specific provider

#### Update Configuration:
```bash
curl -X POST "http://localhost:8000/api/v1/admin/update_config" \
     -H "Content-Type: application/json" \
     -d '{
       "processing_mode": "hybrid",
       "provider_priority": "groq,openai,anthropic",
       "cost_optimization": true,
       "auto_fallback": true
     }'
```

#### Apply Preset:
```bash
curl -X POST "http://localhost:8000/api/v1/admin/apply_preset" \
     -H "Content-Type: application/json" \
     -d '{"preset": "speed"}'
```

### Method 2: Runtime Configuration Script

Use the interactive script for easy configuration management:

```bash
# Interactive menu
python scripts/runtime_config.py interactive

# Direct commands
python scripts/runtime_config.py status
python scripts/runtime_config.py change-mode hybrid
python scripts/runtime_config.py change-priority groq,openai
python scripts/runtime_config.py preset speed
python scripts/runtime_config.py toggle-cost-optimization
python scripts/runtime_config.py toggle-auto-fallback
```

### Method 3: Environment Variables

Directly modify environment variables for immediate effect:

```bash
# Windows PowerShell
$env:DEFAULT_PROCESSING_MODE = "complete_llm"
$env:PROVIDER_PRIORITY = "openai,anthropic,groq"
$env:ENABLE_COST_OPTIMIZATION = "false"
$env:ENABLE_AUTO_FALLBACK = "true"

# Linux/Mac
export DEFAULT_PROCESSING_MODE=complete_llm
export PROVIDER_PRIORITY=openai,anthropic,groq
export ENABLE_COST_OPTIMIZATION=false
export ENABLE_AUTO_FALLBACK=true
```

### Method 4: Configuration Presets

Apply pre-configured settings for common scenarios:

#### Available Presets:

**Speed Preset** (fastest processing):
```bash
python scripts/runtime_config.py preset speed
# OR
curl -X POST "http://localhost:8000/api/v1/admin/apply_preset" \
     -H "Content-Type: application/json" \
     -d '{"preset": "speed"}'
```

**Accuracy Preset** (highest accuracy):
```bash
python scripts/runtime_config.py preset accuracy
```

**Cost Preset** (lowest cost):
```bash
python scripts/runtime_config.py preset cost
```

**Development Preset**:
```bash
python scripts/runtime_config.py preset dev
```

**Production Preset**:
```bash
python scripts/runtime_config.py preset prod
```

## Configuration Options

### Processing Modes

- `hybrid` - Uses library extraction + LLM enhancement (faster, cost-effective)
- `complete_llm` - Uses full LLM processing (more accurate, slower)

### Provider Priority

Set the order of LLM providers to try:
- `groq,openai,anthropic` - Try Groq first (fastest)
- `openai,anthropic,groq` - Try OpenAI first (balanced)
- `anthropic,openai,groq` - Try Anthropic first

### Cost Optimization

- `true` - Enable cost-saving measures
- `false` - Disable cost optimization for maximum quality

### Auto Fallback

- `true` - Automatically try next provider if current fails
- `false` - Fail immediately if primary provider fails

## Real-Time Testing

### Test Current Configuration

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/v1/admin/test_config"
```

**Via Script:**
```bash
python scripts/runtime_config.py test
```

### Monitor Configuration Changes

Run the comprehensive demo to see all methods in action:
```bash
python runtime_configuration_demo.py
```

## Session-Specific Overrides

Force a specific provider for a particular session:

```bash
curl -X POST "http://localhost:8000/api/v1/admin/force_provider/groq" \
     -H "session-id: my-session-123"
```

Clear session overrides:
```bash
curl -X DELETE "http://localhost:8000/api/v1/admin/clear_session_overrides" \
     -H "session-id: my-session-123"
```

## Best Practices

### 1. Development Workflow
```bash
# Start with speed preset for development
python scripts/runtime_config.py preset dev

# Test with sample files
python scripts/runtime_config.py test

# Switch to accuracy for final testing
python scripts/runtime_config.py preset accuracy
```

### 2. Production Deployment
```bash
# Use production preset
python scripts/runtime_config.py preset prod

# Monitor configuration
curl -X GET "http://localhost:8000/api/v1/admin/current_config"

# Test periodically
curl -X POST "http://localhost:8000/api/v1/admin/test_config"
```

### 3. Troubleshooting
```bash
# Check provider availability
python scripts/runtime_config.py test

# Force a working provider
curl -X POST "http://localhost:8000/api/v1/admin/force_provider/groq"

# Reset to defaults
python scripts/runtime_config.py preset dev
```

## Important Notes

- ✅ **No server restart required** - All changes take effect immediately
- ✅ **Changes apply to new uploads** - Existing processing continues with old config
- ✅ **Multiple update methods** - Choose the most convenient method
- ✅ **Configuration persistence** - Settings persist through environment variables
- ✅ **Fallback system** - Automatic provider fallback prevents failures
- ✅ **Real-time testing** - Test configuration changes immediately

## Troubleshooting

### Server Not Responding
```bash
# Check if server is running
curl -X GET "http://localhost:8000/health"

# Start server if needed
python main.py
```

### Configuration Not Taking Effect
```bash
# Verify environment variables
python scripts/runtime_config.py status

# Test configuration
python scripts/runtime_config.py test

# Apply known good preset
python scripts/runtime_config.py preset speed
```

### Provider Issues
```bash
# Check provider availability
curl -X POST "http://localhost:8000/api/v1/admin/test_config"

# Force working provider
python scripts/runtime_config.py change-priority groq,openai
```

---

**Need help?** Run the interactive configuration menu:
```bash
python scripts/runtime_config.py interactive
```
