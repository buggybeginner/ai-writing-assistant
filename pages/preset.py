import streamlit as st
import time
from datetime import datetime

def show():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem;">🎭 Preset Personalities</h1>
        <p style="color: #64748b;">Choose from carefully crafted writing styles</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Personality Database
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
    
    # Two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎨 Choose Your Style")
        
        # Personality selection
        selected_key = st.radio(
            "Select a personality:",
            options=list(PERSONALITIES.keys()),
            format_func=lambda x: f"{PERSONALITIES[x]['icon']} {PERSONALITIES[x]['name']}",
            key="personality_selector"
        )
        
        personality = PERSONALITIES[selected_key]
        
        # Display details
        st.markdown(f"#### {personality['icon']} {personality['name']}")
        st.write(personality['desc'])
        
        st.markdown("**Best for:**")
        for use_case in personality['best_for']:
            st.write(f"• {use_case}")
        
        st.markdown("**Example phrases:**")
        for example in personality['examples']:
            st.write(f"> *{example}*")
        
        # Settings
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        creativity = st.slider("Creativity Level", 0.0, 1.0, 0.7, 
                             help="Lower = more predictable, Higher = more creative")
        max_length = st.slider("Max Length", 50, 500, 200, 50)
    
    with col2:
        st.markdown("### ✍️ Write with Your Style")
        
        # Text input
        user_input = st.text_area(
            "What would you like to write about?",
            "Write an email to a colleague thanking them for their help...",
            height=150,
            key="preset_input"
        )
        
        # Character counter
        st.caption(f"📝 Characters: {len(user_input)}/500")
        
        # Quick prompts
        st.markdown("**💡 Quick Prompts:**")
        quick_cols = st.columns(2)
        quick_prompts = [
            "Social media post for product launch",
            "Professional email to a client",
            "Motivational message for the team",
            "Academic paper abstract"
        ]
        
        for idx, prompt in enumerate(quick_prompts):
            with quick_cols[idx % 2]:
                if st.button(prompt, use_container_width=True):
                    st.session_state.preset_input = prompt
                    st.rerun()
        
        # Generation button
        generate_clicked = st.button(
            f"✨ Generate with {personality['name']} Style", 
            type="primary", 
            use_container_width=True
        )
        
        if generate_clicked and user_input.strip():
            with st.spinner(f"Writing in {personality['name']} style..."):
                time.sleep(2)
                
                # Mock responses
                responses = {
                    "casual_friendly": f"Hey! I just wanted to say a huge thanks for helping out with that project. Your ideas were seriously awesome and made everything so much smoother. Let's grab coffee soon to chat more about it! 😊",
                    "corporate_professional": f"Dear Colleague, Please accept my sincere gratitude for your valuable assistance with the recent project. Your contributions were instrumental in achieving our objectives, and I look forward to future collaboration.",
                    "formal_academic": f"This correspondence serves to acknowledge and express gratitude for your scholarly contributions to the aforementioned project. Your expertise proved invaluable to the research outcomes and methodological rigor.",
                    "motivational_speaker": f"Your help on this project was incredible! You showed up, gave your best, and together we achieved something amazing. Remember, this is how winning teams are built - by lifting each other up!"
                }
                
                generated = responses.get(selected_key, f"Generated text in {personality['name']} style.")
                
                # Display output
                st.markdown("---")
                st.markdown("### 📝 Generated Output")
                
                st.markdown(f"""
                <div style="
                    background: #f0f9ff;
                    padding: 1.5rem;
                    border-radius: 0.75rem;
                    border-left: 4px solid #0ea5e9;
                    margin: 1rem 0;
                ">
                    {generated}
                </div>
                """, unsafe_allow_html=True)
                
                # Output controls
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.download_button(
                        "📥 Download Text",
                        data=generated,
                        file_name=f"{personality['name'].replace(' ', '_')}_output.txt",
                        mime="text/plain"
                    )
                with col_b:
                    if st.button("📋 Copy"):
                        st.toast("Copied to clipboard!", icon="✅")
                
                # Add to history
                if "generation_history" not in st.session_state:
                    st.session_state.generation_history = []
                
                st.session_state.generation_history.append({
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "personality": personality['name'],
                    "input": user_input[:100] + ("..." if len(user_input) > 100 else user_input),
                    "output": generated[:150] + ("..." if len(generated) > 150 else generated)
                })
        
        elif not user_input.strip():
            st.warning("⚠️ Please enter some text to generate")
        
        # Show recent history
        if "generation_history" in st.session_state and st.session_state.generation_history:
            st.markdown("---")
            st.markdown("### 📜 Recent Generations")
            
            for idx, item in enumerate(list(reversed(st.session_state.generation_history))[:3]):
                with st.expander(f"{item['personality']} - {item['timestamp']}"):
                    st.write(f"**Input:** {item['input']}")
                    st.write(f"**Output:** {item['output']}")