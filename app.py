from pathlib import Path
from urllib.parse import urlencode
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ambev Scorecard", page_icon="🍺", layout="wide", initial_sidebar_state="collapsed")
CLIENT_ID = "2609a149-fd2a-409a-a4b6-700c940a1f74"
TENANT_ID = "cef04b19-7776-4a94-b89b-375c77a8f936"
REDIRECT_URI = "https://scorecardoffco.streamlit.app/"
BASE_DIR = Path(__file__).resolve().parent
SCORECARD_HTML = BASE_DIR / "scorecard.html"
HEINEKEN_HTML = BASE_DIR / "heineken_ultimate_painel_completo_v16.html"

st.markdown("""
<style>
.stApp{background:#f5f7f8}[data-testid="stHeader"]{background:transparent}.block-container{max-width:1600px;padding-top:1.4rem;padding-bottom:2rem}
.auth-spacer{height:7vh}.auth-card{max-width:510px;margin:0 auto;padding:2.5rem 2.7rem 2rem;border-radius:20px;border:1px solid #e3e9e8;background:#fff;box-shadow:0 12px 38px rgba(22,48,61,.09);text-align:center}
.auth-brand{display:flex;justify-content:center;align-items:center;margin-bottom:1.2rem}.auth-brand-mark{width:58px;height:58px;border-radius:16px;display:grid;place-items:center;background:linear-gradient(145deg,#08785d,#14506b);color:#fff;font-size:30px}
.auth-divider{height:1px;background:#e8eeec;margin:1.2rem 0}.auth-card h1{color:#173b43;font-size:1.8rem;margin:0;font-weight:700}.auth-subtitle{color:#07805f;font-size:1rem;font-weight:650;margin:.3rem 0 1rem}.auth-description{color:#687b80;font-size:.94rem;line-height:1.55;margin-bottom:1.35rem}
.auth-button{display:flex;align-items:center;justify-content:center;gap:12px;width:100%;box-sizing:border-box;padding:14px 18px;border-radius:9px;background:#08785d;color:white!important;text-decoration:none;font-weight:650}.auth-button:hover{background:#06664f}
.microsoft-mark{display:grid;grid-template-columns:9px 9px;grid-template-rows:9px 9px;gap:2px}.microsoft-mark span:nth-child(1){background:#f25022}.microsoft-mark span:nth-child(2){background:#7fba00}.microsoft-mark span:nth-child(3){background:#00a4ef}.microsoft-mark span:nth-child(4){background:#ffb900}
.auth-security{color:#87979a;font-size:.78rem;margin:1rem 0 0}.app-heading{display:flex;align-items:center;gap:14px;padding:1rem 1.25rem;border:1px solid #e2eae7;border-radius:15px;background:#fff;margin-bottom:1rem}
.app-heading-mark{width:44px;height:44px;display:grid;place-items:center;border-radius:12px;color:white;background:linear-gradient(145deg,#08785d,#14506b);font-size:23px;flex-shrink:0}.app-heading h1{margin:0;color:#173b43;font-size:1.35rem}.app-heading p{margin:.2rem 0 0;color:#718287;font-size:.88rem}
div[data-testid="stTabs"] button{font-weight:650}div[data-testid="stTabs"] button[aria-selected="true"]{color:#08785d}div[data-testid="stTabs"] [data-baseweb="tab-highlight"]{background:#08785d}
</style>
""", unsafe_allow_html=True)


def microsoft_login_url():
    params = {"client_id": CLIENT_ID, "response_type": "code", "redirect_uri": REDIRECT_URI,
              "response_mode": "query", "scope": "openid profile email User.Read"}
    return f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?{urlencode(params)}"


def login_page():
    st.markdown('<div class="auth-spacer"></div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.45, 1])
    with center:
        st.markdown(f"""
        <div class="auth-card"><div class="auth-brand"><div class="auth-brand-mark">🍺</div></div>
        <div class="auth-divider"></div><h1>Ambev Scorecard</h1>
        <p class="auth-subtitle">Indicadores e acompanhamento</p>
        <p class="auth-description">Acesse o painel com sua conta corporativa.</p>
        <a class="auth-button" href="{microsoft_login_url()}">
        <span class="microsoft-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
        <span>Entrar com Microsoft</span></a>
        <p class="auth-security">Conexão segura com sua conta corporativa</p></div>
        """, unsafe_allow_html=True)


def show_html(path: Path, height: int):
    if not path.is_file():
        st.error(f"Não encontrei **{path.name}** na pasta do aplicativo.")
        return
    components.html(path.read_text(encoding="utf-8"), height=height, scrolling=True)


# O callback aponta explicitamente para o domínio do Scorecard.
if "code" in st.query_params:
    st.session_state.autenticado = True
if not st.session_state.get("autenticado", False):
    login_page()
    st.stop()

st.markdown("""
<div class="app-heading"><div class="app-heading-mark">🍺</div><div><h1>Ambev Scorecard</h1><p>Painéis de acompanhamento</p></div></div>
""", unsafe_allow_html=True)
_, exit_col = st.columns([6, 1])
with exit_col:
    if st.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()
score_tab, heineken_tab = st.tabs(["📊 Scorecard", "🍃 Heineken Ultimate"])
with score_tab:
    show_html(SCORECARD_HTML, 2200)
with heineken_tab:
    show_html(HEINEKEN_HTML, 2600)
