from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

import asyncio
import json
import os

load_dotenv()


# Pydantic models for structured output
class EntityAnalysis(BaseModel):
    entity_assessment: str = Field(
        description="Detailed analysis of entity optimization"
    )
    knowledge_panel_readiness: int = Field(description="Score from 0-100")
    key_improvements: List[str] = Field(description="Top 3 improvements needed")


class CredibilityAnalysis(BaseModel):
    credibility_assessment: str = Field(description="Overall credibility analysis")
    neeat_scores: Dict[str, int] = Field(
        description="Individual N-E-E-A-T-T component scores"
    )
    trust_signals: List[str] = Field(description="Identified trust signals")


class ConversationAnalysis(BaseModel):
    conversation_readiness: str = Field(description="Overall assessment")
    query_patterns: List[str] = Field(description="Identified query patterns")
    engagement_score: int = Field(description="Score from 0-100")
    gaps: List[str] = Field(description="Identified conversational gaps")


class PlatformPresence(BaseModel):
    platform_coverage: Dict[str, str] = Field(
        description="Coverage analysis per platform"
    )
    visibility_scores: Dict[str, int] = Field(description="Scores per platform type")
    optimization_opportunities: List[str] = Field(description="List of opportunities")


class SEORecommendations(BaseModel):
    strategic_recommendations: List[str] = Field(
        description="Major strategic recommendations"
    )
    quick_wins: List[str] = Field(description="Immediate action items")
    long_term_strategy: List[str] = Field(description="Long-term strategic goals")
    priority_matrix: Dict[str, str] = Field(
        description="Priority matrix by impact/effort"
    )


