"""
API endpoints for SEO analysis
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi import Depends
from typing import Dict, Any
import os
import tempfile
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from app.models.schemas import (
    AnalyzeRequest, 
    AnalyzeResponse, 
    DownloadRequest,
    TaskStatus
)
from app.core.task_manager import task_manager
from app.exceptions.handlers import SEOAnalysisError

router = APIRouter()


@router.post("/analyze", response_model=Dict[str, str])
async def analyze_website(request: AnalyzeRequest):
    """
    Start a new website analysis task
    
    This endpoint initiates an asynchronous SEO analysis of the provided website URL.
    The analysis runs in the background and can be monitored using the task_id.
    """
    try:
        # Convert request to dict
        analysis_params = {
            "url": str(request.url),
            "sitemap_url": str(request.sitemap_url) if request.sitemap_url else None,
            "analyze_headings": request.analyze_headings,
            "analyze_extra_tags": request.analyze_extra_tags,
            "follow_links": request.follow_links,
            "run_llm_analysis": request.run_llm_analysis,
            "analysis_mode": request.analysis_mode,
            "ai_mode": request.ai_mode,
            "max_pages": request.max_pages
        }
        
        # Create analysis task
        task_id = task_manager.create_task(analysis_params)
        
        return {
            "task_id": task_id,
            "message": "Analysis started",
            "status_url": f"/api/v1/tasks/{task_id}"
        }
        
    except Exception as e:
        raise SEOAnalysisError(
            message="Failed to start analysis",
            detail=str(e)
        )


@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """
    Get the status of an analysis task
    
    Returns the current status, progress, and results (if completed) 
    for the specified analysis task.
    """
    status = task_manager.get_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatus(**status)


@router.get("/tasks/{task_id}/result")
async def get_analysis_result(task_id: str):
    """
    Get the analysis result for a completed task
    
    Returns the full analysis results if the task has completed.
    Returns 404 if the task doesn't exist or hasn't completed.
    """
    result = task_manager.get_result(task_id)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="Task not found or not completed"
        )
    
    return {
        "success": True,
        "data": result,
        "analyzed_at": result.get("analyzed_at"),
        "analyzed_url": result.get("analyzed_url")
    }


@router.post("/download_report")
async def download_report(request: DownloadRequest):
    """
    Generate and download an HTML report
    
    Creates an HTML report from the analysis results and returns it as a downloadable file.
    """
    try:
        if not request.result:
            raise SEOAnalysisError("No analysis results provided")
        
        # Get template path - use modern template
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report_modern.html")
        
        # Convert result to proper format for template
        result_data = request.result
        
        # Ensure required fields exist with safe defaults
        if 'page_count_summary' not in result_data:
            result_data['page_count_summary'] = {
                'total': len(result_data.get('pages', [])),
                'successful': len([p for p in result_data.get('pages', []) if not p.get('error')])
            }
        
        if 'keywords' not in result_data:
            result_data['keywords'] = {'words': [], 'bigrams': []}
            
        if 'total_time' not in result_data:
            result_data['total_time'] = 0
            
        if 'errors' not in result_data:
            result_data['errors'] = []
            
        # Generate HTML content
        html_content = template.render(result=result_data)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.html', 
            delete=False, 
            encoding='utf-8'
        )
        temp_file.write(html_content)
        temp_file.close()
        
        # Generate filename
        analyzed_url = request.result.get('analyzed_url', 'website')
        filename = f"seo_report_{analyzed_url.replace('://', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        return FileResponse(
            temp_file.name,
            media_type='text/html',
            filename=filename
        )
        
    except Exception as e:
        raise SEOAnalysisError(
            message="Failed to generate report",
            detail=str(e)
        )