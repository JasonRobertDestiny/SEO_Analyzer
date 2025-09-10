"""
Task manager for handling async analysis jobs with persistence
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Optional, Any
import uuid
import os
import pickle

from pyseoanalyzer.analyzer import analyze
from pyseoanalyzer.analyzer_super_fast import analyze_super_fast, analyze_lightning_fast
from pyseoanalyzer.analyzer_fast_async import analyze_fast_async
from pyseoanalyzer.llm_analyst import LLMSEOEnhancer


class TaskManager:
    """Manages background analysis tasks with persistence"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self.tasks_file = "tasks_cache.pkl"
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'rb') as f:
                    self.tasks = pickle.load(f)
                print(f"Loaded {len(self.tasks)} tasks from cache")
        except Exception as e:
            print(f"Failed to load tasks: {e}")
            self.tasks = {}
    
    def _save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.tasks_file, 'wb') as f:
                pickle.dump(self.tasks, f)
        except Exception as e:
            print(f"Failed to save tasks: {e}")
            # Don't raise the exception to avoid disrupting the main flow
    
    def create_task(self, analysis_params: Dict[str, Any]) -> str:
        """Create a new analysis task"""
        task_id = str(uuid.uuid4())
        
        self.tasks[task_id] = {
            "status": "pending",
            "progress": 0,
            "message": "Task created",
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat()
        }
        
        # Save tasks immediately
        self._save_tasks()
        
        # Start the analysis in background
        asyncio.create_task(self._run_analysis(task_id, analysis_params))
        
        return task_id
    
    async def _run_analysis(self, task_id: str, params: Dict[str, Any]):
        """Run the analysis in background"""
        try:
            self.tasks[task_id].update({
                "status": "running",
                "progress": 10,
                "message": "正在初始化分析..."
            })
            self._save_tasks()
            
            # Update progress
            self.tasks[task_id].update({
                "progress": 20,
                "message": "正在获取网站内容..."
            })
            self._save_tasks()
            
            # Run analysis with the new async analyzers
            self.tasks[task_id].update({
                "progress": 30,
                "message": "正在运行基础分析..."
            })
            self._save_tasks()
            
            # Choose analysis mode
            analysis_mode = params.get("analysis_mode", "super_fast")
            max_pages = params.get("max_pages", 10)
            
            try:
                if analysis_mode == "lightning":
                    result = await analyze_lightning_fast(params["url"])
                elif analysis_mode == "super_fast":
                    result = await analyze_super_fast(params["url"], max_pages)
                elif analysis_mode == "fast":
                    result = await analyze_fast_async(params["url"], max_pages)
                else:
                    # Fallback to standard analysis
                    result = analyze(
                        params["url"],
                        sitemap_url=params.get("sitemap_url"),
                        run_llm_analysis=False  # 先关闭LLM避免冲突
                    )
            except Exception as analysis_error:
                raise Exception(f"分析执行失败: {str(analysis_error)}")
            
            # Update progress for AI analysis
            run_llm_analysis = params.get("run_llm_analysis", False)
            if run_llm_analysis and result.get("success", True):
                self.tasks[task_id].update({
                    "progress": 70,
                    "message": "正在运行AI增强分析..."
                })
                self._save_tasks()
                
                try:
                    # Run AI enhancement
                    enhancer = LLMSEOEnhancer()
                    ai_result = await enhancer.enhance_seo_analysis(result)
                    
                    # Merge AI results with basic analysis
                    result.update({
                        "ai_analysis": ai_result,
                        "ai_enhanced": True
                    })
                    
                    self.tasks[task_id].update({
                        "progress": 90,
                        "message": "AI分析完成，正在生成报告..."
                    })
                    self._save_tasks()
                    
                except Exception as ai_error:
                    print(f"AI分析失败: {ai_error}")
                    result.update({
                        "ai_analysis": {
                            "error": f"AI分析失败: {str(ai_error)}",
                            "fallback_recommendations": [
                                "优化页面标题包含主要关键词",
                                "完善Meta描述提升点击率", 
                                "添加内部链接增强页面权重",
                                "提升页面内容质量和原创性"
                            ]
                        },
                        "ai_enhanced": False
                    })
            
            # 保存最终结果
            self.tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "message": "分析完成",
                "result": result,
                "analyzed_at": datetime.now().isoformat(),
                "analyzed_url": str(params["url"])
            })
            
        except Exception as e:
            print(f"Analysis failed for task {task_id}: {e}")
            self.tasks[task_id].update({
                "status": "failed",
                "progress": 0,
                "message": f"分析失败: {str(e)}",
                "error": str(e)
            })
    
    def get_status(self, task_id: str) -> Optional[Dict]:
        """Get task status"""
        status = self.tasks.get(task_id)
        if status:
            # Ensure task_id is included in the response
            status["task_id"] = task_id
        return status
    
    def get_result(self, task_id: str) -> Optional[Dict]:
        """Get task result"""
        task = self.tasks.get(task_id)
        if task and task["status"] == "completed":
            return task["result"]
        return None
    
    async def cleanup(self):
        """Clean up completed tasks older than 1 hour"""
        current_time = datetime.now()
        tasks_to_remove = []
        
        for task_id, task in self.tasks.items():
            if task["status"] in ["completed", "failed"]:
                task_time = datetime.fromisoformat(task["created_at"])
                if (current_time - task_time).total_seconds() > 3600:
                    tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.tasks[task_id]


# Global task manager instance
task_manager = TaskManager()