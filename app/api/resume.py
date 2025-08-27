from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException, status
from typing import Literal, Optional
import re
import uuid
import datetime
import os
from ..services.resume_processing import ResumeProcessingService
from ..services.file_extraction import FileExtractionService
from ..services.processing_selection import ProcessingSelectionService
from ..core.mongo import mongodb
from ..core.s3 import s3client
from ..core.config import settings
from ..schemas.resume import ResumeCreate
from ..schemas.user import UserCreate
from ..schemas.session import SessionCreate

router = APIRouter()

@router.get("/processing_options")
async def get_processing_options():
    """
    Get available processing modes and LLM providers with recommendations.
    """
    llm_service = ResumeProcessingService()
    available_providers = llm_service.get_available_providers()
    
    return {
        "processing_modes": {
            "hybrid": {
                "description": "Library extraction + LLM processing",
                "advantages": ["Fast", "Cost-effective", "Reliable fallback", "Good for simple resumes"],
                "best_for": "Standard resumes, high-volume processing, cost optimization"
            },
            "complete_llm": {
                "description": "Direct file upload to LLM only",
                "advantages": ["Best context understanding", "Links items correctly", "Handles complex layouts", "Superior accuracy"],
                "best_for": "Complex resumes, creative layouts, maximum accuracy needed"
            }
        },
        "llm_providers": {
            "auto": {
                "description": "Smart automatic selection",
                "logic": "Chooses best provider based on processing mode and availability"
            },
            "openai": {
                "description": "OpenAI GPT-4 / GPT-4 Vision",
                "advantages": ["Best accuracy", "File upload support", "Complex document understanding"],
                "available": available_providers.get("openai", False),
                "best_for": "Maximum accuracy, complex documents, direct file processing"
            },
            "groq": {
                "description": "Groq Mixtral",
                "advantages": ["Fastest processing", "Cost-effective", "Good accuracy"],
                "available": available_providers.get("groq", False),
                "best_for": "High-volume processing, speed optimization, text processing"
            },
            "anthropic": {
                "description": "Anthropic Claude",
                "advantages": ["Excellent reasoning", "Large context", "Good accuracy"],
                "available": available_providers.get("anthropic", False),
                "best_for": "Complex analysis, large documents, detailed extraction"
            }
        },
        "recommendations": {
            "cost_optimized": {
                "processing_mode": "hybrid",
                "llm_provider": "groq",
                "description": "Fastest and most cost-effective option"
            },
            "accuracy_optimized": {
                "processing_mode": "complete_llm",
                "llm_provider": "openai",
                "description": "Best accuracy and context understanding"
            },
            "balanced": {
                "processing_mode": "hybrid",
                "llm_provider": "auto",
                "description": "Good balance of speed, cost, and accuracy"
            }
        },
        "current_status": {
            "available_providers": available_providers,
            "default_processing_mode": "hybrid",
            "default_llm_provider": "auto"
        }
    }

@router.post("/test_processing_switches")
async def test_processing_switches(
    processing_mode: Literal["hybrid", "complete_llm"] = Form("hybrid"),
    llm_provider: Literal["auto", "openai", "groq", "anthropic"] = Form("auto")
):
    """
    Test endpoint to validate switch combinations without uploading a file.
    """
    llm_service = ResumeProcessingService()
    available_providers = llm_service.get_available_providers()
    
    # Validate provider selection
    if llm_provider != "auto":
        if llm_provider not in available_providers or not available_providers[llm_provider]:
            return {
                "status": "error",
                "message": f"Provider '{llm_provider}' is not available",
                "available_providers": [k for k, v in available_providers.items() if v]
            }
    
    # Simulate provider selection logic
    if llm_provider == "auto":
        if processing_mode == "complete_llm":
            provider_priority = ["openai", "anthropic", "groq"]
        else:
            provider_priority = ["groq", "openai", "anthropic"]
        
        selected_provider = None
        for provider in provider_priority:
            if provider in available_providers and available_providers[provider]:
                selected_provider = provider
                break
    else:
        selected_provider = llm_provider
    
    # Capability analysis
    capabilities = {
        "direct_file_upload": llm_service.file_upload_support.get(selected_provider, False),
        "text_processing": True,  # All providers support text
        "recommended_for_mode": selected_provider in (["openai", "anthropic"] if processing_mode == "complete_llm" else ["groq", "openai"])
    }
    
    warnings = []
    if selected_provider == "groq" and processing_mode == "complete_llm":
        warnings.append("Groq doesn't support direct file upload - will use text fallback")
    if processing_mode == "complete_llm":
        warnings.append("Complete LLM mode may be more expensive")
    if llm_provider != "auto" and not capabilities["recommended_for_mode"]:
        warnings.append(f"Provider '{llm_provider}' forced - may not be optimal for {processing_mode} mode")
    
    return {
        "status": "success",
        "configuration": {
            "processing_mode": processing_mode,
            "llm_provider_requested": llm_provider,
            "llm_provider_selected": selected_provider,
            "auto_selection": llm_provider == "auto"
        },
        "capabilities": capabilities,
        "warnings": [w for w in warnings if w],
        "recommendation": f"✅ Good choice!" if capabilities["recommended_for_mode"] else f"⚠️ Consider using 'auto' provider selection for {processing_mode} mode"
    }

