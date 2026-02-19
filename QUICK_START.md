# Quick Start Guide - Running the App

This guide walks you through running the Misinformation Analyzer step by step.

## Prerequisites Checklist

✓ Python 3.8+ installed  
✓ Terminal/Command Prompt access  
✓ Project folder downloaded/cloned  

## Step-by-Step Instructions

### Step 1️⃣: Open Terminal

#### macOS/Linux
```bash
# Navigate to project folder
cd /path/to/capstone
# or
cd ~/Desktop/capstone
```

#### Windows
```bash
# Navigate to project folder
cd C:\path\to\capstone
```

### Step 2️⃣: Create Virtual Environment

This keeps dependencies isolated from your system Python.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**Expected output after activation:**
```
(venv) $ 
```

### Step 3️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- streamlit (web framework)
- python-dotenv (environment configuration)
- requests (HTTP library)
- And other analysis tools

### Step 4️⃣: Start the App

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

The browser should automatically open. If not, go to: **http://localhost:8501**

### Step 5️⃣: Use the App

#### Input Options

1. **Paste Video Link**
   - TikTok: `https://www.tiktok.com/video/12345...`
   - Instagram: `https://www.instagram.com/reel/ABC123...`
   - YouTube: `https://www.youtube.com/watch?v=abc123...`

2. **Click Analyze Button**
   - Status shows: "🔗 Validating video link..."
   - Then: "📝 Extracting transcript..."
   - Then: "🔎 Detecting claims..."
   - Then: "⚠️ Analyzing risks..."
   - Finally: "📊 Generating report..."

#### Review Results

After analysis completes, you'll see:

**Credibility Score Card**
```
      70
   /100
Credibility Score
```

**Risk Badges**
```
🟢 Scam Risk: LOW    |    🟡 Deepfake Risk: MEDIUM
```

**Information Sections** (click to expand)
- 📹 Video Information
- 📝 Transcript
- 🔍 Detected Claims
- ⚠️ Risk Analysis Details

#### Download Report

Click **"📥 Download JSON Report"** button
- Saves as: `analysis_20260218_201532.json`
- Contains complete analysis data
- Can be imported into other tools

## Troubleshooting

### Issue: "Port Already in Use"

**Error:**
```
StreamlitAPIException: Server failed to start. Error code 48.
```

**Solution:**
Use a different port:
```bash
streamlit run app.py --server.port 8502
```

Then access: **http://localhost:8502**

### Issue: "Module Not Found"

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
Ensure virtual environment is activated and dependencies installed:
```bash
# Verify venv is active (should show (venv) at start of prompt)
which python
# Should show: /path/to/venv/bin/python

# Reinstall
pip install -r requirements.txt
```

### Issue: "Video Not Processing"

**Possible causes:**
1. URL is incomplete or malformed
2. Video is private or restricted
3. Platform not supported
4. Internet connection issue

**Check:**
- ✓ URL is fully formatted: `https://www.tiktok.com/video/...`
- ✓ Video is public (can you view it in browser?)
- ✓ Using supported platform (TikTok, Instagram, YouTube)
- ✓ Internet connection is working

### Issue: "Could not extract transcript"

**This is normal!** 

The warning:
```
⚠️ Could not extract transcript. Proceeding with visual analysis...
```

Means:
- YouTube: Video has captions disabled
- TikTok/Instagram: No transcript API available
- App will continue with metadata analysis

The analysis still works - it just uses different signals.

### Issue: "DuplicateWidgetID" Error

**Error:**
```
DuplicateWidgetID: There are multiple identical st.text_area widgets 
with the same generated key.
```

**Solution:**
This was a bug in earlier versions. **Update the app:**
```bash
# Restart the app
streamlit run app.py
```

If issue persists, clear cache:
```bash
# Press 'C' in the terminal to stop the app
# Then run:
streamlit cache clear
streamlit run app.py
```

## Advanced Usage

### Environment Variables

Create `.env` file for optional configuration:

```env
YOUTUBE_API_KEY=your_key_here
STREAMLIT_SERVER_PORT=8501
```

### Using Different Port

```bash
streamlit run app.py --server.port 9000
# Access at: http://localhost:9000
```

### Disable Email Collection

```bash
streamlit run app.py --logger.level=warning
```

### Run in Headless Mode

Good for CI/CD pipelines:

```bash
STREAMLIT_SERVER_HEADLESS=true streamlit run app.py
```

## File Structure After Setup

After installation, your folder should look like:

```
capstone/
├── venv/                      ← Virtual environment (created)
├── .venv/                     ← Alternative venv location
├── app.py                     ← Main app ✅
├── requirements.txt           ← Dependencies ✅
├── README.md                  ← Documentation ✅
├── API_GUIDE.md               ← API Reference ✅
├── QUICK_START.md             ← This file
├── .env.example               ← Config template
├── modules/                   ← Analysis code
│   ├── video_processor.py
│   ├── transcript_extractor.py
│   ├── claim_detector.py
│   ├── risk_analyzer.py
│   └── report_generator.py
└── utils/
    └── helpers.py
```

## Testing the App

### Quick Test Videos

Try these public videos to test the app:

**YouTube:**
- Any video with captions enabled
- News or educational content works well

**TikTok:**
- Popular videos (@tiktok channel)
- Make sure it's public

**Instagram:**
- Public Reels (@instagram or others)

## Next Steps

1. ✅ App is running
2. ✅ Analyzed some videos
3. ✨ Ready to deploy or customize!

### Want to Customize?

See the module files:
- `modules/risk_analyzer.py` - Change risk thresholds
- `modules/claim_detector.py` - Add more keywords
- `app.py` - Modify UI layout

### Want to Deploy?

Options:
- **Streamlit Cloud**: Push to GitHub, deploy at streamlit.app
- **Docker**: Containerize with Dockerfile
- **Self-hosted**: Deploy to your server

## Common Tasks

### Change Analysis Thresholds

Edit `modules/risk_analyzer.py`:

```python
def _calculate_scam_score(self, transcript: str, claims: List[Dict]) -> int:
    score = 10  # Change base score
    indicator_count = sum(...)
    score += indicator_count * 8  # Change multiplier
    return min(100, max(0, score))
```

### Add Custom Keywords

Edit `modules/claim_detector.py`:

```python
self.claim_keywords = [
    'studies show',
    'research proves',
    'YOUR_CUSTOM_KEYWORD'  # Add here
]
```

### Change UI Colors

Edit `app.py` CSS section:

```python
st.markdown("""
    <style>
    .risk-high { color: #E74C3C; }  # Change red color
    .credibility-score { font-size: 48px; }  # Change size
    </style>
    """, unsafe_allow_html=True)
```

## Support

- **README.md**: Full documentation
- **API_GUIDE.md**: JSON response format
- **Source Code**: Comments in modules/
- **Streamlit Docs**: https://docs.streamlit.io

Happy analyzing! 🔍
