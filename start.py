#!/usr/bin/env python3
"""
SmartSEO Analyzer - Startup Script
Simple startup script for FastAPI application
"""
import os
import sys
import uvicorn

def show_banner():
    """显示启动横幅"""
    print("=" * 60)
    print("🚀 SmartSEO AI分析器")
    print("💡 智能SEO分析与优化建议")
    print("🌐 FastAPI后端服务")
    print("=" * 60)

if __name__ == "__main__":
    # 显示横幅
    show_banner()
    
    # 获取配置
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    
    # 配置信息
    print(f"🌐 服务地址: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    print("-" * 60)
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info"
    )