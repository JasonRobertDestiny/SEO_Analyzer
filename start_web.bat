@echo off
chcp 65001 >nul
cls
echo.
echo ████████████████████████████████████████████████
echo ██                                            ██
echo ██        🔍 SEO分析工具 Web版本 🔍           ██
echo ██                                            ██
echo ████████████████████████████████████████████████
echo.
echo 💡 这是一个用户友好的网页版SEO分析工具
echo 📊 支持技术SEO检查和AI智能分析
echo 🤖 集成硅基流动Qwen2.5-VL模型
echo.
echo ⚡ 正在启动Web服务器...
timeout /t 2 /nobreak >nul
echo.

cd /d "%~dp0"

echo 🔧 检查Python环境...
D:/Python/python.exe --version
if errorlevel 1 (
    echo ❌ Python未找到，请确保Python已正确安装
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.
echo 🚀 启动Flask应用...
echo.
echo ┌─────────────────────────────────────────┐
echo │  访问地址: http://localhost:5000       │
echo │  按 Ctrl+C 可停止服务器               │
echo └─────────────────────────────────────────┘
echo.

D:/Python/python.exe web_app.py

echo.
echo 👋 服务器已停止
pause
