# 🚀 ATS-Checker: AI-Powered Resume Processing System

> **Advanced Applicant Tracking System with Multi-LLM Support and Intelligent Resume Analysis**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat&logo=python)](https://python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg?style=flat&logo=mongodb)](https://mongodb.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg?style=flat&logo=openai)](https://openai.com)
[![Groq](https://img.shields.io/badge/Groq-Mixtral-purple.svg?style=flat)](https://groq.com)

## 📋 Table of Contents
1. [🎯 Project Overview](#-project-overview)
2. [✨ Key Features](#-key-features)
3. [🛠️ Technology Stack](#️-technology-stack)
4. [⚡ Quick Start](#-quick-start)
5. [🔧 Environment Setup](#-environment-setup)
6. [📡 API Testing with Postman](#-api-testing-with-postman)
7. [🎮 Usage Examples](#-usage-examples)
8. [🏗️ System Architecture](#️-system-architecture)
9. [📊 Processing Modes](#-processing-modes)
10. [🔒 Security](#-security)
11. [📈 Performance](#-performance)
12. [🤝 Contributing](#-contributing)

---

## 🎯 Project Overview

**ATS-Checker** is a cutting-edge resume processing system that leverages multiple Large Language Models (LLMs) to extract, analyze, and structure resume data with unprecedented accuracy. The system supports both traditional text extraction methods and direct file processing through AI vision models.

### 🌟 What Makes ATS-Checker Special?

- **🧠 Multi-LLM Architecture**: Support for OpenAI GPT-4, Groq Mixtral, and Anthropic Claude
- **🔄 Intelligent Processing Modes**: Switch between hybrid and complete LLM processing
- **📄 Advanced File Support**: Direct PDF/DOCX processing with vision AI
- **⚡ Smart Provider Selection**: Automatic fallback and cost optimization
- **🎯 Context-Aware Extraction**: Links URLs and information to specific resume sections
- **📊 Confidence Scoring**: Built-in quality assessment and validation

---

## ✨ Key Features

### 🔍 **Intelligent Resume Processing**
- **Dual Processing Modes**: Hybrid (text + LLM) and Complete LLM (direct file processing)
- **Multi-Format Support**: PDF, DOCX with visual layout understanding
- **Section Linking**: Accurately associates URLs and achievements with specific experiences
- **Comprehensive Extraction**: Personal info, skills, experience, projects, achievements, education

### 🤖 **Multi-LLM Support**
- **Provider Selection**: OpenAI, Groq, Anthropic with smart auto-selection
- **Fallback System**: Automatic provider switching for reliability
- **Cost Optimization**: Intelligent routing based on complexity and cost
- **Confidence Scoring**: Quality assessment for each extraction

### 📊 **Data Management**
- **MongoDB Atlas Integration**: Cloud-native data storage
- **Session Management**: User session tracking and data persistence
- **Audit Trail**: Complete extraction history and confidence metrics
- **Structured Output**: Consistent JSON schema across all providers

### 🔒 **Enterprise Security**
- **Environment Variables**: Secure API key management
- **Rate Limiting**: API protection and resource management
- **Validation**: Input sanitization and data validation
- **Error Handling**: Comprehensive error management and logging

---

## 🛠️ Technology Stack

### **Backend Framework**
- **FastAPI** (0.104.1) - High-performance async API framework
- **Uvicorn** - ASGI server with auto-reload support
- **Pydantic** - Data validation and serialization

### **AI & Machine Learning**
- **OpenAI API** (1.3.7) - GPT-4 and GPT-4 Vision models
- **Groq** (0.31.0) - High-speed LLM inference
- **Anthropic Claude** - Advanced reasoning capabilities

### **Database & Storage**
- **MongoDB Atlas** - Cloud document database
- **Motor** - Async MongoDB driver
- **AWS S3** (Optional) - File storage and backup

### **File Processing**
- **PyPDF2** (3.0.1) - PDF text extraction
- **python-docx** (1.1.0) - DOCX document processing
- **lxml** - XML/HTML processing for complex documents

### **Development Tools**
- **Python 3.12+** - Latest Python features and performance
- **python-dotenv** - Environment variable management
- **python-multipart** - File upload support

---

## ⚡ Quick Start

> **📚 For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

### **Prerequisites**
- Python 3.12+ (tested with 3.12.10)
- MongoDB Atlas account (free tier available)  
- At least one LLM API key (OpenAI or Groq recommended)

### 1. **Clone the Repository**
```bash
git clone <repository-url>
cd DuoNova
```

### 2. **Set Up Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all packages
pip install -r requirements.txt
```

### 4. **Configure Environment**
```bash
# Copy environment template
cp env.template .env

# Edit .env with your actual API keys and MongoDB URL
# See SETUP_GUIDE.md for detailed configuration instructions
```

### 5. **Start the Server**
```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. **Verify Installation**
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

> **🚨 Important**: Make sure to configure your `.env` file with valid API keys before starting the server!

---

## 🔧 Environment Setup

### **Required Environment Variables**

Create a `.env` file in the project root with the following configuration:

```bash
# MongoDB Atlas Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=ATS-Checker
MONGODB_DATABASE=ats_checker

# LLM Provider API Keys
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional

# AWS S3 Configuration (Optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=ats-checker-resumes

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_secret_key_for_jwt_or_sessions
ALGORITHM=HS256

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=pdf,docx

# Session Configuration
SESSION_EXPIRE_HOURS=24

# Processing Configuration
DEFAULT_PROCESSING_MODE=hybrid
PROVIDER_PRIORITY=groq,openai,anthropic
ENABLE_COST_OPTIMIZATION=true
ENABLE_AUTO_FALLBACK=true
```

### **API Keys Setup Guide**

1. **OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create new API key
   - Add to `.env` as `OPENAI_API_KEY`

2. **Groq API Key**:
   - Visit [Groq Console](https://console.groq.com/keys)
   - Generate API key
   - Add to `.env` as `GROQ_API_KEY`

3. **MongoDB Atlas**:
   - Create cluster at [MongoDB Atlas](https://cloud.mongodb.com/)
   - Get connection string
   - Replace `<password>` with actual password in `MONGODB_URL`

---

## 📡 API Testing with Postman

### **🚀 Quick Setup**

1. **Import Collection**:
   - Download `ATS_Checker.postman_collection.json`
   - Open Postman → Import → Upload Files
   - Select the collection file

2. **Environment Setup**:
   ```json
   {
     "base_url": "http://localhost:8000",
     "api_version": "v1"
   }
   ```

### **📋 Available Endpoints**

#### **1. Health Check**
```http
GET {{base_url}}/health
```
**Response**: Server health status

#### **2. Processing Options**
```http
GET {{base_url}}/api/{{api_version}}/processing_options
```
**Response**: Available processing modes and LLM providers

#### **3. S3 Status Check**
```http
GET {{base_url}}/api/{{api_version}}/s3/status
```
**Response**: S3 configuration and connection status

#### **4. Test Processing Switches**
```http
POST {{base_url}}/api/{{api_version}}/test_processing_switches
Content-Type: application/x-www-form-urlencoded

processing_mode=hybrid&llm_provider=groq
```
**Response**: Validation of processing mode and provider combination

#### **5. Upload Resume (Production)**
```http
POST {{base_url}}/api/{{api_version}}/upload_resume
Content-Type: multipart/form-data

resume: [Upload your PDF/DOCX file]
level: mid
processing_mode: hybrid
llm_provider: groq
```
**Response**: Complete resume analysis with S3 upload information

#### **6. Download Resume**
```http
GET {{base_url}}/api/{{api_version}}/download/{{resume_id}}
```
**Response**: Presigned S3 URL for file download

#### **7. List User Resumes**
```http
GET {{base_url}}/api/{{api_version}}/user/{{user_id}}/resumes
```
**Response**: All resumes for user with download links

#### **8. Delete Resume**
```http
DELETE {{base_url}}/api/{{api_version}}/delete/{{resume_id}}
```
**Response**: Remove file from S3 and metadata from MongoDB

### **🧪 Test Scenarios**

#### **Scenario 1: Cost-Optimized Processing**
```http
POST /api/v1/test_processing_switches
Body: processing_mode=hybrid&llm_provider=groq
Expected: Fast, cost-effective processing
```

#### **Scenario 2: Maximum Accuracy**
```http
POST /api/v1/test_processing_switches  
Body: processing_mode=complete_llm&llm_provider=openai
Expected: Highest accuracy with vision processing
```

#### **Scenario 3: Auto Provider Selection**
```http
POST /api/v1/test_processing_switches
Body: processing_mode=hybrid&llm_provider=auto
Expected: Smart provider selection based on availability
```

### **📊 Sample Response Structure**

```json
{
  "status": "success",
  "session_id": "uuid-session-id",
  "user_id": "uuid-user-id",
  "resume_id": "uuid-resume-id",
  "processing_info": {
    "mode": "hybrid",
    "provider": "groq",
    "confidence": 0.95,
    "processing_time": "2.3s"
  },
  "file_info": {
    "filename": "resume.pdf",
    "size": 245760,
    "storage_location": "s3",
    "file_path": "s3://bucket/resumes/user123/resume.pdf"
  },
  "s3_info": {
    "uploaded": true,
    "bucket": "ats-checker-resumes",
    "key": "resumes/user123/20240827_abc123.pdf",
    "url": "https://bucket.s3.region.amazonaws.com/key",
    "public_url": "https://bucket.s3.region.amazonaws.com/key"
  },
  "extracted_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john.doe@email.com",
      "phone": "+1-555-123-4567",
      "linkedin": "linkedin.com/in/johndoe"
    },
    "skills": {
      "technical_skills": ["Python", "JavaScript", "React"],
      "frameworks": ["FastAPI", "Node.js"],
      "databases": ["MongoDB", "PostgreSQL"]
    },
    "experience": [
      {
        "company": "TechCorp",
        "position": "Senior Software Engineer",
        "duration": "2020-2023",
        "achievements": ["Improved performance by 40%"],
        "technologies": ["Python", "React"]
      }
    ]
  }
}
```

### **🗄️ S3 File Storage Integration**

The system includes comprehensive S3 integration for secure file storage:

#### **✅ S3 Features**
- **Automatic file upload** to AWS S3 during resume processing
- **Organized storage structure**: `resumes/{user_id}/{timestamp}_{uuid}.{ext}`
- **Presigned URLs** for secure file downloads (1-hour expiration)
- **Graceful fallback** to metadata-only storage when S3 unavailable
- **File management** with upload, download, list, and delete operations
- **Content-type detection** for proper file handling

#### **🔧 S3 Configuration**

Add these variables to your `.env` file for S3 functionality:

```bash
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=ats-checker-resumes
```

#### **📂 S3 Storage Structure**
```
s3://your-bucket/
├── resumes/
│   ├── user_123/
│   │   ├── 20240827_abc123.pdf
│   │   └── 20240827_def456.docx
│   └── user_456/
│       └── 20240827_ghi789.pdf
```

#### **🔄 S3 Workflow**
1. **Upload**: File → S3 bucket with organized path
2. **Metadata**: S3 URL and key stored in MongoDB
3. **Download**: Generate presigned URL for secure access
4. **Management**: List, download, and delete operations
5. **Fallback**: System works without S3 (metadata only)

#### **🚨 Troubleshooting S3 Issues**

**Problem**: Files showing as `local://` instead of S3 URLs in MongoDB

**Diagnosis**:
```bash
# Check S3 status
curl http://localhost:8000/api/v1/s3/status

# Test S3 upload directly
python -c "from app.core.s3 import s3client; print('S3 enabled:', s3client.enabled)"
```

**Common Solutions**:

1. **Missing AWS Permissions** (Most Common):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::your-bucket/*"
    },
    {
      "Effect": "Allow", 
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::your-bucket"
    }
  ]
}
```

2. **Check Environment Variables**:
```bash
# Verify all S3 variables are set
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=your_bucket
AWS_REGION=us-east-1
```

3. **Run Diagnostic Script**:
```bash
python aws_permissions_fix.py
```

### **🔧 Postman Collection Features**

- **✅ Pre-configured endpoints** for all API routes including S3 operations
- **✅ Environment variables** for easy URL and ID management  
- **✅ Test scripts** for response validation
- **✅ Example requests** for each processing mode and S3 operation
- **✅ Error handling examples** for troubleshooting
- **✅ S3 file management** endpoints (upload, download, list, delete)
- **✅ Resume variable extraction** for chaining requests

---
- User Management Service
- Session Management Service
- Validation Service

### Data Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐     ┌─────────────────────────────┐   │
│  │      MongoDB        │     │        AWS S3              │   │
│  │                     │     │                             │   │
│  │  ┌───────────────┐  │     │  ┌─────────────────────┐   │   │
│  │  │     Users     │  │     │  │    Resume Files     │   │   │
│  │  │  Collection   │  │     │  │      Storage        │   │   │
│  │  └───────────────┘  │     │  └─────────────────────┘   │   │
│  │                     │     │                             │   │
│  │  ┌───────────────┐  │     │  ┌─────────────────────┐   │   │
│  │  │   Sessions    │  │     │  │    File Backup      │   │   │
│  │  │  Collection   │  │     │  │   & Versioning      │   │   │
│  │  └───────────────┘  │     │  └─────────────────────┘   │   │
│  │                     │     │                             │   │
│  │  ┌───────────────┐  │     │                             │   │
│  │  │    Resumes    │  │     │                             │   │
│  │  │  Collection   │  │     │                             │   │
│  │  └───────────────┘  │     │                             │   │
│  └─────────────────────┘     └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Storage Components:**
- **MongoDB**: Metadata storage
  - Users Collection
  - Sessions Collection
  - Resumes Collection
- **AWS S3**: File storage
  - Resume Files Storage
  - File Backup & Versioning

---

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │  FastAPI    │    │  Business   │    │    Data     │
│ Application │    │   Layer     │    │   Logic     │    │   Layer     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                    │                    │                    │
      │ 1. Upload Resume   │                    │                    │
      ├───────────────────►│                    │                    │
      │                    │ 2. Validate File   │                    │
      │                    ├───────────────────►│                    │
      │                    │                    │ 3. Save to S3     │
      │                    │                    ├───────────────────►│
      │                    │                    │ 4. Extract Text    │
      │                    │                    │◄───────────────────┤
      │                    │                    │ 5. Process w/ LLM  │
      │                    │                    │                    │
      │                    │                    │ 6. Validate Data   │
      │                    │                    │                    │
      │                    │                    │ 7. Find/Create User│
      │                    │                    ├───────────────────►│
      │                    │                    │ 8. Create Session  │
      │                    │                    ├───────────────────►│
      │                    │                    │ 9. Save Resume     │
      │                    │                    ├───────────────────►│
      │ 10. Return Response│                    │                    │
      │◄───────────────────┤◄───────────────────┤                    │
```

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Raw      │    │   Text      │    │    LLM      │    │ Structured  │
│    Text     │    │ Processing  │    │ Processing  │    │    Data     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                    │                    │                    │
      │ PDF/DOCX Content   │                    │                    │
      ├───────────────────►│                    │                    │
      │                    │ Clean & Chunk      │                    │
      │                    ├───────────────────►│                    │
      │                    │                    │ Primary LLM        │
      │                    │                    │ (GPT-4)           │
      │                    │                    ├───────────────────►│
      │                    │                    │ Fallback LLM       │
      │                    │                    │ (Claude/Groq)     │
      │                    │                    │ if needed         │
      │                    │                    ├───────────────────►│
      │                    │                    │ Validate JSON      │
      │                    │                    ├───────────────────►│
      │                    │                    │ Confidence Score   │
      │                    │                    ├───────────────────►│
```

```
┌─────────────────────────────────────────────────────────────────┐
│                        MongoDB Schema                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Users Collection                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {                                                       │   │
│  │   "_id": "ObjectId",                                    │   │
│  │   "user_id": "USER_001",                               │   │
│  │   "primary_email": "user@example.com",                 │   │
│  │   "alternate_emails": ["old@email.com"],               │   │
│  │   "phone": "+1234567890",                              │   │
│  │   "linkedin": "linkedin.com/in/user",                  │   │
│  │   "name": "John Doe",                                  │   │
│  │   "verification_status": "verified",                   │   │
│  │   "created_at": "datetime",                            │   │
│  │   "updated_at": "datetime"                             │   │
│  │ }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Sessions Collection                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {                                                       │   │
│  │   "_id": "ObjectId",                                    │   │
│  │   "session_id": "uuid-string",                         │   │
│  │   "user_id": "USER_001",                               │   │
│  │   "extracted_email": "from_resume@email.com",          │   │
│  │   "ip_address": "192.168.1.1",                         │   │
│  │   "created_at": "datetime",                            │   │
│  │   "expires_at": "datetime",                            │   │
│  │   "status": "active"                                   │   │
│  │ }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Resumes Collection                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {                                                       │   │
│  │   "_id": "ObjectId",                                    │   │
│  │   "resume_id": "RESUME_001",                           │   │
│  │   "session_id": "uuid-string",                         │   │
│  │   "user_id": "USER_001",                               │   │
│  │   "file_name": "resume.pdf",                           │   │
│  │   "file_path": "s3://bucket/path/file.pdf",            │   │
│  │   "file_size": 1234567,                                │   │
│  │   "raw_text": "extracted text...",                     │   │
│  │   "json_data": { /* structured data */ },             │   │
│  │   "extraction_confidence": 0.85,                       │   │
│  │   "created_at": "datetime"                             │   │
│  │ }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Provider Strategy                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Primary Provider: OpenAI GPT-4                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Highest accuracy for structured extraction           │   │
│  │ • Best JSON compliance                                  │   │
│  │ • Advanced reasoning capabilities                       │   │
│  │ • Cost: Higher but justified for quality               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Secondary Provider: Anthropic Claude                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Good accuracy and reliability                         │   │
│  │ • Better at handling complex layouts                    │   │
│  │ • Fallback when OpenAI fails                           │   │
│  │ • Cost: Medium                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Fallback Provider: Groq/Llama                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Fast processing speed                                 │   │
│  │ • Lower cost                                            │   │
│  │ • Last resort option                                    │   │
│  │ • Local deployment possible                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│                      AWS S3 Integration                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Storage Strategy                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Standard Storage: Recent uploads (30 days)           │   │
│  │ • Intelligent Tiering: Automatic cost optimization     │   │
│  │ • Glacier: Archive old resumes (90+ days)              │   │
│  │ • Cross-Region Replication: Disaster recovery          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Security & Access                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Pre-signed URLs: Secure file access                  │   │
│  │ • IAM Roles: Principle of least privilege              │   │
│  │ • Encryption: At rest and in transit                   │   │
│  │ • Lifecycle Policies: Automatic archival               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```
## 1. Component Architecture

### 1.1 API Layer (FastAPI)

**Components:**
- Resume Endpoints
- Session Management
- User Endpoints
- Middleware & Security
  - Authentication
  - Rate Limiting
  - CORS
  - Request Validation
  - Error Handling

### 1.2 Business Logic Layer

**Core Services:**
- Resume Processing Service
- File Extraction Service
- LLM Orchestrator Service
- User Management Service
- Session Management Service
- Validation Service

### 1.3 Data Layer

**Storage Components:**
- **MongoDB**: Metadata storage
  - Users Collection
  - Sessions Collection
  - Resumes Collection
- **AWS S3**: File storage
  - Resume Files Storage
  - File Backup & Versioning

## 2. Data Flow Architecture

### 2.1 Resume Upload & Processing Flow

1. **Client Application** → Upload Resume
2. **FastAPI Layer** → Validate File
3. **Business Logic** → Save to S3
4. **Business Logic** → Extract Text
5. **Business Logic** → Process with LLM
6. **Business Logic** → Validate Data
7. **Business Logic** → Find/Create User
8. **Business Logic** → Create Session
9. **Business Logic** → Save Resume
10. **FastAPI Layer** → Return Response

### 2.2 LLM Processing Pipeline

1. **Raw Text** (PDF/DOCX Content)
2. **Text Processing** (Clean & Chunk)
3. **LLM Processing**
   - Primary LLM (GPT-4)
   - Fallback LLM (Claude/Groq) if needed
4. **Structured Data**
   - Validate JSON
   - Confidence Score

## 3. Database Design

## 3. Database Schema

### 3.1 MongoDB Collections Schema

#### Users Collection

```json
{
  "_id": "ObjectId",
  "user_id": "USER_001",
  "primary_email": "user@example.com",
  "alternate_emails": ["old@email.com"],
  "phone": "+1234567890",
  "linkedin": "linkedin.com/in/user",
  "name": "John Doe",
  "verification_status": "verified",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Indexes:**
- `primary_email` (unique)
- `user_id` (unique)
- `created_at` (descending)
- `verification_status`

#### Sessions Collection

```json
{
  "_id": "ObjectId",
  "session_id": "uuid-string",
  "user_id": "USER_001",
  "extracted_email": "from_resume@email.com",
  "ip_address": "192.168.1.1",
  "created_at": "datetime",
  "expires_at": "datetime",
  "status": "active"
}
```

**Indexes:**
- `session_id` (unique)
- `user_id`
- `expires_at` (TTL index)
- `status`

#### Resumes Collection

```json
{
  "_id": "ObjectId",
  "resume_id": "RESUME_001",
  "session_id": "uuid-string",
  "user_id": "USER_001",
  "file_name": "resume.pdf",
  "file_path": "s3://bucket/path/file.pdf",
  "file_size": 1234567,
  "raw_text": "extracted text...",
  "json_data": { /* structured data */ },
  "extraction_confidence": 0.85,
  "created_at": "datetime"
}
```

**Indexes:**
- `resume_id` (unique)
- `session_id`
- `user_id`
- `created_at` (descending)
- `extraction_confidence`

---

## 4. External Integrations

### 4.1 LLM Provider Integration

#### Primary Provider: OpenAI GPT-4
- **Purpose:** Highest accuracy for structured extraction
- **Best Use Case:** JSON compliance and complex data extraction
- **Rate Limits:** 10,000 requests/minute
- **Cost:** $0.03/1K input tokens, $0.06/1K output tokens

#### Secondary Provider: Anthropic Claude
- **Purpose:** Fallback and quality verification
- **Best Use Case:** Long document processing and context understanding
- **Rate Limits:** 5,000 requests/minute
- **Cost:** $0.008/1K input tokens, $0.024/1K output tokens

#### Tertiary Provider: Groq/Llama
- **Purpose:** Cost-effective backup solution
- **Best Use Case:** Simple extractions when budget is a concern
- **Rate Limits:** 14,400 requests/minute
- **Cost:** $0.00027/1K input tokens, $0.00027/1K output tokens

#### Provider Selection Logic

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Provider Selection                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Start Resume Processing                                       │
│           │                                                     │
│           ▼                                                     │
│   ┌─────────────┐                                              │
│   │ File Size?  │                                              │
│   └─────────────┘                                              │
│           │                                                     │
│     ┌─────┴─────┐                                              │
│     ▼           ▼                                              │
│ ┌───────┐   ┌───────┐                                         │
│ │< 2MB  │   │> 2MB  │                                         │
│ └───────┘   └───────┘                                         │
│     │           │                                              │
│     ▼           ▼                                              │
│ ┌───────┐   ┌───────┐                                         │
│ │OpenAI │   │Claude │                                         │
│ │GPT-4  │   │ 3.5   │                                         │
│ └───────┘   └───────┘                                         │
│     │           │                                              │
│     ▼           ▼                                              │
│ ┌─────────────────┐                                           │
│ │  Success?       │                                           │
│ └─────────────────┘                                           │
│     │                                                          │
│ ┌───┴───┐                                                     │
│ ▼       ▼                                                     │
│Yes     No                                                     │
│ │       │                                                     │
│ │       ▼                                                     │
│ │   ┌─────────┐                                              │
│ │   │ Groq    │                                              │
│ │   │ Llama   │                                              │
│ │   └─────────┘                                              │
│ │       │                                                     │
│ ▼       ▼                                                     │
│ Return Result                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 AWS S3 Integration

#### Bucket Configuration
- **Primary Bucket:** `ats-checker-resumes-prod`
- **Backup Bucket:** `ats-checker-resumes-backup`
- **Lifecycle Policy:**
  - Standard storage: 30 days
  - Infrequent Access: 90 days
  - Archive: 365 days
  - Deep Archive: 7 years

#### Security Configuration
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT:role/ATS-Checker-Service"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::ats-checker-resumes-prod/*"
    }
  ]
}
```

---
- Advanced reasoning capabilities
- Cost: Higher but justified for quality

#### Secondary Provider: Anthropic Claude
- Good accuracy and reliability
- Better at handling complex layouts
- Fallback when OpenAI fails
- Cost: Medium

#### Fallback Provider: Groq/Llama
- Fast processing speed
- Lower cost
- Last resort option
- Local deployment possible

### 4.2 File Storage Integration

#### AWS S3 Integration

**Storage Strategy:**
- Standard Storage: Recent uploads (30 days)
- Intelligent Tiering: Automatic cost optimization
- Glacier: Archive old resumes (90+ days)
- Cross-Region Replication: Disaster recovery

**Security & Access:**
- Pre-signed URLs: Secure file access
- IAM Roles: Principle of least privilege
- Encryption: At rest and in transit
- Lifecycle Policies: Automatic archival

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| Metric | Target | Critical Threshold |
|--------|--------|--------------------|
| **Response Time** | < 2 seconds | < 5 seconds |
| **Processing Time** | < 30 seconds | < 60 seconds |
| **Throughput** | 100 concurrent uploads | 50 minimum |
| **Availability** | 99.9% uptime | 99.5% minimum |

### 5.2 Security Requirements

| Component | Requirement | Implementation |
|-----------|-------------|----------------|
| **Data Encryption** | AES-256 at rest, TLS 1.3 in transit | AWS KMS, HTTPS only |
| **Access Control** | Session-based authentication | JWT tokens, expiry |
| **Data Privacy** | GDPR compliant data handling | Data retention policies |
| **File Validation** | Malware scanning, type validation | ClamAV integration |

### 5.3 Scalability Requirements

| Resource | Scaling Strategy | Capacity Planning |
|----------|------------------|-------------------|
| **API Layer** | Horizontal scaling, stateless design | Auto-scaling groups |
| **Database** | MongoDB replica sets, sharding | Read replicas |
| **File Storage** | Unlimited S3 capacity | Multi-region backup |
| **LLM Processing** | Rate limiting, load balancing | Provider rotation |

---

## 6. Monitoring & Observability

### 6.1 Key Metrics Dashboard

| Category | Metrics | Alerts | Tools |
|----------|---------|--------|--------|
| **Performance** | Upload success/failure rates, Response times, Processing times | > 5% error rate, > 10s response time | CloudWatch, Grafana |
| **Cost Management** | LLM processing costs, S3 storage costs, Database costs | Monthly budget exceeded | AWS Cost Explorer |
| **System Health** | Database query performance, File storage usage, API endpoint health | Connection failures, Storage quota > 80% | DataDog, New Relic |
| **User Analytics** | Session analytics, User engagement, Feature usage | Unusual traffic patterns | Google Analytics |

### 6.2 Alerting Strategy

#### Critical Alerts (Immediate Response)
- **High Error Rates** (>5%) → PagerDuty notification
- **LLM Provider Failures** → Auto-failover + SMS alert
- **Database Connection Issues** → Service restart + email alert
- **Security Incidents** → Immediate escalation

#### Warning Alerts (Next Business Day)
- **Storage Quota Warnings** (>80%) → Email notification
- **Performance Degradation** (>5s response) → Slack alert
- **Cost Threshold** (>Monthly budget) → Finance team notification

### 6.3 Logging Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                      Logging Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Application│    │   System    │    │   Security  │         │
│  │     Logs     │    │    Logs     │    │    Logs     │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Centralized Logging                     │   │
│  │                 (AWS CloudWatch Logs)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Log Analysis & Search                      │   │
│  │                (ELK Stack / Splunk)                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Log Levels:**
- **DEBUG:** Development debugging information
- **INFO:** General application flow
- **WARN:** Potential issues that don't break functionality
- **ERROR:** Error conditions that need attention
- **CRITICAL:** System-breaking errors requiring immediate action

---

## 7. API Specifications

### 7.1 Core Endpoints

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| **GET** | `/health` | Health Check | None | `{"status": "healthy"}` |
| **POST** | `/resumes/upload` | Resume Upload | Multipart file | Resume metadata |
| **GET** | `/resumes/{resume_id}` | Get Resume | Path param | Resume details |
| **GET** | `/users/{user_id}/resumes` | Get User Resumes | Path param | Resume list |
| **GET** | `/users/by-email/{email}` | Get User by Email | Path param | User details |
| **GET** | `/session/{session_id}/user` | Get User by Session | Path param | User details |
| **POST** | `/session/{session_id}/verify-email` | Verify Email | Email in body | Verification result |

### 7.2 Request/Response Models

#### Resume Upload Request
```json
{
  "file": "multipart/form-data",
  "session_id": "uuid-string",
  "user_email": "user@example.com"
}
```

#### Resume Response Model
```json
{
  "resume_id": "RESUME_001",
  "user_id": "USER_001",
  "session_id": "uuid-string",
  "filename": "resume.pdf",
  "file_size": 1234567,
  "processing_status": "completed",
  "extraction_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john.doe@email.com",
      "phone": "+1234567890",
      "location": "New York, NY",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe",
      "confidence_score": 0.95
    },
    "professional_summary": {
      "summary": "Software engineer with 5 years experience...",
      "confidence_score": 0.88
    },
    "experience": [
      {
        "company": "Tech Corp",
        "position": "Senior Developer",
        "start_date": "2020-01",
        "end_date": "2023-12",
        "description": "Led development of web applications...",
        "confidence_score": 0.92
      }
    ],
    "education": [
      {
        "institution": "University of Technology",
        "degree": "Bachelor of Computer Science",
        "field": "Computer Science",
        "graduation_date": "2019-05",
        "gpa": "3.8",
        "confidence_score": 0.95
      }
    ],
    "skills": {
      "technical_skills": ["Python", "JavaScript", "React", "AWS"],
      "soft_skills": ["Leadership", "Communication", "Problem Solving"],
      "confidence_score": 0.90
    },
    "certifications": [
      {
        "name": "AWS Solutions Architect",
        "issuer": "Amazon Web Services",
        "date": "2022-06",
        "confidence_score": 0.98
      }
    ]
  },
  "extraction_confidence": 0.92,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Error Response Model
```json
{
  "error": {
    "code": "PROCESSING_FAILED",
    "message": "Resume processing failed due to invalid file format",
    "details": {
      "field": "file_type",
      "expected": ["pdf", "docx"],
      "received": "txt"
    },
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### 7.3 HTTP Status Codes

| Status Code | Description | Use Cases |
|-------------|-------------|-----------|
| **200 OK** | Success | Successful GET requests |
| **201 Created** | Resource created | Successful POST requests |
| **400 Bad Request** | Invalid request | Validation errors, invalid file format |
| **401 Unauthorized** | Authentication required | Invalid session |
| **404 Not Found** | Resource not found | Resume/User not found |
| **413 Payload Too Large** | File too large | File size > 10MB |
| **415 Unsupported Media Type** | Invalid file type | Non-PDF/DOCX files |
| **429 Too Many Requests** | Rate limit exceeded | Too many uploads |
| **500 Internal Server Error** | Server error | LLM processing failures |
| **503 Service Unavailable** | Service down | External service failures |

---
```json
{
  "status": "success",
  "session_id": "uuid-string",
  "user_id": "USER_001",
  "resume_id": "RESUME_001",
  "extracted_email": "user@example.com",
  "verification_needed": false,
  "message": "Resume processed successfully"
}
```

## 8. Cost Analysis

### 8.1 Storage Costs (AWS S3)

| Scale | Volume | Storage Cost | Transfer Cost | Total Monthly |
|--------|---------|--------------|---------------|---------------|
| **Small** | 10,000 resumes (20GB) | $0.46 | $1.80 | $2.26 |
| **Medium** | 100,000 resumes (200GB) | $4.60 | $18.00 | $22.60 |
| **Large** | 1,000,000 resumes (2TB) | $46.00 | $180.00 | $226.00 |

### 8.2 LLM Processing Costs

| Provider | Cost per Resume | Accuracy | Speed | Best Use Case |
|----------|-----------------|----------|-------|---------------|
| **OpenAI GPT-4** | $0.03 | 95% | Medium | Complex extraction |
| **Anthropic Claude** | $0.02 | 92% | Fast | Long documents |
| **Groq/Llama** | $0.005 | 85% | Very Fast | Simple extraction |

### 8.3 Infrastructure Costs

| Component | Small Scale | Medium Scale | Large Scale |
|-----------|-------------|--------------|-------------|
| **API Servers** | $50/month | $200/month | $800/month |
| **Database** | $25/month | $100/month | $400/month |
| **Monitoring** | $20/month | $50/month | $150/month |
| **Backup & DR** | $10/month | $30/month | $100/month |

### 8.4 Total Cost Projections

| Scale | Resumes/Month | Total Monthly Cost | Cost per Resume |
|-------|---------------|-------------------|-----------------|
| **Small** | 1,000 | $107 | $0.11 |
| **Medium** | 10,000 | $403 | $0.04 |
| **Large** | 100,000 | $1,676 | $0.02 |

---

## 9. Implementation Roadmap

### 9.1 Phase 1: MVP Foundation (4-6 weeks)

| Week | Deliverable | Components | Success Criteria |
|------|-------------|------------|------------------|
| **1-2** | Core Infrastructure | FastAPI setup, MongoDB connection, S3 integration | Health checks pass, basic CRUD operations work |
| **3-4** | File Processing | Upload endpoint, text extraction, basic LLM integration | Single file upload and processing works |
| **5-6** | User Management | Session handling, user identification, basic validation | End-to-end workflow functional |

### 9.2 Phase 2: Enhanced Processing (2-4 weeks)

| Week | Deliverable | Components | Success Criteria |
|------|-------------|------------|------------------|
| **1-2** | Multi-LLM Support | Provider abstraction, fallback logic, error handling | Fallback mechanism works reliably |
| **3-4** | Data Quality | Confidence scoring, validation rules, data enrichment | 90%+ accuracy on test dataset |

### 9.3 Phase 3: Production Readiness (2-3 weeks)

| Week | Deliverable | Components | Success Criteria |
|------|-------------|------------|------------------|
| **1** | Monitoring & Logging | CloudWatch setup, alerting, dashboards | All metrics visible and alerts functional |
| **2** | Security & Testing | Security audit, load testing, performance optimization | Passes security scan, handles 100 concurrent users |
| **3** | Documentation & Deployment | API docs, deployment automation, user guides | Production deployment successful |

### 9.4 Success Metrics

| Phase | Key Performance Indicators | Target Values |
|-------|---------------------------|---------------|
| **MVP** | Upload success rate, Processing time, Basic accuracy | >95%, <30s, >80% |
| **Enhanced** | Multi-provider reliability, Data quality, Error handling | >99%, >90%, <1% failure |
| **Production** | System uptime, Response time, Security compliance | >99.9%, <2s, 100% pass |

---

## 10. Risk Assessment & Mitigation

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation Strategy | Contingency Plan |
|------|--------|-------------|---------------------|------------------|
| **LLM Provider Outages** | High | Medium | Multi-provider fallback, health checks | Manual provider switching, cached responses |
| **Data Quality Issues** | Medium | High | Confidence scoring, validation rules | Human review process, data correction tools |
| **Scalability Bottlenecks** | High | Low | Cloud-native design, load testing | Auto-scaling, performance monitoring |
| **Security Vulnerabilities** | High | Medium | Regular audits, secure coding practices | Incident response plan, security patches |

### 10.2 Business Risks

| Risk | Impact | Probability | Mitigation Strategy | Contingency Plan |
|------|--------|-------------|---------------------|------------------|
| **Cost Overruns** | Medium | Medium | Usage monitoring, budget alerts | Provider switching, feature scaling |
| **Performance Degradation** | High | Low | Comprehensive testing, monitoring | Performance optimization, infrastructure scaling |
| **Data Compliance Issues** | High | Low | GDPR by design, legal review | Compliance audit, data purging |
| **Vendor Lock-in** | Medium | High | Abstraction layers, multi-cloud | Provider migration plan, data portability |

### 10.3 Operational Risks

| Risk | Impact | Probability | Mitigation Strategy | Contingency Plan |
|------|--------|-------------|---------------------|------------------|
| **Key Personnel Loss** | Medium | Medium | Documentation, knowledge sharing | Cross-training, external contractors |
| **Infrastructure Failures** | High | Low | Multi-region deployment, backups | Disaster recovery, failover procedures |
| **Third-party Dependencies** | Medium | Medium | Service monitoring, SLA tracking | Alternative providers, service redundancy |

### 10.4 Risk Monitoring

#### Automated Monitoring
- **System Health:** Real-time dashboards for all critical components
- **Performance Metrics:** Automated alerts for degradation
- **Cost Tracking:** Daily budget monitoring and projections
- **Security Scans:** Continuous vulnerability assessment

#### Manual Reviews
- **Monthly Risk Assessment:** Review and update risk register
- **Quarterly Security Audit:** External security assessment
- **Annual Business Continuity Test:** End-to-end disaster recovery testing

---

## Conclusion

This High-Level Design document provides a comprehensive blueprint for the ATS Checker application, covering all aspects from system architecture to implementation roadmap. The design emphasizes:

1. **Scalability** through cloud-native architecture
2. **Reliability** via multi-provider LLM strategy
3. **Security** with encryption and compliance measures
4. **Cost-effectiveness** through intelligent provider selection
5. **Maintainability** via modular design and comprehensive monitoring

The phased implementation approach ensures a working MVP can be delivered quickly while allowing for iterative improvements and feature enhancements based on user feedback and business requirements.

---

*Document Version: 1.0*  
*Last Updated: January 2024*  
*Next Review Date: February 2024*