@router.get("/intelligent_processing_info")
async def get_intelligent_processing_info():
    """
    Get information about the current intelligent processing configuration.
    Shows how the system automatically selects processing modes and providers.
    """
    try:
        from ..services.processing_selection import ProcessingSelectionService
        from ..config.processing_config import ProcessingConfig
        
        selection_service = ProcessingSelectionService()
        config = ProcessingConfig()
        
        # Test configuration with sample files
        test_results = selection_service.test_configuration()
        
        return {
            "status": "success",
            "message": "Intelligent processing is active - no manual configuration needed!",
            "how_it_works": {
                "automatic_selection": "System chooses optimal processing based on file characteristics",
                "factors_considered": [
                    "File type (PDF, DOCX, TXT)",
                    "File size (large files use complete LLM)",
                    "Available LLM providers",
                    "Cost optimization settings",
                    "Processing rules and fallbacks"
                ]
            },
            "current_configuration": config.get_current_config(),
            "sample_selections": test_results["test_results"],
            "available_providers": test_results["available_providers"],
            "configuration_help": {
                "change_settings": "Use scripts/config_manager.py to modify configuration",
                "presets_available": ["speed", "accuracy", "cost", "dev", "prod"],
                "environment_variables": [
                    "DEFAULT_PROCESSING_MODE",
                    "PROVIDER_PRIORITY", 
                    "ENABLE_COST_OPTIMIZATION",
                    "ENABLE_AUTO_FALLBACK"
                ]
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to load intelligent processing info: {str(e)}",
            "fallback_info": "Manual configuration may be needed"
        }

@router.post("/explain_file_processing") 
async def explain_file_processing(
    file: UploadFile = File(...),
    level: Literal["entry", "mid", "senior"] = Form("mid")
):
    """
    Explain what processing strategy would be used for a specific file
    without actually processing it.
    """
    try:
        from ..services.processing_selection import ProcessingSelectionService
        
        # Read file to get size
        contents = await file.read()
        file_size = len(contents)
        
        # Reset file position 
        file.file.seek(0)
        
        selection_service = ProcessingSelectionService()
        explanation = selection_service.get_processing_explanation(file.filename, file_size)
        
        return {
            "status": "success",
            "message": f"Processing explanation for {file.filename}",
            **explanation
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to explain processing for file: {str(e)}"
        }


@router.post("/upload_resume")
async def upload_resume(
    request: Request,
    resume: UploadFile = File(...),
    level: Literal["entry", "mid", "senior"] = Form(...),
    job_description: Optional[str] = Form(None),
    # Configuration-driven processing - no user input needed!
    # Processing mode and provider are automatically selected based on:
    # - File characteristics (size, type)
    # - Available providers
    # - Configuration rules
    # - Cost optimization settings
):
    """
    Upload a resume file with intelligent automatic processing selection.
    
    Parameters:
    - resume: The resume file (PDF or DOCX)
    - level: Job level (entry, mid, senior)
    - job_description: Optional job description for context (not used in processing yet)
    
    The system automatically selects the optimal processing strategy based on:
    - File type and size (PDF/DOCX, large/small files)
    - Available LLM providers and their capabilities  
    - Cost optimization preferences
    - Configuration rules and fallback strategies
    
    No need to specify processing mode or provider - the system chooses optimally!
    """
    # 1. Get client IP address automatically
    ip_address = request.client.host
    if request.headers.get("x-forwarded-for"):
        ip_address = request.headers.get("x-forwarded-for").split(",")[0].strip()
    elif request.headers.get("x-real-ip"):
        ip_address = request.headers.get("x-real-ip")
    
    # 2. Validate file type and size
    if not resume.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid file type. Only PDF and DOCX are supported.")
    
    contents = await resume.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large. Maximum size is 10MB.")

    # 3. INTELLIGENT PROCESSING STRATEGY SELECTION
    # Use configuration-driven automatic selection
    selection_service = ProcessingSelectionService()
    
    # DEBUG: Check what configuration is being used
    current_config = selection_service.config.get_current_config()
    print(f"🔍 DEBUG - Current config: {current_config}")
    print(f"🔍 DEBUG - Environment vars: DEFAULT_PROCESSING_MODE={os.getenv('DEFAULT_PROCESSING_MODE')}, PROVIDER_PRIORITY={os.getenv('PROVIDER_PRIORITY')}")
    
    # Get intelligent processing strategy based on file characteristics
    processing_mode_enum, selected_provider_enum, selection_reasoning = selection_service.select_processing_strategy(
        file_name=resume.filename,
        file_size_bytes=len(contents),
        user_level=level
    )
    
    print(f"🤖 Auto-selected strategy: {processing_mode_enum.value} mode with {selected_provider_enum.value} provider")
    print(f"💡 Selection reasoning: {selection_reasoning}")
    
    # Convert enum values to strings for processing
    processing_mode_str = processing_mode_enum.value
    selected_provider_str = selected_provider_enum.value
    
    # 4. MODE-SPECIFIC TEXT PROCESSING BASED ON INTELLIGENT SELECTION
    raw_text = None
    extracted_emails = []
    primary_email = None
    file_type = ".pdf" if resume.filename.lower().endswith(".pdf") else ".docx"
    
    if processing_mode_str == "hybrid":
        # Hybrid Mode: Extract raw text using library first
        try:
            raw_text = FileExtractionService.extract_text(contents, file_type)
            if not raw_text.strip():
                print("Warning: Library extraction failed, auto-switching to complete LLM mode")
                processing_mode_str = "complete_llm"
        except Exception as e:
            print(f"Library text extraction failed: {e}, auto-switching to complete LLM mode")
            processing_mode_str = "complete_llm"

        # Extract email using regex patterns (library-based validation)
        if raw_text and processing_mode_str == "hybrid":
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}\b'
            ]
            
            for pattern in email_patterns:
                matches = re.findall(pattern, raw_text, re.IGNORECASE)
                extracted_emails.extend(matches)
            
            # Clean and deduplicate emails
            extracted_emails = list(set([email.replace(" ", "").lower() for email in extracted_emails]))
            primary_email = extracted_emails[0] if extracted_emails else None

    elif processing_mode_str == "complete_llm":
        # Complete LLM Mode: Skip library extraction entirely
        print("Complete LLM mode: Using direct file processing")
        raw_text = None
        extracted_emails = []
        primary_email = None

    # Get LLM service for processing
    llm_service = ResumeProcessingService()

    # 5. PROCESS WITH LLM BASED ON SELECTED MODE AND PROVIDER
    try:
        # Check if selected provider supports file upload
        llm_service = ResumeProcessingService()
        provider_supports_files = llm_service.file_upload_support.get(selected_provider_str, False)
        
        if processing_mode_str == "complete_llm":
            if provider_supports_files:
                # Provider supports file upload - use direct file processing
                resume_data = llm_service.extract_structured_data(
                    file_bytes=contents,
                    file_type=file_type,
                    text=None,
                    provider=selected_provider_str
                )
            else:
                # Provider doesn't support file upload - extract text first
                print(f"⚠️ Provider {selected_provider_str} doesn't support file upload, extracting text first")
                try:
                    raw_text = FileExtractionService.extract_text(contents, file_type)
                    if not raw_text.strip():
                        raise ValueError("Text extraction failed")
                except Exception as e:
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Provider {selected_provider_str} requires text but text extraction failed: {str(e)}"
                    )
                
                resume_data = llm_service.extract_structured_data(
                    file_bytes=None,
                    file_type=file_type,
                    text=raw_text,
                    provider=selected_provider_str
                )
        else:
            # Hybrid mode: Always extract text, prefer file upload if supported
            resume_data = llm_service.extract_structured_data(
                file_bytes=contents if provider_supports_files else None,
                file_type=file_type,
                text=raw_text,  # Use extracted text as fallback or primary
                provider=selected_provider_str
            )
        
        # Enhance with library-extracted email if available and LLM didn't find it
        if primary_email and not resume_data.get("personal_info", {}).get("email"):
            if "personal_info" not in resume_data:
                resume_data["personal_info"] = {}
            resume_data["personal_info"]["email"] = primary_email
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {str(e)}")

    # DEBUG: Print what LLM returned
    print(f"DEBUG - LLM returned keys: {list(resume_data.keys())}")
    print(f"DEBUG - Processing mode: {processing_mode_str}")
    print(f"DEBUG - Resume data structure: {resume_data}")

    # 6. Enhanced validation
    validation_result = llm_service.validate_data(resume_data)
    
    # Additional validation for critical fields - more lenient for complete_llm mode
    if processing_mode_str == "complete_llm":
        # For complete LLM mode, only require personal_info (name/email can be extracted separately)
        critical_fields = ["personal_info"]
    else:
        # For hybrid mode, require all critical sections
        critical_fields = ["personal_info", "skills", "experience"]
    
    missing_critical = [field for field in critical_fields if not resume_data.get(field)]
    
    # Email validation - more lenient in complete LLM mode
    final_email = resume_data.get("personal_info", {}).get("email", primary_email)
    if not final_email:
        if processing_mode_str == "complete_llm":
            print("Warning: No email found in complete LLM mode - this might be acceptable for some use cases")
        else:
            raise HTTPException(status_code=400, detail="No email address found in resume. Please ensure your resume contains a valid email address.")
    
    if missing_critical:
        raise HTTPException(
            status_code=400, 
            detail=f"Critical resume sections missing: {missing_critical}. Please ensure your resume contains complete information."
        )

    # 9. Connect to MongoDB
    db = await mongodb.connect()
    
    # 10. Find/Create user using extracted email
    users_col = db["users"]
    user = await users_col.find_one({"primary_email": final_email})
    
    if not user:
        user_id = str(uuid.uuid4())
        user_obj = UserCreate(
            primary_email=final_email,
            name=resume_data.get("personal_info", {}).get("name"),
            phone=resume_data.get("personal_info", {}).get("phone"),
            linkedin=resume_data.get("personal_info", {}).get("linkedin")
        )
        await users_col.insert_one({
            **user_obj.dict(), 
            "user_id": user_id, 
            "created_at": datetime.datetime.utcnow(),
            "verification_status": "pending"
        })
    else:
        user_id = user["user_id"]

    # 11. Create session
    sessions_col = db["sessions"]
    session_id = str(uuid.uuid4())
    session_obj = SessionCreate(
        user_id=user_id, 
        extracted_email=final_email, 
        ip_address=ip_address
    )
    await sessions_col.insert_one({
        **session_obj.dict(), 
        "session_id": session_id, 
        "created_at": datetime.datetime.utcnow(),
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "status": "active"
    })

    # 12. Upload file to S3 and save resume metadata to MongoDB
    resumes_col = db["resumes"]
    resume_id = str(uuid.uuid4())
    
    # Upload to S3
    s3_info = None
    file_path = f"local://{resume.filename}"  # Default fallback
    file_url = None
    s3_upload_attempted = False
    s3_error_reason = None
    
    if s3client.enabled:
        s3_upload_attempted = True
        try:
            print(f"Starting S3 upload for file: {resume.filename}")
            
            # Determine content type
            content_type = "application/pdf" if resume.filename.lower().endswith('.pdf') else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            
            # Upload to S3
            s3_info = s3client.upload_file_bytes(
                file_bytes=contents,
                filename=resume.filename,
                user_id=user_id,
                content_type=content_type
            )
            
            if s3_info:
                file_path = f"s3://{s3_info['bucket']}/{s3_info['key']}"
                file_url = s3_info['url']
                print(f"✅ File uploaded to S3: {file_path}")
            else:
                s3_error_reason = "S3 upload returned None (check AWS permissions)"
                print(f"❌ S3 upload failed: {s3_error_reason}")
        except Exception as e:
            s3_error_reason = f"S3 upload exception: {str(e)}"
            print(f"❌ S3 upload error: {s3_error_reason}")
    else:
        s3_error_reason = "S3 not enabled (check AWS credentials and configuration)"
        print(f"ℹ️  S3 not configured, storing metadata only: {s3_error_reason}")
    
    resume_obj = ResumeCreate(
        session_id=session_id,
        user_id=user_id,
        file_name=resume.filename,
        file_path=file_path,  # S3 path or local fallback
        file_size=len(contents),
        raw_text=raw_text or "Processed directly by LLM",  # May be None if direct file processing
        json_data=resume_data,
        extraction_confidence=validation_result.get("confidence_score", 0.9),
        level=level,
        job_description=job_description
    )
    
    # Add S3 information if available
    resume_doc = {
        **resume_obj.dict(), 
        "resume_id": resume_id, 
        "created_at": datetime.datetime.utcnow(),
        "extraction_method": resume_data.get("processing_method", "hybrid"),  # Direct file or hybrid
        "llm_provider_used": resume_data.get("used_provider", selected_provider_str),
        "library_extracted_emails": extracted_emails,
        "auto_detected_ip": ip_address,
        "file_processing_method": resume_data.get("processing_method", "text_fallback"),
        "intelligent_selection": {
            "processing_mode_selected": processing_mode_str,
            "llm_provider_selected": selected_provider_str,
            "selection_reasoning": selection_reasoning,
            "auto_selected": True
        }
    }
    
    # Add S3 metadata if upload was successful
    if s3_info:
        resume_doc.update({
            "s3_bucket": s3_info['bucket'],
            "s3_key": s3_info['key'],
            "s3_url": s3_info['url'],
            "s3_public_url": s3_info['public_url'],
            "file_storage": "s3",
            "s3_upload_success": True,
            "s3_upload_attempted": s3_upload_attempted
        })
    else:
        resume_doc.update({
            "file_storage": "local_metadata_only",
            "s3_upload_success": False,
            "s3_upload_attempted": s3_upload_attempted,
            "s3_error_reason": s3_error_reason
        })
    
    await resumes_col.insert_one(resume_doc)

    # 13. Return comprehensive structured response with S3 information
    response_data = {
        "status": "success",
        "session_id": session_id,
        "user_id": user_id,
        "resume_id": resume_id,
        "extracted_email": final_email,
        "extraction_confidence": validation_result.get("confidence_score", 0.9),
        "llm_provider_used": resume_data.get("used_provider", selected_provider_str),
        "extraction_method": resume_data.get("processing_method", "hybrid_fallback"),
        "file_processing": "direct_upload" if resume_data.get("processing_method") == "direct_file" else "library_extraction_fallback",
        "processing_mode_used": processing_mode_str,  # Auto-selected processing mode
        "llm_provider_selected": selected_provider_str,  # Auto-selected provider
        "selection_reasoning": selection_reasoning,  # Why this configuration was chosen
        "auto_detected_ip": ip_address,
        "file_info": {
            "filename": resume.filename,
            "size": len(contents),
            "storage_location": "s3" if s3_info else "metadata_only",
            "file_path": file_path
        },
        "extracted_data": {
            "personal_info": resume_data.get("personal_info", {}),
            "skills_count": len(resume_data.get("skills", {}).get("technical_skills", [])),
            "experience_count": len(resume_data.get("experience", [])),
            "education_count": len(resume_data.get("education", [])),
            "projects_count": len(resume_data.get("projects", [])),
            "achievements_count": len(resume_data.get("achievements", []))
        },
        "verification_needed": user is None,  # New user needs verification
        "intelligent_processing": {
            "processing_mode": processing_mode_str,
            "llm_provider_used": selected_provider_str,
            "selection_reasoning": selection_reasoning,
            "auto_selected": True
        },
        "processing_note": f"Mode: {processing_mode_str} | Provider: {selected_provider_str} (intelligently auto-selected)",
        "message": f"Resume processed successfully using {processing_mode_str} mode with {selected_provider_str} LLM"
    }
    
    # Add S3 information if upload was successful
    if s3_info:
        response_data["s3_info"] = {
            "uploaded": True,
            "bucket": s3_info['bucket'],
            "key": s3_info['key'],
            "url": s3_info['url'],
            "public_url": s3_info['public_url'],
            "attempted": s3_upload_attempted
        }
    else:
        response_data["s3_info"] = {
            "uploaded": False,
            "attempted": s3_upload_attempted,
            "reason": s3_error_reason or "S3 not configured or upload failed"
        }
    
    return response_data


