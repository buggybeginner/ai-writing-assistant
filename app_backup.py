import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys

# Add the pages directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="PersonaWrite AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== SESSION STATE =====================
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "generation_history" not in st.session_state:
    st.session_state.generation_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = "casual_friendly"

# ===================== CUSTOM CSS =====================
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        # Fallback basic CSS
        st.markdown("""
        <style>
        .main-header { text-align: center; padding: 2rem 0; }
        .feature-card { 
            background: white; padding: 1.5rem; border-radius: 10px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 1rem 0;
            border-left: 4px solid #4f46e5;
        }
        </style>
        """, unsafe_allow_html=True)

# ===================== SIDEBAR NAVIGATION =====================
def show_sidebar():
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 1.8rem; margin: 0;">🎭 PersonaWrite AI</h1>
            <p style="color: #64748b; margin: 0;">Final Year Project</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Preset Personalities", "Personal Style", "Dashboard"],
            icons=["house", "palette", "person", "bar-chart"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "#f59e0b", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px 0",
                    "border-radius": "8px",
                    "padding": "10px 15px"
                },
                "nav-link-selected": {
                    "background-color": "#4f46e5",
                    "color": "white"
                },
            }
        )
        
        st.markdown("---")
        
        # User info
        st.markdown("### 👤 User Info")
        if st.session_state.user_id:
            st.success(f"Welcome, {st.session_state.user_name}!")
        else:
            st.info("Guest Mode")
            if st.button("🆔 Sign In (Demo)"):
                st.session_state.user_id = "demo_user"
                st.session_state.user_name = "Demo User"
                st.success("Signed in as Demo User!")
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Generations", len(st.session_state.generation_history))
        with col2:
            st.metric("Files", len(st.session_state.uploaded_files))
        
        st.markdown("---")
        
        # Team info
        st.markdown("""
        <div style="font-size: 0.85rem; color: #64748b;">
        <strong>👥 Team:</strong><br>
        • Person A: Backend/AI<br>
        • Person B: Frontend/UX<br>
        <strong>🎓 FYP Status:</strong> Development
        </div>
        """, unsafe_allow_html=True)
        
        return selected

# ===================== PAGE ROUTING =====================
def main():
    # Load CSS
    load_css()
    
    # Get selected page from sidebar
    selected_page = show_sidebar()
    
    # Route to the appropriate page module
    try:
        if selected_page == "Home":
            from pages.home import show
            show()
        elif selected_page == "Preset Personalities":
            from pages.preset import show
            show()
        elif selected_page == "Personal Style":
            from pages.personal import show
            show()
        elif selected_page == "Dashboard":
            from pages.dashboard import show
            show()
        else:
            st.error("Page not found!")
    except ImportError as e:
        st.error(f"Module import error: {e}")
        st.info("Please make sure all page modules are created in the 'pages/' directory")
    except Exception as e:
        st.error(f"Error loading page: {e}")
    
    # Global footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
        <p>🎭 <strong>PersonaWrite AI - Intelligent Writing Assistant</strong></p>
        <p>✅ Frontend: Complete | ⚙️ Backend: Integration Pending</p>
        <p>📧 Contact: personb@university.edu | 📱 Version: 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()