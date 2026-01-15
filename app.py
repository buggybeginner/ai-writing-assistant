import streamlit as st
import os
import sys
import base64

# --------------------- PATHS ---------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "assets", "icons")
sys.path.append(os.path.join(BASE_DIR, "ui_pages"))

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="PersonaWrite AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------- SESSION STATE ---------------------
if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Home"

# --------------------- LOAD CSS ---------------------
def load_css():
    with open(os.path.join(BASE_DIR, "assets", "styles.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------- SVG TO BASE64 ---------------------
def svg_to_base64(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"

# --------------------- SIDEBAR ---------------------
def show_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">PersonaWrite</div>
            <div class="sidebar-subtitle">AI Writing Assistant ✨</div>
            <div class="sidebar-nav">
            """,
            unsafe_allow_html=True,
        )

        def nav_item(label, icon):
            is_active = st.session_state.nav_selection == label
            active_class = "active" if is_active else ""
            icon_src = svg_to_base64(os.path.join(ICON_DIR, icon))

            # VISUAL CONTAINER
            st.markdown(
                f"""
                <div class="sidebar-btn {active_class}">
                    <img src="{icon_src}">
                """,
                unsafe_allow_html=True,
            )

            # CLICKABLE BUTTON (STREAMLIT CONTROLLED)
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state.nav_selection = label
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        nav_item("Home", "home.svg")
        nav_item("Preset Personalities", "preset.svg")
        nav_item("Personal Style", "personal.svg")
        nav_item("Dashboard", "dashboard.svg")

        st.markdown(
            """
            </div>
            <div class="sidebar-footer">✨ Powered by AI ✨</div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.nav_selection


# --------------------- MAIN ROUTER ---------------------
def main():
    load_css()
    page = show_sidebar()

    if page == "Home":
        from ui_pages.home import show
        show()

    elif page == "Preset Personalities":
        from ui_pages.preset import show
        show()

    elif page == "Personal Style":
        from ui_pages.personal import show
        show()

    elif page == "Dashboard":
        from ui_pages.dashboard import show
        show()

if __name__ == "__main__":
    main()
