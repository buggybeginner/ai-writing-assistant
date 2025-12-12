import streamlit as st
import time

def show():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem;">👤 Personal Style Learning</h1>
        <p style="color: #64748b;">Train AI to write exactly like you</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step tracker
    st.markdown("### 📋 Process Overview")
    steps = ["Upload Files", "Style Analysis", "Profile Creation", "Generate in Your Style"]
    current_step = 0
    
    cols = st.columns(4)
    for idx, step in enumerate(steps):
        with cols[idx]:
            if idx < current_step:
                status = "✅"
                color = "#10b981"
            elif idx == current_step:
                status = "⏳"
                color = "#f59e0b"
            else:
                status = f"{idx+1}"
                color = "#cbd5e1"
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: {color};
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 0.5rem;
                    color: white;
                    font-weight: bold;
                ">
                    {status}
                </div>
                <div style="font-size: 0.9rem;">{step}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.progress(0.25)
    
    # File upload section
    st.markdown("---")
    st.markdown("### 📁 Step 1: Upload Your Writing Samples")
    
    uploaded_files = st.file_uploader(
        "Upload text files (.txt), documents (.docx), or PDFs",
        type=['txt', 'pdf', 'docx'],
        accept_multiple_files=True,
        help="Upload emails, essays, chat exports - anything you've written!"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} files!")
        
        # File preview
        for file in uploaded_files[:3]:  # Show first 3
            with st.expander(f"📄 {file.name}"):
                try:
                    content = file.read().decode("utf-8")
                    st.text_area("Preview:", content[:500] + ("..." if len(content) > 500 else ""), 
                                height=150, disabled=True, key=f"preview_{file.name}")
                except:
                    st.info("Preview not available for this file type")
        
        if len(uploaded_files) > 3:
            st.info(f"... and {len(uploaded_files) - 3} more files")
        
        # Analysis section
        st.markdown("---")
        st.markdown("### 🧠 Step 2: Analyze Your Writing Style")
        
        if st.button("🚀 Analyze My Writing Patterns", type="primary", use_container_width=True):
            with st.spinner("Analyzing vocabulary, sentence structure, and writing patterns..."):
                time.sleep(3)
                
                # Mock analysis results
                st.markdown("#### 📊 Your Writing Fingerprint")
                
                metrics_cols = st.columns(4)
                metrics = [
                    ("Formality", "72%", "+12% from average"),
                    ("Sentence Length", "18 words", "Medium"),
                    ("Emotional Tone", "Positive", "😊"),
                    ("Vocabulary", "High", "Diverse word choice")
                ]
                
                for idx, (title, value, delta) in enumerate(metrics):
                    with metrics_cols[idx]:
                        st.metric(title, value, delta)
                
                # Style features
                st.markdown("#### ✨ Detected Style Features")
                features = [
                    "Prefers conversational tone",
                    "Uses emojis frequently 😊",
                    "Direct communication style",
                    "Medium sentence complexity",
                    "Active voice preference",
                    "Frequent use of contractions"
                ]
                
                for feature in features:
                    st.write(f"• {feature}")
                
                st.success("✅ Personal style profile created! You can now generate text that sounds like YOU.")
                
                # Update progress
                current_step = 2
                st.progress(0.75)
        
        # Generate in personal style
        st.markdown("---")
        st.markdown("### ✍️ Step 3: Generate in YOUR Style")
        
        personal_prompt = st.text_area(
            "What should I write in YOUR style?",
            "Write a message to a friend about weekend plans...",
            height=100,
            key="personal_prompt"
        )
        
        if st.button("🖋️ Write Like Me", use_container_width=True):
            with st.spinner("Channeling your unique writing voice..."):
                time.sleep(2)
                
                st.markdown("""
                <div style="
                    background: #f0f9ff;
                    padding: 1.5rem;
                    border-radius: 0.75rem;
                    border-left: 4px solid #0ea5e9;
                    margin: 1rem 0;
                ">
                    <strong>Generated in your personal style:</strong><br><br>
                    "Hey! So I was thinking about the weekend and honestly, 
                    it's a really good time to relax and have some fun. 
                    The way I see it, we should just go for it and see what happens. 
                    What do you think? 😊"
                </div>
                """, unsafe_allow_html=True)
                
                # Update progress
                current_step = 3
                st.progress(1.0)
                st.balloons()
    
    else:
        st.info("👆 Upload your writing samples to create your personal AI writing twin!")
        
        # Example files suggestion
        with st.expander("💡 What kind of files should I upload?"):
            st.markdown("""
            **Best files for style analysis:**
            
            • **Emails** - Both personal and professional
            • **Essays/Reports** - Academic or work-related
            • **Chat exports** - WhatsApp, Telegram, or Messenger conversations
            • **Social media posts** - Facebook, Twitter, Instagram
            • **Blog posts/articles** - If you have any published content
            
            **Tips:**
            - The more text, the better the analysis
            - Mix different types of writing for comprehensive style capture
            - Minimum recommended: 2,000+ words total
            """)