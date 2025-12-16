import streamlit as st
import time
from datetime import datetime

def show():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem;">🎭 Preset Personalities</h1>
        <p style="color: #64748b;">Choose from carefully
                 crafted writing styles</p>
    </div>
    """, unsafe_allow_html=True)

    # ===================== PERSONALITY DATA =====================
    PERSONALITIES = {
        "casual_friendly": {
            "name": "Casual Friendly",
            "icon": "😊",
            "desc": "Warm, conversational tone perfect for social media and personal messages.",
            "examples": ["Hey there!", "Just wanted to check in...", "So excited to share this!"],
            "best_for": ["Social media", "Personal emails", "Chat messages"]
        },
        "corporate_professional": {
            "name": "Corporate Professional",
            "icon": "💼",
            "desc": "Formal, polished language for business emails, reports, and presentations.",
            "examples": ["Per our discussion...", "Moving forward...", "To optimize results..."],
            "best_for": ["Business emails", "Reports", "Proposals"]
        },
        "formal_academic": {
            "name": "Formal Academic",
            "icon": "🎓",
            "desc": "Scholarly, precise writing suitable for research papers and academic work.",
            "examples": ["Upon examination...", "The literature suggests...", "It is concluded that..."],
            "best_for": ["Research papers", "Theses", "Academic articles"]
        },
        "motivational_speaker": {
            "name": "Motivational Speaker",
            "icon": "🚀",
            "desc": "Inspiring, energetic language to motivate and encourage teams or individuals.",
            "examples": ["Imagine a world...", "Together we can...", "Every challenge is..."],
            "best_for": ["Speeches", "Team motivation", "Inspirational posts"]
        }
    }

    # Layout
    col1, col2 = st.columns([1, 2])

    # ===================== LEFT SIDE =====================
    with col1:
        st.markdown("### 🎨 Choose Your Style")

        # Let Streamlit manage the radio state completely
        selected_key = st.radio(
            "Select a personality:",
            options=list(PERSONALITIES.keys()),
            format_func=lambda x: f"{PERSONALITIES[x]['icon']} {PERSONALITIES[x]['name']}",
            key="personality_selector"
        )
        
        personality = PERSONALITIES[selected_key]

        st.markdown(f"#### {personality['icon']} {personality['name']}")
        st.write(personality["desc"])

        st.markdown("**Best for:**")
        for item in personality["best_for"]:
            st.write(f"• {item}")

        st.markdown("**Example phrases:**")
        for ex in personality["examples"]:
            st.write(f"> *{ex}*")

        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        creativity = st.slider("Creativity Level", 0.0, 1.0, 0.7, key="creativity")
        max_length = st.slider("Max Length", 50, 500, 200, 50, key="max_length")

    # ===================== RIGHT SIDE =====================
    with col2:
        st.markdown("### ✍️ Write with Your Style")

        # Quick prompts - store the clicked prompt
        if "last_prompt" not in st.session_state:
            st.session_state.last_prompt = ""
        
        st.markdown("**💡 Quick Prompts:**")
        prompt_cols = st.columns(2)
        
        quick_prompts = [
            "Social media post for product launch",
            "Professional email to a client", 
            "Motivational message for the team",
            "Academic paper abstract"
        ]
        
        # Check which prompt was clicked
        clicked_prompt = None
        for i, prompt in enumerate(quick_prompts):
            with prompt_cols[i % 2]:
                if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
                    clicked_prompt = prompt
        
        # Text area - use clicked prompt if available, otherwise use current
        current_text = clicked_prompt if clicked_prompt else st.session_state.get("user_text", "")
        
        user_input = st.text_area(
            "What would you like to write about?",
            value=current_text,
            height=150,
            key="text_input"
        )
        
        # Store the text for next time
        st.session_state.user_text = user_input
        
        st.caption(f"📝 Characters: {len(user_input)}/500")
        st.markdown("---")
        
        # Generate button
        if st.button(f"✨ Generate with {personality['name']} Style", type="primary", key="generate"):
            if not user_input.strip():
                st.warning("⚠️ Please enter some text to generate.")
            else:
                with st.spinner(f"Writing in {personality['name']} style..."):
                    time.sleep(1.5)
                
                mock_responses = {
                    "casual_friendly": f"Hey there! Just wanted to drop a quick thank-you for '{user_input[:30]}...' Super appreciate it! 😊",
                    "corporate_professional": f"Dear Colleague, Regarding '{user_input[:30]}...', I recommend we proceed with the following action items.",
                    "formal_academic": f"This analysis of '{user_input[:30]}...' suggests several key findings warrant further examination.",
                    "motivational_speaker": f"Team! Let's talk about '{user_input[:30]}...' Every challenge is an opportunity! 🚀"
                }
                
                output = mock_responses.get(selected_key, f"Generated text about: {user_input[:50]}...")
                
                st.markdown("### 📝 Generated Output")
                st.success(output)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.download_button("📥 Download Text", data=output, 
                                     file_name=f"{personality['name'].replace(' ', '_')}_output.txt")
                with col2:
                    if st.button("📋 Copy", key="copy"):
                        st.success("📋 Copied!")