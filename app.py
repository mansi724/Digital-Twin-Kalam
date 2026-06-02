# app.py
# Streamlit UI for APJ Abdul Kalam Digital Twin

import streamlit as st
from bot import DigitalTwin

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────

st.set_page_config(
    page_title="Dr. APJ Abdul Kalam - Digital Twin",
    page_icon="🚀",
    layout="wide"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .header-text {
        text-align: center;
        color: #FFD700;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .subheader-text {
        text-align: center;
        color: #a0a0a0;
        font-size: 1rem;
    }
    .source-text {
        color: #a0a0a0;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# INITIALIZE BOT (only once)
# ─────────────────────────────────────────

@st.cache_resource
def load_twin():
    return DigitalTwin()

twin = load_twin()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────

st.markdown('<p class="header-text">🚀 Dr. APJ Abdul Kalam</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">Missile Man of India • Former President • Visionary Scientist</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">1931 - 2015</p>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

with st.sidebar:
    st.image("APJ_image.webp", 
             caption="Dr. APJ Abdul Kalam", 
             use_column_width=True)
    
    st.divider()
    st.markdown("### 🧠 Memory Dashboard")

    memory = twin.long_term.memory

    with st.expander("👤 User Profile"):
        st.write("**Name:**", memory.get("user_name"))
        st.write("**Education:**", memory.get("education"))
        st.write("**Career Goal:**", memory.get("career_goal"))

    with st.expander("❤️ Interests"):
        st.write(memory.get("user_interests", []))

    with st.expander("📌 Past Topics"):
        st.write(memory.get("past_topics", [])[-10:])

    with st.expander("💡 Important Facts"):
        st.write(memory.get("important_facts", []))

    with st.expander("📊 Session Info"):
        st.write("Sessions:", memory.get("session_count"))
        st.write("Last Session:", memory.get("last_session"))
        st.markdown("### About Dr. Kalam")
        st.markdown("""
        - 🎓 Aerospace Engineer
        - 🚀 Father of India's Missile Program  
        - 🇮🇳 11th President of India
        - 📚 Author of Wings of Fire
        - ❤️ People's President
        """)
    
    st.divider()
    
    st.markdown("### Knowledge Base")
    st.markdown("""
    This Digital Twin is grounded in:
    - 📖 Wings of Fire
    - 📖 Ignited Minds
    - 📖 India 2020
    - 📖 My Journey
    - 🎤 10+ Speeches
    - 💬 Interviews & Quotes
    """)

    st.divider()

    # Memory info
    st.markdown("### Memory")
    memory = twin.long_term.memory
    st.markdown(f"**Sessions:** {memory['session_count']}")
    if memory['user_name']:
        st.markdown(f"**Your name:** {memory['user_name']}")
    if memory['past_topics']:
        st.markdown("**Recent topics:**")
        for topic in memory['past_topics'][-3:]:
            st.markdown(f"- {topic[:40]}...")

    st.divider()

    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        twin.short_term.clear()
        st.rerun()

# ─────────────────────────────────────────
# CHAT INTERFACE
# ─────────────────────────────────────────

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    welcome = """Namaste! My dear friend, I am Dr. APJ Abdul Kalam. 

I am delighted to speak with you today. Whether you wish to discuss science, 
education, India's future, or simply seek some inspiration — I am here.

As I always say, *"Dream, Dream, Dream. Dreams transform into thoughts and 
thoughts result in action."*

What would you like to talk about today? 🚀"""
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome,
        "sources": []
    })

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🚀"):
            st.markdown(message["content"])
            if message.get("sources"):
                st.markdown(f'<p class="source-text">📚 Sources: {", ".join(set(message["sources"]))}</p>', 
                          unsafe_allow_html=True)

# ─────────────────────────────────────────
# HANDLE USER INPUT
# ─────────────────────────────────────────

if prompt := st.chat_input("Ask Dr. Kalam anything..."):

    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant", avatar="🚀"):
        with st.spinner("Dr. Kalam is thinking..."):
            response, sources = twin.chat(prompt)
        
        st.markdown(response)
        
        if sources:
            st.markdown(f'<p class="source-text">📚 Sources: {", ".join(set(sources))}</p>', 
                      unsafe_allow_html=True)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources
    })