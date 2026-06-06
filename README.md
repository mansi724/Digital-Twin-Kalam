# 🚀 Digital Twin of Dr. APJ Abdul Kalam

> *"Dream, Dream, Dream. Dreams transform into thoughts and thoughts result in action."*
> — Dr. APJ Abdul Kalam

An AI-powered Digital Twin of Dr. APJ Abdul Kalam built as part of **AIMS DTU Summer Project 2026**. This agent reproduces not just what he knew, but how he reasoned, taught, and spoke.

---

## 📌 Overview

This project simulates Dr. Kalam's:

- Knowledge
- Personality
- Teaching style
- Reasoning approach

It allows interactive conversations using:

- RAG (Retrieval Augmented Generation)
- Memory System
- Gemini 2.5 Flash API

---

## 🧠 Key Features

### 1. Persona Simulation
The AI responds like Dr. Kalam using a carefully designed system prompt. It is timeline aware — it knows events only up to July 2015 and handles modern questions gracefully.

### 2. RAG Pipeline
- Uses PDFs, speeches, and interviews
- Stored in ChromaDB vector database
- Retrieves relevant context for every answer
- Knowledge base: Wings of Fire, Ignited Minds, India 2020, My Journey, 10 speeches, 3 interviews, quotes

### 3. Memory System
- Short-term memory: current conversation history
- Long-term memory: user name, interests, goals, topics — persists across sessions

### 4. Chain of Thought
Before every response, the bot shows its complete reasoning process — mood detected, documents found, knowledge level assessed, timeline checked.

### 5. Self Reflection
After every answer, a second Gemini call evaluates the response — was it in character, accurate, and how confident is it.

### 6. Mood Detection
Detects if the user is sad, stressed, excited, or frustrated and adjusts Kalam's response accordingly.

### 7. Depth Controller
Adapts the complexity of answers based on the user's knowledge level — beginner, intermediate, or advanced.

### 8. Live Knowledge Graph
Interactive visual graph of topics and connections built during the conversation using PyVis.

### 9. Embedding Space Visualizer
2D plot showing where your questions land in Kalam's knowledge space using PCA and Plotly.

### 10. Kalam Challenge
Daily challenge generator — science question, philosophical question, creative task, or practical challenge in Kalam's voice.

### 11. Voice System
Text-to-speech using edge-tts with Indian English male voice. Also attempted voice cloning using Voicebox with Qwen TTS 1.7B — resembled Kalam's speech style but was too slow for real-time chat.

### 12. Streamlit UI
- Interactive chat interface with dark space theme
- Sidebar with memory dashboard, recent chats, knowledge base info
- Suggested question buttons
- Toggleable Chain of Thought, Self Reflection, Sources

---

## 🧪 Sample Capabilities

- Remembers user details across sessions
- Answers science, leadership, and life questions
- Uses real Kalam writings via RAG
- Maintains personality consistency throughout
- Shows reasoning process via Chain of Thought
- Speaks responses using Indian English TTS

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Google Gemini 2.5 Flash | LLM |
| ChromaDB | Vector database |
| Sentence Transformers | Embeddings |
| PyVis | Knowledge graph |
| Plotly | Embedding visualizer |
| edge-tts | Text to speech |
| pypdf | PDF extraction |

---

## 🏗️ Architecture

User
↓
Streamlit UI (app.py)
↓
Bot Brain (bot.py)
↓              ↓             ↓
RAG Pipeline   Memory       Persona
↓              ↓
ChromaDB     JSON File
↓
Knowledge Base → Gemini 2.5 Flash → Response

---

## 📁 Project Structure

digital_twin/
├── app.py                   → Streamlit UI
├── bot.py                   → Main bot brain
├── persona.py               → Kalam's persona & system prompt
├── knowledge_graph.py       → Live knowledge graph
├── embedding_visualizer.py  → Embedding space visualizer
├── voice.py                 → Text to speech
├── requirements.txt
├── data/                    → PDFs, speeches, interviews
├── rag/
│   └── rag_pipeline.py      → RAG pipeline
└── memory/
└── memory.py            → Memory system

---

## ▶️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/digital-twin-kalam.git
cd digital-twin-kalam

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API key
# Create .env file and add:
# GEMINI_API_KEY=your_key_here

# 5. Add data files to data/ folder

# 6. Run
streamlit run app.py
```

---

## 🔮 Future Enhancements

- Authentic Kalam voice clone with GPU support
- Multi-agent debate — Young Kalam vs President Kalam
- Historical conversation mode
- Mission Control Simulator
- Export conversation as PDF

---

## 👩‍💻 Made by

**Mansi** — AIMS DTU Summer Project 2026

---

*Built with curiosity, late nights, and a lot of "Dr. Kalam is thinking..." spinners* 🚀