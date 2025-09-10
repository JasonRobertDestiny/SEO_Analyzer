#!/usr/bin/env python3
"""
性能配置模块
包含所有性能优化相关的配置和建议
"""

# 性能优化建议
PERFORMANCE_TIPS = [
    "🚀 使用闪电级模式进行快速首页检查",
    "⚡ 超级快速模式适合日常SEO监控(5-10页)",
    "🔄 启用缓存可减少90%的AI分析时间",
    "🎯 根据网站规模调整并发限制",
    "⏰ 设置合理的超时时间避免长时间等待",
    "📊 使用批量分析处理多个网站",
    "🛠️ 定期清理缓存保持分析准确性",
    "📈 监控分析性能指标优化配置",
    "🔧 针对网站类型选择合适的分析深度",
    "💾 使用本地缓存减少网络请求"
]

# 超时配置
TIMEOUT_CONFIG = {
    "lightning_mode": 15,          # 闪电级模式超时
    "super_fast_mode": 30,         # 超级快速模式超时
    "fast_mode": 60,               # 快速模式超时
    "standard_mode": 120,          # 标准模式超时
    "ai_analysis": 45,             # AI分析超时
    "single_page": 10,             # 单页面分析超时
    "batch_analysis": 300,         # 批量分析超时
    "cache_timeout": 3600          # 缓存超时(1小时)
}

# 并发配置
CONCURRENT_CONFIG = {
    "lightning": {
        "max_concurrent": 2,
        "semaphore_limit": 2,
        "connection_pool": 5
    },
    "super_fast": {
        "max_concurrent": 5,
        "semaphore_limit": 5,
        "connection_pool": 10
    },
    "fast": {
        "max_concurrent": 10,
        "semaphore_limit": 8,
        "connection_pool": 15
    },
    "standard": {
        "max_concurrent": 15,
        "semaphore_limit": 12,
        "connection_pool": 20
    }
}

# 分析模式配置
ANALYSIS_MODES = {
    "lightning": {
        "name": "闪电级",
        "description": "仅分析首页，3秒内完成",
        "max_pages": 1,
        "ai_enabled": False,
        "cache_enabled": True,
        "timeout": TIMEOUT_CONFIG["lightning_mode"],
        "concurrent": CONCURRENT_CONFIG["lightning"],
        "use_case": "快速页面检查，SEO监控"
    },
    "super_fast": {
        "name": "超级快速",
        "description": "分析5-10个核心页面，30秒内完成",
        "max_pages": 10,
        "ai_enabled": True,
        "ai_mode": "lightweight",
        "cache_enabled": True,
        "timeout": TIMEOUT_CONFIG["super_fast_mode"],
        "concurrent": CONCURRENT_CONFIG["super_fast"],
        "use_case": "日常SEO分析，竞争对手监控"
    },
    "fast": {
        "name": "快速",
        "description": "分析15-20个页面，包含基础AI分析",
        "max_pages": 20,
        "ai_enabled": True,
        "ai_mode": "standard",
        "cache_enabled": True,
        "timeout": TIMEOUT_CONFIG["fast_mode"],
        "concurrent": CONCURRENT_CONFIG["fast"],
        "use_case": "全面SEO审核，优化建议"
    },
    "standard": {
        "name": "标准",
        "description": "全面分析，包含深度AI洞察",
        "max_pages": 50,
        "ai_enabled": True,
        "ai_mode": "enhanced",
        "cache_enabled": False,
        "timeout": TIMEOUT_CONFIG["standard_mode"],
        "concurrent": CONCURRENT_CONFIG["standard"],
        "use_case": "详细SEO报告，策略制定"
    }
}

# 缓存配置
CACHE_CONFIG = {
    "enabled": True,
    "max_size": 1000,              # 最大缓存条目数
    "ttl": 3600,                   # 生存时间(秒)
    "cleanup_interval": 300,        # 清理间隔(秒)
    "compression": True,            # 启用压缩
    "memory_limit": 100            # 内存限制(MB)
}

# AI性能配置
AI_PERFORMANCE_CONFIG = {
    "lightweight": {
        "model": "lightweight",
        "max_tokens": 1000,
        "temperature": 0.3,
        "timeout": 15,
        "retry_attempts": 2,
        "cache_results": True
    },
    "standard": {
        "model": "standard",
        "max_tokens": 2000,
        "temperature": 0.5,
        "timeout": 30,
        "retry_attempts": 3,
        "cache_results": True
    },
    "enhanced": {
        "model": "enhanced",
        "max_tokens": 4000,
        "temperature": 0.7,
        "timeout": 60,
        "retry_attempts": 3,
        "cache_results": False
    }
}

# 网络配置
NETWORK_CONFIG = {
    "user_agent": "SmartSEO-Analyzer/2.0 (Performance Optimized)",
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    "max_redirects": 5,
    "ssl_verify": False,           # 在测试环境中禁用SSL验证以提高速度
    "cookie_jar": True
}

