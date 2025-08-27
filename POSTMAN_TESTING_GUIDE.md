# Postman Collection Testing Guide

## 📋 **Updated Postman Collection Overview**

The complete Postman collection includes **6 main folders** with **25+ endpoints** for comprehensive testing of the DuoNova ATS Checker runtime configuration system.

## 🚀 **Quick Setup Instructions**

### **1. Import Collection & Environment**

1. **Import Collection:**
   - Open Postman
   - Click **Import** 
   - Select `postman_collection.json`

2. **Import Environment:**
   - Click **Import**
   - Select `postman_environment.json`
   - Select the "DuoNova ATS Checker Environment"

3. **Configure Variables:**
   - Click the **Environment** dropdown
   - Select "DuoNova ATS Checker Environment"
   - Update variables:
     - `base_url`: `http://localhost:8000`
     - `api_key`: `your-secure-api-key` (optional for development)

### **2. Start Your Server**
```bash
python main.py
```

## 📁 **Collection Structure**

### **📋 Health & Status**
- ✅ Health Check
- ✅ API Root Info

### **🔧 Configuration Management**
- ✅ Get Current Configuration
- ✅ Update Configuration - Processing Mode
- ✅ Update Configuration - Complete LLM Mode
- ✅ Update Configuration - Provider Priority  
- ✅ Update Configuration - Multiple Settings
- ✅ Test Current Configuration

### **📋 Configuration Presets**
- ✅ Apply Speed Preset
- ✅ Apply Accuracy Preset
- ✅ Apply Cost Preset
- ✅ Apply Development Preset
- ✅ Apply Production Preset

### **🎛️ Session Management**
- ✅ Force Provider - Groq
- ✅ Force Provider - OpenAI
- ✅ Force Provider - Anthropic
- ✅ Clear Session Overrides

### **📄 Resume Processing**
- ✅ Get Processing Options
- ✅ Get Intelligent Processing Info
- ✅ Test Processing Switches
- ✅ Upload Resume - Intelligent Processing

### **🧪 Testing Workflows**
- ✅ Full Speed Test Workflow (3 steps)
- ✅ Full Accuracy Test Workflow (3 steps)
- ✅ Runtime Configuration Demo (5 steps)

## 🧪 **Recommended Testing Workflows**

### **Workflow 1: Basic Configuration Testing**

1. **Health Check**
   ```
   GET {{base_url}}/health
   Expected: 200 OK with {"status": "healthy"}
   ```

2. **Get Current Configuration**
   ```
   GET {{base_url}}/api/v1/admin/current_config
   Expected: Current settings and provider status
   ```

3. **Apply Speed Preset**
   ```
   POST {{base_url}}/api/v1/admin/apply_preset
   Body: {"preset": "speed"}
   Expected: Speed configuration applied
   ```

4. **Verify Configuration Change**
   ```
   GET {{base_url}}/api/v1/admin/current_config
   Expected: Updated settings reflecting speed preset
   ```

### **Workflow 2: Runtime Switching Demo**

1. **Switch to Hybrid Mode**
   ```
   POST {{base_url}}/api/v1/admin/update_config
   Body: {"processing_mode": "hybrid"}
   Expected: Mode changed to hybrid
   ```

2. **Upload Resume (Hybrid Mode)**
   ```
   POST {{base_url}}/api/v1/upload_resume
   Form-data: resume=file, level=mid
   Expected: Fast processing with hybrid selection
   ```

3. **Switch to Complete LLM Mode**
   ```
   POST {{base_url}}/api/v1/admin/update_config
   Body: {"processing_mode": "complete_llm"}
   Expected: Mode changed to complete_llm
   ```

4. **Upload Same Resume (Complete LLM Mode)**
   ```
   POST {{base_url}}/api/v1/upload_resume
   Form-data: resume=file, level=mid
   Expected: Accurate processing with complete LLM
   ```

### **Workflow 3: Provider Testing**

1. **Force Groq Provider**
   ```
   POST {{base_url}}/api/v1/admin/force_provider/groq
   Headers: session-id: test-session-123
   Expected: Groq forced for session
   ```

