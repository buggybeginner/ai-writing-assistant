import streamlit as st
import time

def show():

    st.markdown("""<div class="home-hero">
<h1>PersonaWrite AI</h1>
<p>Write smarter. Match any style. Sound like yourself.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="home-container">
<h2>Transform Your Writing Instantly</h2>
<p style="color:#475569;">
PersonaWrite AI helps you generate high-quality content in different
writing styles — from casual messages to professional and academic writing.
</p>

<div class="home-card card-blue">
<h3>Preset Personalities</h3>
<p>Switch between professionally designed writing styles instantly.</p>
</div>

<div class="home-card card-pink">
<h3>Personal Style Learning</h3>
<p>Upload your own writing and let AI learn your unique tone.</p>
</div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Explore Preset Styles", use_container_width=True):
            st.session_state.pending_nav = "Preset Personalities"
            st.rerun()

    with col2:
        if st.button("Use My Writing Style", use_container_width=True):
            st.session_state.pending_nav = "Personal Style"
            st.rerun()

    st.markdown("### Quick Preview")

    prompt = st.text_input("Try a prompt:", "Write a birthday message")

    if st.button("Generate Preview", use_container_width=True):
        with st.spinner("Generating..."):
            time.sleep(1)

        st.markdown("""<div class="generated-output">
Happy Birthday! Wishing you a day filled with joy, laughter,
and all the things that make you smile. Have an amazing year ahead!
</div>""", unsafe_allow_html=True)

    st.markdown("""<div style="text-align:center; margin:2rem 0; color:#94a3b8;">
© 2024 PersonaWrite AI
</div>""", unsafe_allow_html=True)