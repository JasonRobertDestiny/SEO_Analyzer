# 🚀 SmartSEO - AI-Powered SEO Analysis Platform

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

## ⚡ Quick Start [快速开始](#快速开始)

### 🎯 One-Click Launch [一键启动](#一键启动)

```bash
# 启动SmartSEO服务
python start.py
```

### 🌐 Access URLs [访问地址](#访问地址)

| Service | URL | Description |
|---------|-----|-------------|
| 🚀 **SmartSEO** | http://localhost:8000 | 现代化SEO分析平台 |
| 📖 **API Docs** | http://localhost:8000/docs | 交互式API文档 |
| 🏥 **Health Check** | http://localhost:8000/health | 服务状态检查 |

### 📁 Key Files [关键文件](#关键文件)

- **`start.py`** → 🚀 主启动脚本
- **`main.py`** → 📱 FastAPI应用核心
- **`app/`** → 📁 应用模块目录
- **`pyseoanalyzer/`** → 🔍 SEO分析引擎

> 💡 **建议**: 服务启动后访问 http://localhost:8000 即可使用Web界面进行SEO分析！

---

## 📋 Overview [概述](#概述)

SmartSEO is an intelligent SEO analysis platform that combines traditional technical SEO audits with cutting-edge AI-powered insights. Features both a powerful command-line tool and an intuitive web interface, making professional SEO analysis accessible to everyone.

SmartSEO是一个智能SEO分析平台，结合了传统的技术SEO审计和尖端的AI驱动洞察。拥有强大的命令行工具和直观的Web界面，使专业SEO分析对每个人都变得可及。


## ✨ Key Features [主要功能](#主要功能)

### 🎯 Dual Interface Experience [双界面体验](#双界面体验)
- **Web Interface**: Modern, user-friendly GUI for non-technical users
- **CLI Tool**: Powerful command-line interface for developers and automation

- **Web界面**: 现代、用户友好的GUI，适合非技术用户
- **CLI工具**: 强大的命令行界面，适合开发者和自动化

### 🤖 AI-Enhanced Analysis [AI增强分析](#ai增强分析)
- **Qwen2.5-VL-72B Model**: Advanced language model for deep SEO insights
- **Entity Optimization**: Knowledge panel readiness assessment
- **Credibility Analysis**: N-E-E-A-T-T principle evaluation
- **Conversational Search**: Voice search and AI assistant optimization
- **Platform Presence**: Multi-platform visibility scoring

- **Qwen2.5-VL-72B模型**: 用于深度SEO洞察的高级语言模型
- **实体优化**: 知识面板准备度评估
- **可信度分析**: N-E-E-A-T-T原则评估
- **对话搜索**: 语音搜索和AI助手优化
- **平台存在感**: 多平台可见性评分

### 🔍 Comprehensive Technical SEO [全面技术SEO](#全面技术-seo)
- **On-Page Analysis**: Titles, descriptions, headings, meta tags
- **Content Optimization**: Keyword density, readability, structure
- **Technical Health**: Image alt attributes, internal linking, duplicates
- **Performance Metrics**: Page load insights and optimization suggestions

- **页面分析**: 标题、描述、标题标签、元标签
- **内容优化**: 关键词密度、可读性、结构
- **技术健康**: 图片alt属性、内部链接、重复内容
- **性能指标**: 页面加载洞察和优化建议

## 🚀 Quick Start [快速开始](#快速开始)

### Local Installation [本地安装](#本地安装)

**Install Dependencies [安装依赖]**
```bash
pip install -r requirements.txt
```

**Start Web Interface [启动Web界面]**
```bash
# Windows
python web_app.py

# macOS/Linux
python web_app.py
```

**Access Application [访问应用]**
Open your browser to: http://localhost:8000

打开浏览器访问: http://localhost:8000

### 4. Command Line Usage [命令行使用](#命令行使用)

```bash
# Basic analysis
smartseo https://example.com

# AI-powered analysis
smartseo https://example.com --run-llm-analysis

# Generate HTML report
smartseo https://example.com --output-format html > report.html

# Custom sitemap
smartseo https://example.com --sitemap https://example.com/sitemap.xml
```

## ⚙️ Configuration [配置](#配置)

