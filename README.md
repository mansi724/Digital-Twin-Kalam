# 🚀 Digital Twin of Dr. APJ Abdul Kalam

## 📌 Overview
This project is an AI-powered Digital Twin of Dr. APJ Abdul Kalam that simulates his:
- Knowledge
- Personality
- Teaching style
- Reasoning approach

It allows interactive conversations using:
- RAG (Retrieval Augmented Generation)
- Memory System
- Gemini API

---

## 🧠 Key Features

### 1. Persona Simulation
The AI responds like Dr. Kalam using a carefully designed system prompt.

### 2. RAG Pipeline
- Uses PDFs, speeches, interviews
- Stored in ChromaDB
- Retrieves relevant context for answers

### 3. Memory System
- Short-term memory: conversation history
- Long-term memory: user name, interests, goals, topics

### 4. Streamlit UI
- Interactive chat interface
- Sidebar memory dashboard
- Quick prompt buttons

---

## ⚙️ Tech Stack
- Python
- Streamlit
- Google Gemini API
- ChromaDB
- Sentence Transformers
- PyPDF

---

## 🏗️ Architecture
User → Streamlit UI → Bot Engine → (Memory + RAG) → Gemini → Response

---

## 🧪 Sample Capabilities
- Remembers user details
- Answers science and leadership questions
- Uses real Kalam writings via RAG
- Maintains personality consistency

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py