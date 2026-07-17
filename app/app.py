import streamlit as st
import requests

API_BASE = "http://localhost:8000/agent"

st.set_page_config(
    page_title="Email Agent — Inbox AI",
    page_icon="✉️",
    layout="wide",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: #080b12;
    color: #d4d8e8;
    min-height: 100vh;
}

/* ── Animated mesh background ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 90%, rgba(168,85,247,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(14,165,233,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10,12,20,0.92) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
    backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 2.5rem 3rem !important;
    max-width: 900px !important;
}

/* ── Logo / title ── */
.ai-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 2rem;
}
.ai-logo-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 0 20px rgba(99,102,241,0.5);
}
.ai-logo-text {
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.01em;
}
.ai-logo-sub {
    font-size: 0.7rem;
    color: #3f4468;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Sidebar step nav ── */
.step-nav {
    margin-bottom: 0.4rem;
    padding: 0.65rem 0.9rem;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: #4b5280;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    cursor: default;
}
.step-nav.active {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.3);
    color: #818cf8;
}
.step-nav.done {
    background: rgba(34,197,94,0.07);
    border-color: rgba(34,197,94,0.2);
    color: #4ade80;
}
.step-num {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
}
.step-nav.active .step-num { background: rgba(99,102,241,0.4); }
.step-nav.done .step-num   { background: rgba(34,197,94,0.3); }

/* ── Sidebar status card ── */
.sb-status {
    margin-top: 1.5rem;
    padding: 1rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    font-size: 0.78rem;
    line-height: 1.8;
}
.sb-status-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #3f4468;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.sb-row { display: flex; justify-content: space-between; color: #545880; }
.sb-val { color: #818cf8; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }

/* ── Page header ── */
.page-header {
    margin-bottom: 2.2rem;
}
.page-title {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e0e7ff 0%, #c084fc 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.3rem;
}
.page-desc {
    font-size: 0.875rem;
    color: #3f4468;
    font-weight: 400;
}

/* ── Section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3f4468;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.2), transparent);
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s ease;
}
.glass-card:hover {
    border-color: rgba(99,102,241,0.2);
}
.card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #3f4468;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.45rem;
}
.card-value {
    font-size: 0.9rem;
    color: #c4c8e8;
    font-weight: 400;
    word-break: break-all;
}
.card-value.mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6366f1;
}

/* ── Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.22rem 0.6rem;
    border-radius: 999px;
    font-weight: 500;
}
.badge-review  { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.badge-ready   { background: rgba(34,197,94,0.12);  color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
.badge-sent    { background: rgba(99,102,241,0.12); color: #818cf8; border: 1px solid rgba(99,102,241,0.25); }
.badge-error   { background: rgba(239,68,68,0.12);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

/* ── Alert strip ── */
.alert-strip {
    padding: 0.8rem 1.1rem;
    border-radius: 12px;
    font-size: 0.845rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1.2rem;
}
.alert-amber {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.2);
    color: #fbbf24;
}
.alert-green {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.2);
    color: #4ade80;
}
.alert-red {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    color: #f87171;
}
.alert-indigo {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    color: #818cf8;
}

/* ── Draft box ── */
.draft-box {
    background: rgba(8,11,18,0.8);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    color: #9ca3c8;
    line-height: 1.85;
    white-space: pre-wrap;
    margin-bottom: 1.2rem;
    position: relative;
}
.draft-box::before {
    content: 'DRAFT';
    position: absolute;
    top: 0.7rem;
    right: 1rem;
    font-size: 0.58rem;
    letter-spacing: 0.15em;
    color: #3f4468;
}

/* ── Sent banner ── */
.sent-banner {
    background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(99,102,241,0.08));
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-top: 0.5rem;
}
.sent-icon {
    font-size: 2rem;
    line-height: 1;
}
.sent-title {
    font-size: 1rem;
    font-weight: 600;
    color: #4ade80;
    margin-bottom: 0.2rem;
}
.sent-sub {
    font-size: 0.8rem;
    color: #3a5a42;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.2), transparent);
    margin: 2rem 0;
}

