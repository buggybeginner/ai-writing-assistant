import streamlit as st
import time

def show():
    # ===================== HERO =====================
    st.markdown("""
    <div style="text-align: center; padding: 2.5rem 0;">
        <h1 style="
            font-size: 3rem;
            background: linear-gradient(90deg, #4f46e5, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">
            🎭 PersonaWrite AI
        </h1>
        <p style="
            font-size: 1.2rem;
            color: #64748b;
            max-width: 600px;
            margin: 0 auto;
        ">
            Write smarter. Match any style. Sound like yourself.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===================== MAIN SECTION =====================
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### ✨ Transform Your Writing Instantly

        PersonaWrite AI helps you generate high-quality content in different writing styles
        — from casual messages to professional and academic writing.

        **🎭 Preset Personalities**  
        Switch between professionally designed writing styles instantly.

        **👤 Personal Style Learning**  
        Upload your own writing and let AI learn your unique tone.

        **🌈 Style Blending**  
        Combine personal style with preset personalities.

        **⚡ Save Time**  
        Generate polished content in seconds.
        """)

        # CTA Buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Explore Preset Styles", use_container_width=True):
                st.session_state.pending_nav = "Preset Personalities"
                st.rerun()

        with col_b:
            if st.button("📁 Use My Writing Style", use_container_width=True):
                st.session_state.pending_nav = "Personal Style"
                st.rerun()

    with col2:
        st.markdown("### 🎬 Quick Preview")

        demo_text = st.text_input(
            "Try a quick prompt:",
            "Write a birthday message"
        )

        if st.button("✨ Generate Preview", use_container_width=True):
            with st.spinner("Creating your message..."):
                time.sleep(1.2)

            st.success(
                "Happy Birthday! 🎉 Wishing you a day filled with joy, laughter, "
                "and all the things that make you smile. Have an amazing year ahead!"
            )

    # ===================== FEATURES =====================
    st.markdown("---")
    st.markdown("## 🚀 Why PersonaWrite AI?")

    features = [
        ("🎯", "Style Accuracy", "Maintains tone consistency across generations"),
        ("🔒", "Privacy First", "Your writing stays on your system"),
        ("⚡", "Fast Generation", "Results in seconds"),
        ("📱", "Responsive Design", "Works on all screen sizes"),
        ("🔄", "Real-time Preview", "Instant feedback as you write"),
        ("🧠", "Adaptive Learning", "Improves with your usage")
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 1rem;
                border: 1px solid #e2e8f0;
                margin-bottom: 1rem;
                border-left: 4px solid #4f46e5;
            ">
                <div style="font-size: 2rem;">{icon}</div>
                <h4 style="margin: 0.5rem 0;">{title}</h4>
                <p style="color: #64748b; font-size: 0.9rem;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ===================== FOOTER =====================
    st.markdown("""
    <div style="
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 1.5rem 0;
    ">
        © 2024 PersonaWrite AI
    </div>
    """, unsafe_allow_html=True)
