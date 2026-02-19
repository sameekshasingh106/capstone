# Misinformation Analyzer - API Guide

This document explains the JSON response structure returned by the analysis tool.

## Quick Start

1. **Access the app**: http://localhost:8501
2. **Paste a video link**: TikTok, Instagram, or YouTube URL
3. **Click "Analyze"**: Wait for processing
4. **Download report**: Click "📥 Download JSON Report"

## JSON Response Structure

### Complete Response Example

```json
{
  "timestamp": "2026-02-18T20:15:32.456789",
  "video_info": {
    "platform": "youtube",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "video_id": "dQw4w9WgXcQ",
    "title": "Sample Video Title",
    "duration": 120,
    "upload_date": null
  },
  "transcript": "Video transcript content here...",
  "claims": [
    {
      "text": "Studies show that this product cures cancer",
      "confidence": 78,
      "status": "unknown",
      "is_suspicious": true,
      "keywords_found": ["studies show", "cures"]
    },
    {
      "text": "Limited time offer available today",
      "confidence": 92,
      "status": "unknown",
      "is_suspicious": true,
      "keywords_found": ["limited time", "today"]
    }
  ],
  "risk_analysis": {
    "scam_risk_level": "high",
    "scam_risk_score": 72,
    "deepfake_risk_level": "medium",
    "deepfake_risk_score": 45,
    "manipulation_indicators": [
      "emotional_manipulation",
      "urgency_tactic",
      "fear_mongering"
    ],
    "red_flags": [
      "no_sources_cited",
      "vague_language"
    ]
  },
  "credibility_score": 28,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

## Field Descriptions

### Root Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string (ISO 8601) | When the analysis was performed |
| `video_info` | object | Metadata about the video |
| `transcript` | string | Extracted or available transcript text |
| `claims` | array | All detected claims from the video |
| `risk_analysis` | object | Risk assessment results |
| `credibility_score` | integer (0-100) | Overall credibility rating |
| `url` | string | Original video URL provided |

### video_info Object

```json
{
  "platform": "youtube",           // "youtube", "tiktok", or "instagram"
  "url": "https://...",            // Full video URL
  "video_id": "dQw4w9WgXcQ",       // Platform-specific video ID
  "title": "Video Title",          // Video title from platform
  "duration": 120,                 // Video length in seconds
  "upload_date": null              // Upload date (null if unavailable)
}
```

**Supported Platforms:**
- `youtube` - YouTube videos
- `tiktok` - TikTok videos
- `instagram` - Instagram Reels/Posts

### claims Array

Each claim object contains:

```json
{
  "text": "Claim statement from video",
  "confidence": 85,                // 0-100: How confident we are this is a claim
  "status": "unknown",             // "verified", "false", or "unknown"
  "is_suspicious": false,          // true if language patterns are suspicious
  "keywords_found": [              // Keywords detected in this claim
    "studies show",
    "research"
  ]
}
```

**Status Values:**
- `unknown` - Claim requires external fact-checking
- `verified` - Claim appears to be accurate (local analysis)
- `false` - Claim appears to be false or misleading

**Confidence Score:**
- 0-30: Low confidence (barely qualifies as a claim)
- 31-70: Medium confidence (appears to be a factual claim)
- 71-100: High confidence (strong claim pattern)

**Suspicious Indicators:**
- `is_suspicious: true` when claim includes:
  - "They don't want you to know"
  - "Secret/hidden truth"
  - "Government conspiracy"
  - "This one trick"
  - Other inflammatory language

### risk_analysis Object

```json
{
  "scam_risk_level": "medium",     // "low", "medium", or "high"
  "scam_risk_score": 56,           // 0-100: Detailed risk score
  "deepfake_risk_level": "low",    // "low", "medium", or "high"
  "deepfake_risk_score": 22,       // 0-100: Detailed risk score
  "manipulation_indicators": [     // Detected manipulation tactics
    "emotional_manipulation",
    "urgency_tactic",
    "fear_mongering"
  ],
  "red_flags": [                   // Specific warning signs
    "no_sources_cited",
    "vague_language",
    "all_unverified_claims"
  ]
}
```

#### Scam Risk Levels

| Level | Score | Description |
|-------|-------|-------------|
| Low | 0-30 | Minimal scam indicators |
| Medium | 31-70 | Some suspicious elements |
| High | 71-100 | Multiple scam warning signs |

**Scam Indicators Detected:**
- "buy now", "limited time", "act fast"
- "guaranteed returns", "risk-free"
- "make money fast", "payment required"
- High-pressure sales language
- Urgency and exclusivity claims

#### Deepfake Risk Levels

| Level | Score | Description |
|-------|-------|-------------|
| Low | 0-30 | Minimal deepfake risk |
| Medium | 31-70 | Moderate risk factors |
| High | 71-100 | High-risk content characteristics |

**Deepfake Risk Factors:**
- Platform: TikTok (+10), Instagram (+5)
- Video duration < 15 seconds (+5)
- Video quality issues
- Unusual artifacts or inconsistencies

#### Manipulation Indicators

- `emotional_manipulation` - Uses emotional triggers (shocking, devastating, etc.)
- `social_pressure` - References "everyone knows", trends, popular opinion
- `fear_mongering` - Creates unnecessary fear with danger/threat language
- `urgency_tactic` - Uses "now", "today", "immediately", "limited"

#### Red Flags

- `no_sources_cited` - Claims lack attribution or sources
- `vague_language` - Uses "some people say", "they say", "this one trick"
- `all_unverified_claims` - Every claim detected is unverified

### credibility_score

**Integer from 0-100**

```
Score Range | Interpretation
0-25        | Very Low - Likely misinformation
26-50       | Low - Contains concerning elements
51-75       | Medium - Mixed signals, needs verification
76-90       | High - Generally credible
91-100      | Very High - Appears highly credible
```

**Calculation:**
```
base_score = 100
- scam_risk deduction (5-40 points)
- deepfake_risk deduction (5-35 points)
- false_claims penalty (10 points each)
= final credibility_score (0-100)
```

## Common Response Scenarios

### Scenario 1: High-Risk Scam Video

```json
{
  "credibility_score": 15,
  "risk_analysis": {
    "scam_risk_level": "high",
    "scam_risk_score": 82,
    "deepfake_risk_level": "low",
    "manipulation_indicators": ["urgency_tactic", "emotional_manipulation"],
    "red_flags": ["no_sources_cited", "vague_language"]
  }
}
```

### Scenario 2: Legitimate News Video

```json
{
  "credibility_score": 82,
  "risk_analysis": {
    "scam_risk_level": "low",
    "scam_risk_score": 12,
    "deepfake_risk_level": "low",
    "manipulation_indicators": [],
    "red_flags": []
  }
}
```

### Scenario 3: Transcript Unavailable

```json
{
  "transcript": "[No transcript available]",
  "claims": [
    {
      "text": "Detected from visual analysis or metadata",
      "confidence": 65
    }
  ]
}
```

## Using the JSON Response

### Save for Records
```bash
# Download via web interface
# File saves as: analysis_20260218_201532.json
```

### Process Programmatically
```python
import json

