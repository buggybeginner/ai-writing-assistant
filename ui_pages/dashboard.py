import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem;">📊 Dashboard</h1>
        <p style="color: #64748b;">Track your writing analytics and progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Overview
    st.markdown("### 📈 Activity Overview")
    
    # Mock data - replace with real data from session state
    total_generations = len(st.session_state.get('generation_history', []))
    unique_styles = len(set([g.get('personality', '') for g in st.session_state.get('generation_history', [])]))
    uploaded_files = len(st.session_state.get('uploaded_files', []))
    time_saved = total_generations * 15  # 15 minutes per generation
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Generations", total_generations)
    with col2:
        st.metric("Styles Used", unique_styles)
    with col3:
        st.metric("Files Uploaded", uploaded_files)
    with col4:
        st.metric("Time Saved", f"{time_saved} min")
    
    # Usage breakdown
    st.markdown("---")
    st.markdown("### 🎭 Style Usage Breakdown")
    
    if st.session_state.get('generation_history'):
        # Calculate style frequencies
        style_counts = {}
        for gen in st.session_state.generation_history:
            personality = gen.get('personality', 'Unknown')
            style_counts[personality] = style_counts.get(personality, 0) + 1
        
        # Display as bars
        for style, count in style_counts.items():
            st.write(f"**{style}**")
            progress = min(count / 10, 1.0)  # Cap at 10 for visualization
            st.progress(progress)
            st.caption(f"{count} generations")
    else:
        st.info("📭 No generation history yet. Try creating some content on the Preset Personalities page!")
    
    # Recent activity table
    st.markdown("---")
    st.markdown("### 📝 Recent Activity")
    
    if st.session_state.get('generation_history'):
        # Create a simple table
        recent_data = []
        for gen in list(reversed(st.session_state.generation_history))[:5]:
            recent_data.append({
                "Time": gen.get('timestamp', ''),
                "Style": gen.get('personality', 'Unknown'),
                "Input Preview": gen.get('input', '')[:50] + ("..." if len(gen.get('input', '')) > 50 else ''),
                "Words": len(gen.get('output', '').split())
            })
        
        # Display as dataframe
        df = pd.DataFrame(recent_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export option
        if st.button("📤 Export History as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                "💾 Download CSV",
                data=csv,
                file_name=f"personawrite_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.write("No activity to display.")
    
    # Writing improvement tips
    st.markdown("---")
    st.markdown("### 💡 Writing Improvement Tips")
    
    tips = [
        "**Vary sentence length** - Mix short and long sentences for better rhythm",
        "**Use active voice** - Makes writing more direct and engaging",
        "**Read aloud** - Helps identify awkward phrasing",
        "**Use specific examples** - Instead of 'good', say 'efficient, clear, or insightful'",
        "**Take breaks** - Fresh eyes catch more errors"
    ]
    
    for tip in tips:
        st.write(f"• {tip}")
    
    # Reset options
    st.markdown("---")
    st.markdown("### ⚙️ Data Management")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Clear All History", use_container_width=True):
            st.session_state.generation_history = []
            st.session_state.uploaded_files = []
            st.success("History cleared successfully!")
            st.rerun()
    with col_b:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Comprehensive report generation will be available in the next update")