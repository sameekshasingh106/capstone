"""
Main Streamlit Application for Misinformation Detection
Analyzes TikTok/Instagram videos for claims, scams, and deepfakes
"""

import streamlit as st
import json
from datetime import datetime
from modules.video_processor import VideoProcessor
from modules.transcript_extractor import TranscriptExtractor
from modules.claim_detector import ClaimDetector
from modules.risk_analyzer import RiskAnalyzer
from modules.report_generator import ReportGenerator
from utils.helpers import set_page_config, format_risk_level

# Page configuration
set_page_config()

# Custom CSS for styling
st.markdown("""
    <style>
    .main { padding: 20px; }
    .risk-low { color: #27AE60; font-weight: bold; }
    .risk-medium { color: #F39C12; font-weight: bold; }
    .risk-high { color: #E74C3C; font-weight: bold; }
    .credibility-score { font-size: 48px; font-weight: bold; text-align: center; }
    .metric-card { 
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 10px; 
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'input'

def main():
    """Main application flow"""
    
    # Header
    st.title("🔍 Misinformation Analyzer")
    st.markdown("### Analyze TikTok & Instagram videos for credibility, scams, and deepfakes")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.info("""
        1. **Paste** a TikTok or Instagram video link
        2. **Click** "Analyze" to start processing
        3. **Review** the results on credibility and risks
        4. **Download** the analysis report
        """)
        st.divider()
        st.markdown("**Supported Platforms:**")
        st.write("• TikTok videos")
        st.write("• Instagram Reels/Videos")
        st.write("• YouTube videos (bonus)")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_link = st.text_input(
            "📹 Paste Video Link",
            placeholder="https://www.tiktok.com/...",
            help="Enter the full URL of the TikTok, Instagram, or YouTube video"
        )
    
    with col2:
        analyze_button = st.button("🚀 Analyze", use_container_width=True, type="primary")
    
    st.divider()
    
    # Analysis flow
    if analyze_button:
        if not video_link:
            st.error("⚠️ Please enter a video link first!")
        else:
            # Start analysis
            st.session_state.current_step = 'processing'
            process_video(video_link)
    
    # Display previous results if available
    if st.session_state.analysis_results:
        display_results(st.session_state.analysis_results)


def process_video(video_link):
    """Process the uploaded video through all analysis modules"""
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        # Step 1: Validate and extract video info
        with status_placeholder.container():
            st.info("🔗 Validating video link...")
        
        video_processor = VideoProcessor()
        video_info = video_processor.process_link(video_link)
        
        if not video_info:
            st.error("❌ Could not process this video link. Please check the URL.")
            return
        
        # Step 2: Extract transcript
        with status_placeholder.container():
            st.info("📝 Extracting transcript...")
        
        transcript_extractor = TranscriptExtractor()
        transcript = transcript_extractor.extract(video_info)
        
        if not transcript:
            st.warning("⚠️ Could not extract transcript. Proceeding with visual analysis...")
            transcript = "[No transcript available]"
        
        # Step 3: Detect claims
        with status_placeholder.container():
            st.info("🔎 Detecting claims...")
        
        claim_detector = ClaimDetector()
        claims = claim_detector.detect_claims(transcript)
        
        # Step 4: Analyze risks
        with status_placeholder.container():
            st.info("⚠️ Analyzing risks...")
        
        risk_analyzer = RiskAnalyzer()
        risk_analysis = risk_analyzer.analyze(
            transcript=transcript,
            claims=claims,
            video_info=video_info
        )
        
        # Step 5: Generate credibility score
        credibility_score = calculate_credibility_score(risk_analysis, claims)
        
        # Compile results
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "video_info": video_info,
            "transcript": transcript,
            "claims": claims,
            "risk_analysis": risk_analysis,
            "credibility_score": credibility_score,
            "url": video_link
        }
        
        st.session_state.analysis_results = analysis_results
        
        # Step 6: Generate report
        with status_placeholder.container():
            st.info("📊 Generating report...")
        
        report_generator = ReportGenerator()
        report = report_generator.generate(analysis_results)
        
        # Clear status and show success
        status_placeholder.empty()
        st.success("✅ Analysis complete!")
        
        # Display results
        display_results(analysis_results)
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.session_state.current_step = 'error'


def display_results(results):
    """Display analysis results in a formatted way"""
    
    st.divider()
    st.header("📊 Analysis Results")
    
    # Video Info
    with st.expander("📹 Video Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Title", results['video_info'].get('title', 'Unknown')[:30])
        with col2:
            st.metric("Duration", f"{results['video_info'].get('duration', 0)}s")
        with col3:
            st.metric("Platform", results['video_info'].get('platform', 'Unknown'))
    
    # Credibility Score - Main Focus
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = results['credibility_score']
        st.markdown(f"<div class='credibility-score'>{score}/100</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px;'>Credibility Score</p>", unsafe_allow_html=True)
    
    with col2:
        risk = results['risk_analysis'].get('scam_risk_level', 'low')
        st.markdown(f"<div class='metric-card'><strong>Scam Risk</strong><br><p class='risk-{risk}'>{risk.upper()}</p></div>", unsafe_allow_html=True)
    
    with col3:
        deepfake = results['risk_analysis'].get('deepfake_risk_level', 'low')
        st.markdown(f"<div class='metric-card'><strong>Deepfake Risk</strong><br><p class='risk-{deepfake}'>{deepfake.upper()}</p></div>", unsafe_allow_html=True)
    
    # Transcript
    with st.expander("📝 Transcript"):
        transcript_text = results['transcript']
        if transcript_text == "[No transcript available]":
            st.warning("⚠️ Transcript not available for this video. The app will analyze visual content and metadata instead.")
        st.text_area("Full Transcript", value=transcript_text, height=200, disabled=True, key="transcript_area")
    
    # Detected Claims
    with st.expander("🔍 Detected Claims", expanded=True):
        if results['claims']:
            for i, claim in enumerate(results['claims'], 1):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**Claim {i}:** {claim.get('text', 'N/A')}")
                with col2:
                    status = claim.get('status', 'unknown')
                    color = 'green' if status == 'verified' else 'red' if status == 'false' else 'gray'
                    st.markdown(f"<span style='color: {color};'>**{status.upper()}**</span>", unsafe_allow_html=True)
                st.caption(f"Confidence: {claim.get('confidence', 0)}%")
        else:
            st.info("No significant claims detected.")
    
    # Risk Details
    with st.expander("⚠️ Risk Analysis Details"):
        st.json(results['risk_analysis'], key="risk_details_json")
    
    # Download Report
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        report_json = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download JSON Report",
            data=report_json,
            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # TODO: Add PDF report download
        st.button("📄 Generate PDF Report (Coming Soon)", disabled=True, key="pdf_button")


def calculate_credibility_score(risk_analysis, claims):
    """Calculate credibility score based on risk analysis and claims"""
    
    score = 100
    
    # Deduct based on scam risk
    scam_risk = risk_analysis.get('scam_risk_level', 'low')
    score -= {'low': 5, 'medium': 20, 'high': 40}.get(scam_risk, 0)
    
    # Deduct based on deepfake risk
    deepfake_risk = risk_analysis.get('deepfake_risk_level', 'low')
    score -= {'low': 5, 'medium': 15, 'high': 35}.get(deepfake_risk, 0)
    
    # Deduct based on false claims
    false_claims = sum(1 for claim in claims if claim.get('status') == 'false')
    score -= false_claims * 10
    
    # Floor at 0
    return max(0, min(100, score))


if __name__ == "__main__":
    main()