# 资源限制配置
RESOURCE_LIMITS = {
    "max_memory_usage": 512,       # MB
    "max_cpu_usage": 80,          # 百分比
    "max_disk_space": 1024,       # MB (缓存)
    "max_open_files": 1000,
    "max_network_connections": 100
}

# 监控配置
MONITORING_CONFIG = {
    "enabled": True,
    "log_performance": True,
    "track_memory": True,
    "track_network": True,
    "alert_thresholds": {
        "response_time": 10,       # 秒
        "memory_usage": 400,       # MB
        "error_rate": 0.1         # 10%
    }
}

# 优化建议配置
OPTIMIZATION_RECOMMENDATIONS = {
    "small_site": {
        "pages": "< 10",
        "recommended_mode": "lightning",
        "tips": [
            "使用闪电级模式即可满足需求",
            "启用缓存优化重复分析",
            "可增加AI分析获得更多洞察"
        ]
    },
    "medium_site": {
        "pages": "10-50",
        "recommended_mode": "super_fast",
        "tips": [
            "超级快速模式最适合中型网站",
            "启用轻量级AI分析",
            "考虑定期清理缓存"
        ]
    },
    "large_site": {
        "pages": "50-200",
        "recommended_mode": "fast",
        "tips": [
            "使用快速模式平衡速度和深度",
            "增加并发限制以提高效率",
            "分批次进行大规模分析"
        ]
    },
    "enterprise_site": {
        "pages": "> 200",
        "recommended_mode": "standard",
        "tips": [
            "采用标准模式进行全面分析",
            "使用批量处理提高效率",
            "实施监控和警报机制"
        ]
    }
}

# 性能基准配置
PERFORMANCE_BENCHMARKS = {
    "excellent": {
        "pages_per_second": "> 5",
        "total_time": "< 10s",
        "memory_usage": "< 100MB",
        "success_rate": "> 95%"
    },
    "good": {
        "pages_per_second": "2-5",
        "total_time": "10-30s",
        "memory_usage": "100-200MB",
        "success_rate": "90-95%"
    },
    "acceptable": {
        "pages_per_second": "1-2",
        "total_time": "30-60s",
        "memory_usage": "200-300MB",
        "success_rate": "80-90%"
    },
    "needs_improvement": {
        "pages_per_second": "< 1",
        "total_time": "> 60s",
        "memory_usage": "> 300MB",
        "success_rate": "< 80%"
    }
}


def get_mode_config(mode: str) -> dict:
    """获取指定模式的配置"""
    return ANALYSIS_MODES.get(mode, ANALYSIS_MODES["super_fast"])


def get_optimal_config(page_count: int, priority: str = "speed") -> dict:
    """根据页面数量和优先级获取最优配置"""
    if page_count <= 1:
        return get_mode_config("lightning")
    elif page_count <= 10:
        return get_mode_config("super_fast")
    elif page_count <= 20:
        return get_mode_config("fast")
    else:
        return get_mode_config("standard")


def get_concurrent_limits(mode: str) -> dict:
    """获取并发限制配置"""
    return CONCURRENT_CONFIG.get(mode, CONCURRENT_CONFIG["super_fast"])


def get_timeout_config(mode: str) -> int:
    """获取超时配置"""
    timeout_map = {
        "lightning": TIMEOUT_CONFIG["lightning_mode"],
        "super_fast": TIMEOUT_CONFIG["super_fast_mode"],
        "fast": TIMEOUT_CONFIG["fast_mode"],
        "standard": TIMEOUT_CONFIG["standard_mode"]
    }
    return timeout_map.get(mode, TIMEOUT_CONFIG["super_fast_mode"])


def get_ai_config(ai_mode: str) -> dict:
    """获取AI配置"""
    return AI_PERFORMANCE_CONFIG.get(ai_mode, AI_PERFORMANCE_CONFIG["lightweight"])


def validate_config(config: dict) -> bool:
    """验证配置是否有效"""
    required_keys = ["max_pages", "timeout", "concurrent"]
    return all(key in config for key in required_keys)


def get_performance_tips_for_mode(mode: str) -> list:
    """获取特定模式的性能建议"""
    mode_tips = {
        "lightning": [
            "闪电级模式专为快速检查设计",
            "适合首页SEO健康度监控",
            "启用缓存可进一步提升速度"
        ],
        "super_fast": [
            "最佳的速度与深度平衡",
            "适合日常SEO分析任务", 
            "启用轻量级AI获得智能建议"
        ],
        "fast": [
            "提供全面的SEO分析",
            "包含基础AI洞察",
            "适合定期SEO审核"
        ],
        "standard": [
            "最详细的SEO分析报告",
            "包含深度AI策略建议",
            "适合制定SEO优化策略"
        ]
    }
    return mode_tips.get(mode, PERFORMANCE_TIPS[:3])
