import streamlit as st
import os
import sys

# Add ui_pages to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "ui_pages"))

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(
    page_title="PersonaWrite AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------- SESSION DEFAULTS ---------------------
defaults = {
    "user_id": None,
    "user_name": "Guest",
    "generation_history": [],
    "uploaded_files": [],
    "selected_personality": "casual_friendly",
    "nav_selection": "Home",     # <- the ONLY navigation variable
    "pending_nav": None          # <- used by buttons
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

# --------------------- LOAD CSS ---------------------
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

# --------------------- SIDEBAR ---------------------
def show_sidebar():
    # 🔥 Handle home-page button-click navigation
    if st.session_state.pending_nav:
        st.session_state.nav_selection = st.session_state.pending_nav
        st.session_state.pending_nav = None

    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 1.8rem; margin: 0;">🎭 PersonaWrite AI</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        pages = ["Home", "Preset Personalities", "Personal Style", "Dashboard"]

        selected = st.radio(
            "Navigation",
            pages,
            index=pages.index(st.session_state.nav_selection),
            key="nav_selection"  # <-- THIS MUST NEVER BE MODIFIED IN OTHER FILES
        )

        return selected

# --------------------- MAIN ROUTER ---------------------
def main():
    load_css()
    selected_page = show_sidebar()

    try:
        if selected_page == "Home":
            from ui_pages.home import show
            show()

        elif selected_page == "Preset Personalities":
            from ui_pages.preset import show
            show()

        elif selected_page == "Personal Style":
            from ui_pages.personal import show
            show()

        elif selected_page == "Dashboard":
            from ui_pages.dashboard import show
            show()

    except Exception as e:
        st.error(f"Error loading page: {e}")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
        🎭 <strong>PersonaWrite AI</strong><br>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
