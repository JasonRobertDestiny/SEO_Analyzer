import time
import asyncio
import aiohttp
from operator import itemgetter
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import logging

from .website import Website
from .page import Page

logger = logging.getLogger(__name__)


def calc_total_time(start_time):
    return time.time() - start_time


class SEOAnalyzer:
    """基础SEO分析器类"""
    
    def __init__(self, max_pages: int = 50, timeout: int = 120):
        self.max_pages = max_pages
        self.timeout = timeout
        
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """分析网站 - 需要在子类中实现"""
        raise NotImplementedError("子类必须实现analyze_website方法")
    
    async def _analyze_single_page(self, session: aiohttp.ClientSession, url: str) -> Optional[Page]:
        """分析单个页面"""
        try:
            # 使用 Page 类正确的初始化方式
            page = Page(
                url=url,
                base_domain=url,
                analyze_headings=True,
                analyze_extra_tags=True
            )
            # Page 类有自己的 analyze 方法来获取和分析页面内容
            success = page.analyze()
            if success:
                return page
            else:
                logger.warning(f"页面分析失败: {url}")
                return None
        except Exception as e:
            logger.error(f"分析页面失败: {url} - {e}")
            return None
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "pages": [],
            "total_pages": 0,
            "keywords": {"words": [], "bigrams": []},
            "success": False,
            "error": error_message,
            "analysis_time": 0
        }


def analyze(
    url,
    sitemap_url=None,
    analyze_headings=False,
    analyze_extra_tags=False,
    follow_links=True,
    run_llm_analysis=False,
):
    start_time = time.time()

    output = {
        "pages": [],
        "keywords": [],
        "errors": [],
        "total_time": 0,  # Initialize to 0 before calculation
    }

    site = Website(
        base_url=url,
        sitemap=sitemap_url,
        analyze_headings=analyze_headings,
        analyze_extra_tags=analyze_extra_tags,
        follow_links=follow_links,
        run_llm_analysis=run_llm_analysis,
    )

    site.crawl()

    for p in site.crawled_pages:
        output["pages"].append(p.as_dict())

    output["duplicate_pages"] = [
        list(site.content_hashes[p])
        for p in site.content_hashes
        if len(site.content_hashes[p]) > 1
    ]

    sorted_words = sorted(site.wordcount.items(), key=itemgetter(1), reverse=True)
    sorted_bigrams = sorted(site.bigrams.items(), key=itemgetter(1), reverse=True)
    sorted_trigrams = sorted(site.trigrams.items(), key=itemgetter(1), reverse=True)

    output["keywords"] = []

    for w in sorted_words:
        if w[1] > 4:
            output["keywords"].append(
                {
                    "word": w[0],
                    "count": w[1],
                }
            )

    for w, v in sorted_bigrams:
        if v > 4:
            output["keywords"].append(
                {
                    "word": w,
                    "count": v,
                }
            )

    for w, v in sorted_trigrams:
        if v > 4:
            output["keywords"].append(
                {
                    "word": w,
                    "count": v,
                }
            )

    # Sort one last time...
    output["keywords"] = sorted(
        output["keywords"], key=itemgetter("count"), reverse=True
    )

    output["total_time"] = calc_total_time(start_time)

    return output
