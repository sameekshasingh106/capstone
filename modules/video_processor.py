"""
Video Processor Module
Extracts video information from platform links
"""

import re
from typing import Dict, Optional


class VideoProcessor:
    """Process video links and extract metadata"""
    
    def __init__(self):
        self.supported_platforms = ['tiktok', 'instagram', 'youtube']
    
    def process_link(self, url: str) -> Optional[Dict]:
        """
        Process video link and extract metadata
        
        Args:
            url: Video URL
            
        Returns:
            Dictionary with video info or None if invalid
        """
        
        if not url:
            return None
        
        # Determine platform
        platform = self._identify_platform(url)
        
        if not platform:
            return None
        
        # Extract video ID based on platform
        if platform == 'tiktok':
            video_id = self._extract_tiktok_id(url)
        elif platform == 'instagram':
            video_id = self._extract_instagram_id(url)
        elif platform == 'youtube':
            video_id = self._extract_youtube_id(url)
        else:
            return None
        
        if not video_id:
            return None
        
        return {
            'platform': platform,
            'url': url,
            'video_id': video_id,
            'title': 'Video Analysis',  # Would be extracted from platform API
            'duration': 0,  # Would be extracted from platform API
            'upload_date': None,  # Would be extracted from platform API
        }
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identify platform from URL"""
        url_lower = url.lower()
        
        if 'tiktok.com' in url_lower or 'vm.tiktok.com' in url_lower:
            return 'tiktok'
        elif 'instagram.com' in url_lower or 'instagr.am' in url_lower:
            return 'instagram'
        elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        
        return None
    
    def _extract_tiktok_id(self, url: str) -> Optional[str]:
        """Extract TikTok video ID"""
        # Pattern for tiktok.com/video/{id}
        match = re.search(r'/video/(\d+)', url)
        if match:
            return match.group(1)
        
        # Pattern for vm.tiktok.com/{id}
        match = re.search(r'/([a-zA-Z0-9]+)$', url)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_instagram_id(self, url: str) -> Optional[str]:
        """Extract Instagram video/reel ID"""
        # Pattern for instagram.com/p/{id} or /reel/{id}
        match = re.search(r'/(p|reel)/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(2)
        
        return None
    
    def _extract_youtube_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID"""
        # Pattern for youtube.com/watch?v={id}
        match = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
        if match:
            return match.group(1)
        
        # Pattern for youtu.be/{id}
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
        if match:
            return match.group(1)
        
        return None
