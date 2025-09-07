from flask import Flask, render_template, request, jsonify, send_file
from pyseoanalyzer import analyze
import json
import os
import tempfile
from datetime import datetime
import traceback

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_website():
    """网站分析API"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': '请输入有效的网站URL'}), 400
        
        # 确保URL有协议前缀
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 获取分析选项
        options = {
            'sitemap_url': data.get('sitemap_url'),
            'analyze_headings': data.get('analyze_headings', False),
            'analyze_extra_tags': data.get('analyze_extra_tags', False),
            'follow_links': data.get('follow_links', True),
            'run_llm_analysis': data.get('run_llm_analysis', False)
        }
        
        # 执行分析
        result = analyze(url, **options)
        
        # 添加分析时间戳
        result['analyzed_at'] = datetime.now().isoformat()
        result['analyzed_url'] = url
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'分析失败: {error_msg}'
        }), 500

@app.route('/download_report', methods=['POST'])
def download_report():
    """下载HTML报告"""
    try:
        data = request.get_json()
        result = data.get('result')
        
        if not result:
            return jsonify({'error': '没有分析结果可下载'}), 400
        
        # 使用Jinja2模板生成HTML报告
        from jinja2 import Environment, FileSystemLoader
        
        # 获取模板路径
        template_dir = os.path.join(os.path.dirname(__file__), 'pyseoanalyzer', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('index.html')
        
        # 生成HTML内容
        html_content = template.render(result=result)
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html_content)
        temp_file.close()
        
        # 生成文件名
        analyzed_url = result.get('analyzed_url', 'website')
        filename = f"seo_report_{analyzed_url.replace('://', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'生成报告失败: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
