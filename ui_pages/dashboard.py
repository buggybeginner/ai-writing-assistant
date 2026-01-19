import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    # ---------------- SAFE SESSION INIT ----------------
    if "generation_history" not in st.session_state:
        st.session_state.generation_history = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    # ---------------- HEADER ----------------
    st.markdown("""
        <div class="home-hero animate-fade-in">
            <h1 class="sidebar-title">📈 Dashboard</h1>
            <p class="sidebar-subtitle">
                Track your PersonaWrite AI activity and insights 📊✨
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- DATA ----------------
    history_data = st.session_state.generation_history
    total_gens = len(history_data)
    styles_used = len(set(item.get("personality", "General") for item in history_data)) if history_data else 0
    time_saved_val = total_gens * 15

    # ---------------- METRICS ----------------
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""<div class="dash-card dash-blue">
            <div class="dash-card-icon">📄</div>
            <div class="dash-card-value">{total_gens}</div>
            <div class="dash-card-label">Generated</div>
            </div>""",
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""<div class="dash-card dash-purple">
            <div class="dash-card-icon">🎨</div>
            <div class="dash-card-value">{styles_used}</div>
            <div class="dash-card-label">Styles</div>
            </div>""",
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""<div class="dash-card dash-orange">
            <div class="dash-card-icon">🕒</div>
            <div class="dash-card-value">{time_saved_val}m</div>
            <div class="dash-card-label">Time Saved</div>
            </div>""",
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            """<div class="dash-card dash-green">
            <div class="dash-card-icon">📈</div>
            <div class="dash-card-value">96%</div>
            <div class="dash-card-label">Success Rate</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- MAIN CONTENT ----------------
    col_left, col_right = st.columns([1.5, 1], gap="medium")

    # -------- Recent Generations --------
    with col_left:
        st.markdown("""
            <div class="preset-card">
            <h3 style="color:#1e293b; margin-bottom:1.5rem;">
                📄 Recent Generations
            </h3>
        """, unsafe_allow_html=True)

        if not history_data:
            st.write("No activity to display.")
        else:
            for item in reversed(history_data[-5:]):
                ts = item.get("timestamp")
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts)
                    except:
                        ts = None

                time_label = ts.strftime("%d %b %H:%M") if ts else "Recently"

                st.markdown(f"""
                    <div class="history-item">
                        <div class="history-content">
                            <div class="history-title">
                                {item.get("input","Untitled")[:40]}...
                            </div>
                            <div class="history-meta">
                                <span class="history-tag">
                                    {item.get("personality","General")}
                                </span>
                                <span class="history-time">
                                    {time_label}
                                </span>
                            </div>
                        </div>
                        <div class="check-badge">✓</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Popular Styles --------
    with col_right:
        st.markdown("""
            <div class="preset-card-highlight">
            <h3 style="color:#1e293b; margin-bottom:1.5rem;">
                ✨ Popular Styles
            </h3>
        """, unsafe_allow_html=True)

        style_counts = {}
        for item in history_data:
            style = item.get("personality", "General")
            style_counts[style] = style_counts.get(style, 0) + 1

        total = sum(style_counts.values()) or 1

        for style, count in style_counts.items():
            percent = int((count / total) * 100)
            st.markdown(f"""
                <div style="margin-bottom:1.2rem;">
                    <div style="display:flex; justify-content:space-between;
                        font-weight:700; font-size:0.85rem; margin-bottom:6px;">
                        <span>{style}</span>
                        <span>{percent}%</span>
                    </div>
                    <div class="progress-bg">
                        <div class="progress-fill" style="width:{percent}%;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="info-card-active" style="
                margin-top:1.5rem;
                background:linear-gradient(135deg,#8b5cf6,#ec4899);">
                <strong>⚡ Quick Tip</strong>
                <p style="font-size:0.8rem; margin:0;">
                    Try Style Learning for better accuracy!
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DATA MANAGEMENT ----------------
    st.markdown("<br><hr><h3 style='color:#1e293b;'>⚙️ Data Management</h3>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("🔄 Clear All History", use_container_width=True):
            st.session_state.generation_history.clear()
            st.session_state.uploaded_files.clear()
            st.success("History cleared!")
            st.rerun()

    with b2:
        if st.button("📊 Generate Report", use_container_width=True):
            if history_data:
                df = pd.DataFrame(history_data)
                st.download_button(
                    "⬇️ Download Report (CSV)",
                    df.to_csv(index=False),
                    "personawrite_report.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No data to generate report.")

    st.markdown("""
        <div class='page-footer'>
            ✨ PersonaWrite AI v2.0 • Dashboard Insights ✨
        </div>
    """, unsafe_allow_html=True)
