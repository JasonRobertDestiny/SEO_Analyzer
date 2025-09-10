"""
Pydantic models for request and response validation
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, HttpUrl, Field, validator


class AnalyzeRequest(BaseModel):
    """Request model for website analysis"""
    url: HttpUrl = Field(..., description="Website URL to analyze")
    sitemap_url: Optional[HttpUrl] = Field(None, description="Sitemap URL (optional)")
    analyze_headings: bool = Field(False, description="Analyze heading structure")
    analyze_extra_tags: bool = Field(False, description="Analyze additional meta tags")
    follow_links: bool = Field(True, description="Follow links during crawling")
    run_llm_analysis: bool = Field(False, description="Run LLM-powered analysis")
    analysis_mode: str = Field("fast", description="Analysis mode: lightning, super_fast, fast, full")
    ai_mode: str = Field("lightweight", description="AI analysis mode: lightweight, full")
    max_pages: Optional[int] = Field(20, description="Maximum pages to analyze")

    @validator('url')
    def validate_url_scheme(cls, v):
        if not isinstance(v, str):
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @validator('analysis_mode')
    def validate_analysis_mode(cls, v):
        allowed_modes = ['lightning', 'super_fast', 'fast', 'full']
        if v not in allowed_modes:
            raise ValueError(f'Analysis mode must be one of: {", ".join(allowed_modes)}')
        return v
    
    @validator('ai_mode')
    def validate_ai_mode(cls, v):
        allowed_modes = ['lightweight', 'full']
        if v not in allowed_modes:
            raise ValueError(f'AI mode must be one of: {", ".join(allowed_modes)}')
        return v
    
    @validator('max_pages')
    def validate_max_pages(cls, v):
        if v is not None and v < 1:
            raise ValueError('max_pages must be at least 1')
        if v is not None and v > 100:
            raise ValueError('max_pages cannot exceed 100 for performance reasons')
        return v


class AnalyzeResponse(BaseModel):
    """Response model for website analysis"""
    success: bool = Field(..., description="Whether the analysis was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Analysis results")
    error: Optional[str] = Field(None, description="Error message if failed")
    analyzed_at: Optional[str] = Field(None, description="Timestamp of analysis")
    analyzed_url: Optional[str] = Field(None, description="URL that was analyzed")


class DownloadRequest(BaseModel):
    """Request model for report download"""
    result: Dict[str, Any] = Field(..., description="Analysis results to include in report")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str = Field(..., description="Error details")
    success: bool = Field(False, description="Always false for error responses")


class TaskStatus(BaseModel):
    """Model for analysis task status"""
    task_id: str = Field(..., description="Unique task identifier")
    status: str = Field(..., description="Current status (pending, running, completed, failed)")
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    message: Optional[str] = Field(None, description="Status message")
    result: Optional[Dict[str, Any]] = Field(None, description="Analysis results (when completed)")
    error: Optional[str] = Field(None, description="Error message (if failed)")


class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field("healthy", description="Application health status")
    version: str = Field(..., description="Application version")
    timestamp: str = Field(..., description="Check timestamp")