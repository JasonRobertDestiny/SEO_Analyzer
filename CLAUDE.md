# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running the Application
```bash
# CLI usage
python -m pyseoanalyzer https://example.com
python -m pyseoanalyzer https://example.com --run-llm-analysis

# Web interface
python web_app.py                    # Development server
python start_production.py           # Production server
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
docker run -p 5000:5000 smartseo-analyzer
```

## Architecture Overview

### Core Components
- **analyzer.py**: Main analysis orchestrator that coordinates crawling and analysis
- **website.py**: Handles website crawling, sitemap parsing, and page collection
- **page.py**: Individual page analysis for SEO metrics
- **llm_analyst.py**: AI-powered analysis using LangChain and OpenAI/SiliconFlow APIs
- **http.py**: HTTP request handling with rate limiting and error management

### Key Design Patterns
- **Modular Architecture**: Analysis engine separated from web interface
- **Dual Interface**: Same core logic serves both CLI and web interfaces
- **Optional AI Enhancement**: LLM analysis is opt-in via --run-llm-analysis flag
- **Template-based Reports**: Uses Jinja2 for flexible report generation

### Data Flow
1. Input URL → website.py crawls and collects pages
2. Each page → page.py extracts SEO metrics
3. Aggregated results → analyzer.py generates comprehensive report
4. Optional: Results → llm_analyst.py for AI-powered insights
5. Output → JSON/HTML via templates or direct web response

### Important Implementation Details
- Uses BeautifulSoup4 for HTML parsing and Trafilatura for content extraction
- Rate limiting implemented in http.py to respect server resources
- AI analysis requires valid API keys in environment variables
- Web interface uses Flask with Bootstrap 5 for responsive design
- Production deployment via Gunicorn (Unix) or Waitress (Windows)

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `SILICONFLOW_API_KEY`: SiliconFlow API key (alternative to OpenAI)
- `FLASK_ENV`: Set to 'production' for deployment