# app.py
# Streamlit UI for APJ Abdul Kalam Digital Twin
# Enhanced UI with animations, better theme, recent chats

import streamlit as st
import os
import json
from datetime import datetime
from bot import DigitalTwin
from voice import speak_fast

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a1628 100%);
}

/* Animated header */
@keyframes glow {
    0% { text-shadow: 0 0 10px #FFD70044; }
    50% { text-shadow: 0 0 30px #FFD700aa, 0 0 60px #FFD70044; }
    100% { text-shadow: 0 0 10px #FFD70044; }
}

.main-title {
    animation: glow 3s ease-in-out infinite;
    color: #FFD700;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 4px;
}

/* Subtitle */
.main-subtitle {
    text-align: center;
    color: #7a7a9a;
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.main-date {
    text-align: center;
    color: #444466;
    font-size: 0.8rem;
    margin-bottom: 0;
}

/* User chat bubble */
.stChatMessage[data-testid="stChatMessageUser"] {
    background: linear-gradient(135deg, rgba(100,200,255,0.08), rgba(100,150,255,0.05)) !important;
    border: 1px solid rgba(100,200,255,0.15) !important;
    border-radius: 18px 18px 4px 18px !important;
    margin: 8px 0 !important;
    padding: 4px !important;
}

/* Bot chat bubble */
.stChatMessage[data-testid="stChatMessageAssistant"] {
    background: linear-gradient(135deg, rgba(255,215,0,0.06), rgba(255,150,50,0.03)) !important;
    border: 1px solid rgba(255,215,0,0.12) !important;
    border-radius: 18px 18px 18px 4px !important;
    margin: 8px 0 !important;
    padding: 4px !important;
}

/* Input box */
.stChatInput textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,215,0,0.2) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stChatInput textarea:focus {
    border-color: rgba(255,215,0,0.5) !important;
    box-shadow: 0 0 15px rgba(255,215,0,0.1) !important;
}

/* Thought process box */
.thought-box {
    background: rgba(255,215,0,0.04);
    border-left: 3px solid #FFD700;
    border-radius: 0 8px 8px 0;
    padding: 8px 14px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #a0a0c0;
    font-family: monospace;
}

/* Reflection box */
.reflection-box {
    background: rgba(100,200,255,0.04);
    border-left: 3px solid #64c8ff;
    border-radius: 0 8px 8px 0;
    padding: 8px 14px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #a0c0ff;
}

/* Source box */
.source-box {
    background: rgba(100,255,150,0.04);
    border-left: 3px solid #64ff96;
    border-radius: 0 8px 8px 0;
    padding: 6px 14px;
    margin: 3px 0;
    font-size: 0.75rem;
    color: #80c0a0;
}

/* Mood badge */
.mood-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    margin: 4px 0;
    font-weight: 500;
}

/* Suggested question buttons */
.stButton button {
    background: rgba(255,215,0,0.06) !important;
    border: 1px solid rgba(255,215,0,0.2) !important;
    color: #FFD700 !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    padding: 4px 12px !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: rgba(255,215,0,0.15) !important;
    border-color: rgba(255,215,0,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #0d1117 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 8px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 12px 0 !important;
}

/* Recent chat item */
.recent-chat {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.78rem;
    color: #7a7a9a;
    cursor: pointer;
}

.recent-chat:hover {
    background: rgba(255,215,0,0.05);
    border-color: rgba(255,215,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# INITIALIZE BOT
# ─────────────────────────────────────────

@st.cache_resource
def load_twin():
    return DigitalTwin()

twin = load_twin()

# ─────────────────────────────────────────
# SAVE CHAT HISTORY
# ─────────────────────────────────────────

CHAT_HISTORY_FILE = "memory/chat_history.json"

def save_chat_history(messages):
    """Saves current chat to history file."""
    os.makedirs("memory", exist_ok=True)
    history = load_all_chats()

    # Save current session
    session = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": [
            {"role": m["role"], "content": m["content"][:100]}
            for m in messages if m.get("content")
        ]
    }

    history.append(session)
    history = history[-10:]  # Keep last 10 sessions

    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_all_chats():
    """Loads all past chat sessions."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def get_mood_badge(mood):
    mood_map = {
        "sad":       ("😢 Sad", "#ff6b6b"),
        "stressed":  ("😰 Stressed", "#ffa500"),
        "excited":   ("🎉 Excited", "#51cf66"),
        "frustrated":("😤 Frustrated", "#ff8c42"),
        "neutral":   ("😊 Neutral", "#74c0fc")
    }
    label, color = mood_map.get(mood, ("😊 Neutral", "#74c0fc"))
    return f'<span class="mood-badge" style="background:rgba(255,255,255,0.06);color:{color};border:1px solid {color}44;">{label}</span>'

def play_audio(audio_path):
    """Plays audio file in Streamlit."""
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────

st.markdown('<h1 class="main-title">🚀 Dr. APJ Abdul Kalam</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Missile Man of India &nbsp;·&nbsp; 11th President &nbsp;·&nbsp; Visionary Scientist</p>', unsafe_allow_html=True)
st.markdown('<p class="main-date">October 15, 1931 — July 27, 2015</p>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

with st.sidebar:
    st.image(
        "APJ_image.webp",
        caption="Dr. APJ Abdul Kalam",
        use_container_width=True
    )

    st.divider()

    # ── Kalam Challenge ──
    st.markdown("### 🎯 Kalam Challenge")
    if st.button("Generate Today's Challenge", use_container_width=True):
        with st.spinner("Preparing your challenge..."):
            challenge = twin.generate_challenge()
            st.session_state.challenge = challenge
    if "challenge" in st.session_state:
        st.markdown(st.session_state.challenge)

    st.divider()

    # ── Memory Info ──
    st.markdown("### 🧠 Memory")
    memory = twin.long_term.memory
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sessions", memory["session_count"])
    with col2:
        st.metric("Topics", len(memory.get("past_topics", [])))

    if memory["user_name"]:
        st.markdown(f"👤 **{memory['user_name']}**")

    if memory["past_topics"]:
        st.markdown("**Recent Topics:**")
        for topic in memory["past_topics"][-3:]:
            st.markdown(f'<div class="recent-chat">💬 {topic[:40]}</div>',
                       unsafe_allow_html=True)

    st.divider()

    # ── Recent Chats ──
    st.markdown("### 📜 Recent Chats")
    all_chats = load_all_chats()
    if all_chats:
        for chat in reversed(all_chats[-5:]):
            with st.expander(f"🕐 {chat['timestamp']}"):
                for msg in chat["messages"][:3]:
                    role = "You" if msg["role"] == "user" else "Dr. Kalam"
                    st.markdown(f"**{role}:** {msg['content'][:60]}...")
    else:
        st.caption("No past chats yet!")

    st.divider()

    # ── Knowledge Base ──
    st.markdown("### 📚 Knowledge Base")
    st.markdown("""
    - 📖 Wings of Fire
    - 📖 Ignited Minds
    - 📖 India 2020
    - 📖 My Journey
    - 🎤 10+ Speeches
    - 💬 Interviews & Quotes
    """)

    st.divider()

    # ── Settings ──
    st.markdown("### ⚙️ Settings")
    show_thoughts   = st.toggle("🧠 Chain of Thought", value=True)
    show_reflection = st.toggle("🪞 Self Reflection", value=True)
    show_sources    = st.toggle("📚 Show Sources", value=True)
    show_graph      = st.toggle("🕸️ Knowledge Graph", value=True)
    show_embeddings = st.toggle("🗺️ Embedding Visualizer", value=True)
    enable_voice    = st.toggle("🔊 Enable Voice", value=False)

    st.divider()

    # ── Clear Chat ──
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        if st.session_state.messages:
            save_chat_history(st.session_state.messages)
        st.session_state.messages = []
        twin.short_term.clear()
        st.rerun()

# ─────────────────────────────────────────
# SUGGESTED QUESTIONS
# ─────────────────────────────────────────

SUGGESTED_QUESTIONS = [
    "What was your childhood like?",
    "Tell me about the Agni missile",
    "What is your vision for India?",
    "How should I deal with failure?",
    "What do you think about education?",
    "Tell me about ISRO",
]

# ─────────────────────────────────────────
# CHAT INTERFACE
# ─────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = """Namaste! My dear friend, I am Dr. APJ Abdul Kalam.

I am delighted to speak with you today. Whether you wish to discuss science, education, India's future, or simply seek some inspiration — I am here for you.

As I always say, *"Dream, Dream, Dream. Dreams transform into thoughts and thoughts result in action."*

What would you like to talk about today? 🚀"""

    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome,
        "sources": [],
        "thoughts": [],
        "reflection": "",
        "mood": "neutral"
    })

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🚀"):
            if message.get("mood") and message["mood"] != "neutral":
                st.markdown(get_mood_badge(message["mood"]), unsafe_allow_html=True)

            st.markdown(message["content"])

            if show_thoughts and message.get("thoughts"):
                with st.expander("🧠 Chain of Thought"):
                    for thought in message["thoughts"]:
                        st.markdown(f'<div class="thought-box">{thought}</div>',
                                   unsafe_allow_html=True)

            if show_reflection and message.get("reflection"):
                with st.expander("🪞 Self Reflection"):
                    st.markdown(f'<div class="reflection-box">{message["reflection"]}</div>',
                               unsafe_allow_html=True)

            if show_sources and message.get("sources"):
                with st.expander("📚 Sources"):
                    for source in set(message["sources"]):
                        st.markdown(f'<div class="source-box">📄 {source}</div>',
                                   unsafe_allow_html=True)

            if enable_voice and message["role"] == "assistant":
                if st.button("🔊 Listen", key=f"voice_{st.session_state.messages.index(message)}"):
                    with st.spinner("Generating audio..."):
                        audio_path = speak_fast(message["content"][:300])
                        if audio_path:
                            play_audio(audio_path)

# ─────────────────────────────────────────
# SUGGESTED QUESTIONS
# ─────────────────────────────────────────

if len(st.session_state.messages) <= 1:
    st.markdown("#### 💡 Suggested Questions")
    cols = st.columns(3)
    for i, question in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 3]:
            if st.button(question, key=f"suggested_{i}"):
                st.session_state.suggested_prompt = question
                st.rerun()

# ─────────────────────────────────────────
# HANDLE USER INPUT
# ─────────────────────────────────────────

# Handle suggested question click
if "suggested_prompt" in st.session_state:
    prompt = st.session_state.suggested_prompt
    del st.session_state.suggested_prompt
else:
    prompt = None

user_input = st.chat_input("Ask Dr. Kalam anything...")
if user_input:
    prompt = user_input

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🚀"):
        with st.spinner("Dr. Kalam is thinking..."):
            response, sources, thoughts, reflection, mood = twin.chat(prompt)

        if mood != "neutral":
            st.markdown(get_mood_badge(mood), unsafe_allow_html=True)

        st.markdown(response)

        if show_thoughts:
            with st.expander("🧠 Chain of Thought"):
                for thought in thoughts:
                    st.markdown(f'<div class="thought-box">{thought}</div>',
                               unsafe_allow_html=True)

        if show_reflection:
            with st.expander("🪞 Self Reflection"):
                st.markdown(f'<div class="reflection-box">{reflection}</div>',
                           unsafe_allow_html=True)

        if show_sources and sources:
            with st.expander("📚 Sources"):
                for source in set(sources):
                    st.markdown(f'<div class="source-box">📄 {source}</div>',
                               unsafe_allow_html=True)

        if enable_voice:
            with st.spinner("Generating Kalam's voice..."):
                audio_path = speak_fast(response[:300])
                if audio_path:
                    play_audio(audio_path)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources,
        "thoughts": thoughts,
        "reflection": reflection,
        "mood": mood
    })

    # Auto save chat history
    save_chat_history(st.session_state.messages)

# ─────────────────────────────────────────
# KNOWLEDGE GRAPH
# ─────────────────────────────────────────

if show_graph and len(st.session_state.messages) > 1:
    st.divider()
    st.markdown("### 🕸️ Live Knowledge Graph")
    st.caption("Topics and connections discovered in this conversation")

    graph_path = twin.knowledge_graph.render()

    if graph_path and os.path.exists(graph_path):
        stats = twin.knowledge_graph.get_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nodes", stats["nodes"])
        with col2:
            st.metric("Connections", stats["edges"])

        with open(graph_path, "r", encoding="utf-8") as f:
            graph_html = f.read()
        st.components.v1.html(graph_html, height=420)
    else:
        st.caption("Start chatting to build the knowledge graph!")

# ─────────────────────────────────────────
# EMBEDDING VISUALIZER
# ─────────────────────────────────────────

if show_embeddings and len(st.session_state.messages) > 3:
    st.divider()
    st.markdown("### 🗺️ Embedding Space Visualizer")
    st.caption("See where your questions land in Kalam's knowledge space")

    fig = twin.embedding_viz.render()

    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Ask at least 2 questions to see the embedding space!")