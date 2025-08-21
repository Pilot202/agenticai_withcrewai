import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Pilot-AI Marketing Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .output-container {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚀 Pilot-AI Marketing Agent")
st.markdown("""
Create AI-powered marketing content and strategies with our intelligent marketing agents.
""")

# Sidebar configuration
st.sidebar.header("Configuration")
platform = st.sidebar.selectbox(
    "Select Platform",
    ["Twitter", "LinkedIn", "Blog", "Facebook"]
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Content Generation")
    
    message = st.text_area(
        "Content Description",
        placeholder="Describe what you want to create..."
    )
    
    goal = st.text_input(
        "Marketing Goal",
        placeholder="e.g., Increase brand awareness, Generate leads..."
    )
    
    audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Small business owners, Tech professionals..."
    )

with col2:
    st.subheader("Quick Actions")
    action_options = [
        "Generate Campaign",
        "Create Content Calendar",
        "Analyze Market",
        "Generate Blog Post",
        "Create Social Media Posts"
    ]
    quick_action = st.selectbox("Select Action", action_options)

# Get backend URL from environment variable
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8007')

# Generate button
if st.button("Generate Content"):
    if not message or not goal or not audience:
        st.error("Please fill in all required fields")
    else:
        with st.spinner('Creating your marketing content...'):
            try:
                # API request
                response = requests.post(
                    f"{BACKEND_URL}/run",
                    json={
                        "message": message,
                        "goal": goal,
                        "audience": audience,
                        "platform": platform
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.markdown("### Generated Content")
                    with st.expander("View Content", expanded=True):
                        st.markdown(result.get("content") or result.get("reply"))
                        
                        # Download button for the content
                        content = result.get("content") or result.get("reply")
                        st.download_button(
                            label="Download Content",
                            data=content,
                            file_name=f"marketing_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                else:
                    st.error(f"Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display recent activities or examples
with st.sidebar:
    st.markdown("### Recent Activities")
    st.markdown("- Generated Twitter campaign")
    st.markdown("- Created content calendar")
    st.markdown("- Analyzed market trends")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using CrewAI and Streamlit")