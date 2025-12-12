import streamlit as st
import time
from datetime import datetime
import json

def show_loading(message="Processing...", icon="⏳"):
    """Display an elegant loading indicator with icon"""
    with st.spinner(f"{icon} {message}"):
        time.sleep(0.5)

def success_toast(message, duration=3):
    """Show a temporary success message"""
    toast = st.success(f"✅ {message}")
    time.sleep(duration)
    toast.empty()

def personality_card(name, description, icon="🎭", is_selected=False, key=None):
    """Create a selectable personality card component"""
    
    # Determine styling based on selection
    border_color = "#4f46e5" if is_selected else "#e2e8f0"
    bg_color = "#eff6ff" if is_selected : "#ffffff"
    shadow = "0 4px 6px -1px rgba(79, 70, 229, 0.2)" if is_selected else "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    
    # Create the card HTML
    card_html = f"""
    <div class="personality-card" style="
        border: 2px solid {border_color};
        background: {bg_color};
        box-shadow: {shadow};
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin: 0.75rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1rem;
    ">
        <div style="
            font-size: 1.5rem;
            width: 3rem;
            height: 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
            border-radius: 0.5rem;
        ">
            {icon}
        </div>
        <div style="flex: 1;">
            <h4 style="margin: 0 0 0.25rem 0; color: #1e293b;">{name}</h4>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">{description}</p>
        </div>
        {f'<div style="color: #4f46e5; font-size: 1.2rem;">✓</div>' if is_selected else ''}
    </div>
    """
    
    # Use Streamlit's button to make it clickable
    clicked = st.button("", key=key or name)
    st.markdown(card_html, unsafe_allow_html=True)
    
    return clicked

def text_area_with_counter(label, key, max_chars=1000, height=200, placeholder="Type here..."):
    """Enhanced text area with character counter"""
    
    # Create the text area
    text = st.text_area(label, key=key, height=height, placeholder=placeholder, 
                       help=f"Maximum {max_chars} characters")
    
    # Calculate metrics
    chars = len(text)
    words = len(text.split())
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    
    # Display counters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📝 **Characters:** {chars}/{max_chars}")
    with col2:
        st.caption(f"📖 **Words:** {words}")
    with col3:
        st.caption(f"📑 **Paragraphs:** {paragraphs}")
    
    # Warning if limit exceeded
    if chars > max_chars:
        st.error(f"⚠️ Exceeds limit by {chars - max_chars} characters")
    
    return text

def progress_tracker(steps, current_step, title="Progress"):
    """Visual progress tracker for multi-step processes"""
    
    st.markdown(f"**{title}**")
    
    # Create progress HTML
    progress_html = """
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1.5rem 0;
        position: relative;
    ">
    """
    
    # Add connector lines
    progress_html += """
    <div style="
        position: absolute;
        top: 20px;
        left: 20px;
        right: 20px;
        height: 3px;
        background: #e2e8f0;
        z-index: 1;
    "></div>
    """
    
    for i, step in enumerate(steps):
        if i < current_step:
            # Completed step
            status = "✅"
            bg_color = "#10b981"
            text_color = "#10b981"
            border_color = "#10b981"
        elif i == current_step:
            # Current step
            status = "⏳"
            bg_color = "#f59e0b"
            text_color = "#f59e0b"
            border_color = "#f59e0b"
        else:
            # Future step
            status = f"{i+1}"
            bg_color = "#ffffff"
            text_color = "#94a3b8"
            border_color = "#cbd5e1"
        
        progress_html += f"""
        <div style="
            text-align: center;
            flex: 1;
            position: relative;
            z-index: 2;
        ">
            <div style="
                width: 40px;
                height: 40px;
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 0.5rem;
                color: white;
                font-weight: bold;
                font-size: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                {status}
            </div>
            <span style="
                color: {text_color};
                font-size: 0.85rem;
                font-weight: 500;
            ">{step}</span>
        </div>
        """
    
    progress_html += "</div>"
    
    # Display the tracker
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Add a progress bar
    progress_percent = (current_step + 1) / len(steps)
    st.progress(progress_percent)
    
    return current_step

def file_upload_widget(allowed_types=['txt', 'pdf', 'docx'], max_files=10):
    """Enhanced file upload widget with preview"""
    
    uploaded_files = st.file_uploader(
        "📁 Upload your writing samples",
        type=allowed_types,
        accept_multiple_files=True,
        help=f"Supported formats: {', '.join(allowed_types)}. Max {max_files} files."
    )
    
    if uploaded_files:
        # Display file summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", len(uploaded_files))
        with col2:
            total_size = sum(f.size for f in uploaded_files) / 1024
            st.metric("Total Size", f"{total_size:.1f} KB")
        with col3:
            st.metric("Status", "✅ Ready")
        
        # File details in expanders
        for idx, file in enumerate(uploaded_files[:5]):  # Show first 5
            with st.expander(f"📄 {file.name} ({file.type})"):
                try:
                    if file.type == "text/plain":
                        content = file.read().decode("utf-8")
                        st.text_area("Preview:", content[:500] + ("..." if len(content) > 500 else ""), 
                                    height=150, disabled=True)
                        file.seek(0)  # Reset file pointer
                    else:
                        st.info(f"Binary file preview not available for {file.type}")
                except Exception as e:
                    st.warning(f"Could not preview file: {str(e)}")
        
        if len(uploaded_files) > 5:
            st.info(f"... and {len(uploaded_files) - 5} more files")
    
    return uploaded_files

