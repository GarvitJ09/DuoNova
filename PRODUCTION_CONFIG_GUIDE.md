# Production Configuration Setup Guide

## 🏭 Production Processing Method Switching

### **Step 1: Environment Setup**

#### Set up environment variables (required):
```powershell
# Windows Production Server
$env:CONFIG_API_KEY = "your-secure-api-key-here"
$env:API_BASE_URL = "https://your-production-domain.com"
$env:DEFAULT_PROCESSING_MODE = "complete_llm"
$env:PROVIDER_PRIORITY = "openai,anthropic,groq"
$env:ENABLE_COST_OPTIMIZATION = "false"
$env:ENABLE_AUTO_FALLBACK = "true"
```

```bash
# Linux Production Server
export CONFIG_API_KEY="your-secure-api-key-here"
export API_BASE_URL="https://your-production-domain.com"
export DEFAULT_PROCESSING_MODE="complete_llm"
export PROVIDER_PRIORITY="openai,anthropic,groq"
export ENABLE_COST_OPTIMIZATION="false"
export ENABLE_AUTO_FALLBACK="true"
```

### **Step 2: Production Switching Methods**

#### **Method 1: Secure API Calls (Recommended)**

```bash
# Switch to hybrid mode for faster processing
curl -X POST "https://your-domain.com/api/v1/admin/update_config" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-secure-api-key" \
     -d '{"processing_mode": "hybrid"}'

# Switch to complete LLM for highest accuracy  
curl -X POST "https://your-domain.com/api/v1/admin/update_config" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-secure-api-key" \
     -d '{"processing_mode": "complete_llm"}'

# Apply production preset
curl -X POST "https://your-domain.com/api/v1/admin/apply_preset" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-secure-api-key" \
     -d '{"preset": "prod"}'
```

#### **Method 2: Production Management Script**

```bash
# Switch processing mode
python scripts/production_config.py switch-mode --mode hybrid
python scripts/production_config.py switch-mode --mode complete_llm

# Apply environment-specific presets
python scripts/production_config.py apply-preset --environment prod
python scripts/production_config.py apply-preset --environment staging

# Check current status
python scripts/production_config.py status

# Emergency reset to safe defaults
python scripts/production_config.py emergency-reset
```

#### **Method 3: Infrastructure as Code (IaC)**

**Docker Environment Variables:**
```dockerfile
ENV DEFAULT_PROCESSING_MODE=complete_llm
ENV PROVIDER_PRIORITY=openai,anthropic,groq
ENV ENABLE_COST_OPTIMIZATION=false
ENV ENABLE_AUTO_FALLBACK=true
```

**Kubernetes ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: duonova-config
data:
  DEFAULT_PROCESSING_MODE: "complete_llm"
  PROVIDER_PRIORITY: "openai,anthropic,groq"
  ENABLE_COST_OPTIMIZATION: "false"
  ENABLE_AUTO_FALLBACK: "true"
```

**AWS Parameter Store:**
```bash
aws ssm put-parameter \
    --name "/duonova/processing/mode" \
    --value "complete_llm" \
    --type "String" \
    --overwrite

aws ssm put-parameter \
    --name "/duonova/processing/provider_priority" \
    --value "openai,anthropic,groq" \
    --type "String" \
    --overwrite
```

### **Step 3: Production Deployment Scenarios**

#### **Scenario 1: High Traffic Period (Switch to Speed)**
```bash
# Switch to hybrid mode for faster processing
python scripts/production_config.py switch-mode --mode hybrid

# Or via API
curl -X POST "https://your-domain.com/api/v1/admin/update_config" \
     -H "X-API-Key: $CONFIG_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"processing_mode": "hybrid", "provider_priority": "groq,openai,anthropic"}'
```

#### **Scenario 2: Quality-Critical Period (Switch to Accuracy)**
```bash
# Switch to complete LLM for highest accuracy
python scripts/production_config.py switch-mode --mode complete_llm

# Apply accuracy-focused settings
curl -X POST "https://your-domain.com/api/v1/admin/apply_preset" \
     -H "X-API-Key: $CONFIG_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"preset": "accuracy"}'
