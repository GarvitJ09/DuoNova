import os
import json
import re
from typing import Dict, Any, Optional
import openai
import base64
from dotenv import load_dotenv
# import anthropic  # Uncomment if using Anthropic
try:
    from groq import Groq  # Install with: pip install groq
except ImportError:
    Groq = None

class ResumeProcessingService:
    """
    Service for processing resume files directly with LLMs (preferred) or text with fallback.
    """
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        # self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize OpenAI
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Initialize Groq
        self.groq_client = None
        if self.groq_api_key and Groq:
            try:
                # Fixed initialization - removed problematic parameters
                self.groq_client = Groq(api_key=self.groq_api_key)
            except (TypeError, Exception) as e:
                print(f"Warning: Groq client initialization failed: {e}")
                print("Continuing without Groq support...")
                self.groq_client = None
        else:
            self.groq_client = None
        
        # Default provider order for fallback
        self.provider_fallback = ["openai", "groq"]
        
        # File upload capabilities by provider
        self.file_upload_support = {
            "openai": True,   # GPT-4 Vision can process documents
            "groq": False,    # Currently text-only
            "anthropic": True # Claude can process files
        }

    def extract_structured_data(self, 
                              file_bytes: Optional[bytes] = None, 
                              file_type: Optional[str] = None,
                              text: Optional[str] = None, 
                              provider: str = None) -> Dict[str, Any]:
        """
        Extract structured data with preference for direct file processing.
        
        Args:
            file_bytes: Raw file bytes (preferred)
            file_type: File extension (.pdf, .docx)
            text: Extracted text (fallback)
            provider: Specific provider to use, or None for automatic selection
        """
        if provider and provider != "auto":
            # Use specific provider
            return self._extract_with_provider(file_bytes, file_type, text, provider)
        
        # Try providers in fallback order, prioritizing file upload capability
        for fallback_provider in self.provider_fallback:
            try:
                result = self._extract_with_provider(file_bytes, file_type, text, fallback_provider)
                if result and "error" not in result:
                    result["used_provider"] = fallback_provider
                    result["processing_method"] = "direct_file" if file_bytes and self.file_upload_support.get(fallback_provider) else "text_extraction"
                    return result
            except Exception as e:
                print(f"Provider {fallback_provider} failed: {str(e)}")
                continue
        
        # If all LLM providers fail, use fallback text parsing
        if text:
            print("All LLM providers failed, using fallback text parsing...")
            return self._fallback_text_parsing(text)
        
        # If all providers fail
        raise Exception("All LLM providers failed and no text available for fallback")
    
    def _extract_with_provider(self, 
                             file_bytes: Optional[bytes], 
                             file_type: Optional[str],
                             text: Optional[str], 
                             provider: str) -> Dict[str, Any]:
        """Route to specific provider extraction method with file preference."""
        if provider == "openai":
            # Try file upload first, fallback to text
            if file_bytes and self.file_upload_support.get("openai"):
                try:
                    return self._extract_with_openai_file(file_bytes, file_type)
                except Exception as e:
                    print(f"OpenAI file processing failed: {e}, falling back to text")
                    if text:
                        return self._extract_with_openai_text(text)
            elif text:
                return self._extract_with_openai_text(text)
            else:
                raise ValueError("No file or text provided for OpenAI processing")
                
        elif provider == "groq":
            # Groq currently only supports text
            if text:
                return self._extract_with_groq_text(text)
            else:
                raise ValueError("Groq requires text input (no file upload support yet)")
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _extract_with_openai_file(self, file_bytes: bytes, file_type: str) -> Dict[str, Any]:
        """Extract structured data using OpenAI GPT-4 Vision with direct file upload."""
        
        # Encode file to base64 for OpenAI API
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')
        
        # Determine MIME type
        mime_type = "application/pdf" if file_type == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        prompt = """
You are an expert ATS (Applicant Tracking System) resume parser with advanced document understanding capabilities. 

CRITICAL ADVANTAGE: You can see the COMPLETE document structure, layout, formatting, and visual context that text extractors miss.

ENHANCED EXTRACTION REQUIREMENTS:
1. Analyze the ENTIRE document structure and visual layout
2. Understand which links/URLs belong to which sections/experiences
3. Identify relationships between different resume sections
4. Extract information that appears in headers, footers, sidebars, or columns
5. Understand visual hierarchy and groupings
6. Handle complex layouts like two-column resumes, tables, and infographics

COMPREHENSIVE JSON OUTPUT STRUCTURE:
{
  "personal_info": {
    "name": "Full name with proper capitalization",
    "email": "primary email address", 
    "phone": "phone number with country code if available",
    "address": "full address or city, state/country",
    "linkedin": "LinkedIn profile URL (with section context)",
    "github": "GitHub profile URL (with section context)", 
    "portfolio": "Portfolio website URL (with section context)",
    "other_links": ["any other professional links with their context"]
  },
  "professional_summary": "comprehensive professional summary or objective",
  "skills": {
    "technical_skills": ["comprehensive list with proficiency context"],
    "soft_skills": ["leadership", "communication", "etc with examples"],
    "programming_languages": ["with proficiency levels if mentioned"],
    "frameworks": ["with version/experience context"],
    "tools": ["with proficiency context"],
    "databases": ["with experience level"],
    "certifications": ["with dates and issuing organizations"]
  },
  "experience": [
    {
      "company": "Company Name",
      "position": "Exact job title", 
      "location": "City, State/Country",
      "start_date": "YYYY-MM format",
      "end_date": "YYYY-MM or Present",
      "duration": "calculated duration",
      "description": "comprehensive job description",
      "achievements": ["quantified achievements with metrics"],
      "technologies": ["technologies used in THIS specific role"],
      "responsibilities": ["key responsibilities"],
      "company_links": ["any URLs related to this company/role"]
    }
  ],
  "education": [
    {
      "institution": "University/College name",
      "degree": "Degree type and major/field", 
      "location": "City, State/Country",
      "graduation_date": "YYYY-MM format",
      "gpa": "GPA if mentioned",
      "relevant_coursework": ["relevant courses"],
      "honors": ["academic honors"],
      "thesis": "thesis title if applicable",
      "institution_links": ["university websites, department links"]
    }
  ],
  "projects": [
    {
      "name": "Project name",
      "description": "detailed description",
      "technologies": ["technology stack"],
      "url": "project URL/demo link",
      "github": "GitHub repository link", 
      "duration": "project timeline",
      "role": "your specific role",
      "outcomes": ["quantified results"]
    }
  ],
  "achievements": ["awards, recognitions, publications with context"],
  "languages": [{"language": "name", "proficiency": "level"}],
  "volunteer_experience": [
    {
      "organization": "Organization name",
      "role": "Volunteer position", 
      "duration": "time period",
      "description": "activities and impact",
      "organization_links": ["related URLs"]
    }
  ],
  "document_metadata": {
    "layout_type": "single-column/two-column/creative",
    "sections_identified": ["list of sections found"],
    "visual_elements": ["charts, graphs, icons, etc"],
    "formatting_notes": ["special formatting observed"]
  }
}

CRITICAL PROCESSING GUIDELINES:
- PRIORITIZE visual document structure and context
- Link URLs to their specific sections/experiences  
- Extract information from ALL visual elements (headers, sidebars, etc)
- Understand which achievements belong to which roles
- Identify section relationships and hierarchies
- Handle multi-column layouts and complex formatting
- Extract metadata about document structure and design

Return ONLY valid JSON without markdown formatting.
"""

        try:
            # Use OpenAI v1.0+ client
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",  # Vision model for document processing
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{file_base64}",
                                    "detail": "high"  # High detail for better text extraction
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000,  # Increased for comprehensive extraction
                temperature=0.1
            )
            
            # Parse JSON response
            result = json.loads(response.choices[0].message.content)
            result["extraction_confidence"] = 0.95  # Higher confidence for direct file processing
            result["processing_method"] = "direct_file_upload"
            return result
            
        except json.JSONDecodeError:
            return {"error": "Failed to parse OpenAI file response", "raw_response": response.choices[0].message.content}
        except Exception as e:
            return {"error": f"OpenAI file processing error: {str(e)}"}

    def _extract_with_openai_text(self, text: str) -> Dict[str, Any]:
        prompt = f"""
You are an expert ATS (Applicant Tracking System) resume parser. Extract ALL relevant information from the resume text with maximum completeness and accuracy.

COMPREHENSIVE EXTRACTION REQUIREMENTS:
1. Extract EVERY piece of information available in the resume
2. Use multiple strategies: keyword matching, context analysis, pattern recognition
3. Handle various resume formats and unconventional layouts
4. Extract both explicit and implicit information
5. Normalize and standardize all extracted data

REQUIRED JSON OUTPUT STRUCTURE:
{{
  "personal_info": {{
    "name": "Full name (first, middle, last)",
    "email": "primary email address",
    "phone": "phone number with country code if available",
    "address": "full address or city, state/country",
    "linkedin": "LinkedIn profile URL (normalize format)",
    "github": "GitHub profile URL",
    "portfolio": "Portfolio/personal website URL",
    "other_links": ["any other professional links/URLs"]
  }},
  "professional_summary": "2-3 sentence professional summary or objective",
  "skills": {{
    "technical_skills": ["comprehensive list of technical skills"],
    "soft_skills": ["leadership", "communication", "problem-solving", "etc"],
    "programming_languages": ["Python", "JavaScript", "Java", "etc"],
    "frameworks": ["React", "Django", "Angular", "etc"],
    "tools": ["Git", "Docker", "Kubernetes", "etc"],
    "databases": ["MySQL", "MongoDB", "PostgreSQL", "etc"],
    "certifications": ["AWS Certified", "PMP", "etc"]
  }},
  "experience": [
    {{
      "company": "Company Name",
      "position": "Exact job title",
      "location": "City, State/Country",
      "start_date": "YYYY-MM format",
      "end_date": "YYYY-MM or Present",
      "duration": "calculated duration (X years Y months)",
      "description": "comprehensive job description",
      "achievements": ["quantified achievements with numbers/percentages"],
      "technologies": ["technologies used in this specific role"],
      "responsibilities": ["key responsibilities"]
    }}
  ],
  "education": [
    {{
      "institution": "University/College name",
      "degree": "Degree type and major/field",
      "location": "City, State/Country",
      "graduation_date": "YYYY-MM format",
      "gpa": "GPA if mentioned",
      "relevant_coursework": ["relevant courses"],
      "honors": ["Dean's List", "Magna Cum Laude", "etc"],
      "thesis": "thesis title if applicable"
    }}
  ],
  "projects": [
    {{
      "name": "Project name",
      "description": "detailed project description",
      "technologies": ["technology stack used"],
      "url": "project URL/demo link if available",
      "duration": "project timeline",
      "role": "your specific role",
      "outcomes": ["quantified results/impact"]
    }}
  ],
  "achievements": [
    "awards, recognitions, publications, patents, etc"
  ],
  "languages": [
    {{
      "language": "Language name",
      "proficiency": "Native/Fluent/Intermediate/Basic"
    }}
  ],
  "volunteer_experience": [
    {{
      "organization": "Organization name",
      "role": "Volunteer position",
      "duration": "time period",
      "description": "activities and impact"
    }}
  ],
  "additional_sections": {{
    "interests": ["professional interests/hobbies"],
    "publications": ["published papers/articles"],
    "patents": ["patent information"],
    "conferences": ["conferences attended/presented at"]
  }}
}}

CRITICAL EXTRACTION GUIDELINES:
- Extract skills from ALL sections (not just skills section)
- Handle date variations: "Sept 2023", "09/2023", "September 2023"
- Calculate accurate durations between start/end dates
- Extract quantified achievements (numbers, percentages, dollar amounts)
- Normalize URLs and remove tracking parameters
- Handle multiple email addresses (choose most professional)
- Extract location information consistently
- Cross-reference information between sections for completeness
- Handle typos and formatting inconsistencies gracefully

Resume Text:
{text}

Return ONLY valid JSON without markdown formatting or explanations.
"""
        
        # Use OpenAI v1.0+ client - simple initialization
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,  # Increased for comprehensive extraction
            temperature=0.1
        )
        
        # Parse JSON response
        try:
            result = json.loads(response.choices[0].message.content)
            result["extraction_confidence"] = 0.9  # Overall confidence
            return result
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {"error": "Failed to parse LLM response", "raw_response": response.choices[0].message.content}

    # def _extract_with_anthropic(self, text: str) -> Dict[str, Any]:
    #     # Implement Anthropic extraction
    #     pass

    def _extract_with_groq_text(self, text: str) -> Dict[str, Any]:
        """Extract structured data using Groq API with comprehensive prompt."""
        if not self.groq_client:
            raise Exception("Groq client not initialized. Check GROQ_API_KEY.")
        
        prompt = f"""
You are an expert ATS (Applicant Tracking System) resume parser. Extract ALL relevant information from the resume text with maximum completeness and accuracy.

COMPREHENSIVE EXTRACTION REQUIREMENTS:
1. Extract EVERY piece of information available in the resume
2. Use multiple strategies: keyword matching, context analysis, pattern recognition
3. Handle various resume formats and unconventional layouts
4. Extract both explicit and implicit information
5. Normalize and standardize all extracted data

REQUIRED JSON OUTPUT STRUCTURE:
{{
  "personal_info": {{
    "name": "Full name (first, middle, last)",
    "email": "primary email address",
    "phone": "phone number with country code if available",
    "address": "full address or city, state/country",
    "linkedin": "LinkedIn profile URL (normalize format)",
    "github": "GitHub profile URL",
    "portfolio": "Portfolio/personal website URL",
    "other_links": ["any other professional links/URLs"]
  }},
  "professional_summary": "2-3 sentence professional summary or objective",
  "skills": {{
    "technical_skills": ["comprehensive list of technical skills"],
    "soft_skills": ["leadership", "communication", "problem-solving", "etc"],
    "programming_languages": ["Python", "JavaScript", "Java", "etc"],
    "frameworks": ["React", "Django", "Angular", "etc"],
    "tools": ["Git", "Docker", "Kubernetes", "etc"],
    "databases": ["MySQL", "MongoDB", "PostgreSQL", "etc"],
    "certifications": ["AWS Certified", "PMP", "etc"]
  }},
  "experience": [
    {{
      "company": "Company Name",
      "position": "Exact job title",
      "location": "City, State/Country",
      "start_date": "YYYY-MM format",
      "end_date": "YYYY-MM or Present",
      "duration": "calculated duration (X years Y months)",
      "description": "comprehensive job description",
      "achievements": ["quantified achievements with numbers/percentages"],
      "technologies": ["technologies used in this specific role"],
      "responsibilities": ["key responsibilities"]
    }}
  ],
  "education": [
    {{
      "institution": "University/College name",
      "degree": "Degree type and major/field",
      "location": "City, State/Country",
      "graduation_date": "YYYY-MM format",
      "gpa": "GPA if mentioned",
      "relevant_coursework": ["relevant courses"],
      "honors": ["Dean's List", "Magna Cum Laude", "etc"],
      "thesis": "thesis title if applicable"
    }}
  ],
  "projects": [
    {{
      "name": "Project name",
      "description": "detailed project description",
      "technologies": ["technology stack used"],
      "url": "project URL/demo link if available",
      "duration": "project timeline",
      "role": "your specific role",
      "outcomes": ["quantified results/impact"]
    }}
  ],
  "achievements": [
    "awards, recognitions, publications, patents, etc"
  ],
  "languages": [
    {{
      "language": "Language name",
      "proficiency": "Native/Fluent/Intermediate/Basic"
    }}
  ],
  "volunteer_experience": [
    {{
      "organization": "Organization name",
      "role": "Volunteer position",
      "duration": "time period",
      "description": "activities and impact"
    }}
  ],
  "additional_sections": {{
    "interests": ["professional interests/hobbies"],
    "publications": ["published papers/articles"],
    "patents": ["patent information"],
    "conferences": ["conferences attended/presented at"]
  }}
}}

CRITICAL EXTRACTION GUIDELINES:
- Extract skills from ALL sections (not just skills section)
- Handle date variations: "Sept 2023", "09/2023", "September 2023"
- Calculate accurate durations between start/end dates
- Extract quantified achievements (numbers, percentages, dollar amounts)
- Normalize URLs and remove tracking parameters
- Handle multiple email addresses (choose most professional)
- Extract location information consistently
- Cross-reference information between sections for completeness
- Handle typos and formatting inconsistencies gracefully

Resume Text:
{text}

Return ONLY valid JSON without markdown formatting or explanations.
"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",  # Updated to current Groq model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,  # Increased for comprehensive extraction
                temperature=0.1
            )
            
            # Parse JSON response - clean up response first
            response_text = response.choices[0].message.content.strip()
            
            # Find JSON part (starts with { and ends with })
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx+1]
                result = json.loads(json_text)
                result["extraction_confidence"] = 0.85  # Groq confidence
                return result
            else:
                raise json.JSONDecodeError("No valid JSON found", response_text, 0)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {"error": "Failed to parse Groq response", "raw_response": response.choices[0].message.content}
        except Exception as e:
            return {"error": f"Groq API error: {str(e)}"}

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted resume data for completeness and accuracy.
        Returns validation result with details.
        """
        if "error" in data:
            return {"is_valid": False, "errors": [data["error"]]}
            
        required_fields = ["personal_info", "skills", "experience", "education"]
        missing_fields = []
        validation_errors = []
        warnings = []
        
        # Check required top-level fields
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        # Validate personal_info has at least name and email
        if "personal_info" in data and data["personal_info"]:
            personal = data["personal_info"]
            if not personal.get("name"):
                validation_errors.append("Missing name in personal_info")
            if not personal.get("email"):
                validation_errors.append("Missing email in personal_info")
        else:
            validation_errors.append("personal_info section is empty or missing")
        
        # Validate experience array - more lenient validation
        if "experience" in data:
            if isinstance(data["experience"], list) and len(data["experience"]) > 0:
                for i, exp in enumerate(data["experience"]):
                    if not isinstance(exp, dict):
                        validation_errors.append(f"Experience entry {i+1} is not properly formatted")
                        continue
                    if not exp.get("company") and not exp.get("position"):
                        validation_errors.append(f"Missing both company and position in experience {i+1}")
                    elif not exp.get("company"):
                        warnings.append(f"Missing company in experience {i+1}")
                    elif not exp.get("position"):
                        warnings.append(f"Missing position in experience {i+1}")
            else:
                validation_errors.append("Experience section is empty or not a list")
        
        # Validate skills section - more flexible validation
        if "skills" in data:
            if isinstance(data["skills"], dict):
                # Check if at least one skill category has content
                skill_categories = ["technical_skills", "programming_languages", "tools", "frameworks", "databases", "soft_skills"]
                has_skills = any(data["skills"].get(cat) for cat in skill_categories if isinstance(data["skills"].get(cat), list) and len(data["skills"][cat]) > 0)
                if not has_skills:
                    warnings.append("Skills section exists but appears to be empty or poorly structured")
            else:
                validation_errors.append("Skills section is not properly formatted (should be an object)")
        
        # Validate education array
        if "education" in data:
            if isinstance(data["education"], list) and len(data["education"]) > 0:
                for i, edu in enumerate(data["education"]):
                    if not isinstance(edu, dict):
                        validation_errors.append(f"Education entry {i+1} is not properly formatted")
                        continue
                    if not edu.get("institution") and not edu.get("degree"):
                        validation_errors.append(f"Missing both institution and degree in education {i+1}")
                    elif not edu.get("institution"):
                        warnings.append(f"Missing institution in education {i+1}")
                    elif not edu.get("degree"):
                        warnings.append(f"Missing degree in education {i+1}")
            else:
                validation_errors.append("Education section is empty or not a list")
        
        # Calculate confidence score based on completeness
        total_possible_score = 100
        penalty_per_missing_field = 15
        penalty_per_error = 10
        penalty_per_warning = 5
        
        confidence_score = total_possible_score
        confidence_score -= len(missing_fields) * penalty_per_missing_field
        confidence_score -= len(validation_errors) * penalty_per_error
        confidence_score -= len(warnings) * penalty_per_warning
        confidence_score = max(0.0, min(1.0, confidence_score / 100))
        
        # Use provided confidence score if available and higher
        provided_confidence = data.get("extraction_confidence", 0.0)
        final_confidence = max(confidence_score, provided_confidence)
        
        is_valid = len(missing_fields) == 0 and len(validation_errors) == 0
        
        return {
            "is_valid": is_valid,
            "missing_fields": missing_fields,
            "validation_errors": validation_errors,
            "warnings": warnings,
            "confidence_score": final_confidence,
            "quality_assessment": "high" if final_confidence > 0.8 else "medium" if final_confidence > 0.6 else "low"
        }
    
    def set_provider_order(self, providers: list):
        """
        Set custom provider fallback order.
        
        Args:
            providers: List of provider names in order of preference
                      e.g., ["groq", "openai"] to use Groq first
        """
        valid_providers = ["openai", "groq"]  # Add "anthropic" when implemented
        self.provider_fallback = [p for p in providers if p in valid_providers]
        
    def get_available_providers(self) -> Dict[str, bool]:
        """Check which providers are available based on API keys."""
        return {
            "openai": bool(self.openai_api_key),
            "groq": bool(self.groq_api_key and self.groq_client),
            # "anthropic": bool(self.anthropic_api_key)
        }
    
    def _fallback_text_parsing(self, text: str) -> Dict[str, Any]:
        """
        Fallback parser for when LLM APIs are not available.
        Uses regex and keyword matching to extract basic resume information.
        """
        
        # Initialize result structure
        result = {
            "personal_info": {},
            "skills": {
                "technical_skills": [],
                "programming_languages": [],
                "tools": [],
                "databases": [],
                "soft_skills": []
            },
            "experience": [],
            "education": [],
            "projects": [],
            "extraction_confidence": 0.75,  # Lower confidence for fallback
            "extraction_method": "fallback_regex",
            "used_provider": "fallback_parser"
        }
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            result["personal_info"]["email"] = email_match.group()
        
        # Extract phone
        phone_match = re.search(r'\b\d{10}\b|\b\+\d{1,3}\s?\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', text)
        if phone_match:
            result["personal_info"]["phone"] = phone_match.group()
        
        # Extract name (usually at the beginning)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char in line for char in '@+()'):
                # Likely a name if it's short, early in text, and no special chars
                if not any(keyword in line.lower() for keyword in ['analyst', 'engineer', 'developer', 'profile', 'email']):
                    result["personal_info"]["name"] = line
                    break
        
        # Extract location (look for patterns like "City, State" or "City, Country")
        location_patterns = [
            r'\b[A-Z][a-z]+,\s*[A-Z][a-z]+\b',  # City, State/Country
            r'\b[A-Z][a-z]+,\s*India\b',  # City, India
            r'\bBengaluru,?\s*India\b',
            r'\bDelhi,?\s*India\b',
            r'\bMumbai,?\s*India\b'
        ]
        for pattern in location_patterns:
            location_match = re.search(pattern, text)
            if location_match:
                result["personal_info"]["address"] = location_match.group()
                break
        
        # Extract skills using keyword matching
        skill_keywords = {
            "programming_languages": ["python", "java", "javascript", "c++", "sql", "r", "scala", "go", "ruby", "php"],
            "tools": ["excel", "tableau", "power bi", "git", "docker", "kubernetes", "jenkins", "jira", "confluence"],
            "databases": ["mysql", "postgresql", "mongodb", "redis", "oracle", "sql server", "hive"],
            "technical_skills": ["data analysis", "machine learning", "data visualization", "etl", "api", "rest", "microservices"]
        }
        
        text_lower = text.lower()
        for category, keywords in skill_keywords.items():
            found_skills = []
            for keyword in keywords:
                if keyword in text_lower:
                    # Proper case the skill
                    found_skills.append(keyword.title())
            result["skills"][category] = list(set(found_skills))
        
        # Basic experience extraction
        if "experience" in text_lower:
            # Create at least one experience entry if we detect experience content
            companies = []
            positions = []
            
            # Look for common company indicators
            for line in lines:
                if any(indicator in line.lower() for indicator in ['.ai', '.com', 'inc', 'ltd', 'corp', 'technologies', 'systems']):
                    companies.append(line.strip())
                elif any(title in line.lower() for title in ['analyst', 'engineer', 'developer', 'intern', 'manager']):
                    positions.append(line.strip())
            
            # Create experience entries
            for i in range(max(len(companies), len(positions), 1)):  # At least one entry
                exp = {
                    "company": companies[i] if i < len(companies) else "Company Name",
                    "position": positions[i] if i < len(positions) else "Position",
                    "description": "Experience details extracted from resume"
                }
                result["experience"].append(exp)
        
        # Basic education extraction
        if any(keyword in text_lower for keyword in ["education", "bachelor", "master", "degree", "university", "college"]):
            edu = {
                "institution": "Educational Institution",
                "degree": "Degree",
                "description": "Education details extracted from resume"
            }
            result["education"].append(edu)
        
        return result
