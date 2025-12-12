import streamlit as st
import time

def show():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; background: linear-gradient(90deg, #4f46e5, #0ea5e9); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎭 PersonaWrite AI
        </h1>
        <p style="font-size: 1.2rem; color: #64748b; max-width: 600px; margin: 0 auto;">
            Your Intelligent Writing Style Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### ✨ Transform Your Writing
        
        PersonaWrite AI helps you write in any style instantly:
        
        **🎭 Preset Personalities** - Switch between 8+ carefully crafted writing styles
        
        **👤 Personal Style Learning** - AI learns your unique writing patterns
        
        **🌈 Hybrid Blending** - Mix personal and preset styles creatively
        
        **⚡ Time Saver** - Generate high-quality content in seconds
        """)
        
        # Quick Start Buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Start with Presets", use_container_width=True):
                st.session_state.page = "preset"
                st.rerun()
        with col_b:
            if st.button("📁 Upload My Style", use_container_width=True):
                st.session_state.page = "personal"
                st.rerun()
    
    with col2:
        # Status Panel
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 1rem; 
                    border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0;">✅ System Status</h3>
            <p>🎯 <strong>Frontend:</strong> Active (Person B)</p>
            <p>⚙️ <strong>Backend:</strong> Ready for Integration</p>
            <p>📊 <strong>Pages:</strong> 4 / 4 Complete</p>
            <p>🎨 <strong>UI Components:</strong> 15+</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Demo
        st.markdown("### 🎬 Quick Demo")
        demo_text = st.text_input("Try a prompt:", "Write a birthday message")
        
        if st.button("✨ Generate Demo", use_container_width=True):
            with st.spinner("Creating your message..."):
                time.sleep(1.5)
                st.success("""
                **Generated (Friendly Style):**
                
                "Happy Birthday! 🎉 Wishing you a day as amazing as you are! 
                Hope it's filled with joy, laughter, and all your favorite things."
                """)
    
    # Features Grid
    st.markdown("---")
    st.markdown("## 🔥 Core Features")
    
    features = [
        {"icon": "🚀", "title": "Fast Setup", "desc": "Get started in under 5 minutes"},
        {"icon": "🎯", "title": "High Accuracy", "desc": "85%+ style matching in tests"},
        {"icon": "🔒", "title": "Privacy First", "desc": "Your data never leaves your device"},
        {"icon": "📈", "title": "Continuous Learning", "desc": "Improves with every interaction"},
        {"icon": "📱", "title": "Mobile Ready", "desc": "Responsive design for all devices"},
        {"icon": "🔄", "title": "Real-time Preview", "desc": "See changes as you make them"}
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: white; 
                padding: 1.5rem; 
                border-radius: 1rem;
                border: 1px solid #e2e8f0;
                margin: 0.5rem 0;
                border-left: 4px solid #4f46e5;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feature['icon']}</div>
                <h4 style="margin: 0 0 0.5rem 0;">{feature['title']}</h4>
                <p style="color: #64748b; margin: 0; font-size: 0.9rem;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
        <p>🎓 <strong>PersonaWrite AI - Final Year Project</strong></p>
        <p>👥 <strong>Team:</strong> Person A (Backend/AI) | Person B (Frontend/UX)</p>
    </div>
    """, unsafe_allow_html=True)