/* ── Streamlit button overrides ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.855rem !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
    height: 42px !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 25px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #9ca3c8 !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.18) !important;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(8,11,18,0.9) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 12px !important;
    color: #9ca3c8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    line-height: 1.8 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
.stTextArea label { color: #3f4468 !important; font-size: 0.78rem !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Info/success/error/warning overrides ── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────────
for key, default in {
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

# ── Derive current step for sidebar highlight ──────────────────────────────────
def current_step():
    if st.session_state.sent:
        return 3
    if st.session_state.thread_id and st.session_state.draft_response:
        return 2
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
            <div class="ai-logo-sub">Inbox AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Fetch & Process", 1),
        ("02", "Review Draft", 2),
        ("03", "Send Reply", 3),
    ]
    for num, label, s in steps:
        css = "done" if step > s else ("active" if step == s else "")
        icon = "✓" if step > s else num
        st.markdown(f"""
        <div class="step-nav {css}">
            <div class="step-num">{icon}</div>
            {label}
        </div>
        """, unsafe_allow_html=True)

    # Status snapshot
    tid_display = (st.session_state.thread_id[:16] + "…") if st.session_state.thread_id else "—"
    sender_display = (st.session_state.sender or "—")[:22]
    status_val = "sent" if st.session_state.sent else ("review" if st.session_state.needs_review else ("draft" if st.session_state.draft_response else "idle"))

    st.markdown(f"""
    <div class="sb-status">
        <div class="sb-status-label">Session</div>
        <div class="sb-row"><span>Thread</span><span class="sb-val">{tid_display}</span></div>
        <div class="sb-row"><span>From</span><span class="sb-val">{sender_display}</span></div>
        <div class="sb-row"><span>Status</span><span class="sb-val">{status_val}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-title">Email Agent</div>
    <div class="page-desc">Autonomous email processing — classify, draft, review, send.</div>
</div>
""", unsafe_allow_html=True)

# ── Step 1 — Fetch & Process ──────────────────────────────────────────────────
st.markdown('<div class="section-label">Step 01 — Fetch & Process</div>', unsafe_allow_html=True)

col_btn, col_hint = st.columns([2, 3])
with col_btn:
    process_btn = st.button("⟳  Process Latest Email", use_container_width=True, type="primary", key="process_btn")
with col_hint:
    st.markdown(
        '<div style="color:#3f4468;font-size:0.8rem;padding-top:0.7rem;">'
        'Fetches the most recent unread email and runs it through the agent pipeline.'
        '</div>',
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
            resp = requests.post(f"{API_BASE}/process-latest", timeout=60)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "no_email":
                st.markdown(
                    '<div class="alert-strip alert-indigo">📭&nbsp; No unread emails found in inbox.</div>',
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

    # ── Step 2 — Review / Draft ───────────────────────────────────────────────
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
                    resp = requests.post(f"{API_BASE}/review", json={
                        "thread_id": st.session_state.thread_id,
                        "approved": True,
                        "edited_response": edited,
                    }, timeout=30)
                    resp.raise_for_status()
                    result = resp.json()
                    st.session_state.draft_response = result.get("draft_response") or edited
                    st.session_state.review_done    = True
                    st.session_state.needs_review   = False
                    st.rerun()
                except requests.exceptions.HTTPError as e:
                    st.error(f"Review failed: {e.response.status_code} — {e.response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        if reject_btn:
            with st.spinner("Submitting rejection…"):
                try:
                    resp = requests.post(f"{API_BASE}/review", json={
                        "thread_id": st.session_state.thread_id,
                        "approved": False,
                        "edited_response": None,
                    }, timeout=30)
                    resp.raise_for_status()
                    st.session_state.draft_response = None
                    st.session_state.review_done    = True
                    st.session_state.needs_review   = False
                    st.rerun()
                except requests.exceptions.HTTPError as e:
                    st.error(f"Rejection failed: {e.response.status_code} — {e.response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

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
                '<div class="alert-strip alert-red">✕&nbsp; No draft available — email was rejected or the agent could not produce a reply.</div>',
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
            with st.spinner("Dispatching email via Gmail API…"):
                try:
                    resp = requests.post(f"{API_BASE}/send", json={"thread_id": st.session_state.thread_id}, timeout=30)
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

    # ── Sent confirmation ──────────────────────────────────────────────────────
    if st.session_state.sent:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sent-banner">
            <div class="sent-icon">🚀</div>
            <div>
                <div class="sent-title">Reply Sent Successfully</div>
                <div class="sent-sub">Email delivered via Gmail — thread closed.</div>
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