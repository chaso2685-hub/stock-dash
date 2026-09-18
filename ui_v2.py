from __future__ import annotations

import html
import streamlit as st


NAV_ITEMS = [
    ("홈", "⌂"),
    ("시장 현황", "▥"),
    ("종목 분석", "◫"),
    ("공시 분석", "▤"),
    ("테마 & 섹터", "◇"),
    ("포트폴리오", "▣"),
    ("관심 종목", "☆"),
    ("AI 인사이트", "✦"),
    ("데이터 연결 관리", "⚙"),
]


def apply_theme():
    st.markdown(
        """
<style>
:root {
  --bg: #F7F8FC;
  --surface: #FFFFFF;
  --surface-soft: #FBFCFF;
  --line: #E8EAF2;
  --line-strong: #D9DDF0;
  --text: #1B2A4A;
  --muted: #7A879F;
  --blue: #6D7EF7;
  --blue-soft: #EEF0FF;
  --lavender: #B9A7F7;
  --mint: #86DCC8;
  --pink: #F4A7C1;
  --peach: #F7C99B;
  --green: #10B981;
  --red: #F43F5E;
}

html, body, [class*="css"] {
  font-family: Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
}
.stApp {
  background:
    radial-gradient(circle at 5% 0%, rgba(185,167,247,.13), transparent 26%),
    radial-gradient(circle at 95% 5%, rgba(134,220,200,.12), transparent 24%),
    var(--bg);
  color: var(--text);
}
.block-container {
  max-width: 1480px;
  padding-top: 1.25rem;
  padding-bottom: 4rem;
}
header[data-testid="stHeader"] {
  background: rgba(247,248,252,.82);
  backdrop-filter: blur(14px);
}
section[data-testid="stSidebar"] {
  background: rgba(255,255,255,.92);
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] > div {
  padding-top: .9rem;
}
[data-testid="stSidebar"] .stRadio > label {
  display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
  gap: .3rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius: 13px;
  padding: .55rem .7rem;
  color: #52617D;
  transition: all .15s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: #F5F4FF;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(135deg, #F0EEFF, #EEF9F7);
  color: #5969D9;
  font-weight: 750;
  box-shadow: inset 3px 0 #8D83F7;
}
h1, h2, h3, h4 {
  color: var(--text);
  letter-spacing: -.035em;
}
h1 { font-weight: 800; }
h2, h3 { font-weight: 760; }
p, li { line-height: 1.62; }
[data-testid="stCaptionContainer"] {
  color: var(--muted);
}
[data-testid="stMetric"] {
  background: rgba(255,255,255,.92);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 8px 26px rgba(87,98,140,.06);
}
[data-testid="stMetricLabel"] { color: var(--muted); }
[data-testid="stMetricValue"] {
  color: var(--text);
  font-weight: 780;
}
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--line) !important;
  border-radius: 18px !important;
  background: rgba(255,255,255,.9);
  box-shadow: 0 8px 28px rgba(87,98,140,.055);
}
.stButton > button, .stFormSubmitButton > button {
  border-radius: 12px;
  min-height: 2.7rem;
  font-weight: 700;
  border-color: #DDE1F1;
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
  background: linear-gradient(135deg, #7485F8, #9A8BF4);
  border-color: #7485F8;
  color: #fff;
}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
  border-radius: 13px !important;
  border-color: #E1E4EF !important;
  background: #fff;
}
.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
  background: transparent;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 999px;
  padding: 8px 13px;
}
.stTabs [aria-selected="true"] {
  background: #EFEDFF;
  color: #5D68D9;
}
.stDataFrame {
  border: 1px solid var(--line);
  border-radius: 14px;
  overflow: hidden;
}
.planx-brand {
  display:flex; align-items:center; gap:10px; margin: 2px 0 22px 0;
}
.planx-brand-mark {
  width:36px; height:36px; border-radius:11px;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(145deg,#7182F7,#A997F7);
  color:white; font-size:19px; font-weight:800;
  box-shadow: 0 7px 18px rgba(113,130,247,.22);
}
.planx-brand-title {
  font-size:19px; line-height:1.15; font-weight:800; letter-spacing:-.03em;
}
.planx-brand-sub {
  font-size:10px; color:#9AA4BA; margin-top:3px;
}
.planx-hero {
  background: linear-gradient(135deg, rgba(255,255,255,.96), rgba(247,246,255,.96) 52%, rgba(241,251,249,.96));
  border: 1px solid #E7E8F2;
  border-radius: 22px;
  padding: 25px 28px;
  margin-bottom: 18px;
  box-shadow: 0 12px 34px rgba(87,98,140,.06);
  position: relative;
  overflow: hidden;
}
.planx-hero::after {
  content:"";
  position:absolute;
  width:170px; height:170px;
  right:-55px; top:-70px;
  border-radius:50%;
  background:rgba(134,220,200,.18);
}
.planx-eyebrow {
  color:#7180E8; font-size:11px; font-weight:800; letter-spacing:.1em;
  text-transform:uppercase; margin-bottom:7px;
}
.planx-hero h1 {
  margin:0; font-size:34px; line-height:1.18;
}
.planx-hero p {
  margin:9px 0 0; color:#78849A; font-size:14px;
}
.planx-card {
  background:linear-gradient(145deg,#FFFFFF,#FCFCFF);
  border:1px solid #E8EAF2;
  border-radius:17px;
  padding:17px 18px;
  min-height:116px;
  box-shadow:0 8px 24px rgba(87,98,140,.045);
}
.planx-card-title {
  font-size:12px; color:#7A879F; margin-bottom:8px; font-weight:700;
}
.planx-card-value {
  font-size:22px; color:#1B2A4A; font-weight:800; letter-spacing:-.03em;
}
.planx-card-note {
  margin-top:7px; font-size:11px; color:#9AA4BA;
}
.planx-empty {
  background: #FFFFFF;
  border:1px dashed #D4D8E8;
  border-radius:16px;
  padding:22px;
  color:#78849A;
}
.planx-source {
  display:inline-flex; align-items:center; gap:5px;
  color:#78849A; background:#F7F8FC; border:1px solid #E5E7F0;
  padding:4px 8px; border-radius:999px; font-size:10px;
}
.planx-status-ok { color:#078A68; background:#ECFBF6; border-color:#BDEBDD; }
.planx-status-wait { color:#9A6B16; background:#FFF8EA; border-color:#F5DFA9; }
.planx-status-bad { color:#C43D59; background:#FFF0F4; border-color:#F4C5D2; }
hr { border-color:#E8EAF2 !important; }
@media (max-width: 900px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .planx-hero { padding:22px 20px; }
  .planx-hero h1 { font-size:28px; }
}
@media (max-width:640px) {
  .block-container { padding-top:1.3rem; }
  .planx-hero h1 { font-size:28px; }
  .planx-card { min-height:100px; padding:14px; }
  .planx-card-value { font-size:23px; }
}
</style>
""",
        unsafe_allow_html=True,
    )
def brand():
    st.markdown(
        """
<div class="planx-brand">
  <div class="planx-brand-mark">↗</div>
  <div>
    <div class="planx-brand-title">StockDash</div>
    <div class="planx-brand-sub">Data to Insight.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "PLANX INVESTMENT OS"):
    st.markdown(
        f"""
<div class="planx-hero">
  <div class="planx-eyebrow">{html.escape(eyebrow)}</div>
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def card(title: str, value: str, note: str = "", status: str = ""):
    status_html = f'<div class="planx-card-note">{html.escape(status)}</div>' if status else ""
    st.markdown(
        f"""
<div class="planx-card">
  <div class="planx-card-title">{html.escape(title)}</div>
  <div class="planx-card-value">{html.escape(value)}</div>
  <div class="planx-card-note">{html.escape(note)}</div>
  {status_html}
</div>
""",
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str):
    st.markdown(
        f"""
<div class="planx-empty">
  <strong style="color:#334155">{html.escape(title)}</strong><br>
  <span>{html.escape(message)}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def source_badge(label: str, state: str = "wait"):
    cls = {"ok": "planx-status-ok", "bad": "planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(
        f'<span class="planx-source {cls}">{html.escape(label)}</span>',
        unsafe_allow_html=True,
    )