@router.get("/download/{resume_id}")
async def download_resume(resume_id: str):
    """
    Generate a presigned URL to download resume file from S3.
    """
    try:
        # Connect to MongoDB
        db = await mongodb.connect()
        resumes_col = db["resumes"]
        
        # Find resume record
        resume = await resumes_col.find_one({"resume_id": resume_id})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Check if file is stored in S3
        if not resume.get("s3_key"):
            raise HTTPException(status_code=404, detail="Resume file not stored in S3")
        
        # Generate presigned URL
        s3_key = resume["s3_key"]
        presigned_url = s3client.generate_presigned_url(s3_key, expiration=3600)  # 1 hour
        
        if not presigned_url:
            raise HTTPException(status_code=500, detail="Failed to generate download URL")
        
        return {
            "status": "success",
            "resume_id": resume_id,
            "filename": resume["file_name"],
            "download_url": presigned_url,
            "expires_in": 3600,
            "file_size": resume["file_size"],
            "upload_date": resume["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/user/{user_id}/resumes")
async def list_user_resumes(user_id: str):
    """
    List all resumes for a specific user with download links.
    """
    try:
        # Connect to MongoDB
        db = await mongodb.connect()
        resumes_col = db["resumes"]
        
        # Find all resumes for user
        cursor = resumes_col.find({"user_id": user_id}).sort("created_at", -1)
        resumes = await cursor.to_list(length=None)
        
        if not resumes:
            return {
                "status": "success",
                "user_id": user_id,
                "resumes": [],
                "total_count": 0
            }
        
        # Format resume list with download info
        resume_list = []
        for resume in resumes:
            resume_info = {
                "resume_id": resume["resume_id"],
                "filename": resume["file_name"],
                "upload_date": resume["created_at"],
                "file_size": resume["file_size"],
                "extraction_confidence": resume.get("extraction_confidence", 0.0),
                "processing_mode": resume.get("user_switches", {}).get("processing_mode_requested", "unknown"),
                "llm_provider": resume.get("llm_provider_used", "unknown"),
                "level": resume.get("level", "unknown"),
                "storage_type": resume.get("file_storage", "unknown"),
                "s3_available": bool(resume.get("s3_key"))
            }
            
            # Add download URL if file is in S3
            if resume.get("s3_key"):
                try:
                    download_url = s3client.generate_presigned_url(resume["s3_key"], expiration=3600)
                    if download_url:
                        resume_info["download_url"] = download_url
                        resume_info["download_expires_in"] = 3600
                except Exception as e:
                    print(f"Failed to generate download URL for {resume['resume_id']}: {e}")
            
            resume_list.append(resume_info)
        
        return {
            "status": "success",
            "user_id": user_id,
            "resumes": resume_list,
            "total_count": len(resume_list),
            "s3_enabled": s3client.enabled
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list resumes: {str(e)}")


@router.delete("/delete/{resume_id}")
async def delete_resume(resume_id: str):
    """
    Delete resume file from S3 and remove metadata from MongoDB.
    """
    try:
        # Connect to MongoDB
        db = await mongodb.connect()
        resumes_col = db["resumes"]
        
        # Find resume record
        resume = await resumes_col.find_one({"resume_id": resume_id})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Delete from S3 if exists
        s3_deleted = False
        if resume.get("s3_key"):
            s3_deleted = s3client.delete_file(resume["s3_key"])
        
        # Delete from MongoDB
        result = await resumes_col.delete_one({"resume_id": resume_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete resume metadata")
        
        return {
            "status": "success",
            "resume_id": resume_id,
            "filename": resume["file_name"],
            "metadata_deleted": True,
            "s3_file_deleted": s3_deleted,
            "message": "Resume deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.get("/s3/status")
async def get_s3_status():
    """
    Check S3 configuration and connection status.
    """
    return {
        "s3_enabled": s3client.enabled,
        "bucket_name": s3client.bucket if s3client.enabled else None,
        "aws_region": settings.AWS_REGION,
        "status": "connected" if s3client.enabled else "not_configured"
    }
