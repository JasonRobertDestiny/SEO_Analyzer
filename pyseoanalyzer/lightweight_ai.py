#!/usr/bin/env python3
"""
轻量级AI分析模块
提供快速、简化的AI SEO分析功能
"""
import asyncio
import time
import logging
from typing import Dict, List, Optional, Any, Union
import json

logger = logging.getLogger(__name__)


class LightweightAIAnalyzer:
    """轻量级AI分析器"""
    
    def __init__(self, enable_cache: bool = True):
        self.enable_cache = enable_cache
        self.cache = {} if enable_cache else None
        self.analysis_patterns = self._load_analysis_patterns()
    
    def _load_analysis_patterns(self) -> Dict[str, Any]:
        """加载分析模式"""
        return {
            "title_patterns": {
                "good": ["包含关键词", "长度适中", "具有吸引力"],
                "bad": ["过长", "过短", "重复", "无关键词"]
            },
            "meta_patterns": {
                "good": ["150-160字符", "包含关键词", "行动呼吁"],
                "bad": ["过长", "过短", "重复", "无描述"]
            },
            "content_patterns": {
                "good": ["结构清晰", "关键词密度适中", "原创性高"],
                "bad": ["内容稀少", "关键词堆砌", "重复内容"]
            }
        }
    
    async def quick_ai_enhance(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """快速AI增强分析"""
        try:
            start_time = time.time()
            
            # 检查缓存
            cache_key = self._generate_cache_key(seo_data)
            if self.enable_cache and cache_key in self.cache:
                logger.info("使用缓存的AI分析结果")
                return self.cache[cache_key]
            
            # 快速模式分析
            enhancement = await self._analyze_fast_mode(seo_data)
            
            # 添加分析时间
            enhancement["ai_analysis_time"] = time.time() - start_time
            enhancement["analysis_mode"] = "lightweight"
            
            # 缓存结果
            if self.enable_cache:
                self.cache[cache_key] = enhancement
            
            logger.info(f"轻量级AI分析完成 ({enhancement['ai_analysis_time']:.2f}秒)")
            return enhancement
            
        except Exception as e:
            logger.error(f"轻量级AI分析失败: {e}")
            return self._create_fallback_result(seo_data)
    
    async def _analyze_fast_mode(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """快速模式分析"""
        pages = seo_data.get("pages", [])
        if not pages:
            return self._create_empty_result()
        
        # 分析主页面
        main_page = pages[0]
        
        # 快速分析各个方面
        title_analysis = self._analyze_title_fast(main_page.get("title", ""))
        meta_analysis = self._analyze_meta_fast(main_page.get("meta_description", ""))
        content_analysis = self._analyze_content_fast(main_page)
        
        # 生成简化建议
        recommendations = self._generate_quick_recommendations(
            title_analysis, meta_analysis, content_analysis
        )
        
        return {
            "ai_insights": {
                "title_score": title_analysis["score"],
                "meta_score": meta_analysis["score"],
                "content_score": content_analysis["score"],
                "overall_score": (title_analysis["score"] + meta_analysis["score"] + content_analysis["score"]) / 3
            },
            "quick_recommendations": recommendations,
            "analysis_summary": self._create_summary(title_analysis, meta_analysis, content_analysis),
            "optimization_priority": self._determine_priority(title_analysis, meta_analysis, content_analysis)
        }
    
    def _analyze_title_fast(self, title: str) -> Dict[str, Any]:
        """快速标题分析"""
        if not title:
            return {"score": 0, "issues": ["缺少标题"], "suggestions": ["添加页面标题"]}
        
        score = 50  # 基础分数
        issues = []
        suggestions = []
        
        # 长度检查
        length = len(title)
        if length < 30:
            issues.append("标题过短")
            suggestions.append("扩展标题长度至30-60字符")
        elif length > 60:
            issues.append("标题过长")
            suggestions.append("缩短标题至60字符以内")
            score -= 20
        else:
            score += 30
        
        # 关键词检查 (简化版)
        if any(word in title.lower() for word in ["seo", "优化", "网站", "分析"]):
            score += 20
        else:
            suggestions.append("在标题中包含相关关键词")
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _analyze_meta_fast(self, meta_description: str) -> Dict[str, Any]:
        """快速Meta描述分析"""
        if not meta_description:
            return {
                "score": 0,
                "issues": ["缺少Meta描述"],
                "suggestions": ["添加150-160字符的Meta描述"]
            }
        
        score = 50
        issues = []
        suggestions = []
        
        length = len(meta_description)
        if length < 120:
            issues.append("Meta描述过短")
            suggestions.append("扩展Meta描述至120-160字符")
        elif length > 160:
            issues.append("Meta描述过长")
            suggestions.append("缩短Meta描述至160字符以内")
            score -= 15
        else:
            score += 40
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _analyze_content_fast(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """快速内容分析"""
        score = 50
        issues = []
        suggestions = []
        
        # 检查H1标签
        h1_tags = page_data.get("h1", [])
        if not h1_tags:
            issues.append("缺少H1标签")
            suggestions.append("添加主要H1标题")
            score -= 20
        elif len(h1_tags) > 1:
            issues.append("多个H1标签")
            suggestions.append("每页只使用一个H1标签")
            score -= 10
        else:
            score += 20
        
        # 检查字数
        word_count = page_data.get("word_count", 0)
        if word_count < 300:
            issues.append("内容过少")
            suggestions.append("增加页面内容至300字以上")
            score -= 15
        else:
            score += 20
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _generate_quick_recommendations(self, title_analysis: Dict, meta_analysis: Dict, content_analysis: Dict) -> List[str]:
        """生成快速建议"""
        recommendations = []
        
        # 根据具体问题生成针对性建议
        if title_analysis["score"] < 70:
            recommendations.extend([
                f"🎯 优化页面标题：{', '.join(title_analysis['suggestions'][:2])}",
                "📝 确保标题包含主要关键词并控制在30-60字符",
                "✨ 让标题更有吸引力，提高点击率"
            ])
        
        if meta_analysis["score"] < 70:
            recommendations.extend([
                f"📄 改进Meta描述：{', '.join(meta_analysis['suggestions'][:2])}",
                "🎯 在描述中包含行动号召语言",
                "📏 保持Meta描述在150-160字符之间"
            ])
        
        if content_analysis["score"] < 70:
            recommendations.extend([
                f"📋 优化页面内容：{', '.join(content_analysis['suggestions'][:2])}",
                "🔗 添加更多内部链接提升页面权重",
                "📊 增加页面内容深度和相关性"
            ])
        
        # 添加通用优化建议
        if len(recommendations) < 5:
            recommendations.extend([
                "🚀 提升页面加载速度，优化用户体验",
                "📱 确保网站响应式设计适配移动设备",
                "🔍 研究竞争对手关键词策略",
                "📈 设置Google Analytics跟踪分析效果",
                "💡 定期更新内容保持网站活跃度"
            ])
        
        return recommendations[:8]  # 返回最多8个建议
    
    def _create_summary(self, title_analysis: Dict, meta_analysis: Dict, content_analysis: Dict) -> str:
        """创建分析摘要"""
        overall_score = (title_analysis["score"] + meta_analysis["score"] + content_analysis["score"]) / 3
        
        if overall_score >= 80:
            return "页面SEO优化良好，只需要微调即可。"
        elif overall_score >= 60:
            return "页面SEO有改进空间，建议优化标题和内容。"
        elif overall_score >= 40:
            return "页面SEO需要重要改进，特别是元素标签和内容结构。"
        else:
            return "页面SEO亟需全面优化，建议从基础元素开始改进。"
    
    def _determine_priority(self, title_analysis: Dict, meta_analysis: Dict, content_analysis: Dict) -> List[str]:
        """确定优化优先级"""
        priorities = []
        
        scores = [
            ("标题优化", title_analysis["score"]),
            ("Meta描述优化", meta_analysis["score"]),
            ("内容优化", content_analysis["score"])
        ]
        
        # 按分数排序，分数低的优先级高
        scores.sort(key=lambda x: x[1])
        
        return [item[0] for item in scores]
    
    def _generate_cache_key(self, seo_data: Dict[str, Any]) -> str:
        """生成缓存键"""
        # 使用页面URL和主要内容生成简单的hash
        pages = seo_data.get("pages", [])
        if pages:
            first_page = pages[0]
            key_data = f"{first_page.get('url', '')}-{first_page.get('title', '')}"
            return str(hash(key_data))
        return "default"
    
    def _create_fallback_result(self, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建回退结果"""
        return {
            "ai_insights": {
                "title_score": 50,
                "meta_score": 50,
                "content_score": 50,
                "overall_score": 50
            },
            "quick_recommendations": [
                "检查页面标题是否包含关键词",
                "确保Meta描述长度在150-160字符",
                "添加适当的H1标签",
                "增加页面内容丰富度"
            ],
            "analysis_summary": "使用基础分析模式，建议进行标准SEO优化。",
            "optimization_priority": ["标题优化", "Meta描述优化", "内容优化"],
            "ai_analysis_time": 0.1,
            "analysis_mode": "fallback"
        }
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """创建空结果"""
        return {
            "ai_insights": {
                "title_score": 0,
                "meta_score": 0,
                "content_score": 0,
                "overall_score": 0
            },
            "quick_recommendations": ["无法分析页面，请检查URL是否有效"],
            "analysis_summary": "未能获取页面数据进行分析。",
            "optimization_priority": [],
            "ai_analysis_time": 0.01,
            "analysis_mode": "empty"
        }


# 全局实例
_global_analyzer = None

async def quick_ai_enhance(seo_data: Dict[str, Any], use_cache: bool = True) -> Dict[str, Any]:
    """快速AI增强分析入口函数"""
    global _global_analyzer
    
    if _global_analyzer is None:
        _global_analyzer = LightweightAIAnalyzer(enable_cache=use_cache)
    
    return await _global_analyzer.quick_ai_enhance(seo_data)


def create_lightweight_analyzer(enable_cache: bool = True) -> LightweightAIAnalyzer:
    """创建轻量级分析器实例"""
    return LightweightAIAnalyzer(enable_cache=enable_cache)


async def batch_quick_enhance(seo_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """批量快速增强"""
    analyzer = LightweightAIAnalyzer()
    tasks = [analyzer.quick_ai_enhance(data) for data in seo_data_list]
    return await asyncio.gather(*tasks, return_exceptions=True)


# 预设分析配置
class LightweightConfig:
    """轻量级配置"""
    
    ULTRA_FAST = {
        "enable_cache": True,
        "analysis_depth": "basic",
        "timeout": 5
    }
    
    BALANCED = {
        "enable_cache": True,
        "analysis_depth": "standard",
        "timeout": 10
    }
    
    THOROUGH = {
        "enable_cache": False,
        "analysis_depth": "detailed",
        "timeout": 20
    }