```

#### **Scenario 3: Cost Optimization Period**
```bash
# Apply cost-optimized preset
python scripts/production_config.py apply-preset --environment staging

# Or manual cost optimization
curl -X POST "https://your-domain.com/api/v1/admin/update_config" \
     -H "X-API-Key: $CONFIG_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "processing_mode": "hybrid",
       "provider_priority": "groq,openai,anthropic",
       "cost_optimization": true
     }'
```

### **Step 4: Production Monitoring**

#### **Health Checks:**
```bash
# Check server health
curl -X GET "https://your-domain.com/health"

# Check configuration status
curl -X GET "https://your-domain.com/api/v1/admin/current_config" \
     -H "X-API-Key: $CONFIG_API_KEY"

# Test current configuration
curl -X POST "https://your-domain.com/api/v1/admin/test_config" \
     -H "X-API-Key: $CONFIG_API_KEY"
```

#### **Automated Monitoring Script:**
```bash
#!/bin/bash
# production_monitor.sh

while true; do
    echo "$(date): Checking production configuration..."
    
    # Get current status
    STATUS=$(python scripts/production_config.py status)
    echo "$STATUS"
    
    # Log to monitoring system
    echo "$STATUS" >> /var/log/duonova/config_status.log
    
    sleep 300  # Check every 5 minutes
done
```

### **Step 5: Rollback Procedures**

#### **Quick Rollback:**
```bash
# Emergency reset to safe defaults
python scripts/production_config.py emergency-reset

# Or restore specific previous configuration
export DEFAULT_PROCESSING_MODE=hybrid
export PROVIDER_PRIORITY=groq,openai,anthropic
export ENABLE_COST_OPTIMIZATION=true
```

#### **Gradual Rollback:**
```bash
# Step 1: Switch to safe mode
curl -X POST "https://your-domain.com/api/v1/admin/update_config" \
     -H "X-API-Key: $CONFIG_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"processing_mode": "hybrid"}'

# Step 2: Test the change
curl -X POST "https://your-domain.com/api/v1/admin/test_config" \
     -H "X-API-Key: $CONFIG_API_KEY"

# Step 3: Apply full rollback if test passes
python scripts/production_config.py apply-preset --environment prod
```

### **Step 6: Security Best Practices**

#### **API Key Management:**
```bash
# Generate secure API key
openssl rand -hex 32

# Store securely (example with AWS Secrets Manager)
aws secretsmanager create-secret \
    --name duonova/config-api-key \
    --secret-string "your-generated-api-key"

# Use in application
export CONFIG_API_KEY=$(aws secretsmanager get-secret-value \
    --secret-id duonova/config-api-key \
    --query SecretString --output text)
```

#### **Access Control:**
```bash
# Restrict API access by IP
# Add to your reverse proxy/load balancer configuration
location /api/v1/admin/ {
    allow 10.0.0.0/8;    # Internal network only
    allow 192.168.0.0/16; # Internal network only
    deny all;
    proxy_pass http://backend;
}
```

### **Step 7: Audit and Logging**

All configuration changes are logged to `config_changes.log`:
```json
{
  "timestamp": "2025-08-27 14:30:00",
  "action": "processing_mode_change", 
  "details": {
    "old_mode": "hybrid",
    "new_mode": "complete_llm",
    "method": "api"
  },
  "user": "admin"
}
```

### **Production Switching Summary:**

| Method | Use Case | Security | Audit Trail |
|--------|----------|-----------|-------------|
| API Calls | Real-time changes | ✅ API Key Auth | ✅ Full logging |
| Environment Variables | Server restart scenarios | ✅ OS-level security | ✅ Change tracking |
| IaC (Docker/K8s) | Deployment automation | ✅ Platform security | ✅ Version control |
| Management Script | Operational tasks | ✅ Key-based auth | ✅ Detailed logs |

**🔒 Security Features:**
- API key authentication
- Request rate limiting  
- IP-based access control
- Audit logging
- Emergency reset capability

**📊 Monitoring Features:**
- Real-time status checking
- Configuration validation
- Provider availability testing
- Performance impact tracking
