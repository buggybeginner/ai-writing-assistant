import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    # ---------------- HEADER ----------------
    st.markdown("""
        <div class="home-hero animate-fade-in">
            <h1 class="sidebar-title">📈 Dashboard</h1>
            <p class="sidebar-subtitle">Track your PersonaWrite AI activity and insights 📊✨</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- TOP METRICS GRID ----------------
    # Logic to fetch real stats from session state
    history_data = st.session_state.get('generation_history', [])
    total_gens = len(history_data)
    styles_used = len(set([g.get('personality', '') for g in history_data])) if history_data else 0
    time_saved_val = total_gens * 15 # mock calculation
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""<div class="dash-card dash-blue"><div class="dash-card-icon">📄</div><div class="dash-card-value">{total_gens}</div><div class="dash-card-label">Generated</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="dash-card dash-purple"><div class="dash-card-icon">🎨</div><div class="dash-card-value">{styles_used}</div><div class="dash-card-label">Styles</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="dash-card dash-orange"><div class="dash-card-icon">🕒</div><div class="dash-card-value">{time_saved_val}m</div><div class="dash-card-label">Time Saved</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="dash-card dash-green"><div class="dash-card-icon">📈</div><div class="dash-card-value">96%</div><div class="dash-card-label">Success Rate</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- MAIN CONTENT AREA ----------------
    col_left, col_right = st.columns([1.5, 1], gap="medium")

    with col_left:
        st.markdown("""<div class="preset-card"><h3 style="color: #1e293b; margin-bottom: 1.5rem;">📄 Recent Generations</h3>""", unsafe_allow_html=True)
        
        if not history_data:
            st.write("No activity to display.")
        else:
            for item in reversed(history_data[-5:]): # Show last 5
                st.markdown(f"""
                    <div class="history-item">
                        <div class="history-content">
                            <div class="history-title">{item.get('input', 'Untitled')[:40]}...</div>
                            <div class="history-meta">
                                <span class="history-tag">{item.get('personality', 'General')}</span> 
                                <span class="history-time">Just now</span>
                            </div>
                        </div>
                        <div class="check-badge" style="width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">✓</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""<div class="preset-card-highlight"><h3 style="color: #1e293b; margin-bottom: 1.5rem;">✨ Popular Styles</h3>""", unsafe_allow_html=True)
        
        # Static mock for UI perfection
        styles = [
            {"label": "Casual Friendly", "val": 45, "color": "#06b6d4"},
            {"label": "Corporate Professional", "val": 30, "color": "#6366f1"},
            {"label": "Personal Style", "val": 15, "color": "#a855f7"}
        ]

        for s in styles:
            st.markdown(f"""
                <div style="margin-bottom: 1.2rem;">
                    <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.85rem; margin-bottom:6px; color:#1e293b;">
                        <span>{s['label']}</span><span>{s['val']}%</span>
                    </div>
                    <div class="progress-bg"><div class="progress-fill" style="width: {s['val']}%; background: {s['color']};"></div></div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div class="info-card-active" style="margin-top: 1.5rem; background: linear-gradient(135deg, #8b5cf6, #ec4899);"><strong>⚡ Quick Tip</strong><p style="font-size:0.8rem; margin:0; opacity:0.9;">Try Style Learning for better accuracy!</p></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DATA MANAGEMENT (FIXED BUTTONS) ----------------
    st.markdown("<br><hr><h3 style='color: #1e293b;'>⚙️ Data Management</h3>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        # Fixed Clear History Button
        if st.button("🔄 Clear All History", use_container_width=True, key="clear_history_btn"):
            st.session_state.generation_history = []
            st.session_state.uploaded_files = [] # Clearing associated files too
            st.success("History cleared!")
            st.rerun()
            
    with btn_col2:
        # Fixed Generate Report Button (Enabled)
        if st.button("📊 Generate Report", use_container_width=True, key="gen_report_btn"):
            st.balloons()
            st.info("Report generated successfully! (Mock Action)")

    st.markdown("<div class='page-footer'>✨ PersonaWrite AI v2.0 • Dashboard Insights ✨</div>", unsafe_allow_html=True)