2. **Upload Resume (Forced Groq)**
   ```
   POST {{base_url}}/api/v1/upload_resume
   Headers: session-id: test-session-123
   Expected: Processing uses Groq provider
   ```

3. **Clear Session Override**
   ```
   DELETE {{base_url}}/api/v1/admin/clear_session_overrides
   Headers: session-id: test-session-123
   Expected: Session overrides cleared
   ```

## 🎯 **Key Test Scenarios**

### **Test 1: Speed vs Accuracy Comparison**

```bash
# Run in Postman Runner or manually:

1. Apply Speed Preset
2. Upload resume → Note processing time and provider
3. Apply Accuracy Preset  
4. Upload same resume → Compare results and timing
```

### **Test 2: Provider Fallback Testing**

```bash
# Test automatic provider fallback:

1. Set provider priority: "groq,openai,anthropic"
2. Force provider unavailable (mock scenario)
3. Upload resume → Verify fallback to next provider
```

### **Test 3: Configuration Persistence**

```bash
# Test that configuration persists:

1. Apply production preset
2. Get current config → Note settings
3. Restart server (python main.py)
4. Get current config → Verify settings persist
```

## 📊 **Expected Response Examples**

### **Configuration Update Response:**
```json
{
  "status": "success",
  "message": "Configuration updated successfully",
  "changes": [
    "processing_mode → complete_llm",
    "provider_priority → openai,anthropic,groq"
  ],
  "note": "Changes take effect immediately for new uploads"
}
```

### **Upload Resume Response:**
```json
{
  "status": "success",
  "message": "Resume processed successfully with intelligent selection",
  "processing_details": {
    "selected_mode": "hybrid",
    "selected_provider": "groq",
    "selection_reasoning": "Small PDF file, hybrid mode for speed",
    "processing_time": "1.2s"
  },
  "resume_data": {
    "personal_info": {...},
    "skills": [...],
    "experience": [...]
  }
}
```

## 🔍 **Debugging Tips**

### **Common Issues:**

1. **Server Not Running:**
   ```
   Error: Could not connect to localhost:8000
   Solution: Run `python main.py`
   ```

2. **Authentication Errors:**
   ```
   Error: 401 Unauthorized
   Solution: Check X-API-Key header or disable authentication for development
   ```

3. **File Upload Issues:**
   ```
   Error: 415 Unsupported Media Type
   Solution: Ensure file is PDF or DOCX format
   ```

### **Postman Console Debugging:**

1. Open **Postman Console** (View → Show Postman Console)
2. Run requests to see detailed logs
3. Check response times and error details

### **Server-Side Debugging:**

1. Check server terminal for processing logs
2. Look for selection reasoning messages
3. Monitor configuration change confirmations

## 🎪 **Advanced Testing Features**

### **1. Environment Switching:**
```bash
# Switch between environments:
- Development: localhost:8000
- Staging: staging.your-domain.com  
- Production: your-production-domain.com
```

### **2. Automated Test Scripts:**
The collection includes automatic tests for:
- ✅ Response time validation
- ✅ Content type checking
- ✅ Error response logging
- ✅ Status code verification

### **3. Pre-request Scripts:**
- ✅ Dynamic timestamp generation
- ✅ Session ID management
- ✅ Environment variable setup

## 🏆 **Best Practices**

1. **Always start with Health Check** to verify server status
2. **Use workflows** for comprehensive testing scenarios  
3. **Check current configuration** before making changes
4. **Test with different file types** (PDF, DOCX, small, large)
5. **Verify configuration persistence** after server restarts
6. **Use session management** for testing user-specific overrides
7. **Monitor processing times** to validate performance changes

## 📝 **Test Checklist**

- [ ] Health check passes
- [ ] Current configuration retrieval works
- [ ] Speed preset applies correctly
- [ ] Accuracy preset applies correctly
- [ ] Configuration updates work
- [ ] Provider forcing works
- [ ] Session overrides clear properly
- [ ] Resume upload with hybrid mode works
- [ ] Resume upload with complete LLM mode works
- [ ] Configuration changes affect processing selection
- [ ] Provider fallback works when providers unavailable
- [ ] Test configuration endpoint validates setup

The updated Postman collection provides comprehensive testing capabilities for all runtime configuration features! 🚀
