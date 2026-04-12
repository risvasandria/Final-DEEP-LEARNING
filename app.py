import streamlit as st
import numpy as np
from PIL import Image
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FishScan AI · Deteksi Kesegaran Ikan",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:         #050d18;
    --surface:    #0b1929;
    --surface2:   #112236;
    --surface3:   #162d47;
    --border:     #1e3a5f;
    --border2:    #2a4f7a;
    --ocean:      #0ea5e9;
    --ocean-dim:  rgba(14,165,233,0.15);
    --fresh:      #22c55e;
    --semi:       #f59e0b;
    --busuk:      #ef4444;
    --text:       #e2f0ff;
    --muted:      #7aadcf;
    --radius:     16px;
    --radius-sm:  10px;
}
html, body {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stApp, .main, .stMainBlockContainer {
    background-color: var(--bg) !important;
}
/* font untuk semua teks */
p, span, div, label, li, td, th, a {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1300px !important; }
h1,h2,h3,h4,h5 { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"],
.css-1d391kg,
.css-6qob1r,
.css-uf99v8 {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div:first-child {
    background: var(--surface) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Sidebar branding */
.sb-brand {
    display: flex; align-items: center; gap: .8rem;
    padding: 1rem 1.2rem 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sb-brand-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #0369a1, #0ea5e9);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(14,165,233,0.3);
}
.sb-brand-text .title {
    font-size: .95rem; font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #38bdf8, #bae6fd);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sb-brand-text .sub {
    font-size: .65rem; color: var(--muted); font-weight: 500; letter-spacing: .05em;
}

/* Nav items */
.nav-section {
    font-size: .65rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    color: var(--muted); padding: 0 1.2rem; margin: .5rem 0 .4rem;
}
.nav-item {
    display: flex; align-items: center; gap: .7rem;
    padding: .65rem 1.2rem; margin: .1rem .6rem;
    border-radius: var(--radius-sm); cursor: pointer;
    font-size: .88rem; font-weight: 600; transition: all .2s;
    border: 1px solid transparent;
}
.nav-item:hover {
    background: var(--surface2);
    border-color: var(--border);
}
.nav-item.active {
    background: linear-gradient(135deg, rgba(14,165,233,0.12), rgba(14,165,233,0.06));
    border-color: rgba(14,165,233,0.35);
    color: #7dd3fc !important;
}
.nav-item .nav-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--ocean); margin-left: auto; opacity: 0;
}
.nav-item.active .nav-dot { opacity: 1; }

/* Algorithm cards in sidebar */
.algo-card {
    margin: .3rem .6rem;
    padding: .8rem 1rem;
    border-radius: var(--radius-sm);
    border: 1.5px solid var(--border);
    background: var(--surface2);
    cursor: pointer;
    transition: all .2s;
    position: relative;
    overflow: hidden;
}
.algo-card:hover { border-color: var(--border2); background: var(--surface3); }
.algo-card.selected {
    border-color: var(--ocean);
    background: linear-gradient(135deg, rgba(14,165,233,0.1), rgba(14,165,233,0.03));
}
.algo-card.selected::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0ea5e9, #38bdf8);
}
.algo-name { font-size: .82rem; font-weight: 700; margin-bottom: .25rem; }
.algo-acc {
    font-size: .72rem; font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}
.algo-badge {
    display: inline-block; font-size: .6rem; font-weight: 700; letter-spacing: .06em;
    padding: .15rem .45rem; border-radius: 50px; margin-top: .3rem;
}
.badge-best { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.badge-base { background: rgba(14,165,233,0.15); color: #7dd3fc; border: 1px solid rgba(14,165,233,0.3); }
.badge-transfer { background: rgba(167,139,250,0.15); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.3); }
.checkmark {
    position: absolute; top: .6rem; right: .7rem;
    width: 18px; height: 18px; border-radius: 50%;
    background: var(--ocean); display: flex; align-items: center; justify-content: center;
    font-size: .6rem; color: white; display: none;
}
.algo-card.selected .checkmark { display: flex; }

/* Sidebar stats */
.sb-stats {
    margin: .5rem .6rem;
    padding: .8rem 1rem;
    border-radius: var(--radius-sm);
    background: var(--surface2);
    border: 1px solid var(--border);
}
.sb-stat-row { display: flex; justify-content: space-between; align-items: center; margin: .25rem 0; }
.sb-stat-label { font-size: .72rem; color: var(--muted); }
.sb-stat-val { font-size: .75rem; font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text); }

/* ── HERO ── */
.hero-wrap {
    background: linear-gradient(135deg, #050d18 0%, #0a1f35 40%, #0c2a47 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute; bottom: -40px; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(34,197,94,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: clamp(2rem, 3.5vw, 3rem);
    font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #38bdf8 0%, #7dd3fc 50%, #bae6fd 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: .5rem;
}
.hero-sub { color: var(--muted); font-size: 1rem; line-height: 1.7; max-width: 600px; }
.hero-badges { display:flex; gap:.6rem; flex-wrap:wrap; margin-top:1.2rem; }
.badge {
    background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.3);
    color: #7dd3fc; padding: .28rem .75rem; border-radius: 50px;
    font-size: .75rem; font-weight: 600; letter-spacing: .03em;
}
.badge-green { background: rgba(34,197,94,0.12); border-color: rgba(34,197,94,0.3); color: #86efac; }
.badge-yellow { background: rgba(245,158,11,0.12); border-color: rgba(245,158,11,0.3); color: #fcd34d; }
.badge-red { background: rgba(239,68,68,0.12); border-color: rgba(239,68,68,0.3); color: #fca5a5; }

/* ── CARDS ── */
.card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1.4rem 1.6rem; margin-bottom: 1rem;
}
.card-title {
    font-size: .72rem; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: .8rem;
    display: flex; align-items: center; gap: .5rem;
}
.card-title::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ── STAT BOXES ── */
.stat-box {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 12px; padding: 1rem 1.2rem; text-align: center;
}
.stat-val { font-size: 1.6rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
.stat-lbl { font-size: .72rem; color: var(--muted); font-weight: 600; letter-spacing: .05em; text-transform: uppercase; margin-top: .2rem; }

/* ── METRIC STRIP ── */
.metric-strip {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: .8rem;
    margin: 1rem 0;
}
.metric-item {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 12px; padding: .9rem 1rem; text-align: center;
}
.metric-val {
    font-size: 1.3rem; font-weight: 800; font-family: 'JetBrains Mono', monospace;
    color: var(--ocean);
}
.metric-lbl {
    font-size: .65rem; color: var(--muted); font-weight: 600;
    letter-spacing: .06em; text-transform: uppercase; margin-top: .2rem;
}

/* ── RESULTS ── */
.result-fresh {
    background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.03));
    border: 2px solid var(--fresh); border-radius: var(--radius); padding: 1.8rem 2rem; text-align: center;
    position: relative; overflow: hidden;
}
.result-semi {
    background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(245,158,11,0.03));
    border: 2px solid var(--semi); border-radius: var(--radius); padding: 1.8rem 2rem; text-align: center;
}
.result-busuk {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.03));
    border: 2px solid var(--busuk); border-radius: var(--radius); padding: 1.8rem 2rem; text-align: center;
}
.result-icon  { font-size: 3.5rem; margin-bottom: .5rem; }
.result-label { font-size: 2rem; font-weight: 800; margin-bottom: .3rem; letter-spacing: .02em; }
.result-conf  { font-size: .88rem; color: var(--muted); margin-top: .5rem; }
.result-model-tag {
    display: inline-block; font-size: .7rem; font-weight: 700;
    background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
    padding: .2rem .65rem; border-radius: 50px; margin-top: .5rem;
    letter-spacing: .04em;
}
.label-fresh  { color: var(--fresh); }
.label-semi   { color: var(--semi); }
.label-busuk  { color: var(--busuk); }

