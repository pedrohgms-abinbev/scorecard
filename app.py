import os
import runpy
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ambev Scorecard",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Microsoft Entra ID: mesmos identificadores e fluxo OAuth do código enviado.
CLIENT_ID = "2609a149-fd2a-409a-a4b6-700c940a1f74"
TENANT_ID = "cef04b19-7776-4a94-b89b-375c77a8f936"
REDIRECT_URI = "https://calendariogeoco.streamlit.app/"

# Arquivos HTML das duas abas. O segundo arquivo pode ser substituído pelo HTML novo.
BASE_DIR = Path(__file__).resolve().parent
FIRST_HTML_FILE = BASE_DIR / "scorecard.html"
SECOND_HTML_FILE = BASE_DIR / "outro_painel.html"

st.markdown("""
<style>
.stApp { background: #f4f6f8; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1600px; }
.score-header {
  background: linear-gradient(115deg,#142b4a 0%,#075b4a 100%);
  border-radius: 18px; padding: 1.35rem 1.7rem; color: #fff;
  margin-bottom: 1.1rem; box-shadow: 0 8px 24px rgba(15,35,55,.12);
}
.score-header h1 { color: #fff; margin: 0; font-size: 1.75rem; }
.score-header p { color: #dce8e7; margin: .3rem 0 0; }
div[data-testid="stTabs"] button { font-weight: 650; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #08785d; }
.login-card {
  max-width: 530px; margin: 8vh auto 1rem; padding: 2.3rem 2rem;
  border: 1px solid #e6ebef; border-radius: 22px; background: white;
  box-shadow: 0 16px 50px rgba(20,43,74,.12); text-align: center;
}
.login-card h1 { color: #142b4a; margin: .5rem 0; }
.login-card p { color: #64748b; }
.auth-button {
  display: inline-flex; align-items: center; justify-content: center; gap: 12px;
  margin-top: 1rem; padding: 13px 22px; border-radius: 9px;
  background: #08785d; color: white !important; text-decoration: none;
  font-weight: 650; width: 100%; box-sizing: border-box;
}
.auth-button:hover { background: #06664f; }
.microsoft-mark { display: grid; grid-template-columns: 9px 9px; grid-template-rows: 9px 9px; gap: 2px; }
.microsoft-mark span:nth-child(1) { background:#f25022; }
.microsoft-mark span:nth-child(2) { background:#7fba00; }
.microsoft-mark span:nth-child(3) { background:#00a4ef; }
.microsoft-mark span:nth-child(4) { background:#ffb900; }
.auth-caption { font-size: .82rem; color: #8491a0; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)


def microsoft_login_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": "openid profile email User.Read",
    }
    return (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?"
        f"{urlencode(params)}"
    )


def login_page():
    st.markdown(
        f"""
        <div class="login-card">
          <div style="font-size:2.8rem">🍺</div>
          <h1>Ambev Scorecard</h1>
          <p>Acesse os painéis com sua conta corporativa.</p>
          <a class="auth-button" href="{microsoft_login_url()}">
            <span class="microsoft-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
            <span>Entrar com Microsoft</span>
          </a>
          <div class="auth-caption">Conexão segura com sua conta Microsoft</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_html(path: Path, title: str):
    if not path.is_file():
        st.info(f"{title}: coloque o arquivo **{path.name}** na mesma pasta de app_score.py.")
        return
    html_content = path.read_text(encoding="utf-8")
    components.html(html_content, height=2000, scrolling=True)


# Mantém o comportamento do fluxo compartilhado: a presença do code na URL
# indica o retorno do provedor. A troca do code por token deve ocorrer no
# backend/OAuth callback para validar a sessão; não marque o usuário autenticado
# apenas pela existência do parâmetro code em uma implantação pública.
query_params = st.query_params
if "code" in query_params:
    st.session_state.microsoft_auth_code = query_params.get("code")
    st.session_state.autenticado = True

if not st.session_state.get("autenticado", False):
    login_page()
    st.stop()

st.markdown(
    """
    <div class="score-header">
      <h1>🍺 Ambev Scorecard</h1>
      <p>Central de indicadores e acompanhamento</p>
    </div>
    """,
    unsafe_allow_html=True,
)

_, logout_col = st.columns([6, 1])
with logout_col:
    if st.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

score_tab, second_tab = st.tabs(["📊 Scorecard", "📈 Segundo painel"])
with score_tab:
    render_html(FIRST_HTML_FILE, "Scorecard")
with second_tab:
    render_html(SECOND_HTML_FILE, "Segundo painel")
