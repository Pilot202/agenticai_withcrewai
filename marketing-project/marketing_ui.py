# marketing_agent_ui.py
import streamlit as st
import requests

# --- CONFIG ---
st.set_page_config(page_title="Marketing Agent", page_icon="🤖", layout="wide")

# Replace with your FastAPI/Flask backend endpoint if agent runs there
BACKEND_URL = "http://localhost:8007/run"

# --- SIDEBAR ---
st.sidebar.title("⚙️ Marketing Agent Settings")
campaign_goal = st.sidebar.text_input("🎯 Campaign Goal", "Promote a new product")
target_audience = st.sidebar.text_input("👥 Target Audience", "Young professionals")
platform = st.sidebar.selectbox("📢 Platform", ["Facebook", "Instagram", "Twitter", "LinkedIn", "All platform"])
generate_button = st.sidebar.button("🚀 Generate Content")

# --- MAIN CHAT AREA ---
st.title("🤖 Marketing Agent Dashboard")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.text_input("💬 Ask the Agent:", "")

if st.button("Send") and user_input.strip():
    # Append user input
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call backend API (replace with your agent logic)
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input, "goal": campaign_goal, "audience": target_audience, "platform": platform},
            timeout=30
        )
        reply = response.json().get("reply", "⚠️ No response from agent.")
    except Exception as e:
        reply = f"❌ Backend error: {e}"

    # Append agent response
    st.session_state.chat_history.append({"role": "agent", "content": reply})

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**🧑 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 Agent:** {chat['content']}")

# --- CAMPAIGN CONTENT GENERATION ---
if generate_button:
    st.subheader("📢 Generated Campaign Content")
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": "Generate campaign content", "goal": campaign_goal, "audience": target_audience, "platform": platform},
            timeout=30
        )
        content = response.json().get("content", "⚠️ No content generated.")
    except Exception as e:
        content = f"❌ Backend error: {e}"

    st.write(content)

# --- ANALYTICS ---
st.subheader("📊 Campaign Analytics (Mock Data for Now)")
col1, col2, col3 = st.columns(3)
col1.metric("Engagement Rate", "12.5%", "+2.1%")
col2.metric("Reach", "54k", "+8.4%")
col3.metric("Conversions", "1.2k", "+0.6%")
