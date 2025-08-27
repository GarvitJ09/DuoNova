# 🔧 DuoNova Configuration Management Guide

## 🎯 **What Changed**

Your upload_resume API has been upgraded from **manual configuration** to **intelligent automatic selection**! 

### Before (Manual)
```python
POST /upload_resume
{
    "file": resume.pdf,
    "level": "mid",
    "processing_mode": "hybrid",      # User had to choose
    "llm_provider": "openai"          # User had to choose
}
```

### After (Intelligent)
```python
POST /upload_resume
{
    "file": resume.pdf,
    "level": "mid"
    # System automatically selects optimal processing!
}
```

## 🚀 **How to Change Processing Types & Models**

You now have **5 easy ways** to control processing configuration:

### 1. 🎯 **Quick Presets** (Easiest)
```bash
# Speed Optimized (Fast & Cheap)
python scripts/config_manager.py preset speed

# Accuracy Optimized (Best Quality)  
python scripts/config_manager.py preset accuracy

# Cost Optimized (Minimize API costs)
python scripts/config_manager.py preset cost

# Development (Balanced for testing)
python scripts/config_manager.py preset dev

# Production (Reliable for production)
python scripts/config_manager.py preset prod
```

### 2. 🎮 **Interactive Menu**
```bash
python scripts/config_manager.py
```
This opens a user-friendly menu where you can:
- View current configuration
- Apply presets
- Change individual settings  
- Test configuration

### 3. ⚡ **Command Line** (Quick Changes)
```bash
# Change processing mode
python scripts/config_manager.py set mode hybrid
python scripts/config_manager.py set mode complete_llm

# Change provider priority
python scripts/config_manager.py set providers groq,openai,anthropic
python scripts/config_manager.py set providers openai,anthropic,groq

# Enable/disable cost optimization
python scripts/config_manager.py set cost true
python scripts/config_manager.py set cost false

# Enable/disable auto fallback
python scripts/config_manager.py set fallback true
```

### 4. 📝 **Environment Variables** (Permanent)
Add to your `.env` file:
```env
# Processing Configuration
DEFAULT_PROCESSING_MODE=hybrid              # or complete_llm
PROVIDER_PRIORITY=groq,openai,anthropic     # comma-separated priority
ENABLE_COST_OPTIMIZATION=true              # true/false
ENABLE_AUTO_FALLBACK=true                   # true/false
```

### 5. 🚀 **API Endpoints** (Runtime Info)
```bash
# Check current configuration
GET /intelligent_processing_info

# See what would be used for a specific file
POST /explain_file_processing
```

## 🤖 **How Intelligent Selection Works**

The system automatically chooses optimal processing based on:

### 📄 **File Characteristics**
- **PDF files** → Complete LLM (better OCR)
- **DOCX files** → Hybrid (library extraction works well)
- **Large files (>5MB)** → Complete LLM (better context handling)
- **Small files** → Hybrid (faster, cheaper)

### 🎯 **Selection Examples**
```
small_resume.docx (500KB)  → hybrid + groq      (fast extraction)
large_resume.pdf (6MB)     → complete_llm + openai (better OCR)  
simple_resume.txt (50KB)   → hybrid + groq      (quick processing)
complex_resume.pdf (2MB)   → complete_llm + openai (layout understanding)
```

### 💰 **Cost Optimization**
- **ON** → Prefer: groq → openai → anthropic (cheapest first)
- **OFF** → Prefer: openai → anthropic → groq (best quality first)

## 📊 **Configuration Options Explained**

### 🔄 **Processing Modes**
| Mode | Description | Best For | Speed | Cost |
|------|-------------|----------|--------|------|
| `hybrid` | Library + LLM | Standard resumes, cost optimization | ⚡ Fast | 💰 Low |
| `complete_llm` | Direct file → LLM | Complex layouts, best accuracy | 🐌 Slower | 💸 Higher |

### 🤖 **LLM Providers**
| Provider | Strengths | Best For | Cost Tier |
|----------|-----------|----------|-----------|
| `groq` | Speed, free tier | Text processing, hybrid mode | 🆓 Free |
| `openai` | File upload, accuracy | PDF processing, complete LLM | 💸 Premium |
| `anthropic` | Large context, detailed | Complex analysis, large docs | 💸 Premium |

## 🔧 **Common Configuration Scenarios**

### 🏃 **Quick Setup Commands**
```bash
# For development/testing
python scripts/config_manager.py preset dev

# For production (best quality)
python scripts/config_manager.py preset prod  

# For cost-conscious usage
python scripts/config_manager.py preset cost

# For maximum speed
python scripts/config_manager.py preset speed

# For best accuracy
python scripts/config_manager.py preset accuracy
```

### 📊 **Check What's Happening**
```bash
# View current configuration
python scripts/config_manager.py show

# Test with sample files
python scripts/config_manager.py test

# See configuration demo
python configuration_demo.py
```

## 🎯 **Example Workflows**

### Scenario 1: Cost-Conscious Startup
```bash
python scripts/config_manager.py preset cost
# Result: Uses groq (free), hybrid mode (cheaper), cost optimization ON
```

### Scenario 2: High-Accuracy Enterprise
```bash  
python scripts/config_manager.py preset accuracy
# Result: Uses openai (best), complete LLM mode, cost optimization OFF
```

### Scenario 3: Development Testing
```bash
python scripts/config_manager.py preset dev
# Result: Balanced settings, auto fallback enabled, good for testing
```

### Scenario 4: Custom Setup
```bash
python scripts/config_manager.py set mode complete_llm
python scripts/config_manager.py set providers openai,groq
python scripts/config_manager.py set cost false
# Result: Custom configuration for specific needs
```

## 🔍 **Monitoring & Debugging**

### Check API Response
The upload response now includes intelligent selection info:
```json
{
  "status": "success",
  "intelligent_processing": {
    "processing_mode": "complete_llm",
    "llm_provider_used": "openai", 
    "selection_reasoning": "Rule-based: PDF files often need OCR capabilities",
    "auto_selected": true
  },
  "processing_note": "Mode: complete_llm | Provider: openai (intelligently auto-selected)"
}
```

### Test Configuration
```bash
# Run comprehensive test
python scripts/config_manager.py test

# Or check via API
GET /intelligent_processing_info
```

## 🎉 **Benefits of New System**

✅ **Simplified API** - Users just upload, no technical decisions  
✅ **Intelligent Selection** - Optimal processing based on file characteristics  
✅ **Cost Optimization** - Automatic use of cost-effective providers  
✅ **Performance** - Speed vs accuracy trade-offs handled automatically  
✅ **Easy Configuration** - Multiple ways to customize behavior  
✅ **Fallback Support** - Graceful handling of provider failures  

## 🚀 **Next Steps**

1. **Try it out:**
   ```bash
   python scripts/config_manager.py preset dev
   python scripts/config_manager.py test
   ```

2. **Upload a file and see automatic selection in action**

3. **Customize for your needs using presets or individual settings**

4. **Monitor performance and adjust configuration as needed**

---

**🎯 Remember: No more manual configuration needed! The system intelligently chooses the best processing for each file automatically.**
