# 🚀 DuoNova Setup Guide

## Prerequisites
- Python 3.12+ (tested with 3.12.10)
- pip (package installer for Python)
- Git
- MongoDB Atlas account (free tier available)
- At least one LLM provider API key (OpenAI or Groq)

## Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd DuoNova
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### 4. Environment Configuration

#### Create .env file
Copy the environment template and configure with your values:
```bash
# Create .env file from template
cp env.template .env
```

#### Required Configuration
Edit `.env` file with your actual values:

**MongoDB (Required)**:
1. Create account at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a free cluster
3. Get connection string and replace in `MONGODB_URL`
4. Set `MONGODB_DATABASE=ats_checker`

**LLM Providers (At least one required)**:

**Option A: OpenAI (Recommended for best accuracy)**
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set `OPENAI_API_KEY=your_actual_key_here`

**Option B: Groq (Recommended for speed/cost)**
1. Get API key from [Groq Console](https://console.groq.com/keys)
2. Set `GROQ_API_KEY=your_actual_key_here`

**AWS S3 (Optional for file storage)**:
1. Get credentials from AWS Console
2. Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### 5. Test Installation
```bash
# Verify setup with automated checker
python verify_setup.py

# If verification passes, start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Verify Setup
Open browser and visit:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 7. Test Resume Upload
You can test the system using:
- Swagger UI at http://localhost:8000/docs
- Postman collection (import `postman_collection.json`)
- Or simple curl command:

```bash
curl -X POST "http://localhost:8000/api/v1/upload_resume" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@your_resume.pdf" \
  -F "level=mid"
```

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. MongoDB Connection Issues**
- Verify connection string in `.env`
- Check network access (whitelist your IP in MongoDB Atlas)
- Ensure database user has proper permissions

**3. LLM Provider Errors**
- Verify API keys are correct and active
- Check rate limits and billing status
- Test with different provider using configuration API

**4. Port Already in Use**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -ti:8000 | xargs kill -9  # macOS/Linux

# Or use different port
uvicorn main:app --reload --port 8001
```

**5. File Upload Issues**
- Ensure files are PDF or DOCX format
- Check file size (10MB limit)
- Verify proper multipart/form-data headers

## Development Setup

### Configuration Management
The system supports runtime configuration changes:

```bash
# Check current configuration
curl http://localhost:8000/api/v1/admin/current_config

# Update processing mode
curl -X POST "http://localhost:8000/api/v1/admin/update_config" \
  -H "Content-Type: application/json" \
  -d '{"processing_mode": "hybrid", "provider_priority": "groq,openai"}'
```

### Running Tests
```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test category
python tests/unit/test_processing_switches.py
```

### Development Server
```bash
# Auto-reload on file changes
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Debug mode with verbose logging
DEBUG=True uvicorn main:app --reload --log-level debug
```

## Production Deployment

### Environment Variables for Production
```bash
DEBUG=False
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_strong_secret_key_here
```

### Performance Recommendations
- Use `DEFAULT_PROCESSING_MODE=hybrid` for cost efficiency
- Set `PROVIDER_PRIORITY=groq,openai` for speed
- Enable `ENABLE_COST_OPTIMIZATION=true`
- Configure proper MongoDB connection pooling

## Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Test individual components (MongoDB, LLM providers)
4. Check API documentation at `/docs` endpoint
