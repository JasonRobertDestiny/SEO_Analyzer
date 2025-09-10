# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running the Application
```bash
# Start the application
python start.py                 # FastAPI server on port 8000

# CLI usage
python -m pyseoanalyzer https://example.com
python -m pyseoanalyzer https://example.com --run-llm-analysis
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analyzer.py

# Run with coverage
pytest --cov=pyseoanalyzer
```

### Docker
```bash
# Build and run
docker build -t smartseo-analyzer .
docker run -p 8000:8000 smartseo-analyzer
```

## Architecture Overview

### Core Components
- **analyzer.py**: Main analysis orchestrator that coordinates crawling and analysis
- **website.py**: Handles website crawling, sitemap parsing, and page collection
- **page.py**: Individual page analysis for SEO metrics
- **llm_analyst.py**: AI-powered analysis using LangChain and SiliconFlow API
- **http.py**: HTTP request handling with rate limiting and error management

### Web Interface
- **FastAPI Implementation** (main.py, app/): Modern async framework with automatic API docs at /docs

### Key Design Patterns
- **Modular Architecture**: Analysis engine separated from web interface
- **Dual Interface**: Same core logic serves both CLI and web interfaces
- **Optional AI Enhancement**: LLM analysis is opt-in via --run-llm-analysis flag
- **Template-based Reports**: Uses Jinja2 for flexible report generation
- **Async Processing**: FastAPI supports concurrent analysis with background tasks

### Data Flow
1. Input URL → website.py crawls and collects pages
2. Each page → page.py extracts SEO metrics
3. Aggregated results → analyzer.py generates comprehensive report
4. Optional: Results → llm_analyst.py for AI-powered insights
5. Output → JSON/HTML via templates or direct web response

### Important Implementation Details
- Uses BeautifulSoup4 for HTML parsing and Trafilatura for content extraction
- Rate limiting implemented in http.py to respect server resources
- AI analysis requires SILICONFLOW_API_KEY in environment variables
- Automatic API documentation available at /docs (Swagger) and /redoc
- Production deployment via uvicorn with multiple worker support
- Background task management with persistence

### Environment Variables
- `SILICONFLOW_API_KEY`: Required for AI analysis features (SiliconFlow)
- `OPENAI_API_KEY`: Alternative OpenAI API key for AI analysis
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode with auto-reload (default: false)