### AI Features Setup [AI功能设置](#ai功能设置)
1. Get API key from [SiliconFlow](https://siliconflow.cn/)
2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   SILICONFLOW_API_KEY=your_api_key_here
   ```

1. 从[SiliconFlow](https://siliconflow.cn/)获取API密钥
2. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑.env文件，添加您的API密钥
   SILICONFLOW_API_KEY=your_api_key_here
   ```

## 📊 Analysis Features [分析功能](#分析功能)

### AI-Powered Insights [AI驱动洞察](#ai驱动洞察)
- **Entity Score**: Optimize for knowledge graphs and rich snippets
- **Credibility Score**: Build trust and authority signals
- **Conversation Score**: Prepare for voice and conversational search
- **Platform Score**: Enhance cross-platform visibility

- **实体得分**: 优化知识图谱和丰富摘要
- **可信度得分**: 建立信任和权威信号
- **对话得分**: 为语音和对话搜索做准备
- **平台得分**: 增强跨平台可见性

### Technical SEO Checks [技术SEO检查](#技术-seo-检查)
- ✅ Title tag optimization (10-70 characters)
- ✅ Meta description quality (140-255 characters)
- ✅ Heading structure (H1-H6 hierarchy)
- ✅ Image alt attributes
- ✅ Open Graph and Twitter Cards
- ✅ Internal link optimization
- ✅ Mobile responsiveness indicators
- ✅ Page performance metrics

- ✅ 标题标签优化（10-70个字符）
- ✅ 元描述质量（140-255个字符）
- ✅ 标题结构（H1-H6层级）
- ✅ 图片alt属性
- ✅ Open Graph和Twitter Cards
- ✅ 内部链接优化
- ✅ 移动响应性指标
- ✅ 页面性能指标

## 🎨 User Interface [用户界面](#用户界面)

### Modern Web Experience [现代Web体验](#现代-web-体验)
- **Responsive Design**: Works seamlessly on all devices
- **Real-time Progress**: Live analysis status updates
- **Visual Scoring**: Color-coded performance indicators
- **Professional Reports**: Download detailed PDF/HTML reports
- **Interactive Dashboard**: Comprehensive SEO overview

- **响应式设计**: 在所有设备上无缝工作
- **实时进度**: 实时分析状态更新
- **视觉评分**: 颜色编码的性能指标
- **专业报告**: 下载详细的PDF/HTML报告
- **交互式仪表板**: 全面的SEO概览

### Smart Analysis Workflow [智能分析工作流](#智能分析工作流)
1. Enter website URL
2. Configure analysis options
3. Launch with one click
4. View real-time progress
5. Explore detailed results
6. Download actionable reports

1. 输入网站URL
2. 配置分析选项
3. 一键启动
4. 查看实时进度
5. 探索详细结果
6. 下载可行报告

## 🏗️ Architecture [架构](#架构)

### Backend Stack [后端技术栈](#后端技术栈)
- **Python 3.8+**: Core language
- **FastAPI**: Web framework
- **LangChain**: AI orchestration
- **BeautifulSoup**: HTML parsing
- **Trafilatura**: Content extraction

### Frontend Stack [前端技术栈](#前端技术栈)
- **Bootstrap 5**: UI framework
- **Font Awesome**: Icon system
- **Chart.js**: Data visualization
- **Vanilla JS**: Interactions

### AI Integration [AI集成](#ai集成)
- **Qwen2.5-VL-72B**: Primary analysis model
- **SiliconFlow**: Model hosting
- **Structured Output**: Pydantic validation

## 📈 Use Cases [使用场景](#使用场景)

### For Businesses [为企业](#为企业)
- Regular SEO health monitoring
- Competitor analysis
- ROI tracking for SEO investments
- Agency-client reporting

- 定期SEO健康监控
- 竞争对手分析
- SEO投资ROI跟踪
- 机构-客户报告

### For SEO Professionals [为SEO专业人士](#为-seo-专业人士)
- Bulk website analysis
- Technical SEO audits
- Client proposal generation
- Performance tracking

- 批量网站分析
- 技术SEO审计
- 客户方案生成
- 性能跟踪

### For Content Creators [为内容创作者](#为内容创作者)
- Content optimization scoring
- Keyword opportunity identification
- Readability improvements
- Search intent alignment

- 内容优化评分
- 关键词机会识别
- 可读性改进
- 搜索意图对齐

## 🔄 Updates [更新](#更新)

### Version 2.0.0 - SmartSEO Edition [SmartSEO版本](#smartseo-版本)
- ✅ Complete UI/UX redesign
- ✅ AI analysis integration
- ✅ Real-time progress tracking
- ✅ Enhanced reporting features
- ✅ Mobile-first responsive design
- ✅ One-click cloud deployment

- ✅ 完整的UI/UX重新设计
- ✅ AI分析集成
- ✅ 实时进度跟踪
- ✅ 增强的报告功能
- ✅ 移动优先的响应式设计
- ✅ 一键云端部署

## 🤝 Contributing [贡献](#贡献)

We welcome contributions! Please see our contributing guidelines:

我们欢迎贡献！请查看我们的贡献指南：

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 打开Pull Request

## 📄 License [许可证](#许可证)

This project is licensed under the BSD License - see the [LICENSE](LICENSE) file for details.

本项目采用BSD许可证 - 详情请查看[LICENSE](LICENSE)文件。

## 🙏 Acknowledgments [致谢](#致谢)

- Original Python SEO Analyzer by [Seth Black](https://github.com/sethblack)
- AI models powered by [SiliconFlow](https://siliconflow.cn/)
- All contributors and the open-source community

- 原始Python SEO Analyzer作者[Seth Black](https://github.com/sethblack)
- AI模型由[SiliconFlow](https://siliconflow.cn/)提供支持
- 所有贡献者和开源社区

## 📞 Support [支持](#支持)

- 📧 Create an issue for bug reports
- 📖 Check our [documentation](DEPLOYMENT.md)
- 💬 Join our community discussions

- 📧 创建问题报告错误
- 📖 查看我们的[文档](DEPLOYMENT.md)
- 💬 加入我们的社区讨论

---

**SmartSEO - Making SEO Analysis Intelligent and Accessible** 🚀

**SmartSEO - 让SEO分析变得智能和可及** 🚀