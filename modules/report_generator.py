"""
Report Generator Module
Generates analysis reports in various formats
"""

from typing import Dict
from datetime import datetime
import json


class ReportGenerator:
    """Generate analysis reports"""
    
    def __init__(self):
        self.report_formats = ['json', 'pdf', 'html']
    
    def generate(self, analysis_results: Dict, format_type: str = 'json') -> str:
        """
        Generate analysis report
        
        Args:
            analysis_results: Complete analysis results
            format_type: Output format (json, pdf, html)
            
        Returns:
            Report as string or file path
        """
        
        if format_type == 'json':
            return self._generate_json_report(analysis_results)
        elif format_type == 'pdf':
            return self._generate_pdf_report(analysis_results)
        elif format_type == 'html':
            return self._generate_html_report(analysis_results)
        else:
            return self._generate_json_report(analysis_results)
    
    def _generate_json_report(self, analysis_results: Dict) -> str:
        """Generate JSON format report"""
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'version': '1.0',
                'tool': 'Misinformation Analyzer'
            },
            'analysis': analysis_results
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_pdf_report(self, analysis_results: Dict) -> str:
        """
        Generate PDF format report
        
        Future implementation will use:
        - reportlab
        - weasyprint
        """
        # Placeholder for PDF implementation
        return "PDF report generation coming soon"
    
    def _generate_html_report(self, analysis_results: Dict) -> str:
        """
        Generate HTML format report
        
        Creates a standalone HTML file with embedded CSS and data
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Misinformation Analysis Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #0066cc;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #0066cc;
                    margin-top: 30px;
                }}
                .score-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    font-size: 48px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .risk-section {{
                    display: flex;
                    gap: 20px;
                    margin: 20px 0;
                }}
                .risk-card {{
                    flex: 1;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .risk-low {{
                    background-color: #d4edda;
                    color: #155724;
                }}
                .risk-medium {{
                    background-color: #fff3cd;
                    color: #856404;
                }}
                .risk-high {{
                    background-color: #f8d7da;
                    color: #721c24;
                }}
                .claim {{
                    background-color: #f8f9fa;
                    padding: 12px;
                    margin: 10px 0;
                    border-left: 4px solid #0066cc;
                    border-radius: 4px;
                }}
                .timestamp {{
                    color: #666;
                    font-size: 12px;
                    text-align: right;
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Misinformation Analysis Report</h1>
                
                <div class="score-card">
                    {analysis_results.get('credibility_score', 0)}/100
                </div>
                
                <h2>Risk Assessment</h2>
                <div class="risk-section">
                    <div class="risk-card risk-{analysis_results['risk_analysis'].get('scam_risk_level', 'low')}">
                        <strong>Scam Risk</strong><br>
                        {analysis_results['risk_analysis'].get('scam_risk_level', 'low').upper()}
                    </div>
                    <div class="risk-card risk-{analysis_results['risk_analysis'].get('deepfake_risk_level', 'low')}">
                        <strong>Deepfake Risk</strong><br>
                        {analysis_results['risk_analysis'].get('deepfake_risk_level', 'low').upper()}
                    </div>
                </div>
                
                <h2>Detected Claims</h2>
                {self._claims_to_html(analysis_results.get('claims', []))}
                
                <h2>Video Information</h2>
                <p><strong>Platform:</strong> {analysis_results['video_info'].get('platform', 'Unknown')}</p>
                <p><strong>URL:</strong> <a href="{analysis_results['url']}">{analysis_results['url']}</a></p>
                
                <div class="timestamp">
                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _claims_to_html(self, claims: list) -> str:
        """Convert claims to HTML"""
        if not claims:
            return "<p>No significant claims detected.</p>"
        
        html = ""
        for claim in claims:
            html += f"""
            <div class="claim">
                <p><strong>Claim:</strong> {claim.get('text', 'N/A')}</p>
                <p><strong>Status:</strong> {claim.get('status', 'unknown').upper()}</p>
                <p><strong>Confidence:</strong> {claim.get('confidence', 0)}%</p>
            </div>
            """
        
        return html