/* ── PROBABILITY BARS ── */
.prob-row { margin: .55rem 0; }
.prob-header { display: flex; justify-content: space-between; font-size: .82rem; margin-bottom: .3rem; align-items: center; }
.prob-track { height: 10px; background: var(--surface2); border-radius: 50px; overflow: hidden; }
.prob-fill-fresh { height:100%; border-radius:50px; background: linear-gradient(90deg, #16a34a, #22c55e); transition: width .5s; }
.prob-fill-semi  { height:100%; border-radius:50px; background: linear-gradient(90deg, #d97706, #f59e0b); }
.prob-fill-busuk { height:100%; border-radius:50px; background: linear-gradient(90deg, #dc2626, #ef4444); }

/* ── INFO / RECOMMENDATION BOX ── */
.info-box {
    background: rgba(14,165,233,0.07); border-left: 3px solid var(--ocean);
    border-radius: 0 10px 10px 0; padding: .9rem 1.2rem;
    font-size: .85rem; color: #a5d8f5; margin: .8rem 0;
}
.warn-box {
    background: rgba(245,158,11,0.07); border-left: 3px solid var(--semi);
    border-radius: 0 10px 10px 0; padding: .9rem 1.2rem;
    font-size: .85rem; color: #fcd34d; margin: .8rem 0;
}
.danger-box {
    background: rgba(239,68,68,0.07); border-left: 3px solid var(--busuk);
    border-radius: 0 10px 10px 0; padding: .9rem 1.2rem;
    font-size: .85rem; color: #fca5a5; margin: .8rem 0;
}
.success-box {
    background: rgba(34,197,94,0.07); border-left: 3px solid var(--fresh);
    border-radius: 0 10px 10px 0; padding: .9rem 1.2rem;
    font-size: .85rem; color: #86efac; margin: .8rem 0;
}

/* ── TABLE ── */
table { width: 100% !important; border-collapse: collapse; }
th {
    background: var(--surface2); padding: .7rem 1rem; font-size: .75rem;
    letter-spacing: .07em; text-transform: uppercase; color: var(--muted); text-align: left;
    border-bottom: 1px solid var(--border);
}
td { padding: .65rem 1rem; border-bottom: 1px solid var(--border); font-size: .88rem; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

/* ── BUTTONS ── */
.stButton>button {
    background: linear-gradient(135deg, #0369a1, #0ea5e9) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: .65rem 1.5rem !important; font-size: .9rem !important;
    box-shadow: 0 4px 15px rgba(14,165,233,0.25) !important;
    transition: all .2s !important;
}
.stButton>button:hover {
    box-shadow: 0 6px 20px rgba(14,165,233,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton>button:disabled {
    background: var(--surface2) !important;
    box-shadow: none !important; transform: none !important;
    opacity: .5 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border) !important; border-radius: 12px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Progress / spinner */
.stSpinner > div { border-top-color: var(--ocean) !important; }

/* Section divider */
.divider {
    height: 1px; background: var(--border); margin: 1.5rem 0;
}

/* Upload placeholder */
.upload-placeholder {
    text-align: center; padding: 3.5rem 1rem;
    color: var(--muted); font-size: .9rem;
    border: 2px dashed var(--border); border-radius: 12px;
    background: var(--surface2);
}
.upload-placeholder .icon { font-size: 2.8rem; margin-bottom: .8rem; }

/* Empty state */
.empty-state {
    text-align: center; padding: 5rem 2rem;
    color: var(--muted);
}
.empty-state .icon { font-size: 3rem; margin-bottom: 1rem; opacity: .5; }

/* Animated pulse for active model indicator */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: .5; }
}
.pulse-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--fresh); animation: pulse 2s infinite;
    display: inline-block; margin-right: .4rem;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
CLASS_NAMES = ["Busuk ", "Fresh", "Semi Fresh "]

MODEL_INFO = {
    "EfficientNetB0": {
        "label": "EfficientNetB0",
        "icon": "⚡",
        "acc": 0.9784, "precision": 0.9790, "recall": 0.9784, "f1": 0.9785,
        "path": "models/efficientnet_model.h5",
        "desc": "Transfer learning EfficientNetB0 + fine-tuning 20 layer terakhir.",
        "detail": "Arsitektur EfficientNet menggunakan compound scaling untuk menyeimbangkan depth, width, dan resolution secara efisien. Fine-tuning 20 layer terakhir dengan LR=1e-5 menghasilkan akurasi tertinggi.",
        "badge": "badge-best", "badge_text": "🏆 TERBAIK",
        "color": "#22c55e",
        "per_class": {
            "Busuk ":      {"p": 0.989, "r": 0.967, "f1": 0.978},
            "Fresh":       {"p": 1.000, "r": 0.973, "f1": 0.986},
            "Semi Fresh ": {"p": 0.957, "r": 0.991, "f1": 0.974},
        }
    },
    "CNN Custom": {
        "label": "CNN Custom",
        "icon": "🔧",
        "acc": 0.8237, "precision": 0.823, "recall": 0.8237, "f1": 0.823,
        "path": "models/cnn_model.h5",
        "desc": "CNN dari scratch: 3x Conv2D + MaxPool, Dense 128, Dropout 0.5.",
        "detail": "Dibangun dari nol dengan 3 blok konvolusi. Rescaling(1/255) ada di dalam model. L2 regularization mencegah overfitting. Cocok sebagai baseline.",
        "badge": "badge-base", "badge_text": "🔧 BASELINE",
        "color": "#0ea5e9",
        "per_class": {
            "Busuk ":      {"p": 0.830, "r": 0.857, "f1": 0.843},
            "Fresh":       {"p": 0.844, "r": 0.878, "f1": 0.861},
            "Semi Fresh ": {"p": 0.804, "r": 0.761, "f1": 0.782},
        }
    },
    "ResNet50": {
        "label": "ResNet50",
        "icon": "🔄",
        "acc": 0.8058, "precision": 0.836, "recall": 0.8058, "f1": 0.799,
        "path": "models/resnet_model.h5",
        "desc": "Transfer learning ResNet50 pretrained ImageNet, frozen weights.",
        "detail": "ResNet50 dengan frozen weights dan classification head baru. Tanpa fine-tuning, sehingga akurasi lebih rendah namun training lebih cepat.",
        "badge": "badge-transfer", "badge_text": "🔄 TRANSFER",
        "color": "#a78bfa",
        "per_class": {
            "Busuk ":      {"p": 0.866, "r": 0.923, "f1": 0.894},
            "Fresh":       {"p": 0.676, "r": 0.986, "f1": 0.802},
            "Semi Fresh ": {"p": 0.918, "r": 0.593, "f1": 0.720},
        }
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model_cached(model_key):
    import tensorflow as tf
    path = MODEL_INFO[model_key]["path"]
    return tf.keras.models.load_model(path)

# ══════════════════════════════════════════════════════════════════════════════
# PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════
def predict(img: Image.Image, model_key: str) -> np.ndarray:
    import tensorflow as tf
    model = load_model_cached(model_key)
    img_resized = img.convert("RGB").resize((224, 224))
    arr = np.array(img_resized, dtype=np.float32)
    if "CNN" in model_key:
        arr = np.expand_dims(arr, axis=0)
    elif "EfficientNet" in model_key:
        arr = tf.keras.applications.efficientnet.preprocess_input(arr)
        arr = np.expand_dims(arr, axis=0)
    elif "ResNet" in model_key:
        arr = tf.keras.applications.resnet50.preprocess_input(arr)
        arr = np.expand_dims(arr, axis=0)
    probs = model.predict(arr, verbose=0)
    return probs[0]

# ══════════════════════════════════════════════════════════════════════════════
# ── SIDEBAR ──────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Branding
    st.markdown("""
    <div class='sb-brand'>
        <div class='sb-brand-icon'>🐟</div>
        <div class='sb-brand-text'>
            <div class='title'>FishScan AI</div>
            <div class='sub'>DEEP LEARNING · v2.0</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Navigation
    st.markdown("<div class='nav-section'>Navigasi</div>", unsafe_allow_html=True)
    page = st.radio(
        "Nav",
        ["🔬 Deteksi Kesegaran", "📊 Performa Model", "ℹ️ Tentang Sistem"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:var(--border);margin:.3rem .6rem 1rem'></div>", unsafe_allow_html=True)

    # Algorithm Selection Header
    st.markdown("<div class='nav-section'>Pilih Algoritma</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.72rem;color:var(--muted);padding:0 .6rem .6rem;line-height:1.5'>
        Pilih model AI yang akan digunakan untuk analisis kesegaran ikan.
    </div>""", unsafe_allow_html=True)

    # Model selection with radio
    model_keys = list(MODEL_INFO.keys())
    model_choice = st.radio(
        "Model AI",
        model_keys,
        label_visibility="collapsed"
    )

    # Show selected model details
    info = MODEL_INFO[model_choice]
    st.markdown(f"""
    <div style='margin:.6rem .6rem 0;padding:.9rem 1rem;
                border-radius:10px;
                background:linear-gradient(135deg, rgba(14,165,233,0.08), rgba(14,165,233,0.02));
                border:1px solid rgba(14,165,233,0.25)'>
        <div style='font-size:.65rem;font-weight:700;letter-spacing:.08em;color:#7dd3fc;margin-bottom:.6rem'>
            <span class='pulse-dot'></span>MODEL AKTIF
        </div>
        <div style='font-size:.9rem;font-weight:800;margin-bottom:.4rem'>{info['icon']} {info['label']}</div>
        <div style='font-size:.72rem;color:var(--muted);line-height:1.5;margin-bottom:.7rem'>{info['desc']}</div>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:.4rem;'>
            <div style='background:var(--surface);border:1px solid var(--border);border-radius:8px;
                        padding:.5rem .6rem;text-align:center'>
                <div style='font-size:1rem;font-weight:800;font-family:JetBrains Mono,monospace;
                            color:{info["color"]}'>{info['acc']*100:.1f}%</div>
                <div style='font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em'>Accuracy</div>
            </div>
            <div style='background:var(--surface);border:1px solid var(--border);border-radius:8px;
                        padding:.5rem .6rem;text-align:center'>
                <div style='font-size:1rem;font-weight:800;font-family:JetBrains Mono,monospace;
                            color:{info["color"]}'>{info['f1']*100:.1f}%</div>
                <div style='font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em'>F1-Score</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:var(--border);margin:1rem .6rem'></div>", unsafe_allow_html=True)

    # System info
    st.markdown("""
    <div style='padding:0 .6rem'>
        <div style='font-size:.65rem;font-weight:700;letter-spacing:.08em;color:var(--muted);margin-bottom:.5rem'>INFO SISTEM</div>
        <div style='font-size:.72rem;color:var(--muted);line-height:1.9'>
            📦 Dataset: 1.654 gambar<br>
            🏷️ Kelas: 3 (Fresh / Semi / Busuk)<br>
            🖼️ Input: 224×224 px RGB<br>
            🧠 Framework: TensorFlow / Keras<br>
            📊 Test Set: 278 gambar
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DETEKSI
# ══════════════════════════════════════════════════════════════════════════════
if "Deteksi" in page:
    # Hero
    st.markdown(f"""
    <div class='hero-wrap'>
        <div class='hero-title'>🐟 Deteksi Kesegaran Ikan</div>
        <div class='hero-sub'>
            Analisis tingkat kesegaran ikan secara otomatis menggunakan <b>Deep Learning</b>.<br>
            Model aktif: <b style='color:#7dd3fc'>{info['icon']} {info['label']}</b>
            &nbsp;&mdash;&nbsp;
            <span style='color:{info["color"]};font-weight:700'>{info['acc']*100:.1f}% akurasi</span>
        </div>
        <div class='hero-badges'>
            <span class='badge badge-green'>✅ Fresh</span>
            <span class='badge badge-yellow'>⚠️ Semi Fresh</span>
            <span class='badge badge-red'>❌ Busuk</span>
            <span class='badge'>3 Model AI</span>
            <span class='badge'>224×224 Input</span>
        </div>
    </div>""", unsafe_allow_html=True)

    col_up, col_res = st.columns([1, 1], gap="large")

    with col_up:
        st.markdown("<div class='card-title'>UPLOAD GAMBAR IKAN</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "", type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption=f"📷 {uploaded.name}", use_container_width=True)
            st.markdown(f"""
            <div style='font-size:.78rem;color:var(--muted);margin:.4rem 0 .8rem;
                        background:var(--surface2);border:1px solid var(--border);
                        border-radius:8px;padding:.5rem .8rem;display:flex;gap:1rem'>
                <span>📐 {img.size[0]}×{img.size[1]} px</span>
                <span>🗂️ {uploaded.type.split('/')[-1].upper()}</span>
                <span>💾 {uploaded.size/1024:.1f} KB</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='upload-placeholder'>
                <div class='icon'>🖼️</div>
                <div style='font-weight:600;margin-bottom:.3rem'>Drag & drop gambar ikan</div>
                <div style='font-size:.78rem'>JPG, PNG, WEBP · Maks 200MB</div>
                <div style='font-size:.72rem;margin-top:.5rem;color:#5a8db0'>
                    Tips: Gunakan foto mata ikan yang jelas
                </div>
            </div>
            <div style='margin-top:.8rem'></div>""", unsafe_allow_html=True)

        run = st.button(
            "🔍 Analisis Sekarang",
            disabled=(uploaded is None),
            use_container_width=True
        )

        # Model quick-reference info
        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>MODEL YANG DIGUNAKAN</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card' style='border-left:3px solid {info["color"]};padding:1rem 1.2rem'>
            <div style='display:flex;align-items:center;gap:.6rem;margin-bottom:.4rem'>
                <span style='font-size:1.2rem'>{info['icon']}</span>
                <span style='font-weight:700;font-size:.92rem'>{info['label']}</span>
                <span class='algo-badge {info["badge"]}'>{info['badge_text']}</span>
            </div>
            <div style='font-size:.78rem;color:var(--muted);line-height:1.6'>{info['detail']}</div>
            <div style='display:flex;gap:1.5rem;margin-top:.7rem'>
                <div style='font-size:.78rem'>
                    <span style='color:var(--muted)'>Acc: </span>
                    <span style='font-family:JetBrains Mono,monospace;font-weight:700;color:{info["color"]}'>{info['acc']*100:.2f}%</span>
                </div>
                <div style='font-size:.78rem'>
                    <span style='color:var(--muted)'>F1: </span>
                    <span style='font-family:JetBrains Mono,monospace;font-weight:700;color:{info["color"]}'>{info['f1']*100:.2f}%</span>
                </div>
                <div style='font-size:.78rem'>
                    <span style='color:var(--muted)'>Prec: </span>
                    <span style='font-family:JetBrains Mono,monospace;font-weight:700;color:{info["color"]}'>{info['precision']*100:.2f}%</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_res:
        st.markdown("<div class='card-title'>HASIL ANALISIS</div>", unsafe_allow_html=True)

        if uploaded and run:
            with st.spinner("⚙️ Memproses gambar dengan model AI..."):
                img = Image.open(uploaded)
                probs = predict(img, model_choice)
                pred_idx   = int(np.argmax(probs))
                pred_class = CLASS_NAMES[pred_idx]
                confidence = float(probs[pred_idx])

            pred_strip = pred_class.strip()

            if pred_strip == "Fresh":
                icon, css, lbl = "✅", "result-fresh", "label-fresh"
                rec_box = "success-box"
                rekomendasi = "🟢 Ikan dalam kondisi sangat segar dan layak konsumsi. Segera olah atau simpan di kulkas (maks. 2 hari)."
            elif pred_strip == "Semi Fresh":
                icon, css, lbl = "⚠️", "result-semi", "label-semi"
                rec_box = "warn-box"
                rekomendasi = "🟡 Ikan masih bisa dikonsumsi namun segera olah dalam 4–6 jam. Jangan ditunda lebih lama."
            else:
                icon, css, lbl = "❌", "result-busuk", "label-busuk"
                rec_box = "danger-box"
                rekomendasi = "🔴 Ikan tidak layak konsumsi. Hindari untuk mencegah keracunan makanan. Buang segera."

            # Result card
            st.markdown(f"""
            <div class='{css}'>
                <div class='result-icon'>{icon}</div>
                <div class='result-label {lbl}'>{pred_strip.upper()}</div>
                <div class='result-conf'>
                    Tingkat Kepercayaan: <b style='font-size:1.1rem'>{confidence*100:.1f}%</b>
                </div>
                <span class='result-model-tag'>{info['icon']} {info['label']}</span>
            </div>""", unsafe_allow_html=True)

            # Probability distribution
            st.markdown("<div style='margin:.9rem 0 .3rem'></div>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>DISTRIBUSI PROBABILITAS</div>", unsafe_allow_html=True)

            color_map = {"Busuk": "busuk", "Fresh": "fresh", "Semi Fresh": "semi"}
            label_color = {"Busuk": "#ef4444", "Fresh": "#22c55e", "Semi Fresh": "#f59e0b"}
            for i, cls in enumerate(CLASS_NAMES):
                pct  = probs[i] * 100
                c    = color_map[cls.strip()]
                lc   = label_color[cls.strip()]
                is_pred = (i == pred_idx)
                bold = "font-weight:800" if is_pred else "font-weight:500"
                indicator = f"<span style='font-size:.6rem;background:{lc};color:#000;padding:.1rem .3rem;border-radius:4px;margin-left:.4rem;font-weight:700'>TOP</span>" if is_pred else ""
                st.markdown(f"""
                <div class='prob-row'>
                    <div class='prob-header'>
                        <span style='{bold};color:{"var(--text)" if is_pred else "var(--muted)"}'>{cls.strip()}{indicator}</span>
                        <span style='font-family:JetBrains Mono,monospace;font-weight:700;
                                     color:{"var(--text)" if is_pred else "var(--muted)"}'>{pct:.1f}%</span>
                    </div>
                    <div class='prob-track'>
                        <div class='prob-fill-{c}' style='width:{pct:.1f}%'></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Recommendation
            st.markdown(f"""
            <div class='{rec_box}' style='margin-top:1rem'>
                <b>Rekomendasi:</b><br>{rekomendasi}
            </div>""", unsafe_allow_html=True)

            # Additional metrics
            st.markdown("<div style='margin:.6rem 0 .3rem'></div>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>METRIK MODEL PADA KELAS INI</div>", unsafe_allow_html=True)
            per = info["per_class"][pred_class]
            st.markdown(f"""
            <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:.6rem;margin-top:.3rem'>
                <div class='metric-item'>
                    <div class='metric-val'>{per['p']*100:.1f}%</div>
                    <div class='metric-lbl'>Precision</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-val'>{per['r']*100:.1f}%</div>
                    <div class='metric-lbl'>Recall</div>
                </div>
                <div class='metric-item'>
                    <div class='metric-val'>{per['f1']*100:.1f}%</div>
                    <div class='metric-lbl'>F1-Score</div>
                </div>
            </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='icon'>🎯</div>
                <div style='font-size:.95rem;font-weight:600;margin-bottom:.4rem'>Siap Menganalisis</div>
                <div style='font-size:.82rem'>Upload gambar ikan lalu klik<br><b>Analisis Sekarang</b></div>
            </div>""", unsafe_allow_html=True)

    # Class guide
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>PANDUAN KELAS KESEGARAN</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, cls, icon_c, color, desc, signs in [
        (c1, "Fresh",      "✅", "#22c55e",
         "Ikan segar, layak konsumsi sepenuhnya.",
         "Mata jernih · Sisik mengkilap · Insang merah cerah · Tidak berbau"),
        (c2, "Semi Fresh", "⚠️", "#f59e0b",
         "Kualitas mulai menurun, segera olah.",
         "Sedikit keruh · Warna pudar · Aroma ringan · Tekstur masih oke"),
        (c3, "Busuk",      "❌", "#ef4444",
         "Tidak layak konsumsi, buang segera.",
         "Mata cekung · Bau menyengat · Tekstur lembek · Warna kusam"),
    ]:
        with col:
            st.markdown(f"""
            <div class='card' style='border-top:3px solid {color};padding:1.2rem 1.4rem'>
                <div style='font-size:2.2rem;margin-bottom:.4rem'>{icon_c}</div>
                <div style='font-weight:800;font-size:1.05rem;color:{color};margin-bottom:.3rem'>{cls}</div>
                <div style='font-size:.8rem;color:var(--text);margin-bottom:.5rem;line-height:1.4'>{desc}</div>
                <div style='font-size:.72rem;color:var(--muted);line-height:1.7;border-top:1px solid var(--border);
                            padding-top:.5rem;margin-top:.3rem'>{signs}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PERFORMA MODEL
# ══════════════════════════════════════════════════════════════════════════════
elif "Performa" in page:
    st.markdown("""
    <div class='hero-wrap'>
        <div class='hero-title'>📊 Performa Model</div>
        <div class='hero-sub'>Evaluasi & perbandingan 3 arsitektur Deep Learning pada test set (278 gambar).</div>
        <div class='hero-badges'>
            <span class='badge'>Test Set: 278 Gambar</span>
            <span class='badge'>3 Arsitektur</span>
            <span class='badge'>3 Kelas</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Model comparison cards
    st.markdown("<div class='card-title'>PERBANDINGAN AKURASI MODEL</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    model_summary = [
        ("EfficientNetB0", 0.9784, 0.9785, 0.9790, 0.9784, "#22c55e", "🏆 Terbaik", "Transfer + Fine-tuning"),
        ("CNN Custom",     0.8237, 0.8230, 0.8230, 0.8237, "#0ea5e9", "🔧 Baseline", "Scratch 3-Layer CNN"),
        ("ResNet50",       0.8058, 0.7989, 0.8360, 0.8058, "#a78bfa", "🔄 Transfer", "Frozen Weights"),
    ]
    for col, (name, acc, f1, prec, rec, color, tag, sub) in zip(cols, model_summary):
        is_active = (name in model_choice)
        active_style = f"box-shadow:0 0 0 2px {color};" if is_active else ""
        active_label = "<span style='font-size:.65rem;background:rgba(14,165,233,0.2);color:#7dd3fc;padding:.1rem .4rem;border-radius:4px;margin-left:.4rem'>AKTIF</span>" if is_active else ""
        with col:
            st.markdown(f"""
            <div class='card' style='border-top:3px solid {color};text-align:center;{active_style}'>
                <div style='font-size:.65rem;font-weight:700;letter-spacing:.08em;color:{color};
                            text-transform:uppercase;margin-bottom:.4rem'>{tag}</div>
                <div style='font-size:1rem;font-weight:800;margin-bottom:.2rem'>{name}{active_label}</div>
                <div style='font-size:.72rem;color:var(--muted);margin-bottom:.8rem'>{sub}</div>
                <div class='stat-val' style='color:{color};font-size:2rem'>{acc*100:.2f}%</div>
                <div class='stat-lbl'>Test Accuracy</div>
                <div style='margin-top:.8rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:.4rem'>
                    <div style='font-size:.68rem;color:var(--muted)'>F1<br><b style='color:var(--text);font-family:JetBrains Mono,monospace'>{f1*100:.1f}%</b></div>
                    <div style='font-size:.68rem;color:var(--muted)'>Prec<br><b style='color:var(--text);font-family:JetBrains Mono,monospace'>{prec*100:.1f}%</b></div>
                    <div style='font-size:.68rem;color:var(--muted)'>Rec<br><b style='color:var(--text);font-family:JetBrains Mono,monospace'>{rec*100:.1f}%</b></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Full comparison table
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>TABEL PERBANDINGAN LENGKAP</div>", unsafe_allow_html=True)
    st.markdown("""
    <table>
    <tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Jenis</th></tr>
    <tr>
        <td><b>🏆 EfficientNetB0</b></td>
        <td style='color:#22c55e;font-weight:700;font-family:JetBrains Mono,monospace'>97.84%</td>
        <td style='font-family:JetBrains Mono,monospace'>97.90%</td>
        <td style='font-family:JetBrains Mono,monospace'>97.84%</td>
        <td style='font-family:JetBrains Mono,monospace'>97.85%</td>
        <td><span style='background:rgba(34,197,94,0.12);color:#4ade80;padding:.15rem .5rem;border-radius:4px;font-size:.78rem'>Transfer + Fine-tune</span></td>
    </tr>
    <tr>
        <td><b>🔧 CNN Custom</b></td>
        <td style='color:#0ea5e9;font-weight:700;font-family:JetBrains Mono,monospace'>82.37%</td>
        <td style='font-family:JetBrains Mono,monospace'>82.30%</td>
        <td style='font-family:JetBrains Mono,monospace'>82.37%</td>
        <td style='font-family:JetBrains Mono,monospace'>82.30%</td>
        <td><span style='background:rgba(14,165,233,0.12);color:#7dd3fc;padding:.15rem .5rem;border-radius:4px;font-size:.78rem'>From Scratch</span></td>
    </tr>
    <tr>
        <td><b>🔄 ResNet50</b></td>
        <td style='color:#a78bfa;font-weight:700;font-family:JetBrains Mono,monospace'>80.58%</td>
        <td style='font-family:JetBrains Mono,monospace'>83.65%</td>
        <td style='font-family:JetBrains Mono,monospace'>80.58%</td>
        <td style='font-family:JetBrains Mono,monospace'>79.89%</td>
        <td><span style='background:rgba(167,139,250,0.12);color:#c4b5fd;padding:.15rem .5rem;border-radius:4px;font-size:.78rem'>Frozen Transfer</span></td>
    </tr>
    </table>""", unsafe_allow_html=True)

    # Per-class performance
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>PERFORMA PER KELAS</div>", unsafe_allow_html=True)
    for mname, mdata in MODEL_INFO.items():
        exp_open = ("EfficientNet" in mname)
        with st.expander(
            f"{mdata['icon']} {mdata['label']} — Accuracy {mdata['acc']*100:.2f}%",
            expanded=exp_open
        ):
            st.markdown(f"""
            <div style='font-size:.78rem;color:var(--muted);margin-bottom:.8rem;
                        background:var(--surface2);padding:.6rem 1rem;border-radius:8px'>
                {mdata['detail']}
            </div>
            <table>
            <tr><th>Kelas</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Sampel Uji</th></tr>
            <tr>
                <td><b style='color:#22c55e'>✅ Fresh</b></td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Fresh']['p']*100:.1f}%</td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Fresh']['r']*100:.1f}%</td>
                <td style='color:#22c55e;font-family:JetBrains Mono,monospace;font-weight:700'>{mdata['per_class']['Fresh']['f1']*100:.1f}%</td>
                <td>74</td>
            </tr>
            <tr>
                <td><b style='color:#f59e0b'>⚠️ Semi Fresh</b></td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Semi Fresh ']['p']*100:.1f}%</td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Semi Fresh ']['r']*100:.1f}%</td>
                <td style='color:#f59e0b;font-family:JetBrains Mono,monospace;font-weight:700'>{mdata['per_class']['Semi Fresh ']['f1']*100:.1f}%</td>
                <td>113</td>
            </tr>
            <tr>
                <td><b style='color:#ef4444'>❌ Busuk</b></td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Busuk ']['p']*100:.1f}%</td>
                <td style='font-family:JetBrains Mono,monospace'>{mdata['per_class']['Busuk ']['r']*100:.1f}%</td>
                <td style='color:#ef4444;font-family:JetBrains Mono,monospace;font-weight:700'>{mdata['per_class']['Busuk ']['f1']*100:.1f}%</td>
                <td>91</td>
            </tr>
            </table>""", unsafe_allow_html=True)

    # Training config
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>KONFIGURASI TRAINING</div>", unsafe_allow_html=True)
    st.markdown("""
    <table>
    <tr><th>Parameter</th><th>Nilai</th></tr>
    <tr><td>📦 Dataset Total</td><td style='font-family:JetBrains Mono,monospace'>1.654 gambar</td></tr>
    <tr><td>✂️ Split</td><td style='font-family:JetBrains Mono,monospace'>70% train / 15% val / 15% test</td></tr>
    <tr><td>🖼️ Input Size</td><td style='font-family:JetBrains Mono,monospace'>224 × 224 px</td></tr>
    <tr><td>📦 Batch Size</td><td style='font-family:JetBrains Mono,monospace'>32</td></tr>
    <tr><td>⚙️ Optimizer</td><td style='font-family:JetBrains Mono,monospace'>Adam</td></tr>
    <tr><td>📉 Loss Function</td><td style='font-family:JetBrains Mono,monospace'>Sparse Categorical Crossentropy</td></tr>
    <tr><td>🔀 Augmentasi</td><td style='font-family:JetBrains Mono,monospace'>RandomFlip, RandomRotation, RandomZoom</td></tr>
    <tr><td>⏹️ Early Stopping</td><td style='font-family:JetBrains Mono,monospace'>patience=3, monitor=val_loss</td></tr>
    <tr><td>🎛️ EfficientNet Fine-tune LR</td><td style='font-family:JetBrains Mono,monospace'>1e-5 (20 layer terakhir)</td></tr>
    </table>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — TENTANG
# ══════════════════════════════════════════════════════════════════════════════
elif "Tentang" in page:
    st.markdown("""
    <div class='hero-wrap'>
        <div class='hero-title'>ℹ️ Tentang Sistem</div>
        <div class='hero-sub'>FishScan AI — Sistem klasifikasi kesegaran ikan berbasis Computer Vision & Deep Learning.</div>
        <div class='hero-badges'>
            <span class='badge'>Computer Vision</span>
            <span class='badge'>Deep Learning</span>
            <span class='badge'>TensorFlow</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div class='card' style='border-left:3px solid #0ea5e9'>
            <div class='card-title'>LATAR BELAKANG</div>
            <p style='font-size:.88rem;line-height:1.8;color:#c5dff0'>
                Penilaian kesegaran ikan secara manual bergantung pada keahlian dan bersifat subjektif.
                Sistem ini memanfaatkan <b>Computer Vision</b> dan <b>Deep Learning</b> untuk
                mengklasifikasikan kondisi ikan secara otomatis dari foto — membantu pedagang,
                konsumen, dan petugas pasar mendapatkan penilaian yang <b>objektif dan konsisten</b>.
            </p>
        </div>
        <div class='card' style='border-left:3px solid #22c55e;margin-top:.8rem'>
            <div class='card-title'>ARSITEKTUR MODEL</div>
            <div style='font-size:.85rem;line-height:1.8;color:#c5dff0'>
                <div style='margin-bottom:.6rem'>
                    <b style='color:#0ea5e9'>🔧 CNN Custom</b><br>
                    3 blok Conv2D + MaxPooling, Rescaling(1/255) internal, Dense 128, Dropout 0.5, L2 regularization.
                </div>
                <div style='margin-bottom:.6rem'>
                    <b style='color:#22c55e'>⚡ EfficientNetB0</b><br>
                    Transfer learning ImageNet, fine-tuning 20 layer terakhir (LR=1e-5), preprocessing efficientnet.
                </div>
                <div>
                    <b style='color:#a78bfa'>🔄 ResNet50</b><br>
                    Transfer learning frozen + classification head baru, preprocessing resnet50.
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card' style='border-left:3px solid #f59e0b'>
            <div class='card-title'>DATASET</div>
            <p style='font-size:.88rem;line-height:1.8;color:#c5dff0'>
                Dataset gabungan sumber primer & sekunder, total <b>1.654 gambar</b>
                berupa foto <b>mata ikan</b>, terbagi 3 kelas:
            </p>
            <div style='display:grid;grid-template-columns:1fr;gap:.4rem;margin-top:.3rem'>
                <div style='background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.2);
                            border-radius:8px;padding:.5rem .8rem;font-size:.82rem'>
                    ✅ <b style='color:#22c55e'>Fresh</b> — 74 sampel uji
                </div>
                <div style='background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);
                            border-radius:8px;padding:.5rem .8rem;font-size:.82rem'>
                    ⚠️ <b style='color:#f59e0b'>Semi Fresh</b> — 113 sampel uji
                </div>
                <div style='background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);
                            border-radius:8px;padding:.5rem .8rem;font-size:.82rem'>
                    ❌ <b style='color:#ef4444'>Busuk</b> — 91 sampel uji
                </div>
            </div>
        </div>
        <div class='card' style='border-left:3px solid #ef4444;margin-top:.8rem'>
            <div class='card-title'>CARA PENGGUNAAN</div>
            <ol style='font-size:.88rem;line-height:2;color:#c5dff0;padding-left:1.2rem'>
                <li>Pilih algoritma model di <b>sidebar kiri</b></li>
                <li>Buka halaman <b>🔬 Deteksi Kesegaran</b></li>
                <li>Upload <b>foto mata ikan</b> (JPG/PNG/WEBP)</li>
                <li>Klik tombol <b>🔍 Analisis Sekarang</b></li>
                <li>Baca hasil prediksi, probabilitas, & rekomendasi</li>
            </ol>
        </div>""", unsafe_allow_html=True)

    # Tech stack
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>TECH STACK</div>", unsafe_allow_html=True)
    tech_cols = st.columns(4)
    techs = [
        ("🧠", "TensorFlow", "2.x", "#f59e0b"),
        ("🔢", "Keras", "API", "#ef4444"),
        ("🌊", "Streamlit", "UI", "#0ea5e9"),
        ("🐍", "Python", "3.x", "#22c55e"),
    ]
    for col, (icon, name, ver, color) in zip(tech_cols, techs):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:1rem'>
                <div style='font-size:1.8rem'>{icon}</div>
                <div style='font-weight:700;font-size:.88rem;margin:.3rem 0'>{name}</div>
                <div style='font-size:.7rem;color:{color};font-weight:600'>{ver}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='card' style='margin-top:.5rem;text-align:center;padding:1rem'>
        <div style='font-size:.78rem;color:var(--muted)'>
            🎓 Dibangun sebagai proyek penelitian Deep Learning untuk klasifikasi visual kualitas pangan
        </div>
    </div>""", unsafe_allow_html=True)