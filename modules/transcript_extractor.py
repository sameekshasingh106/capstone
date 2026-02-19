"""
Transcript Extractor Module - Enhanced
Extracts transcripts from videos using various methods
Gracefully handles unavailable transcripts with informative messages
"""

from typing import Dict, Optional


class TranscriptExtractor:
    """Extract transcripts from videos with graceful fallback"""
    
    def __init__(self):
        self.supported_platforms = ['youtube', 'tiktok', 'instagram']
        self.extraction_notes = {}
    
    def extract(self, video_info: Dict) -> Optional[str]:
        """
        Extract transcript from video with full fallback support
        
        Args:
            video_info: Video metadata dictionary
            
        Returns:
            Transcript text, None if unavailable, or info message
        """
        
        platform = video_info.get('platform', '')
        video_id = video_info.get('video_id')
        
        if not video_id:
            return None
        
        # Try platform-specific extraction
        if platform == 'youtube':
            transcript = self._extract_youtube_transcript(video_id)
        elif platform == 'tiktok':
            transcript = self._extract_tiktok_transcript(video_info)
        elif platform == 'instagram':
            transcript = self._extract_instagram_transcript(video_info)
        else:
            return None
        
        return transcript
    
    def _extract_youtube_transcript(self, video_id: str) -> Optional[str]:
        """
        Extract transcript from YouTube video
        
        Supports:
        - Manually created captions (preferred)
        - Auto-generated captions
        - Multiple languages
        
        Returns None gracefully if unavailable
        """
        if not video_id:
            return None
        
        try:
            # Try to import YouTube Transcript API
            from youtube_transcript_api import YouTubeTranscriptApi
            from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
            
            try:
                # List available transcripts
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # Prefer manually created transcripts
                if transcript_list.manually_created_transcripts:
                    transcript = transcript_list.manually_created_transcripts[0]
                    transcript_data = transcript.fetch()
                    return ' '.join([item['text'] for item in transcript_data])
                
                # Fall back to auto-generated
                elif transcript_list.generated_transcripts:
                    transcript = transcript_list.generated_transcripts[0]
                    transcript_data = transcript.fetch()
                    return ' '.join([item['text'] for item in transcript_data])
                else:
                    return None
                    
            except (TranscriptsDisabled, NoTranscriptFound) as e:
                # Video has transcripts disabled or none available
                print(f"Transcripts not available for YouTube video {video_id}")
                return None
                
        except ImportError:
            print("youtube-transcript-api not installed")
            return None
        except Exception as e:
            print(f"Error extracting YouTube transcript: {e}")
            return None
    
    def _extract_tiktok_transcript(self, video_info: Dict) -> Optional[str]:
        """
        Extract transcript from TikTok
        
        Note: TikTok videos typically don't have accessible transcripts due to:
        - Platform restrictions
        - No public API for captions
        - Text overlays require OCR (requires video download)
        - Audio requires speech-to-text (requires video download)
        
        Future enhancement will use:
        - yt-dlp for video download
        - EasyOCR for text overlays
        - Whisper API for audio transcription
        
        Currently returns None to allow analysis to proceed
        without transcript data.
        """
        return None
    
    def _extract_instagram_transcript(self, video_info: Dict) -> Optional[str]:
        """
        Extract transcript from Instagram
        
        Note: Similar to TikTok, Instagram Reels/Videos have:
        - No public transcript API
        - Text overlays (requires OCR)
        - Audio content (requires speech-to-text)
        
        Currently returns None. When transcript unavailable,
        app analyzes available metadata and visual indicators.
        """
        return None
    
    @staticmethod
    def get_transcript_availability(video_id: str, platform: str) -> Dict:
        """
        Check what transcript formats are available for a video
        
        Returns a detailed dictionary with availability info
        """
        if platform != 'youtube':
            return {
                'available': False,
                'platform': platform,
                'reason': 'Platform transcripts not yet supported'
            }
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            return {
                'available': True,
                'video_id': video_id,
                'manually_created': bool(transcript_list.manually_created_transcripts),
                'auto_generated': bool(transcript_list.generated_transcripts),
                'languages': [t.language for t in (
                    transcript_list.manually_created_transcripts + 
                    transcript_list.generated_transcripts
                )]
            }
        except Exception as e:
            return {
                'available': False,
                'video_id': video_id,
                'reason': str(e)
            }