def generation_history_view(history_list, max_items=5):
    """Display generation history in a clean format"""
    
    if not history_list:
        st.info("📭 No generation history yet. Create some content!")
        return
    
    st.markdown(f"### 📜 Recent Activity (Last {min(len(history_list), max_items)})")
    
    for idx, item in enumerate(list(reversed(history_list))[:max_items]):
        with st.expander(f"{item.get('personality', 'Unknown')} - {item.get('timestamp', '')}", 
                        expanded=idx==0):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Input:** {item.get('input', 'No input')}")
                st.write(f"**Output:** {item.get('output', 'No output')}")
            with col2:
                if st.button("🔄 Reuse", key=f"reuse_{idx}"):
                    st.session_state.last_prompt = item.get('input', '')
                    st.success("Prompt loaded!")
                    st.rerun()

def style_visualization(metrics_dict):
    """Create visual representation of writing style metrics"""
    
    st.markdown("### 📊 Your Writing Fingerprint")
    
    # Display metrics in a grid
    cols = st.columns(4)
    metrics = [
        ("Formality", metrics_dict.get('formality_score', 0), "%"),
        ("Complexity", metrics_dict.get('sentence_complexity_score', 0), "/10"),
        ("Emotion", metrics_dict.get('emotional_tone_score', 0), "/10"),
        ("Creativity", metrics_dict.get('vocabulary_richness', 0), "/10")
    ]
    
    for idx, (title, value, unit) in enumerate(metrics):
        with cols[idx]:
            st.metric(title, f"{value}{unit}")
    
    # Visual radar chart placeholder
    st.markdown("#### 🎯 Style Radar")
    st.info("Visual style radar chart will be implemented with Plotly integration")
    
    # Style features list
    st.markdown("#### ✨ Detected Style Features")
    features = metrics_dict.get('features', [
        "Conversational tone",
        "Medium sentence length",
        "Active voice preference",
        "Frequent contractions"
    ])
    
    for feature in features:
        st.write(f"• {feature}")

def chat_interface(messages, user_input_key="chat_input"):
    """Create a chat-like interface for conversations"""
    
    # Display message history
    for msg in messages:
        is_user = msg.get('role') == 'user'
        bg_color = "#4f46e5" if is_user else "#f1f5f9"
        text_color = "white" if is_user else "#1e293b"
        align = "right" if is_user else "left"
        
        st.markdown(f"""
        <div style="text-align: {align}; margin: 0.5rem 0;">
            <div style="
                display: inline-block;
                background: {bg_color};
                color: {text_color};
                padding: 0.75rem 1rem;
                border-radius: 1rem;
                max-width: 70%;
                text-align: left;
            ">
                {msg.get('content', '')}
                <div style="
                    font-size: 0.75rem;
                    opacity: 0.8;
                    margin-top: 0.25rem;
                ">
                    {msg.get('timestamp', '')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input area
    user_input = st.text_input("💬 Type your message...", key=user_input_key)
    
    return user_input
# Add these functions to your existing utils/ui_components.py

def mobile_optimized_container():
    """Wrapper for mobile-friendly content"""
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .mobile-container { padding: 0.5rem; }
        .mobile-hide { display: none; }
        .mobile-stack { flex-direction: column !important; }
    }
    </style>
    <div class="mobile-container">
    """, unsafe_allow_html=True)
    return st.container()

def animated_transition(element, animation_type="fade"):
    """Add CSS animations to elements"""
    animations = {
        "fade": "opacity 0.5s ease-in-out",
        "slide": "transform 0.3s ease-out",
        "bounce": "transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    }
    return f"style='animation: {animations.get(animation_type, 'fade')};'"

def toast_notification(message, type="success", duration=3000):
    """Custom toast notifications"""
    colors = {
        "success": "#10b981",
        "error": "#ef4444", 
        "warning": "#f59e0b",
        "info": "#3b82f6"
    }
    
    st.markdown(f"""
    <div id='toast' style='
        position: fixed; top: 20px; right: 20px; 
        background: {colors.get(type, "#10b981")}; color: white;
        padding: 1rem; border-radius: 8px; z-index: 1000;
        animation: slideIn 0.3s ease-out;
    '>
        {message}
    </div>
    <script>
    setTimeout(() => document.getElementById('toast').remove(), {duration});
    </script>
    """, unsafe_allow_html=True)