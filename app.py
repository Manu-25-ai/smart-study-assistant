import streamlit as st
import streamlit.components.v1 as components
import os

from utils.youtube import download_audio, extract_audio_from_video
from utils.transcription import transcribe_audio
from utils.notes_generator import generate_notes
from utils.pdf_exporter import generate_pdf
from utils.flashcards import generate_flashcards
from utils.mindmap import generate_mindmap_data

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NoteFlow AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0F0F13 !important; color: #F0F0F5 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stAppViewContainer"] { background: #0F0F13 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"], .stDeployButton { display: none; }
.block-container { max-width: 860px !important; padding: 2rem 2rem 4rem !important; margin: 0 auto !important; }

.hero { text-align: center; padding: 2.5rem 1rem 1.8rem; }
.hero-badge {
    display: inline-block; background: rgba(124,106,247,0.15);
    border: 1px solid rgba(124,106,247,0.35); color: #A395F8;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 0.3rem 0.85rem; border-radius: 99px; margin-bottom: 1.1rem;
}
.hero-title {
    font-size: clamp(2rem, 5vw, 2.9rem); font-weight: 700; line-height: 1.15; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #F0F0F5 30%, #7C6AF7 70%, #4ECDC4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.7rem;
}
.hero-sub { color: #6B6B80; font-size: 0.98rem; max-width: 450px; margin: 0 auto; line-height: 1.6; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #2A2A3A, transparent); margin: 1.5rem 0 2rem; }

[data-testid="stRadio"] > label { color: #9090A8 !important; font-size: 0.85rem !important; font-weight: 500 !important; }
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0 !important; background: #1A1A26 !important; border: 1px solid #25253A !important;
    border-radius: 10px !important; padding: 4px !important; display: flex !important; flex-direction: row !important;
}
[data-testid="stRadio"] label {
    flex: 1 !important; text-align: center !important; cursor: pointer !important;
    padding: 0.5rem 1rem !important; border-radius: 7px !important;
    color: #6B6B80 !important; font-size: 0.88rem !important; font-weight: 500 !important; transition: all 0.2s !important;
}
[data-testid="stRadio"] label:has(input:checked) { background: #7C6AF7 !important; color: #fff !important; }
[data-testid="stRadio"] input { display: none !important; }

.stTextInput > div > div > input {
    background: #0F0F18 !important; border: 1px solid #2A2A3E !important;
    border-radius: 10px !important; color: #F0F0F5 !important;
    font-size: 0.95rem !important; padding: 0.75rem 1rem !important; transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus { border-color: #7C6AF7 !important; box-shadow: 0 0 0 3px rgba(124,106,247,0.12) !important; }
.stTextInput label { color: #9090A8 !important; font-size: 0.85rem !important; font-weight: 500 !important; }

[data-testid="stFileUploader"] > div {
    background: #0F0F18 !important; border: 1.5px dashed #2A2A3E !important;
    border-radius: 12px !important; transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover { border-color: #7C6AF7 !important; }
[data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span { color: #6B6B80 !important; }

.stButton > button {
    background: linear-gradient(135deg, #7C6AF7, #5E4FD4) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 0.95rem !important; padding: 0.7rem 2rem !important;
    width: 100% !important; transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(124,106,247,0.3) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(124,106,247,0.45) !important; }
.stButton > button:active { transform: translateY(0) !important; }

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #4ECDC4, #38b2aa) !important;
    color: #0F0F13 !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 0.9rem !important; padding: 0.65rem 1.5rem !important;
    width: 100% !important; transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(78,205,196,0.3) !important;
}
[data-testid="stDownloadButton"] > button:hover { transform: translateY(-1px) !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #1A1A26 !important; border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important; border: 1px solid #25253A !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #6B6B80 !important; font-weight: 500 !important;
    font-size: 0.88rem !important; padding: 0.5rem 1.1rem !important; border: none !important;
}
.stTabs [aria-selected="true"] { background: #7C6AF7 !important; color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

.notes-card {
    background: #13131C; border: 1px solid #22223A; border-left: 3px solid #7C6AF7;
    border-radius: 14px; padding: 1.8rem 2rem; color: #C8C8D8;
    font-size: 0.95rem; line-height: 1.85; white-space: pre-wrap;
}
.transcript-card {
    background: #0C0C15; border: 1px solid #1E1E30; border-radius: 12px;
    padding: 1.2rem 1.5rem; max-height: 260px; overflow-y: auto;
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
    line-height: 1.75; color: #707088; white-space: pre-wrap;
}
.lang-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(78,205,196,0.12); border: 1px solid rgba(78,205,196,0.3);
    color: #4ECDC4; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 0.3rem 0.85rem; border-radius: 99px; margin-bottom: 1rem;
}
.banner { padding: 0.8rem 1.1rem; border-radius: 10px; font-size: 0.88rem; font-weight: 500; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }
.banner.success { background: rgba(78,205,196,0.1); border: 1px solid rgba(78,205,196,0.25); color: #4ECDC4; }
.banner.error   { background: rgba(255,99,99,0.1);  border: 1px solid rgba(255,99,99,0.25);  color: #FF6363; }
.banner.info    { background: rgba(124,106,247,0.1); border: 1px solid rgba(124,106,247,0.25); color: #A395F8; }
.stats-row { display: flex; gap: 0.85rem; margin: 1.5rem 0; }
.stat-chip { background: #1A1A26; border: 1px solid #25253A; border-radius: 10px; padding: 0.65rem 1rem; flex: 1; text-align: center; }
.stat-value { font-size: 1.25rem; font-weight: 700; color: #7C6AF7; line-height: 1; margin-bottom: 0.2rem; }
.stat-label { font-size: 0.68rem; color: #5A5A70; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0F0F13; }
::-webkit-scrollbar-thumb { background: #2A2A3E; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Whisper · Gemini AI</div>
    <div class="hero-title">Turn Any Video Into Smart Notes</div>
    <div class="hero-sub">Paste a YouTube link or upload a file — get a transcript, summary, key points and a quiz instantly.</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
uploaded_file = None
video_url     = ""
file_path     = None

input_type = st.radio("Choose Input Type", ["YouTube URL", "Upload File"])

if input_type == "YouTube URL":
    video_url = st.text_input("Enter YouTube URL")

if input_type == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload Video or Audio File",
        type=["mp4", "mkv", "mov", "avi", "mp3", "wav", "m4a"]
    )

if uploaded_file is not None:
    extension = uploaded_file.name.split(".")[-1].lower()
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.markdown(f'<div class="banner success">✓ Uploaded: {uploaded_file.name}</div>', unsafe_allow_html=True)
    if extension in ["mp3", "wav", "m4a"]:
        st.markdown('<div class="banner success">✓ Audio file ready for transcription</div>', unsafe_allow_html=True)
    elif extension in ["mp4", "mkv", "mov", "avi"]:
        st.markdown('<div class="banner info">ℹ️ Video file detected — audio will be extracted automatically</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
col_btn, col_gap = st.columns([1, 2])
with col_btn:
    generate_btn = st.button("⚡  Generate Notes")

# ── Generate ───────────────────────────────────────────────────────────────────
if generate_btn:
    if input_type == "YouTube URL":
        with st.spinner("Downloading Audio..."):
            audio_file = download_audio(video_url)
        st.markdown('<div class="banner success">✓ Audio downloaded successfully</div>', unsafe_allow_html=True)
    elif input_type == "Upload File":
        if uploaded_file is None:
            st.markdown('<div class="banner error">✗ Please upload a file first.</div>', unsafe_allow_html=True)
            st.stop()
        extension = uploaded_file.name.split(".")[-1].lower()
        if extension in ["mp4", "mkv", "mov", "avi"]:
            with st.spinner("Extracting audio from video..."):
                audio_file = extract_audio_from_video(file_path)
            st.markdown('<div class="banner success">✓ Audio extracted from video</div>', unsafe_allow_html=True)
        else:
            audio_file = file_path

    with st.spinner("Transcribing Audio... (auto-detecting language)"):
        result     = transcribe_audio(audio_file)
        transcript = result["text"]
        language   = result["language"]
    st.session_state["transcript"] = transcript
    st.session_state["language"]   = language

    with st.spinner("Generating Notes..."):
        notes = generate_notes(transcript)
    st.session_state["notes"] = notes

    with st.spinner("Generating Flashcards..."):
        flashcards = generate_flashcards(transcript)
    st.session_state["flashcards"] = flashcards

    with st.spinner("Building Mind Map..."):
        mindmap = generate_mindmap_data(transcript)
    st.session_state["mindmap"] = mindmap

# ── Results ────────────────────────────────────────────────────────────────────
notes      = st.session_state.get("notes")
transcript = st.session_state.get("transcript", "")
language   = st.session_state.get("language", "unknown")
flashcards = st.session_state.get("flashcards", [])
mindmap    = st.session_state.get("mindmap", {})

LANGUAGE_NAMES = {
    "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French",
    "de": "German", "zh": "Chinese", "ar": "Arabic", "pt": "Portuguese",
    "ru": "Russian", "ja": "Japanese", "ko": "Korean", "it": "Italian",
    "nl": "Dutch", "tr": "Turkish", "pl": "Polish", "uk": "Ukrainian",
}

if notes:
    st.markdown('<div class="divider" style="margin-top:1.5rem"></div>', unsafe_allow_html=True)

    lang_display = LANGUAGE_NAMES.get(language, language.upper())
    st.markdown(f'<div class="lang-badge">🌐 Language detected: {lang_display}</div>', unsafe_allow_html=True)

    word_count = len(transcript.split()) if transcript else 0
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-chip"><div class="stat-value">{word_count:,}</div><div class="stat-label">Words</div></div>
        <div class="stat-chip"><div class="stat-value">{len(flashcards)}</div><div class="stat-label">Flashcards</div></div>
        <div class="stat-chip"><div class="stat-value">{len(mindmap.get("branches", []))}</div><div class="stat-label">Mind Map Nodes</div></div>
        <div class="stat-chip"><div class="stat-value">{lang_display}</div><div class="stat-label">Language</div></div>
    </div>
    """, unsafe_allow_html=True)

    tab_notes, tab_flash, tab_map, tab_transcript = st.tabs([
        "📋  Notes", "🃏  Flashcards", "🗺️  Mind Map", "📄  Transcript"
    ])

    # ── Notes ──────────────────────────────────────────────────────────────────
    with tab_notes:
        st.markdown(f'<div class="notes-card">{notes}</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
        pdf_bytes = generate_pdf(notes, transcript, language)
        col_dl, col_gap = st.columns([1, 2])
        with col_dl:
            st.download_button(
                label="⬇️  Download as PDF",
                data=pdf_bytes,
                file_name="noteflow_notes.pdf",
                mime="application/pdf",
            )

    # ── Flashcards — rendered via components.html ──────────────────────────────
    with tab_flash:
        if flashcards:
            cards_html = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0F0F13; font-family: 'Inter', sans-serif; padding: 1rem; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .card {
    background: #13131C; border: 1px solid #22223A; border-radius: 14px;
    padding: 1.3rem; min-height: 160px; display: flex; flex-direction: column;
    justify-content: space-between; transition: all 0.2s; cursor: default;
  }
  .card:hover { border-color: #7C6AF7; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(124,106,247,0.15); }
  .card-num { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #7C6AF7; margin-bottom: 0.5rem; }
  .q-label { font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #5A5A70; margin-bottom: 0.35rem; }
  .q-text  { font-size: 0.9rem; font-weight: 600; color: #E0E0F0; line-height: 1.5; margin-bottom: 0.8rem; }
  .divider { height: 1px; background: #22223A; margin-bottom: 0.8rem; }
  .a-label { font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #38b2aa; margin-bottom: 0.35rem; }
  .a-text  { font-size: 0.85rem; color: #4ECDC4; line-height: 1.55; }
</style>
</head>
<body>
<div class="grid">
"""
            for i, card in enumerate(flashcards, 1):
                front = card['front'].replace('<', '&lt;').replace('>', '&gt;')
                back  = card['back'].replace('<', '&lt;').replace('>', '&gt;')
                cards_html += f"""
  <div class="card">
    <div>
      <div class="card-num">Card {i:02d}</div>
      <div class="q-label">Question</div>
      <div class="q-text">{front}</div>
    </div>
    <div>
      <div class="divider"></div>
      <div class="a-label">Answer</div>
      <div class="a-text">{back}</div>
    </div>
  </div>
"""
            cards_html += "</div></body></html>"
            components.html(cards_html, height=len(flashcards) * 110 + 40, scrolling=True)
        else:
            st.markdown('<div class="banner info">No flashcards generated yet.</div>', unsafe_allow_html=True)

    # ── Mind Map — rendered via components.html ────────────────────────────────
    with tab_map:
        if mindmap:
            import json as _json
            branches    = mindmap.get("branches", [])
            center_text = mindmap.get("center", "Main Topic")
            nodes_data  = []
            edges_data  = []

            nodes_data.append({"id": "center", "label": center_text, "type": "center"})
            for i, branch in enumerate(branches):
                bid = f"b{i}"
                nodes_data.append({"id": bid, "label": branch["topic"], "type": "branch"})
                edges_data.append({"from": "center", "to": bid})
                for j, sub in enumerate(branch.get("subtopics", [])):
                    sid = f"b{i}s{j}"
                    nodes_data.append({"id": sid, "label": sub, "type": "sub"})
                    edges_data.append({"from": bid, "to": sid})

            nodes_json = _json.dumps(nodes_data)
            edges_json = _json.dumps(edges_data)

            mindmap_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0C0C15; overflow: hidden; }}
  canvas {{ display: block; }}
  #tip {{
    position: fixed; background: #1A1A26; border: 1px solid #7C6AF7;
    color: #E0E0F0; padding: 5px 10px; border-radius: 8px; font-size: 11px;
    font-family: Inter, sans-serif; pointer-events: none; display: none;
    max-width: 180px; line-height: 1.4; z-index: 10;
  }}
</style>
</head>
<body>
<canvas id="c" style="width:100%;height:500px;"></canvas>
<div id="tip"></div>
<script>
const NODES = {nodes_json};
const EDGES = {edges_json};

const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');

// Use fixed dimensions — window.innerWidth is 0 in Streamlit iframes
const W = canvas.width  = 1000;
const H = canvas.height = 650;

const pos = {{}};
pos['center'] = {{ x: W/2, y: H/2 }};

const branches = NODES.filter(n => n.type === 'branch');

branches.forEach((b, i) => {{
  const angle = (2 * Math.PI * i / branches.length) - Math.PI / 2;

  pos[b.id] = {{
    x: W/2 + Math.cos(angle)*240,
    y: H/2 + Math.sin(angle)*220
  }};

  const subs = NODES.filter(n => n.id.startsWith(b.id + 's'));

  subs.forEach((s, j) => {{
    const spread = (j - (subs.length - 1) / 2) * 0.4;
    const sa = angle + spread;

    pos[s.id] = {{
      x: pos[b.id].x + Math.cos(sa)*170,
      y: pos[b.id].y + Math.sin(sa)*150
    }};
  }});
}});

const CFG = {{
  center: {{ fill:'#7C6AF7', text:'#fff',    r:50, font:'700 13px Inter' }},
  branch: {{ fill:'#1A1A36', text:'#A395F8', r:35, font:'600 11px Inter', stroke:'#7C6AF7' }},
  sub:    {{ fill:'#13131C', text:'#C8C8D8', r:28, font:'500 10px Inter', stroke:'#2A2A3E' }},
}};

function wrapText(ctx, text, maxW) {{
  const words = text.split(' ');
  const lines = []; let line = '';
  words.forEach(w => {{
    const t = line ? line + ' ' + w : w;
    if (ctx.measureText(t).width > maxW && line) {{ lines.push(line); line = w; }}
    else line = t;
  }});
  if (line) lines.push(line);
  return lines;
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);

  EDGES.forEach(e => {{
    const f = pos[e.from], t = pos[e.to];
    if (!f || !t) return;
    const toN = NODES.find(n => n.id === e.to);
    ctx.beginPath();
    ctx.moveTo(f.x, f.y);
    ctx.quadraticCurveTo((f.x+t.x)/2, (f.y+t.y)/2, t.x, t.y);
    ctx.strokeStyle = toN && toN.type === 'sub' ? '#2A2A3E' : '#3A3A5E';
    ctx.lineWidth   = toN && toN.type === 'sub' ? 1 : 1.5;
    ctx.stroke();
  }});

  NODES.forEach(n => {{
    const p = pos[n.id]; if (!p) return;
    const c = CFG[n.type];

    if (n.type === 'center') {{
      const g = ctx.createRadialGradient(p.x, p.y, c.r*0.2, p.x, p.y, c.r*1.8);
      g.addColorStop(0, 'rgba(124,106,247,0.2)'); g.addColorStop(1, 'rgba(124,106,247,0)');
      ctx.beginPath(); ctx.arc(p.x, p.y, c.r*1.8, 0, Math.PI*2);
      ctx.fillStyle = g; ctx.fill();
    }}

    ctx.beginPath(); ctx.arc(p.x, p.y, c.r, 0, Math.PI*2);
    ctx.fillStyle = c.fill; ctx.fill();
    if (c.stroke) {{ ctx.strokeStyle = c.stroke; ctx.lineWidth = n.type==='branch'?1.5:1; ctx.stroke(); }}

    ctx.fillStyle = c.text; ctx.font = c.font;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const lines = wrapText(ctx, n.label, (c.r-6)*2);
    const lh = parseInt(c.font) + 3;
    lines.forEach((l, i) => ctx.fillText(l, p.x, p.y + (i-(lines.length-1)/2)*lh));
  }});
}}
draw();

const tip = document.getElementById('tip');
canvas.addEventListener('mousemove', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left, my = e.clientY - rect.top;
  let found = null;
  NODES.forEach(n => {{
    if (n.label.length > 18) {{
    n.label = n.label.substring(0, 18) + "...";
  }}
    const p = pos[n.id]; if (!p) return;
    if (Math.hypot(mx-p.x, my-p.y) < CFG[n.type].r) found = n;
  }});
  if (found) {{
    tip.style.display = 'block';
    tip.style.left = (e.clientX + 14) + 'px';
    tip.style.top  = (e.clientY - 10) + 'px';
    tip.textContent = found.label;
    canvas.style.cursor = 'pointer';
  }} else {{
    tip.style.display = 'none';
    canvas.style.cursor = 'default';
  }}
}});
</script>
</body>
</html>
"""
            components.html(mindmap_html, height=680, scrolling=False)
        else:
            st.markdown('<div class="banner info">No mind map data available.</div>', unsafe_allow_html=True)

    # ── Transcript ─────────────────────────────────────────────────────────────
    with tab_transcript:
        st.markdown(f'<div class="transcript-card">{transcript}</div>', unsafe_allow_html=True)

    # ── Reset ──────────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    col_r, _ = st.columns([1, 3])
    with col_r:
        if st.button("↺  Start Over"):
            for k in ["notes", "transcript", "language", "flashcards", "mindmap"]:
                st.session_state.pop(k, None)
            st.rerun()