class LLMSEOEnhancer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="Qwen/Qwen2.5-VL-72B-Instruct",
            api_key=os.environ.get("SILICONFLOW_API_KEY"),
            base_url="https://api.siliconflow.cn/v1",
            temperature=0,
            max_retries=2,
            max_tokens=2048,  # 进一步减少token数量提升速度
        )
        # 配置超时参数
        self.timeout_duration = 60  # 减少到60秒
        self.single_chain_timeout = 20  # 单个链20秒超时
        
        # 简化缓存机制
        self._cache = {}
        self._setup_chains()

    def _setup_chains(self):
        """Setup modern LangChain runnable sequences using pipe syntax"""
        # Entity Analysis Chain
        entity_parser = PydanticOutputParser(pydantic_object=EntityAnalysis)

        entity_prompt = PromptTemplate.from_template(
            """Analyze SEO entity optimization (be concise):
            Data: {seo_data}
            
            Return JSON only with:
            - entity_assessment (brief)
            - knowledge_panel_readiness (0-100)
            - key_improvements (top 3)
            
            {format_instructions}
            """
        )

        self.entity_chain = (
            {
                "seo_data": RunnablePassthrough(),
                "format_instructions": lambda _: entity_parser.get_format_instructions(),
            }
            | entity_prompt
            | self.llm
            | entity_parser
        )

        # Credibility Analysis Chain
        credibility_parser = PydanticOutputParser(pydantic_object=CredibilityAnalysis)

        credibility_prompt = PromptTemplate.from_template(
            """Evaluate credibility (be brief):
            Data: {seo_data}
            
            Return JSON only:
            - credibility_assessment (brief)
            - neeat_scores (6 scores 0-100)
            - trust_signals (top 3)
            
            {format_instructions}
            """
        )

        self.credibility_chain = (
            {
                "seo_data": RunnablePassthrough(),
                "format_instructions": lambda _: credibility_parser.get_format_instructions(),
            }
            | credibility_prompt
            | self.llm
            | credibility_parser
        )

        # Conversation Analysis Chain
        conversation_parser = PydanticOutputParser(pydantic_object=ConversationAnalysis)

        conversation_prompt = PromptTemplate.from_template(
            """Analyze conversational search readiness (concise):
            Data: {seo_data}
            
            Return JSON only:
            - conversation_readiness (brief)
            - query_patterns (top 3)
            - engagement_score (0-100)
            - gaps (top 3)
            
            {format_instructions}
            """
        )

        self.conversation_chain = (
            {
                "seo_data": RunnablePassthrough(),
                "format_instructions": lambda _: conversation_parser.get_format_instructions(),
            }
            | conversation_prompt
            | self.llm
            | conversation_parser
        )

        # Platform Presence Chain
        platform_parser = PydanticOutputParser(pydantic_object=PlatformPresence)

        platform_prompt = PromptTemplate.from_template(
            """Analyze platform presence (brief):
            Data: {seo_data}
            
            Return JSON only:
            - platform_coverage (brief assessment)
            - visibility_scores (4 scores 0-100)
            - optimization_opportunities (top 3)
            
            {format_instructions}
            """
        )

        self.platform_chain = (
            {
                "seo_data": RunnablePassthrough(),
                "format_instructions": lambda _: platform_parser.get_format_instructions(),
            }
            | platform_prompt
            | self.llm
            | platform_parser
        )

        # Recommendations Chain
        recommendations_parser = PydanticOutputParser(
            pydantic_object=SEORecommendations
        )

        recommendations_prompt = PromptTemplate.from_template(
            """Generate strategic recommendations (concise):
            Analysis: {analysis_results}
            
            Return JSON only:
            - strategic_recommendations (top 3)
            - quick_wins (top 3)
            - long_term_strategy (top 3)
            - priority_matrix (4 brief items)
            
            {format_instructions}
            """
        )

        self.recommendations_chain = (
            {
                "analysis_results": RunnablePassthrough(),
                "format_instructions": lambda _: recommendations_parser.get_format_instructions(),
            }
            | recommendations_prompt
            | self.llm
            | recommendations_parser
        )

    async def enhance_seo_analysis(self, seo_data: Dict) -> Dict:
        """
        Enhanced SEO analysis using modern LangChain patterns with performance optimization
        """
        # 创建数据缓存键
        import hashlib
        cache_key = hashlib.md5(json.dumps(seo_data, sort_keys=True).encode()).hexdigest()
        
        # 检查缓存
        if cache_key in self._cache:
            print("使用缓存的分析结果")
            return self._cache[cache_key]
        
        # Convert seo_data to string for prompt insertion
        seo_data_str = json.dumps(seo_data, indent=2)
        
        try:
            # 使用更短的超时控制
            timeout_duration = self.timeout_duration  # 60秒总超时
            
            print(f"🤖 开始AI分析 (超时: {timeout_duration}秒)")
            
            # 简化数据以减少token使用
            simplified_data = self._simplify_seo_data(seo_data_str)
            
            # Run analysis chains in parallel with aggressive timeout
            tasks = [
                asyncio.wait_for(self.entity_chain.ainvoke(simplified_data), timeout=self.single_chain_timeout),
                asyncio.wait_for(self.credibility_chain.ainvoke(simplified_data), timeout=self.single_chain_timeout),
                asyncio.wait_for(self.conversation_chain.ainvoke(simplified_data), timeout=self.single_chain_timeout),
                asyncio.wait_for(self.platform_chain.ainvoke(simplified_data), timeout=self.single_chain_timeout),
            ]
            
            # 使用gather with return_exceptions
            results = await asyncio.gather(*tasks, return_exceptions=True)
            entity_results, credibility_results, conversation_results, platform_results = results
            
            # 处理结果
            processed_results = {}
            
            if not isinstance(entity_results, Exception):
                processed_results["entity_analysis"] = entity_results.model_dump()
                print("✅ 实体分析完成")
            else:
                print(f"⚠️ 实体分析失败: {type(entity_results).__name__}")
                processed_results["entity_analysis"] = self._get_fallback_entity_analysis()
            
            if not isinstance(credibility_results, Exception):
                processed_results["credibility_analysis"] = credibility_results.model_dump()
                print("✅ 可信度分析完成")
            else:
                print(f"⚠️ 可信度分析失败: {type(credibility_results).__name__}")
                processed_results["credibility_analysis"] = self._get_fallback_credibility_analysis()
            
            if not isinstance(conversation_results, Exception):
                processed_results["conversation_analysis"] = conversation_results.model_dump()
                print("✅ 对话分析完成")
            else:
                print(f"⚠️ 对话分析失败: {type(conversation_results).__name__}")
                processed_results["conversation_analysis"] = self._get_fallback_conversation_analysis()
            
            if not isinstance(platform_results, Exception):
                processed_results["cross_platform_presence"] = platform_results.model_dump()
                print("✅ 平台分析完成")
            else:
                print(f"⚠️ 平台分析失败: {type(platform_results).__name__}")
                processed_results["cross_platform_presence"] = self._get_fallback_platform_analysis()

            # Generate final recommendations with shorter timeout
            try:
                print("📝 生成最终建议...")
                recommendations = await asyncio.wait_for(
                    self.recommendations_chain.ainvoke(
                        json.dumps(processed_results, indent=1)  # 减少缩进
                    ),
                    timeout=30  # 增加到30秒
                )
                processed_results["recommendations"] = recommendations.model_dump()
                print("✅ 建议生成完成")
            except Exception as e:
                print(f"⚠️ 建议生成失败: {type(e).__name__}")
                processed_results["recommendations"] = self._get_fallback_recommendations()

            # Combine all results
            final_results = {
                **seo_data,
                **processed_results,
            }

            # 缓存结果
            formatted_output = self._format_output(final_results)
            self._cache[cache_key] = formatted_output
            
            # 限制缓存大小
            if len(self._cache) > 20:  # 减少缓存大小
                # 移除最旧的缓存项
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            
            print("🎉 AI分析完成!")
            return formatted_output
            
        except asyncio.TimeoutError:
            print("⏰ AI分析超时，返回基础分析结果")
            return self._get_fallback_full_analysis(seo_data)
        except Exception as e:
            print(f"❌ AI分析失败: {e}")
            return self._get_fallback_full_analysis(seo_data)

    def _format_output(self, raw_analysis: Dict) -> Dict:
        """Format analysis results into a clean, structured output"""
        try:
            entity_score = raw_analysis.get("entity_analysis", {}).get("knowledge_panel_readiness", 50)
            
            neeat_scores = raw_analysis.get("credibility_analysis", {}).get("neeat_scores", {})
            credibility_score = sum(neeat_scores.values()) / max(len(neeat_scores), 1) if neeat_scores else 50
            
            conversation_score = raw_analysis.get("conversation_analysis", {}).get("engagement_score", 50)
            
            visibility_scores = raw_analysis.get("cross_platform_presence", {}).get("visibility_scores", {})
            platform_score = sum(visibility_scores.values()) / max(len(visibility_scores), 1) if visibility_scores else 50
            
            return {
                "summary": {
                    "entity_score": entity_score,
                    "credibility_score": credibility_score,
                    "conversation_score": conversation_score,
                    "platform_score": platform_score,
                },
                "detailed_analysis": raw_analysis,
                "quick_wins": raw_analysis.get("recommendations", {}).get("quick_wins", ["优化页面标题", "改善元描述", "增加内部链接"]),
                "strategic_recommendations": raw_analysis.get("recommendations", {}).get("strategic_recommendations", ["提升内容质量", "增强技术SEO", "建立权威性"]),
            }
        except Exception as e:
            print(f"格式化输出失败: {e}")
            return self._get_fallback_full_analysis(raw_analysis)
    
    def _simplify_seo_data(self, seo_data_str: str) -> str:
        """简化SEO数据以减少token使用"""
        try:
            data = json.loads(seo_data_str)
            
            # 只保留关键信息
            simplified = {
                "pages_count": len(data.get("pages", [])),
                "sample_pages": data.get("pages", [])[:2],  # 只取前2页作为样本
                "top_keywords": data.get("keywords", {}).get("words", [])[:5],  # 只取前5个关键词
                "errors_count": len(data.get("errors", [])),
                "duplicate_pages": len(data.get("duplicate_pages", [])),
                "total_time": data.get("total_time", 0)
            }
            
            return json.dumps(simplified, indent=1, ensure_ascii=False)
        except:
            # 如果解析失败，截断原始数据
            return seo_data_str[:1000] + "..." if len(seo_data_str) > 1000 else seo_data_str

    def _get_fallback_entity_analysis(self):
        """实体分析的回退结果"""
        return {
            "entity_assessment": "🏢 实体优化基础分析：网站需要加强品牌实体信号，提升在知识图谱中的表现。建议完善公司信息页面，增加结构化数据标记，提升品牌一致性。",
            "knowledge_panel_readiness": 65,
            "key_improvements": [
                "📋 添加完整的Schema.org结构化数据标记",
                "🏷️ 优化品牌名称在各平台的一致性表现", 
                "🔗 增强实体相关性和权威性信号"
            ]
        }
    
    def _get_fallback_credibility_analysis(self):
        """可信度分析的回退结果"""
        return {
            "credibility_assessment": "🛡️ 可信度评估：网站具备基本的信任信号，但在专业性和透明度方面还有提升空间。建议完善关于我们页面，添加专业资质证明，提升内容的专业深度。",
            "neeat_scores": {
                "naturalness": 70,
                "entity": 65,
                "expertise": 60,
                "authority": 65,
                "trustworthiness": 68,
                "transparency": 62
            },
            "trust_signals": [
                "✅ SSL证书和安全连接已配置",
                "📞 联系信息清晰可见",
                "ℹ️ 关于页面需要进一步完善"
            ]
        }
    
    def _get_fallback_conversation_analysis(self):
        """对话分析的回退结果"""
        return {
            "conversation_readiness": "🗣️ 对话搜索准备度：网站内容结构基本合理，但需要优化以更好适应语音搜索和对话式查询。建议增加FAQ部分，优化长尾关键词，提升内容的问答格式。",
            "query_patterns": [
                "❓ 信息查询类：用户寻找基础信息和解答",
                "⚖️ 比较查询类：用户比较不同选择和方案",
                "📍 本地查询类：用户寻找附近的服务和信息"
            ],
            "engagement_score": 68,
            "gaps": [
                "❓ 缺少系统性的FAQ问答部分",
                "📊 内容深度需要提升以覆盖更多查询意图",
                "🎯 需要优化自然语言和长尾关键词"
            ]
        }
    
    def _get_fallback_platform_analysis(self):
        """平台分析的回退结果"""
        return {
            "platform_coverage": {
                "search_engines": "🔍 搜索引擎：基础SEO已实施，需要进一步优化技术配置和内容质量",
                "social_media": "📱 社交媒体：需要建立或加强社交媒体存在，提升品牌知名度",
                "knowledge_graphs": "🧠 知识图谱：需要改善在Google知识面板和相关实体中的表现"
            },
            "visibility_scores": {
                "google": 70,
                "bing": 65,
                "social": 45,
                "knowledge_graph": 58
            },
            "optimization_opportunities": [
                "🏪 优化Google我的商家资料，提升本地搜索表现",
                "📱 增强社交媒体活跃度，建立品牌社区",
                "🔗 提升在行业知识图谱中的权威地位",
                "📊 监控品牌搜索结果页面的完整性和准确性"
            ]
        }
    
    def _get_fallback_recommendations(self):
        """推荐建议的回退结果"""
        return {
            "strategic_recommendations": [
                "🎯 建立完整的关键词策略：研究目标关键词，分析搜索意图，制定内容计划",
                "🏗️ 优化网站技术架构：提升页面速度，改善移动端体验，确保搜索引擎可抓取性",
                "📝 提升内容质量：创建原创、深度、有价值的内容，满足用户搜索需求",
                "🔗 建立权威性链接：获得高质量外链，优化内部链接结构，提升域名权重"
            ],
            "quick_wins": [
                "✅ 优化页面标题：确保每页标题独特，包含主关键词，控制在30-60字符",
                "📄 完善Meta描述：编写吸引人的描述，包含关键词和行动号召，150-160字符",
                "🏷️ 添加Alt标签：为所有图片添加描述性alt标签，提升可访问性和SEO",
                "🔧 修复技术问题：检查并修复404错误、重复内容、缺失标题等技术SEO问题",
                "📱 优化移动体验：确保网站在移动设备上正常显示和快速加载"
            ],
            "long_term_strategy": [
                "📈 建立内容营销体系：定期发布高质量内容，建立行业权威地位",
                "🌐 扩展数字化存在：优化社交媒体，建设知识图谱，提升品牌知名度", 
                "🎓 培养专业权威性：展示专业知识，获得行业认可，建立信任度",
                "📊 数据驱动优化：持续监控SEO表现，根据数据调整策略，保持竞争优势"
            ],
            "priority_matrix": {
                "高影响-低成本": "🚀 页面标题和Meta描述优化、内部链接优化、技术SEO修复",
                "高影响-高成本": "📝 内容战略重建、网站架构改进、专业SEO团队建设",
                "低影响-低成本": "📱 社交媒体优化、图片alt标签添加、小幅内容更新",
                "低影响-高成本": "🔄 完整网站重建、大规模付费推广、品牌重塑"
            }
        }
    
    def _get_fallback_full_analysis(self, seo_data: Dict):
        """完整的回退分析结果"""
        return {
            "summary": {
                "entity_score": 60,
                "credibility_score": 60,
                "conversation_score": 60,
                "platform_score": 60,
            },
            "detailed_analysis": {
                **seo_data,
                "entity_analysis": self._get_fallback_entity_analysis(),
                "credibility_analysis": self._get_fallback_credibility_analysis(),
                "conversation_analysis": self._get_fallback_conversation_analysis(),
                "cross_platform_presence": self._get_fallback_platform_analysis(),
                "recommendations": self._get_fallback_recommendations()
            },
            "quick_wins": self._get_fallback_recommendations()["quick_wins"],
            "strategic_recommendations": self._get_fallback_recommendations()["strategic_recommendations"],
        }


# Example usage with async support
async def enhanced_modern_analyze(
    site: str, sitemap: Optional[str] = None, api_key: str = None, **kwargs
):
    """
    Enhanced analysis incorporating modern SEO principles using LangChain
    """
    from pyseoanalyzer import analyze

    # Run original analysis
    original_results = analyze(site, sitemap, **kwargs)

    # Enhance with modern SEO analysis if API key provided
    if api_key:
        enhancer = LLMSEOEnhancer()
        enhanced_results = await enhancer.enhance_seo_analysis(original_results)
        return enhancer._format_output(enhanced_results)

    return original_results
