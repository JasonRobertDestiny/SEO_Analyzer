"""
FastAPI main application
"""
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import tempfile
from datetime import datetime
import uuid
import json
import traceback

from app.api.endpoints import router
from app.models.schemas import TaskStatus
from app.core.task_manager import task_manager
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting SmartSEO FastAPI application...")
    yield
    # Shutdown
    print("Shutting down SmartSEO FastAPI application...")


# Create FastAPI app
app = FastAPI(
    title="SmartSEO Analyzer",
    description="AI-powered SEO analysis tool",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Register exception handlers
register_exception_handlers(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index_modern.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint"""
    return Response(status_code=204)


@app.get("/img/icon_wechat.png")
async def wechat_icon():
    """WeChat icon endpoint"""
    raise HTTPException(status_code=404, detail="Not found")




@app.get("/health")
async def health_check():
    """Health check endpoint with basic system info"""
    import psutil
    
    try:
        # 获取基本系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": f"{cpu_percent:.1f}%",
                "memory_usage": f"{memory.percent:.1f}%",
                "memory_available": f"{memory.available / (1024**3):.1f}GB",
                "disk_usage": f"{disk.percent:.1f}%",
                "tasks_count": len(task_manager.tasks)
            }
        }
    except Exception as e:
        return {
            "status": "healthy",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "error": f"无法获取系统信息: {str(e)}",
            "tasks_count": len(task_manager.tasks)
        }


# Task status endpoint is handled in the API router, removing duplicate


