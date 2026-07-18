import streamlit as st
import requests
import uuid
import os

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Email Agent - Inbox AI", page_icon="✉️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0f1115; color: #e2e4ec; min-height: 100vh; }
.stApp::before {
    content: ''; position: fixed; inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% -20%, rgba(255,255,255,0.05) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}
section[data-testid="stSidebar"] { background: #15181e !important; border-right: 1px solid rgba(255,255,255,0.05) !important; }
section[data-testid="stSidebar"] > div { padding-top: 2rem !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 2.5rem 3rem !important; max-width: 900px !important; }
.ai-logo { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; }
.ai-logo-icon { width: 42px; height: 42px; background: #252830; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.1); }
.ai-logo-text { font-size: 1.15rem; font-weight: 600; color: #ffffff; }
.ai-logo-sub { font-size: 0.7rem; color: #8b92a5; letter-spacing: 0.1em; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }
.step-nav { margin-bottom: 0.4rem; padding: 0.65rem 0.9rem; border-radius: 8px; display: flex; align-items: center; gap: 0.75rem; font-size: 0.82rem; font-weight: 500; color: #8b92a5; border: 1px solid transparent; }
.step-nav.active { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); color: #ffffff; }
.step-nav.done { color: #8b92a5; }
.step-num { width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; font-size: 0.68rem; font-family: 'JetBrains Mono', monospace; flex-shrink: 0; }
.step-nav.active .step-num { background: rgba(255,255,255,0.15); color: #ffffff; }
.step-nav.done .step-num { background: transparent; }
.sb-status { margin-top: 1.5rem; padding: 1rem; background: #1c1f26; border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; font-size: 0.78rem; line-height: 1.8; }
.sb-status-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #646a7c; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.6rem; }
.sb-row { display: flex; justify-content: space-between; color: #8b92a5; }
.sb-val { color: #ffffff; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }
.page-header { margin-bottom: 2.2rem; }
.page-title { font-size: 2.1rem; font-weight: 600; letter-spacing: -0.03em; color: #ffffff; line-height: 1.15; margin-bottom: 0.3rem; }
.page-desc { font-size: 0.875rem; color: #8b92a5; }
.section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: #646a7c; margin-bottom: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.05); }
.glass-card { background: #15181e; border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.glass-card:hover { border-color: rgba(255,255,255,0.1); }
.card-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #646a7c; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.45rem; }
.card-value { font-size: 0.9rem; color: #ffffff; }
.card-value.mono { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #ffffff; }
.connect-box { background: #15181e; border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 1.6rem 2rem; margin-bottom: 1.5rem; }
.connect-title { font-size: 1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.4rem; }
.connect-sub { font-size: 0.82rem; color: #8b92a5; margin-bottom: 1rem; }
.draft-box { background: #111318; border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 1.4rem 1.6rem; font-family: 'JetBrains Mono', monospace; font-size: 0.83rem; color: #c4c8e8; line-height: 1.85; white-space: pre-wrap; margin-bottom: 1.2rem; position: relative; }
.draft-box::before { content: 'DRAFT'; position: absolute; top: 0.7rem; right: 1rem; font-size: 0.58rem; letter-spacing: 0.15em; color: #646a7c; }
.sent-banner { background: #15181e; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1.6rem 2rem; display: flex; align-items: center; gap: 1.2rem; margin-top: 0.5rem; }
.sent-title { font-size: 1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.2rem; }
.sent-sub { font-size: 0.8rem; color: #8b92a5; }
.fancy-divider { height: 1px; background: rgba(255,255,255,0.05); margin: 2rem 0; }
.alert-strip { padding: 0.8rem 1.1rem; border-radius: 8px; font-size: 0.845rem; display: flex; align-items: center; gap: 0.65rem; margin-bottom: 1.2rem; background: #15181e; border: 1px solid rgba(255,255,255,0.05); color: #d4d8e8; }
.alert-amber { border-left: 3px solid #fbbf24; }
.alert-green  { border-left: 3px solid #4ade80; }
.alert-red    { border-left: 3px solid #f87171; }
.alert-indigo { border-left: 3px solid #ffffff; }
.stButton > button { font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.855rem !important; border-radius: 6px !important; transition: all 0.2s ease !important; height: 40px !important; border: 1px solid rgba(255,255,255,0.1) !important; background: #15181e !important; color: #ffffff !important; }
.stButton > button:hover { background: #1c1f26 !important; border-color: rgba(255,255,255,0.2) !important; }
.stButton > button[kind="primary"] { background: #ffffff !important; color: #000000 !important; border: none !important; font-weight: 600 !important; }
.stButton > button[kind="primary"]:hover { background: #e2e4ec !important; }
.stTextArea textarea { background: #111318 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px !important; color: #d4d8e8 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.83rem !important; line-height: 1.8 !important; }
.stTextInput input { background: #111318 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 6px !important; color: #d4d8e8 !important; font-family: 'JetBrains Mono', monospace !important; }
.stSpinner > div { border-top-color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {
    "user_id": None,
    "gmail_connected": False,
    "thread_id": None,
    "draft_response": None,
    "needs_review": False,
    "sender": None,
    "subject": None,
    "sent": False,
    "review_done": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Auto-generate a user_id for this browser session if none exists
if not st.session_state.user_id:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:12]}"

def current_step():
    if not st.session_state.gmail_connected:
        return 0
    if st.session_state.sent:
        return 3
    if st.session_state.thread_id:
        return 2
    return 1

step = current_step()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="ai-logo">
        <div class="ai-logo-icon">✉</div>
        <div>
            <div class="ai-logo-text">Email Agent</div>
            <div class="ai-logo-sub">Inbox AI · Composio</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    steps_list = [
        ("00", "Connect Gmail", 0),
        ("01", "Fetch & Process", 1),
        ("02", "Review Draft", 2),
        ("03", "Send Reply", 3),
    ]
    for num, label, s in steps_list:
        css  = "done" if step > s else ("active" if step == s else "")
        icon = "✓"   if step > s else num
        st.markdown(f"""
        <div class="step-nav {css}">
            <div class="step-num">{icon}</div>
            {label}
        </div>
        """, unsafe_allow_html=True)

    uid_short = st.session_state.user_id[:20] if st.session_state.user_id else "—"
    conn_val  = "connected ✓" if st.session_state.gmail_connected else "not connected"
    tid_display = (st.session_state.thread_id[:16] + "…") if st.session_state.thread_id else "—"
    status_val  = "sent" if st.session_state.sent else ("review" if st.session_state.needs_review else ("draft" if st.session_state.draft_response else "idle"))

    st.markdown(f"""
    <div class="sb-status">
        <div class="sb-status-label">Session</div>
        <div class="sb-row"><span>User ID</span><span class="sb-val">{uid_short}</span></div>
        <div class="sb-row"><span>Gmail</span><span class="sb-val">{conn_val}</span></div>
        <div class="sb-row"><span>Thread</span><span class="sb-val">{tid_display}</span></div>
        <div class="sb-row"><span>Status</span><span class="sb-val">{status_val}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺ Reset Session", use_container_width=True, key="reset_sidebar"):
        st.session_state.update({
            "user_id": f"user_{uuid.uuid4().hex[:12]}",
            "gmail_connected": False,
            "thread_id": None, "draft_response": None,
            "needs_review": False, "sender": None,
            "subject": None, "sent": False, "review_done": False,
        })
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-title">Email Agent</div>
    <div class="page-desc">Connect your Gmail, let the AI classify, draft, and reply - for any user.</div>
</div>
""", unsafe_allow_html=True)

# ── Step 0 — Connect Gmail ────────────────────────────────────────────────────
st.markdown('<div class="section-label">Step 00 — Connect Your Gmail</div>', unsafe_allow_html=True)

if st.session_state.gmail_connected:
    st.markdown(
        '<div class="alert-strip alert-green">✓&nbsp; Gmail connected — your account is ready.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(f"""
    <div class="connect-box">
        <div class="connect-title">🔗 Connect your Gmail account</div>
        <div class="connect-sub">
            Click the button below to get your personal OAuth link.<br>
            Open that link, sign in with Google, then come back and click <strong>Check Connection</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_get, col_check = st.columns(2)

    with col_get:
        if st.button("🔗  Get Gmail Auth Link", use_container_width=True, type="primary", key="get_link_btn"):
            with st.spinner("Generating OAuth link…"):
                try:
                    resp = requests.get(
                        f"{API_BASE}/auth/connect-gmail",
                        params={"user_id": st.session_state.user_id},
                        timeout=15,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    st.session_state["_auth_url"] = data.get("auth_url", "")
                except Exception as e:
                    st.markdown(
                        f'<div class="alert-strip alert-red">❌&nbsp; {e}</div>',
                        unsafe_allow_html=True
                    )

    with col_check:
        if st.button("✓  Check Connection", use_container_width=True, key="check_conn_btn"):
            with st.spinner("Checking…"):
                try:
                    resp = requests.get(
                        f"{API_BASE}/auth/status",
                        params={"user_id": st.session_state.user_id},
                        timeout=10,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    if data.get("gmail_connected"):
                        st.session_state.gmail_connected = True
                        st.rerun()
                    else:
                        st.markdown(
                            '<div class="alert-strip alert-amber">⏳&nbsp; Not connected yet — complete the Google login first.</div>',
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.markdown(
                        f'<div class="alert-strip alert-red">❌&nbsp; {e}</div>',
                        unsafe_allow_html=True
                    )

    # Show the auth URL if generated
    if st.session_state.get("_auth_url"):
        st.markdown(
            f'<div class="alert-strip alert-indigo">🔑&nbsp; <a href="{st.session_state["_auth_url"]}" target="_blank" style="color:#818cf8;">Click here to authorize Gmail</a> — then click Check Connection.</div>',
            unsafe_allow_html=True
        )

# ── Step 1 — Fetch & Process (only shown after Gmail connected) ───────────────
if st.session_state.gmail_connected:
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Step 01 — Fetch & Process</div>', unsafe_allow_html=True)

    col_btn, col_hint = st.columns([2, 3])
    with col_btn:
        process_btn = st.button("⟳  Process Latest Email", use_container_width=True, type="primary", key="process_btn")
    with col_hint:
        st.markdown(
            '<div style="color:#3f4468;font-size:0.8rem;padding-top:0.7rem;">Fetches the most recent email from your inbox and runs it through the agent pipeline.</div>',
            unsafe_allow_html=True
        )

    if process_btn:
        st.session_state.update({
            "thread_id": None, "draft_response": None,
            "needs_review": False, "sender": None,
            "subject": None, "sent": False, "review_done": False,
        })
        with st.spinner("Connecting to agent pipeline…"):
            try:
                resp = requests.post(
                    f"{API_BASE}/agent/process-latest",
                    json={"user_id": st.session_state.user_id},
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == "no_email":
                    st.markdown(
                        '<div class="alert-strip alert-indigo">📭&nbsp; No emails found in your inbox.</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.session_state.thread_id     = data["thread_id"]
                    st.session_state.draft_response = data.get("draft_response")
                    st.session_state.needs_review   = data.get("interrupt", False)
                    st.session_state.sender         = data.get("sender")
                    st.session_state.subject        = data.get("subject")
                    st.rerun()
            except requests.exceptions.ConnectionError:
                st.markdown(
                    '<div class="alert-strip alert-red">🔌&nbsp; Cannot reach backend — make sure FastAPI is running on <code>localhost:8000</code>.</div>',
                    unsafe_allow_html=True
                )
            except requests.exceptions.HTTPError as e:
                st.markdown(
                    f'<div class="alert-strip alert-red">API error {e.response.status_code}: {e.response.text}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ── Email metadata ─────────────────────────────────────────────────────────────
if st.session_state.thread_id:
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-label">From</div>
            <div class="card-value">{st.session_state.sender or "—"}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-label">Subject</div>
            <div class="card-value">{st.session_state.subject or "—"}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Thread ID</div>
        <div class="card-value mono">{st.session_state.thread_id}</div>
    </div>""", unsafe_allow_html=True)

    # ── Step 2 — Review ───────────────────────────────────────────────────────
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if st.session_state.needs_review and not st.session_state.review_done:
        st.markdown('<div class="section-label">Step 02 — Human Review Required</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="alert-strip alert-amber">⚠️&nbsp; This email needs your approval before a reply is sent.</div>',
            unsafe_allow_html=True
        )

        edited = st.text_area(
            label="Edit draft if needed",
            value=st.session_state.draft_response or "",
            height=280,
            key="draft_editor",
        )

        col_approve, col_reject = st.columns(2)
        with col_approve:
            approve_btn = st.button("✓  Approve & Save Draft", use_container_width=True, type="primary", key="approve_btn")
        with col_reject:
            reject_btn = st.button("✕  Reject — Handle Manually", use_container_width=True, key="reject_btn")

        if approve_btn:
            with st.spinner("Submitting review…"):
                try:
                    resp = requests.post(f"{API_BASE}/agent/review", json={
                        "thread_id": st.session_state.thread_id,
                        "approved": True,
                        "edited_response": edited,
                    }, timeout=30)
                    resp.raise_for_status()
                    result = resp.json()
                    st.session_state.draft_response = result.get("draft_response") or edited
                    st.session_state.review_done  = True
                    st.session_state.needs_review = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Review failed: {e}")

        if reject_btn:
            with st.spinner("Submitting rejection…"):
                try:
                    resp = requests.post(f"{API_BASE}/agent/review", json={
                        "thread_id": st.session_state.thread_id,
                        "approved": False,
                        "edited_response": None,
                    }, timeout=30)
                    resp.raise_for_status()
                    st.session_state.draft_response = None
                    st.session_state.review_done  = True
                    st.session_state.needs_review = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Rejection failed: {e}")
    else:
        st.markdown('<div class="section-label">Step 02 — Draft Response</div>', unsafe_allow_html=True)
        if st.session_state.draft_response:
            st.markdown(
                '<div class="alert-strip alert-green">✓&nbsp; Draft ready — review below before sending.</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="draft-box">{st.session_state.draft_response}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="alert-strip alert-red">✕&nbsp; No draft — email was rejected or the agent could not produce a reply.</div>',
                unsafe_allow_html=True
            )

    # ── Step 3 — Send ─────────────────────────────────────────────────────────
    if st.session_state.draft_response and not st.session_state.sent:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Step 03 — Send Reply</div>', unsafe_allow_html=True)

        send_col, _ = st.columns([2, 3])
        with send_col:
            send_btn = st.button("✉  Send Reply via Gmail", use_container_width=True, type="primary", key="send_btn")

        if send_btn:
            with st.spinner("Sending via your Gmail…"):
                try:
                    resp = requests.post(
                        f"{API_BASE}/agent/send",
                        json={
                            "thread_id": st.session_state.thread_id,
                            "user_id": st.session_state.user_id,
                        },
                        timeout=30,
                    )
                    resp.raise_for_status()
                    result = resp.json()
                    if result.get("status") == "sent":
                        st.session_state.sent = True
                        st.rerun()
                    else:
                        st.error(f"Send failed: {result.get('error', 'Unknown error')}")
                except requests.exceptions.HTTPError as e:
                    st.error(f"Send error: {e.response.status_code} — {e.response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Sent ──────────────────────────────────────────────────────────────────
    if st.session_state.sent:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sent-banner">
            <div style="font-size:2rem">🚀</div>
            <div>
                <div class="sent-title">Reply Sent Successfully</div>
                <div class="sent-sub">Email delivered via your Gmail — thread closed.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        reset_col, _ = st.columns([2, 3])
        with reset_col:
            if st.button("↺  Process Another Email", use_container_width=True, key="reset_btn"):
                st.session_state.update({
                    "thread_id": None, "draft_response": None,
                    "needs_review": False, "sender": None,
                    "subject": None, "sent": False, "review_done": False,
                })
                st.rerun()