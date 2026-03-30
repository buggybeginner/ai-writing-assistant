import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import json
import os

HISTORY_FILE = "data/history.json"

def load_history_from_file():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def show():
    # ---------------- SAFE SESSION INIT ----------------
    if "generation_history" not in st.session_state:
        st.session_state.generation_history = load_history_from_file()

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "selected_entries" not in st.session_state:
        st.session_state.selected_entries = []

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
        st.markdown(f"""<div class="dash-card dash-blue">
        <div class="dash-card-icon">📄</div>
        <div class="dash-card-value">{total_gens}</div>
        <div class="dash-card-label">Generated</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="dash-card dash-purple">
        <div class="dash-card-icon">🎨</div>
        <div class="dash-card-value">{styles_used}</div>
        <div class="dash-card-label">Styles</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="dash-card dash-orange">
        <div class="dash-card-icon">🕒</div>
        <div class="dash-card-value">{time_saved_val}m</div>
        <div class="dash-card-label">Time Saved</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown("""<div class="dash-card dash-green">
        <div class="dash-card-icon">📈</div>
        <div class="dash-card-value">96%</div>
        <div class="dash-card-label">Success Rate</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= 📈 MATURITY TREND =================
    if history_data:
        st.markdown("### 🧬 Writing Maturity Trend")

        df = pd.DataFrame(history_data)

        if "maturity_score" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.sort_values("timestamp")

            st.line_chart(df.set_index("timestamp")["maturity_score"])

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
                    <div style="display:flex; justify-content:space-between;">
                        <span>{style}</span>
                        <span>{percent}%</span>
                    </div>
                    <div class="progress-bg">
                        <div class="progress-fill" style="width:{percent}%;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= ENTRY SELECTION =================
    if history_data:
        options = [
            f"{i+1}. {item.get('input','Untitled')[:50]}"
            for i, item in enumerate(history_data)
        ]

        selected_labels = st.multiselect(
            "📌 Select entries to include in report",
            options
        )

        selected_entries = []

        for label in selected_labels:
            index = int(label.split(".")[0]) - 1
            selected_entries.append(history_data[index])

        st.session_state.selected_entries = selected_entries

    # ---------------- DATA MANAGEMENT ----------------
    st.markdown("<br><hr><h3 style='color:#1e293b;'>⚙️ Data Management</h3>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("🔄 Clear All History", use_container_width=True):
            st.session_state.generation_history.clear()
            st.session_state.uploaded_files.clear()
            st.session_state.selected_entries = []
            st.success("History cleared!")
            st.rerun()

    with b2:
        if st.button("📊 Generate Report", use_container_width=True):

            selected_entries = st.session_state.selected_entries

            if selected_entries:

                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                doc = SimpleDocTemplate(tmp_file.name)
                elements = []

                styles = getSampleStyleSheet()
                normal = styles["Normal"]
                title_style = styles["Heading1"]
                subtitle_style = styles["Heading3"]

                elements.append(Paragraph("PersonaWrite AI - Selected Report", title_style))
                elements.append(Spacer(1, 0.3 * inch))

                for idx, item in enumerate(selected_entries, start=1):

                    output_data = item.get("output", {})

                    preset_answer = output_data.get("preset", "")
                    personal_answer = output_data.get("personal", "")

                    elements.append(Paragraph(f"Entry {idx}", subtitle_style))
                    elements.append(Spacer(1, 0.15 * inch))

                    elements.append(Paragraph(f"<b>Question:</b> {item.get('input','')}", normal))
                    elements.append(Spacer(1, 0.15 * inch))

                    elements.append(Paragraph(f"<b>Preset Style:</b> {item.get('personality','')}", normal))
                    elements.append(Spacer(1, 0.15 * inch))

                    # ✅ NEW: MATURITY SCORE
                    elements.append(Paragraph(
                        f"<b>Maturity Score:</b> {item.get('maturity_score','N/A')}/100",
                        normal
                    ))
                    elements.append(Spacer(1, 0.2 * inch))

                    elements.append(Paragraph("<b>Preset Answer:</b>", normal))
                    elements.append(Spacer(1, 0.1 * inch))
                    elements.append(Paragraph(preset_answer.replace("\n", "<br/>"), normal))
                    elements.append(Spacer(1, 0.25 * inch))

                    elements.append(Paragraph("<b>Personal Answer:</b>", normal))
                    elements.append(Spacer(1, 0.1 * inch))
                    elements.append(Paragraph(personal_answer.replace("\n", "<br/>"), normal))
                    elements.append(Spacer(1, 0.25 * inch))

                    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
                    elements.append(Spacer(1, 0.4 * inch))

                doc.build(elements)

                with open(tmp_file.name, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ Download Selected PDF Report",
                        pdf_file,
                        "personawrite_selected_report.pdf",
                        "application/pdf",
                        use_container_width=True
                    )

            else:
                st.warning("Please select at least one entry.")