# Load the JSON file
with open('analysis_20260218_201532.json', 'r') as f:
    analysis = json.load(f)

# Access specific fields
credibility = analysis['credibility_score']
scam_risk = analysis['risk_analysis']['scam_risk_level']
claims = analysis['claims']

# Filter high-risk videos
if credibility < 30:
    print("⚠️ This content is high-risk!")
```

### Integrate with External Systems
```bash
# Send to your backend
curl -X POST https://your-api.com/analyze \
  -H "Content-Type: application/json" \
  -d @analysis_20260218_201532.json
```

## Error Handling

### When Analysis Fails

If the app can't process a video, the response will show:
- Empty or missing `transcript` field
- `claims` array may be empty
- `risk_analysis` uses default (low) values

**Common Issues:**
1. **Invalid URL** - Ensure the link is complete and public
2. **Unsupported Platform** - Only TikTok, Instagram, YouTube supported
3. **Private Video** - Video must be publicly accessible
4. **Network Issues** - Check internet connection

## Rate Limiting

Current version has no rate limiting. For production use, consider:
- Caching results (same URL = same result)
- Queuing requests for high volume
- Implementing API key system

## Future Enhancements

The JSON structure will expand to include:

```json
{
  "fact_check_results": {
    "snopes_verdict": "mostly_false",
    "sources": [
      {
        "organization": "PolitiFact",
        "claim": "...",
        "rating": "mostly_true"
      }
    ]
  },
  "ai_deepfake_analysis": {
    "probability": 0.23,
    "confidence": 0.89,
    "regions_suspicious": ["face", "hands"]
  }
}
```

## Questions?

For issues or suggestions, please check:
- README.md - Setup and troubleshooting
- app.py - Source code documentation
- modules/ - Individual module documentation
