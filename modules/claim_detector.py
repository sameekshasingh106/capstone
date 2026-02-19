"""
Claim Detector Module
Identifies and extracts claims from transcript
"""

from typing import List, Dict
import re


class ClaimDetector:
    """Detect factual claims in text"""
    
    def __init__(self):
        self.claim_keywords = [
            'studies show', 'research proves', 'data shows', 'experts say',
            'doctors recommend', 'scientists discovered', 'proven fact',
            'statistics show', 'according to', 'it was found that'
        ]
        
        self.suspicious_keywords = [
            'they dont want you to know', 'secret', 'hidden truth',
            'big pharma', 'government conspiracy', 'cover up',
            'shocking', 'unbelievable', 'this one trick'
        ]
    
    def detect_claims(self, text: str) -> List[Dict]:
        """
        Detect factual claims in text
        
        Args:
            text: Input text/transcript
            
        Returns:
            List of detected claims with metadata
        """
        
        if not text or len(text) < 10:
            return []
        
        claims = []
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        for sentence in sentences:
            if self._contains_claim(sentence):
                claim_obj = {
                    'text': sentence.strip(),
                    'confidence': self._calculate_claim_confidence(sentence),
                    'status': 'unknown',  # Will be filled by fact-checker
                    'is_suspicious': self._is_suspicious_claim(sentence),
                    'keywords_found': self._extract_keywords(sentence)
                }
                claims.append(claim_obj)
        
        return claims[:10]  # Limit to top 10 claims
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting - can be improved with NLTK
        sentences = re.split(r'[.!?]\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _contains_claim(self, sentence: str) -> bool:
        """Check if sentence contains a factual claim"""
        sentence_lower = sentence.lower()
        
        # Check for claim keywords
        has_claim_keyword = any(keyword in sentence_lower for keyword in self.claim_keywords)
        
        # Check for common claim patterns
        has_number = bool(re.search(r'\d+[%]?', sentence))
        
        # Check length (claims are usually longer)
        is_long_enough = len(sentence.split()) > 5
        
        return has_claim_keyword or (has_number and is_long_enough)
    
    def _calculate_claim_confidence(self, sentence: str) -> int:
        """Calculate confidence that this is a factual claim (0-100)"""
        confidence = 50
        
        sentence_lower = sentence.lower()
        
        # Increase confidence for explicit claim indicators
        if any(keyword in sentence_lower for keyword in self.claim_keywords):
            confidence += 20
        
        # Increase confidence for numerical data
        if re.search(r'\d+[%]?', sentence):
            confidence += 15
        
        # Check for attribution (decreases confidence if missing)
        if not any(word in sentence_lower for word in ['according', 'study', 'research', 'reported']):
            confidence -= 10
        
        return min(100, max(0, confidence))
    
    def _is_suspicious_claim(self, sentence: str) -> bool:
        """Check if claim contains suspicious language"""
        sentence_lower = sentence.lower()
        return any(keyword in sentence_lower for keyword in self.suspicious_keywords)
    
    def _extract_keywords(self, sentence: str) -> List[str]:
        """Extract relevant keywords from sentence"""
        sentence_lower = sentence.lower()
        found_keywords = []
        
        for keyword in self.claim_keywords + self.suspicious_keywords:
            if keyword in sentence_lower:
                found_keywords.append(keyword)
        
        return found_keywords
