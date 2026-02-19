"""
Helper functions and utilities
"""

import streamlit as st


def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Misinformation Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/misinformation-analyzer',
            'Report a bug': 'https://github.com/yourusername/misinformation-analyzer/issues',
            'About': '# Misinformation Analyzer\nAnalyze social media videos for credibility and risk.'
        }
    )


def format_risk_level(level: str) -> str:
    """Format risk level text with appropriate styling"""
    level_lower = level.lower()
    
    if level_lower == 'low':
        return '🟢 Low Risk'
    elif level_lower == 'medium':
        return '🟡 Medium Risk'
    elif level_lower == 'high':
        return '🔴 High Risk'
    else:
        return '⚪ Unknown'


def get_risk_color(level: str) -> str:
    """Get color code for risk level"""
    level_lower = level.lower()
    
    if level_lower == 'low':
        return '#27AE60'  # Green
    elif level_lower == 'medium':
        return '#F39C12'  # Orange
    elif level_lower == 'high':
        return '#E74C3C'  # Red
    else:
        return '#95A5A6'  # Gray


def validate_url(url: str) -> bool:
    """Validate if URL is from supported platform"""
    supported_domains = [
        'tiktok.com',
        'vm.tiktok.com',
        'instagram.com',
        'instagr.am',
        'youtube.com',
        'youtu.be'
    ]
    
    url_lower = url.lower()
    return any(domain in url_lower for domain in supported_domains)


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable format"""
    from datetime import datetime
    
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime('%B %d, %Y at %H:%M:%S')
    except:
        return timestamp


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text
