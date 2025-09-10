# SmartSEO 启动指南

## 🚀 快速启动

### 启动应用
```bash
# 启动 SmartSEO 服务
python start.py
```

### 访问应用
- **Web界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📋 系统要求

- Python 3.8+
- pip 包管理器

## 🔧 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/JasonRobertDestiny/SmartSEO_Analyzer.git
cd SmartSEO_Analyzer
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 API 密钥
# SILICONFLOW_API_KEY=your_api_key_here
```

## 🎯 使用方法

### Web界面
1. 启动服务：`python start.py`
2. 访问：http://localhost:8000
3. 输入要分析的网站URL
4. 选择分析选项
5. 点击开始分析

### 命令行使用
```bash
# 基础分析
python -m pyseoanalyzer https://example.com

# 启用AI分析
python -m pyseoanalyzer https://example.com --run-llm-analysis

# 生成HTML报告
python -m pyseoanalyzer https://example.com -f html > report.html
```

## ⚙️ 配置选项

### 环境变量
- `HOST`: 服务器地址（默认：0.0.0.0）
- `PORT`: 服务器端口（默认：8000）
- `DEBUG`: 调试模式（默认：false）
- `SILICONFLOW_API_KEY`: AI分析API密钥

### 分析模式
- `lightning`: 极速模式（最快）
- `super_fast`: 超快模式（推荐）
- `fast`: 快速模式
- `full`: 完整模式（最详细）

## 🐳 Docker部署

### 构建镜像
```bash
docker build -t smartseo-analyzer .
```

### 运行容器
```bash
docker run -p 8000:8000 smartseo-analyzer
```

## 🔍 故障排除

### 端口占用
如果8000端口被占用，可以指定其他端口：
```bash
# Linux/macOS
PORT=8001 python start.py

# Windows
set PORT=8001
python start.py
```

### 依赖问题
如果遇到依赖错误，尝试：
```bash
pip install --upgrade -r requirements.txt
```

### AI分析失败
如果AI分析功能无法使用：
1. 检查 `SILICONFLOW_API_KEY` 是否正确设置
2. 确认网络连接正常
3. 查看服务器日志获取详细错误信息

## 📚 更多信息

- [项目文档](README.md)
- [API文档](http://localhost:8000/docs)
- [提交问题](https://github.com/JasonRobertDestiny/SmartSEO_Analyzer/issues)