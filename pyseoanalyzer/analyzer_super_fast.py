#!/usr/bin/env python3
"""
超级快速SEO分析器 - 多模式性能优化版本
提供闪电级、超级快速、常规快速三种分析模式
"""
import asyncio
import time
from typing import Dict, List, Optional, Any
import aiohttp
from urllib.parse import urljoin, urlparse
import logging

from .analyzer import SEOAnalyzer
from .page import Page
from .http import Http

logger = logging.getLogger(__name__)


def _extract_basic_keywords(pages: List[Page]) -> Dict[str, Any]:
    """提取基础关键词"""
    if not pages:
        return {"words": [], "bigrams": []}
    
    # 简化的关键词提取
    page = pages[0]
    title_words = page.title.lower().split() if page.title else []
    
    return {
        "words": [{"word": word, "count": 1} for word in title_words[:10]],
        "bigrams": []
    }


class SuperFastSEOAnalyzer(SEOAnalyzer):
    """超级快速SEO分析器"""
    
    def __init__(self, max_pages: int = 5, timeout: int = 30, mode: str = "super_fast"):
        super().__init__(max_pages=max_pages, timeout=timeout)
        self.mode = mode
        self.concurrent_limit = self._get_concurrent_limit(mode)
        
    def _get_concurrent_limit(self, mode: str) -> int:
        """根据模式返回并发限制"""
        limits = {
            "lightning": 2,      # 闪电级: 低并发，重点是首页
            "super_fast": 5,     # 超级快速: 中等并发
            "fast": 10           # 快速: 高并发
        }
        return limits.get(mode, 5)
    
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """分析网站"""
        try:
            start_time = time.time()
            
            # 分析首页
            page = await self._analyze_single_page(None, url)
            
            if not page:
                return self._create_error_result("无法访问网站首页")
            
            # 生成分析结果
            result = {
                "pages": [page.as_dict()],
                "total_pages": 1,
                "keywords": _extract_basic_keywords([page]),
                "analysis_mode": self.mode,
                "analysis_time": time.time() - start_time,
                "success": True
            }
            
            logger.info(f"超级快速分析完成: {url} ({result['analysis_time']:.2f}秒)")
            return result
            
        except Exception as e:
            logger.error(f"超级快速分析失败: {url} - {e}")
            return self._create_error_result(str(e))


class LightningFastAnalyzer(SuperFastSEOAnalyzer):
    """闪电级分析器 - 只分析首页和关键页面"""
    
    def __init__(self):
        super().__init__(max_pages=3, timeout=15, mode="lightning")
    
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """闪电级分析 - 仅分析核心页面"""
        try:
            start_time = time.time()
            
            # 只分析首页
            page = await self._analyze_single_page(None, url)
            
            if not page:
                return self._create_error_result("无法访问网站首页")
            
            # 简化的分析结果
            result = {
                "pages": [page.as_dict()],
                "total_pages": 1,
                "keywords": _extract_basic_keywords([page]),
                "analysis_mode": "lightning",
                "analysis_time": time.time() - start_time,
                "success": True
            }
            
            logger.info(f"闪电级分析完成: {url} ({result['analysis_time']:.2f}秒)")
            return result
            
        except Exception as e:
            logger.error(f"闪电级分析失败: {url} - {e}")
            return self._create_error_result(str(e))
    
    def _extract_basic_keywords(self, pages: List[Page]) -> Dict[str, Any]:
        """提取基础关键词"""
        if not pages:
            return {"words": [], "bigrams": []}
        
        # 简化的关键词提取
        page = pages[0]
        title_words = page.title.lower().split() if page.title else []
        
        return {
            "words": [{"word": word, "count": 1} for word in title_words[:10]],
            "bigrams": []
        }


async def analyze_lightning_fast(url: str) -> Dict[str, Any]:
    """闪电级分析入口函数"""
    analyzer = LightningFastAnalyzer()
    return await analyzer.analyze_website(url)


async def analyze_super_fast(url: str, max_pages: int = 10) -> Dict[str, Any]:
    """超级快速分析入口函数"""
    analyzer = SuperFastSEOAnalyzer(max_pages=max_pages, mode="super_fast")
    return await analyzer.analyze_website(url)


async def analyze_fast_async(url: str, max_pages: int = 20) -> Dict[str, Any]:
    """快速异步分析入口函数"""
    analyzer = SuperFastSEOAnalyzer(max_pages=max_pages, mode="fast")
    return await analyzer.analyze_website(url)


async def benchmark_analysis_modes(url: str) -> Dict[str, Dict[str, Any]]:
    """性能基准测试 - 比较不同分析模式"""
    modes = {
        "闪电级": lambda: analyze_lightning_fast(url),
        "超级快速": lambda: analyze_super_fast(url, 5),
        "快速模式": lambda: analyze_fast_async(url, 10)
    }
    
    results = {}
    
    for mode_name, analyzer_func in modes.items():
        try:
            start_time = time.time()
            result = await analyzer_func()
            duration = time.time() - start_time
            
            results[mode_name] = {
                "success": result.get("success", False),
                "duration": round(duration, 2),
                "pages_analyzed": result.get("total_pages", 0),
                "analysis_mode": result.get("analysis_mode", mode_name.lower()),
                "error": None
            }
            
        except Exception as e:
            results[mode_name] = {
                "success": False,
                "duration": 0,
                "pages_analyzed": 0,
                "analysis_mode": mode_name.lower(),
                "error": str(e)
            }
    
    return results


class FastAnalysisConfig:
    """快速分析配置"""
    
    LIGHTNING_CONFIG = {
        "max_pages": 3,
        "timeout": 15,
        "concurrent_limit": 2,
        "skip_images": True,
        "skip_external_links": True
    }
    
    SUPER_FAST_CONFIG = {
        "max_pages": 10,
        "timeout": 30,
        "concurrent_limit": 5,
        "skip_images": True,
        "skip_external_links": False
    }
    
    FAST_CONFIG = {
        "max_pages": 20,
        "timeout": 60,
        "concurrent_limit": 10,
        "skip_images": False,
        "skip_external_links": False
    }


def get_analysis_config(mode: str) -> Dict[str, Any]:
    """获取分析模式配置"""
    configs = {
        "lightning": FastAnalysisConfig.LIGHTNING_CONFIG,
        "super_fast": FastAnalysisConfig.SUPER_FAST_CONFIG,
        "fast": FastAnalysisConfig.FAST_CONFIG
    }
    return configs.get(mode, FastAnalysisConfig.SUPER_FAST_CONFIG)


# 向后兼容性别名
analyze_fast = analyze_fast_async
