"""
Risk Analyzer Module
Analyzes scam and deepfake risks
"""

from typing import Dict, List


class RiskAnalyzer:
    """Analyze risks in content"""
    
    def __init__(self):
        self.scam_indicators = [
            'buy now', 'limited time', 'act fast', 'only today',
            'click here', 'crypto', 'guaranteed returns', 'risk-free',
            'work from home', 'make money fast', 'payment required'
        ]
        
        self.deepfake_indicators = [
            'deepfake', 'ai generated', 'fake', 'synthetic',
            'altered', 'edited', 'morphed'
        ]
    
    def analyze(self, transcript: str, claims: List[Dict], video_info: Dict) -> Dict:
        """
        Analyze risks in content
        
        Args:
            transcript: Video transcript
            claims: Detected claims
            video_info: Video metadata
            
        Returns:
            Risk analysis results
        """
        
        analysis = {
            'scam_risk_level': self._assess_scam_risk(transcript, claims),
            'scam_risk_score': self._calculate_scam_score(transcript, claims),
            'deepfake_risk_level': self._assess_deepfake_risk(video_info, transcript),
            'deepfake_risk_score': self._calculate_deepfake_score(video_info),
            'manipulation_indicators': self._detect_manipulation(transcript),
            'red_flags': self._identify_red_flags(transcript, claims)
        }
        
        return analysis
    
    def _assess_scam_risk(self, transcript: str, claims: List[Dict]) -> str:
        """Assess overall scam risk level"""
        score = self._calculate_scam_score(transcript, claims)
        
        if score < 30:
            return 'low'
        elif score < 70:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_scam_score(self, transcript: str, claims: List[Dict]) -> int:
        """Calculate scam risk score (0-100)"""
        score = 10  # Base score
        
        transcript_lower = transcript.lower()
        
        # Check for scam indicators
        indicator_count = sum(1 for indicator in self.scam_indicators 
                            if indicator in transcript_lower)
        score += indicator_count * 8
        
        # Check for unverified claims
        unverified = sum(1 for claim in claims if claim.get('status') == 'unknown')
        score += unverified * 5
        
        # Check for suspicious language
        suspicious = sum(1 for claim in claims if claim.get('is_suspicious', False))
        score += suspicious * 10
        
        return min(100, max(0, score))
    
    def _assess_deepfake_risk(self, video_info: Dict, transcript: str) -> str:
        """Assess deepfake risk level"""
        score = self._calculate_deepfake_score(video_info)
        
        if score < 25:
            return 'low'
        elif score < 60:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_deepfake_score(self, video_info: Dict) -> int:
        """Calculate deepfake risk score (0-100)"""
        score = 15  # Base score for unknown videos
        
        # Check video quality indicators
        # Lower quality videos have higher deepfake risk
        # (In real implementation, would analyze video frames)
        
        platform = video_info.get('platform', '')
        
        # Platform-specific risk adjustments
        if platform == 'tiktok':
            score += 10  # TikTok has more edited content
        elif platform == 'instagram':
            score += 5   # Instagram also has significant editing
        
        # Duration-based check (very short videos have higher risk)
        duration = video_info.get('duration', 0)
        if duration < 15:
            score += 5
        
        return min(100, max(0, score))
    
    def _detect_manipulation(self, transcript: str) -> List[str]:
        """Detect manipulation tactics in content"""
        tactics = []
        transcript_lower = transcript.lower()
        
        # Emotional manipulation
        emotional_words = ['shocking', 'unbelievable', 'horrific', 'tragic', 'devastating']
        if any(word in transcript_lower for word in emotional_words):
            tactics.append('emotional_manipulation')
        
        # Social pressure
        if any(phrase in transcript_lower for phrase in ['everyone knows', 'most people', 'trend']):
            tactics.append('social_pressure')
        
        # Fear-mongering
        if any(phrase in transcript_lower for phrase in ['danger', 'warning', 'alert', 'threat']):
            tactics.append('fear_mongering')
        
        # Urgency tactics
        if any(phrase in transcript_lower for phrase in ['now', 'today', 'immediately', 'limited']):
            tactics.append('urgency_tactic')
        
        return tactics
    
    def _identify_red_flags(self, transcript: str, claims: List[Dict]) -> List[str]:
        """Identify specific red flags"""
        red_flags = []
        transcript_lower = transcript.lower()
        
        # Missing sources
        if 'study' not in transcript_lower and 'research' not in transcript_lower:
            red_flags.append('no_sources_cited')
        
        # Vague claims
        vague_phrases = [
            'some people say', 'they say', 'doctors hate',
            'this one trick', 'secret method'
        ]
        if any(phrase in transcript_lower for phrase in vague_phrases):
            red_flags.append('vague_language')
        
        # All claims unverified
        unverified_count = sum(1 for claim in claims if claim.get('status') == 'unknown')
        if unverified_count == len(claims) and len(claims) > 0:
            red_flags.append('all_unverified_claims')
        
        return red_flags
