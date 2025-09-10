#!/usr/bin/env python3
"""
快速异步SEO分析器
专注于异步并发处理和性能优化
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
from .analyzer_super_fast import _extract_basic_keywords

logger = logging.getLogger(__name__)


class FastAsyncSEOAnalyzer(SEOAnalyzer):
    """快速异步SEO分析器"""
    
    def __init__(self, max_pages: int = 20, timeout: int = 60, concurrent_limit: int = 10):
        super().__init__(max_pages=max_pages, timeout=timeout)
        self.concurrent_limit = concurrent_limit
        self.semaphore = asyncio.Semaphore(concurrent_limit)
        
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """异步分析网站"""
        try:
            start_time = time.time()
            
            # 分析首页
            main_page = await self._analyze_single_page(None, url)
            if not main_page:
                return self._create_error_result("无法访问网站首页")
            
            # 简化版本：只分析首页
            pages = [main_page]
            
            # 生成分析结果
            result = {
                "pages": [page.as_dict() for page in pages],
                "total_pages": len(pages),
                "keywords": _extract_basic_keywords(pages),
                "internal_links": {"total_internal_links": 0, "unique_internal_links": 0, "most_linked_pages": []},
                "analysis_mode": "fast_async",
                "analysis_time": time.time() - start_time,
                "success": True,
                "performance_metrics": {
                    "concurrent_limit": self.concurrent_limit,
                    "pages_per_second": len(pages) / (time.time() - start_time)
                }
            }
            
            logger.info(f"快速异步分析完成: {url} ({result['analysis_time']:.2f}秒, {len(pages)}页)")
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"分析超时: {url}")
            return self._create_error_result("分析超时")
        except Exception as e:
            logger.error(f"快速异步分析失败: {url} - {e}")
            return self._create_error_result(str(e))
        
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """异步分析网站"""
        try:
            start_time = time.time()
            
            # 使用会话池提高性能
            connector = aiohttp.TCPConnector(limit=self.concurrent_limit)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': 'SmartSEO-Analyzer/2.0 (+https://github.com/your-repo)'}
            ) as session:
                
                # 首先分析首页
                main_page = await self._analyze_page_with_semaphore(session, url)
                if not main_page:
                    return self._create_error_result("无法访问网站首页")
                
                # 收集更多页面URL
                page_urls = await self._collect_page_urls(session, url, main_page)
                
                # 并发分析所有页面
                pages = [main_page]
                if page_urls:
                    additional_pages = await self._analyze_pages_concurrently(session, page_urls)
                    pages.extend([p for p in additional_pages if p])
                
                # 生成分析结果
                result = {
                    "pages": [page.as_dict() for page in pages],
                    "total_pages": len(pages),
                    "keywords": self._analyze_keywords(pages),
                    "internal_links": self._analyze_internal_links(pages),
                    "analysis_mode": "fast_async",
                    "analysis_time": time.time() - start_time,
                    "success": True,
                    "performance_metrics": {
                        "concurrent_limit": self.concurrent_limit,
                        "pages_per_second": len(pages) / (time.time() - start_time)
                    }
                }
                
                logger.info(f"快速异步分析完成: {url} ({result['analysis_time']:.2f}秒, {len(pages)}页)")
                return result
                
        except asyncio.TimeoutError:
            logger.error(f"分析超时: {url}")
            return self._create_error_result("分析超时")
        except Exception as e:
            logger.error(f"快速异步分析失败: {url} - {e}")
            return self._create_error_result(str(e))
    
    async def _analyze_page_with_semaphore(self, session: aiohttp.ClientSession, url: str) -> Optional[Page]:
        """使用信号量控制并发的页面分析"""
        async with self.semaphore:
            return await self._analyze_single_page(session, url)
    
    async def _collect_page_urls(self, session: aiohttp.ClientSession, base_url: str, main_page: Page) -> List[str]:
        """收集页面URL"""
        try:
            # 从首页提取内部链接
            urls = []
            domain = urlparse(base_url).netloc
            
            for link in main_page.internal_links[:self.max_pages-1]:  # 减1因为已有首页
                if urlparse(link).netloc == domain:
                    urls.append(link)
            
            # 如果链接不够，尝试发现更多页面
            if len(urls) < self.max_pages - 1:
                common_paths = ['/about', '/contact', '/services', '/products', '/blog']
                for path in common_paths:
                    url = urljoin(base_url, path)
                    if url not in urls:
                        urls.append(url)
                        if len(urls) >= self.max_pages - 1:
                            break
            
            return urls[:self.max_pages-1]
            
        except Exception as e:
            logger.error(f"收集页面URL失败: {e}")
            return []
    
    async def _analyze_pages_concurrently(self, session: aiohttp.ClientSession, urls: List[str]) -> List[Optional[Page]]:
        """并发分析多个页面"""
        tasks = [self._analyze_page_with_semaphore(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=False)
    
    def _analyze_keywords(self, pages: List[Page]) -> Dict[str, Any]:
        """分析关键词"""
        word_freq = {}
        bigram_freq = {}
        
        for page in pages:
            # 分析单词
            if page.title:
                words = page.title.lower().split()
                for word in words:
                    if len(word) > 2:
                        word_freq[word] = word_freq.get(word, 0) + 1
            
            # 分析双词组合
            if page.title:
                words = page.title.lower().split()
                for i in range(len(words) - 1):
                    bigram = f"{words[i]} {words[i+1]}"
                    if len(bigram) > 5:
                        bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1
        
        # 排序并返回前20个
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "words": [{"word": word, "count": count} for word, count in sorted_words],
            "bigrams": [{"phrase": phrase, "count": count} for phrase, count in sorted_bigrams]
        }
    
    def _analyze_internal_links(self, pages: List[Page]) -> Dict[str, Any]:
        """分析内部链接结构"""
        all_links = []
        for page in pages:
            all_links.extend(page.internal_links)
        
        # 统计链接频率
        link_freq = {}
        for link in all_links:
            link_freq[link] = link_freq.get(link, 0) + 1
        
        return {
            "total_internal_links": len(all_links),
            "unique_internal_links": len(link_freq),
            "most_linked_pages": sorted(link_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        }


async def analyze_fast_async(url: str, max_pages: int = 20, concurrent_limit: int = 10) -> Dict[str, Any]:
    """快速异步分析入口函数"""
    analyzer = FastAsyncSEOAnalyzer(max_pages=max_pages, concurrent_limit=concurrent_limit)
    return await analyzer.analyze_website(url)


class AsyncAnalysisOptimizer:
    """异步分析优化器"""
    
    @staticmethod
    def optimize_for_speed(max_pages: int) -> Dict[str, int]:
        """根据页面数量优化并发设置"""
        if max_pages <= 5:
            return {"concurrent_limit": 3, "timeout": 30}
        elif max_pages <= 15:
            return {"concurrent_limit": 7, "timeout": 45}
        else:
            return {"concurrent_limit": 12, "timeout": 60}
    
    @staticmethod
    def optimize_for_accuracy(max_pages: int) -> Dict[str, int]:
        """根据页面数量优化准确性设置"""
        if max_pages <= 10:
            return {"concurrent_limit": 2, "timeout": 60}
        elif max_pages <= 25:
            return {"concurrent_limit": 5, "timeout": 90}
        else:
            return {"concurrent_limit": 8, "timeout": 120}


async def analyze_with_optimization(url: str, max_pages: int = 20, optimization_mode: str = "speed") -> Dict[str, Any]:
    """使用优化配置进行分析"""
    if optimization_mode == "speed":
        config = AsyncAnalysisOptimizer.optimize_for_speed(max_pages)
    else:
        config = AsyncAnalysisOptimizer.optimize_for_accuracy(max_pages)
    
    analyzer = FastAsyncSEOAnalyzer(
        max_pages=max_pages,
        timeout=config["timeout"],
        concurrent_limit=config["concurrent_limit"]
    )
    
    return await analyzer.analyze_website(url)
