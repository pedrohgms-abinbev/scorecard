from pathlib import Path
import html

import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# Ambev Scorecard | Microsoft Entra ID SSO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ambev Scorecard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CLIENT_ID = "2609a149-fd2a-409a-a4b6-700c940a1f74"
TENANT_ID = "cef04b19-7776-4a94-b89b-375c77a8f936"

QUERY_PARAMS = st.query_params

if "code" not in QUERY_PARAMS and not st.session_state.get("autenticado"):

    login_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri=https://ecossistemagestaooffco.streamlit.app/"
        f"&scope=openid profile email User.Read"
    )

    
    load_css()
    logo_base64 = imagem_para_base64("images/logo.png")

    st.markdown('<div class="auth-spacer"></div>', unsafe_allow_html=True)
    left_space, auth_card, right_space = st.columns([1, 1.45, 1])

    with auth_card:
        st.markdown(
            f"""
            <div class="auth-card">
                <div class="auth-brand">
                    <img src="data:image/png;base64,{logo_base64}" alt="Logo HUB Comercial">
                </div>
                <div class="auth-divider"></div>
                <h1>HUB Comercial</h1>
                <p class="auth-subtitle">Geo CO</p>
                <p class="auth-description">
                    Acesse o portal para consultar informações comerciais.
                </p>
                <a class="auth-button" href="{login_url}">
                    <span class="microsoft-mark" aria-hidden="true">
                        <span></span><span></span><span></span><span></span>
                    </span>
                    <span>Entrar com Microsoft</span>
                </a>
                <p class="auth-security">
                    Conexão segura com sua conta corporativa
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.stop()

st.session_state.autenticado = True

#st.success("Usuário autenticado")

BASE_DIR = Path(__file__).resolve().parent

# Cada arquivo encontrado aqui vira uma aba. Para adicionar outro painel,
# coloque o HTML na mesma pasta do app.py e inclua o nome nesta lista.
# O nome da aba é definido pelo campo "label".
HTML_PANELS = [
    {"file": "scorecard.html", "label": "Scorecard", "height": 2600},
    {
        "file": "radar_heineken_ultimate.html",
        "label": "Radar Heineken Ultimate",
        "height": 3000,
    },
    # Exemplo para adicionar novas abas:
    # {"file": "novo_painel.html", "label": "Novo painel", "height": 2400},
]

# Aparência alinhada ao padrão visual do HUB enviado, adaptada ao Scorecard.
st.markdown(
    """
    <style>
      .stApp { background: #f6f8f9; }
      [data-testid="stHeader"] { background: transparent; }
      .block-container { max-width: 1680px; padding: 1.35rem 2rem 2rem; }
      .auth-space { height: 7vh; }
      .auth-card {
        max-width: 510px; margin: 0 auto; padding: 2.25rem 2.6rem 2rem;
        border: 1px solid #e1e9e6; border-radius: 18px; background: #fff;
        box-shadow: 0 12px 38px rgba(20, 50, 45, .09); text-align: center;
      }
      .auth-logo {
        width: 58px; height: 58px; margin: 0 auto 1.1rem; display: grid;
        place-items: center; border-radius: 15px;
        background: linear-gradient(145deg, #08784f, #174c62);
        color: #fff; font-size: 28px;
      }
      .auth-rule { height: 1px; background: #e8eeeb; margin: 1.1rem 0; }
      .auth-card h1 { margin: 0; color: #173b36; font-size: 1.8rem; font-weight: 750; }
      .auth-subtitle { margin: .35rem 0 1rem; color: #08784f; font-weight: 700; }
      .auth-copy { margin: 0 0 1.25rem; color: #687b78; font-size: .94rem; }
      .app-masthead {
        display: flex; align-items: center; gap: 13px; padding: 1rem 1.2rem;
        border: 1px solid #e1e9e6; border-radius: 13px; background: #fff;
        margin-bottom: 1rem;
      }
      .app-mark {
        width: 43px; height: 43px; display: grid; place-items: center;
        flex: 0 0 43px; border-radius: 11px; color: white; font-size: 22px;
        background: linear-gradient(145deg, #08784f, #174c62);
      }
      .app-masthead h1 { margin: 0; color: #173b36; font-size: 1.35rem; }
      .app-masthead p { margin: .15rem 0 0; color: #71827e; font-size: .86rem; }
      div[data-testid="stTabs"] button { font-weight: 700; }
      div[data-testid="stTabs"] button[aria-selected="true"] { color: #08784f; }
      div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: #08784f; }
      div[data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 5px; }
      .user-chip { color: #657873; font-size: .82rem; text-align: right; padding-top: .35rem; }
      iframe { border: 0; }
      @media (max-width: 700px) {
        .block-container { padding: 1rem .65rem 1.5rem; }
        .auth-card { padding: 1.8rem 1.2rem; }
        .app-masthead { padding: .8rem; }
        .app-masthead h1 { font-size: 1.15rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_login() -> None:
    st.markdown('<div class="auth-space"></div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.45, 1])
    with center:
        st.markdown(
            """
            <div class="auth-card">
              <div class="auth-logo">📊</div>
              <div class="auth-rule"></div>
              <h1>Ambev Scorecard</h1>
              <p class="auth-subtitle">Acompanhamento comercial</p>
              <p class="auth-copy">Entre com sua conta corporativa Microsoft para acessar os painéis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Entrar com Microsoft",
            type="primary",
            use_container_width=True,
            on_click=st.login,
        )
        st.caption("Autenticação corporativa por SSO Microsoft")


def resolve_panels() -> list[dict]:
    """Retorna os painéis configurados que existem ao lado deste app."""
    panels = []
    for item in HTML_PANELS:
        path = BASE_DIR / item["file"]
        if path.is_file():
            panels.append({**item, "path": path})
    return panels


def render_panel(panel: dict) -> None:
    try:
        content = panel["path"].read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        content = panel["path"].read_text(encoding="latin-1")
    except OSError as exc:
        st.error(f"Não foi possível abrir {panel['file']}: {exc}")
        return

    # O conteúdo é executado isoladamente no iframe do Streamlit.
    components.html(
        content,
        height=int(panel.get("height", 2400)),
        scrolling=True,
    )


# st.login usa OIDC de verdade: a identidade é validada pelo Streamlit/Authlib.
# O segredo do cliente fica no secrets.toml, nunca neste arquivo Python.
try:
    auth_cfg = st.secrets["auth"]
    auth_ready = (
        auth_cfg.get("client_id") == CLIENT_ID
        and bool(auth_cfg.get("client_secret"))
        and auth_cfg.get("redirect_uri") == REDIRECT_URI
        and bool(auth_cfg.get("cookie_secret"))
        and bool(auth_cfg.get("server_metadata_url"))
    )
except Exception:
    auth_ready = False

if not auth_ready:
    st.error("Configure a seção [auth] do .streamlit/secrets.toml para habilitar o SSO Microsoft.")
    st.code(
        f"[auth]\nredirect_uri = \"{REDIRECT_URI}\"\ncookie_secret = \"GERE_UM_SEGREDO_ALEATORIO_FORTE\"\nclient_id = \"{CLIENT_ID}\"\nclient_secret = \"COLE_AQUI_O_CLIENT_SECRET_DO_ENTRA_ID\"\nserver_metadata_url = \"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration\"",
        language="toml",
    )
    st.info("Mantenha as configurações existentes do Excel no secrets.toml. Apenas acrescente esta seção [auth].")
    st.stop()

# Não aceite apenas a presença de ?code= na URL como prova de autenticação.
if not st.user.is_logged_in:
    show_login()
    st.stop()

user_name = (
    getattr(st.user, "name", None)
    or getattr(st.user, "preferred_username", None)
    or getattr(st.user, "email", None)
    or "Usuário autenticado"
)

st.markdown(
    """
    <div class="app-masthead">
      <div class="app-mark">📊</div>
      <div>
        <h1>Ambev Scorecard</h1>
        <p>Painéis de performance e acompanhamento</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

user_col, logout_col = st.columns([6, 1])
with user_col:
    st.markdown(
        f'<div class="user-chip">Conectado: {html.escape(str(user_name))}</div>',
        unsafe_allow_html=True,
    )
with logout_col:
    st.button("Sair", use_container_width=True, on_click=st.logout)

panels = resolve_panels()
if not panels:
    st.error("Nenhum HTML de painel foi encontrado. Coloque os arquivos na mesma pasta do app.py.")
    st.stop()

# Uma aba por HTML. Novos arquivos são adicionados em HTML_PANELS.
tabs = st.tabs([panel["label"] for panel in panels])
for tab, panel in zip(tabs, panels):
    with tab:
        render_panel(panel)
