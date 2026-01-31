"""Streamlit web interface for LLM Council with full conversation display."""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="LLM Council",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stage-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
    }
    .model-response {
        background-color: #f0f2f6;
        color: #000000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .chairman-response {
        background-color: #e8f4ea;
        color: #000000;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ca02c;
        margin-top: 1rem;
    }
    .ranking-box {
        background-color: #fff3cd;
        color: #000000;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #ffc107;
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        padding: 0.3rem;
        background-color: #2b2b2b;
        color: #00ff00;
        border-radius: 0.3rem;
    }
    .success-icon {
        color: #2ca02c;
        font-size: 1.2rem;
    }
    .warning-icon {
        color: #ff7f0e;
        font-size: 1.2rem;
    }
    .error-icon {
        color: #d62728;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")
API_BASE = f"{BACKEND_URL}/api"

# Initialize session state
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'logs' not in st.session_state:
    st.session_state.logs = []


def log_message(message, level="INFO"):
    """Add a log message to the session state."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append({
        "timestamp": timestamp,
        "level": level,
        "message": message
    })


def create_conversation():
    """Create a new conversation."""
    try:
        log_message("Creating new conversation...", "INFO")
        response = requests.post(f"{API_BASE}/conversations", json={})
        response.raise_for_status()
        data = response.json()
        log_message(f"Conversation created: {data['id']}", "SUCCESS")
        return data['id']
    except Exception as e:
        log_message(f"Failed to create conversation: {e}", "ERROR")
        st.error(f"Failed to create conversation: {e}")
        return None


def send_message(conversation_id, content):
    """Send a message and get the response."""
    try:
        log_message(f"Sending message to conversation {conversation_id}", "INFO")
        response = requests.post(
            f"{API_BASE}/conversations/{conversation_id}/message",
            json={"content": content}
        )
        response.raise_for_status()
        data = response.json()
        log_message("Message sent successfully", "SUCCESS")
        return data
    except Exception as e:
        log_message(f"Failed to send message: {e}", "ERROR")
        st.error(f"Failed to send message: {e}")
        return None


def display_stage1_results(stage1_results):
    """Display Stage 1 results."""
    st.markdown('<div class="stage-header">📝 Stage 1: Individual Responses</div>', unsafe_allow_html=True)
    st.write(f"**{len(stage1_results)} models provided their initial responses:**")
    
    for i, result in enumerate(stage1_results, 1):
        with st.expander(f"🤖 Model {i}: {result['model']}", expanded=i==1):
            st.markdown(f'<div class="model-response">{result["response"]}</div>', unsafe_allow_html=True)
            st.caption(f"Response length: {len(result['response'])} characters")


def display_stage2_results(stage2_results, label_to_model, aggregate_rankings):
    """Display Stage 2 results."""
    st.markdown('<div class="stage-header">🔍 Stage 2: Peer Rankings</div>', unsafe_allow_html=True)
    st.write(f"**{len(stage2_results)} models ranked each other's responses:**")
    
    # Show aggregate rankings first
    if aggregate_rankings:
        st.markdown("### 📊 Aggregate Rankings")
        st.write("**Overall consensus from all models:**")
        
        for i, ranking in enumerate(aggregate_rankings, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            st.markdown(
                f"{medal} **{ranking['model']}** - Average Rank: {ranking['average_rank']} "
                f"({ranking['rankings_count']} votes)"
            )
        st.divider()
    
    # Show individual rankings
    st.markdown("### 📋 Individual Rankings")
    for i, result in enumerate(stage2_results, 1):
        with st.expander(f"🗳️ Rankings from: {result['model']}", expanded=False):
            st.markdown(f'<div class="ranking-box">{result["ranking"]}</div>', unsafe_allow_html=True)
            
            if result.get('parsed_ranking'):
                st.markdown("**Parsed Ranking:**")
                for rank, label in enumerate(result['parsed_ranking'], 1):
                    model_name = label_to_model.get(label, "Unknown")
                    st.write(f"{rank}. {label} → {model_name}")


def display_stage3_result(stage3_result):
    """Display Stage 3 final result."""
    st.markdown('<div class="stage-header">🎯 Stage 3: Final Synthesis</div>', unsafe_allow_html=True)
    st.write(f"**Chairman ({stage3_result['model']}) synthesized the final answer:**")
    
    st.markdown(f'<div class="chairman-response">{stage3_result["response"]}</div>', unsafe_allow_html=True)
    st.caption(f"Final response length: {len(stage3_result['response'])} characters")


def display_logs():
    """Display the log console."""
    st.markdown("### 📋 Process Logs")
    
    if not st.session_state.logs:
        st.info("No logs yet. Submit a query to see the process logs.")
        return
    
    # Create a scrollable log area
    log_container = st.container()
    
    with log_container:
        for log in st.session_state.logs[-50:]:  # Show last 50 logs
            level_icon = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "ERROR": "❌"
            }.get(log['level'], "ℹ️")
            
            st.markdown(
                f'<div class="log-entry">[{log["timestamp"]}] {level_icon} {log["level"]}: {log["message"]}</div>',
                unsafe_allow_html=True
            )


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🏛️ LLM Council</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #666; font-size: 1.2rem;'>"
        "Harness the collective wisdom of multiple AI models"
        "</p>",
        unsafe_allow_html=True
    )
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Check backend connection
        try:
            response = requests.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                st.success("✅ Backend connected")
            else:
                st.error("❌ Backend not responding")
        except Exception as e:
            st.error(f"❌ Backend connection failed: {e}")
        
        st.divider()
        
        # New conversation button
        if st.button("🆕 New Conversation", use_container_width=True):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.session_state.logs = []
            st.rerun()
        
        st.divider()
        
        # Display current conversation info
        if st.session_state.conversation_id:
            st.info(f"📝 Conversation ID:\n`{st.session_state.conversation_id[:8]}...`")
            st.write(f"💬 Messages: {len(st.session_state.messages)}")
        else:
            st.info("No active conversation")
        
        st.divider()
        
        # Show logs toggle
        show_logs = st.checkbox("Show Process Logs", value=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1] if show_logs else [1, 0])
    
    with col1:
        # Input area
        st.markdown("### 💭 Ask the Council")
        
        with st.form("query_form", clear_on_submit=True):
            user_query = st.text_area(
                "Enter your question:",
                placeholder="Ask anything... The council will deliberate and provide a comprehensive answer.",
                height=100,
                key="user_input"
            )
            submit_button = st.form_submit_button("🚀 Submit to Council", use_container_width=True)
        
        if submit_button and user_query:
            # Create conversation if needed
            if not st.session_state.conversation_id:
                conversation_id = create_conversation()
                if conversation_id:
                    st.session_state.conversation_id = conversation_id
                else:
                    st.error("Failed to create conversation. Please try again.")
                    st.stop()
            
            # Add user message to display
            st.session_state.messages.append({
                "role": "user",
                "content": user_query
            })
            
            # Show progress
            with st.spinner("🏛️ The council is deliberating..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Stage 1
                status_text.text("Stage 1: Collecting individual responses...")
                progress_bar.progress(10)
                log_message("Starting Stage 1: Collecting responses", "INFO")
                
                # Send message and get response
                response_data = send_message(st.session_state.conversation_id, user_query)
                
                if response_data:
                    progress_bar.progress(40)
                    log_message("Stage 1 complete", "SUCCESS")
                    
                    # Stage 2
                    status_text.text("Stage 2: Collecting peer rankings...")
                    progress_bar.progress(60)
                    log_message("Starting Stage 2: Collecting rankings", "INFO")
                    time.sleep(0.5)
                    progress_bar.progress(80)
                    log_message("Stage 2 complete", "SUCCESS")
                    
                    # Stage 3
                    status_text.text("Stage 3: Synthesizing final answer...")
                    progress_bar.progress(90)
                    log_message("Starting Stage 3: Chairman synthesis", "INFO")
                    time.sleep(0.5)
                    progress_bar.progress(100)
                    log_message("Council process complete!", "SUCCESS")
                    
                    # Store the response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_data
                    })
                    
                    status_text.text("✅ Complete!")
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.rerun()
                else:
                    st.error("Failed to get response from the council.")
                    log_message("Failed to get response", "ERROR")
        
        # Display conversation history
        if st.session_state.messages:
            st.divider()
            st.markdown("## 📜 Conversation History")
            
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown("### 👤 Your Question")
                    st.info(msg["content"])
                else:
                    # Display the full council response
                    st.markdown("### 🏛️ Council Response")
                    
                    response = msg["content"]
                    
                    # Create tabs for different views
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📋 Final Answer",
                        "📝 Stage 1: Responses",
                        "🔍 Stage 2: Rankings",
                        "🎯 Full Process"
                    ])
                    
                    with tab1:
                        if "stage3" in response:
                            display_stage3_result(response["stage3"])
                        else:
                            st.warning("Stage 3 data not available")
                    
                    with tab2:
                        if "stage1" in response:
                            display_stage1_results(response["stage1"])
                        else:
                            st.warning("Stage 1 data not available")
                    
                    with tab3:
                        if "stage2" in response and "metadata" in response:
                            display_stage2_results(
                                response["stage2"],
                                response["metadata"].get("label_to_model", {}),
                                response["metadata"].get("aggregate_rankings", [])
                            )
                        else:
                            st.warning("Stage 2 data not available")
                    
                    with tab4:
                        st.markdown("### Full Council Process")
                        
                        # Stage 1
                        if "stage1" in response:
                            display_stage1_results(response["stage1"])
                        
                        # Stage 2
                        if "stage2" in response and "metadata" in response:
                            display_stage2_results(
                                response["stage2"],
                                response["metadata"].get("label_to_model", {}),
                                response["metadata"].get("aggregate_rankings", [])
                            )
                        
                        # Stage 3
                        if "stage3" in response:
                            display_stage3_result(response["stage3"])
                    
                    st.divider()
    
    # Logs panel
    if show_logs:
        with col2:
            display_logs()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
        "LLM Council - Powered by LM Studio"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
