# bot.py
# Main brain of the Digital Twin
# Connects RAG + Memory + Persona + Gemini together

from google import genai
from dotenv import load_dotenv
import os

from persona import get_system_prompt, get_timeline
from rag.rag_pipeline import initialize_rag, retrieve_relevant_chunks
from memory.memory import ShortTermMemory, LongTermMemory
from knowledge_graph import KnowledgeGraph
from embedding_visualizer import EmbeddingVisualizer

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ─────────────────────────────────────────
# MOOD DETECTION
# ─────────────────────────────────────────

def detect_mood(message):
    """
    Detects user's emotional state from their message.
    Returns mood as string.
    """
    message_lower = message.lower()

    sad_words = ["sad", "depressed", "hopeless", "crying", "failure", 
                 "failed", "lost", "alone", "grief", "unhappy", "upset"]
    stressed_words = ["stressed", "anxious", "worried", "nervous", 
                      "scared", "afraid", "panic", "pressure", "tension"]
    excited_words = ["excited", "happy", "amazing", "wonderful", 
                     "great", "awesome", "love", "fantastic", "brilliant"]
    angry_words = ["angry", "frustrated", "annoyed", "hate", 
                   "furious", "upset", "mad", "irritated"]

    if any(word in message_lower for word in sad_words):
        return "sad"
    elif any(word in message_lower for word in stressed_words):
        return "stressed"
    elif any(word in message_lower for word in excited_words):
        return "excited"
    elif any(word in message_lower for word in angry_words):
        return "frustrated"
    else:
        return "neutral"


# ─────────────────────────────────────────
# DEPTH DETECTION
# ─────────────────────────────────────────

def detect_depth(message):
    """
    Detects user's knowledge level from their message.
    Returns depth level as string.
    """
    technical_words = ["quantum", "trajectory", "propulsion", "algorithm",
                       "nuclear", "aerodynamics", "thermodynamics", "vector",
                       "payload", "orbital", "fusion", "fission", "entropy"]

    basic_words = ["what is", "explain", "how does", "tell me about",
                   "i don't understand", "simple", "basics", "beginner"]

    message_lower = message.lower()

    if any(word in message_lower for word in technical_words):
        return "advanced"
    elif any(word in message_lower for word in basic_words):
        return "beginner"
    else:
        return "intermediate"


# ─────────────────────────────────────────
# TIMELINE CHECK
# ─────────────────────────────────────────

def check_timeline(message):
    """
    Checks if the message refers to events after Kalam's death in 2015.
    Returns True if beyond timeline.
    """
    post_2015 = ["2016", "2017", "2018", "2019", "2020", "2021", 
                 "2022", "2023", "2024", "2025", "2026",
                 "chatgpt", "covid", "corona", "chandrayaan 3",
                 "gaganyaan", "artificial intelligence", "chatbot",
                 "ukraine", "pandemic", "modi 3.0"]
    
    message_lower = message.lower()
    return any(word in message_lower for word in post_2015)


# ─────────────────────────────────────────
# DIGITAL TWIN CLASS
# ─────────────────────────────────────────

class DigitalTwin:

    def __init__(self):
        print("Initializing Digital Twin of Dr. APJ Abdul Kalam...")

        # Initialize RAG
        print("Loading knowledge base...")
        self.collection = initialize_rag()

        # Initialize Memory
        self.short_term = ShortTermMemory(max_turns=10)
        self.long_term = LongTermMemory()
        self.long_term.update_session()
        
        self.knowledge_graph = KnowledgeGraph()
        # Initialize Embedding Visualizer
        self.embedding_viz = EmbeddingVisualizer()

        print("Digital Twin ready!\n")

    def chat(self, user_message):
        """
        Main chat function with Chain of Thought.
        Returns response, sources, and thought process.
        """

        thought_process = []

        # ── Step 1 — Detect mood ──
        mood = detect_mood(user_message)
        depth = detect_depth(user_message)
        beyond_timeline = check_timeline(user_message)
        thought_process.append(f"🎭 Mood detected: {mood}")
        thought_process.append(f"📊 Knowledge level: {depth}")

        if beyond_timeline:
            thought_process.append("⏰ Timeline check: Question is beyond 2015 — will acknowledge gracefully")
        else:
            thought_process.append("⏰ Timeline check: Within knowledge period ✓")

        # ── Step 2 — Retrieve relevant chunks from RAG ──
        thought_process.append("🔍 Searching knowledge base...")
        chunks, sources = retrieve_relevant_chunks(
            user_message,
            self.collection,
            top_k=5
        )
        unique_sources = list(set(sources))
        thought_process.append(f"📚 Found relevant content in: {', '.join(unique_sources)}")
        rag_context = "\n\n".join(chunks)

        # ── Step 3 — Get memory context ──
        thought_process.append("🧠 Loading memory context...")
        long_term_context = self.long_term.get_context()
        short_term_context = self.short_term.get_history()

        # ── Step 4 — Build mood aware instruction ──
        mood_instruction = ""
        if mood == "sad":
            mood_instruction = "The user seems sad or distressed. Be extra warm, compassionate and encouraging."
        elif mood == "stressed":
            mood_instruction = "The user seems stressed or anxious. Be calming, reassuring and supportive."
        elif mood == "excited":
            mood_instruction = "The user seems excited and happy. Match their energy with enthusiasm!"
        elif mood == "frustrated":
            mood_instruction = "The user seems frustrated. Be patient, understanding and gently redirect."

        # ── Step 5 — Build depth aware instruction ──
        depth_instruction = ""
        if depth == "beginner":
            depth_instruction = "Use simple language, analogies and examples. Avoid jargon."
        elif depth == "advanced":
            depth_instruction = "Use technical language and go deep into the science and details."
        else:
            depth_instruction = "Use balanced language — clear but not oversimplified."

        thought_process.append(f"💭 Building prompt with mood={mood}, depth={depth}")

        # ── Step 6 — Build the full prompt ──
        full_prompt = f"""
{get_system_prompt()}

## Relevant Knowledge from Your Writings
{rag_context}

## What You Remember About This User
{long_term_context}

## Recent Conversation History
{short_term_context}

## Special Instructions for This Response
{mood_instruction}
{depth_instruction}

## User's Current Message
{user_message}

Now respond as Dr. APJ Abdul Kalam would.
"""

        thought_process.append("✅ Generating response...")

        # ── Step 7 — Get response from Gemini ──
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        bot_response = response.text

        # ── Step 8 — Self Reflection ──
        thought_process.append("🪞 Running self reflection...")
        reflection = self.self_reflect(user_message, bot_response)
        thought_process.append(f"🪞 Reflection: {reflection}")

        # ── Step 9 — Update memory ──
        self.short_term.add_turn("User", user_message)
        self.short_term.add_turn("Dr. Kalam", bot_response)
        self.long_term.add_topic(user_message[:50])
        
        # ── Step 10 — Update Knowledge Graph ──  ← ADD THIS
        self.knowledge_graph.update(user_message, bot_response)
        thought_process.append("🕸️ Knowledge graph updated")
        
        # ── Step 11 — Update Embedding Visualizer ──
        self.embedding_viz.add_turn(user_message, bot_response)

        return bot_response, sources, thought_process, reflection, mood

    def self_reflect(self, question, answer):
        """
        Evaluates the quality and accuracy of the response.
        Returns a short reflection string.
        """
        reflection_prompt = f"""
You are an evaluator checking if this response is truly in the style 
and spirit of Dr. APJ Abdul Kalam.

Question asked: {question}
Response given: {answer[:500]}

Rate the response on these 3 things in ONE short line each:
1. In character? (Yes/Partially/No)
2. Accurate to Kalam's known views? (Yes/Partially/No)  
3. Confidence level? (High/Medium/Low)

Be very brief. Format exactly like:
In character: Yes | Accurate: Yes | Confidence: High
"""
        reflection_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=reflection_prompt
        )
        return reflection_response.text.strip()

    def generate_challenge(self):
        """
        Generates a daily Kalam Challenge.
        Returns challenge as string.
        """
        challenge_prompt = f"""
You are Dr. APJ Abdul Kalam. Generate ONE daily challenge for a young student.

The challenge should be one of these types (pick randomly):
- A science question related to rockets, space, or physics
- A philosophical question about life, dreams, or purpose  
- A creative task like "write a letter to your future self"
- A practical task like "talk to one person today about their dreams"

Format exactly like this:
🚀 KALAM CHALLENGE OF THE DAY

[Type]: Science / Philosophy / Creative / Practical

[Challenge]: Write the challenge here in 2-3 sentences in Kalam's voice.

[Hint]: A small hint to get started.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=challenge_prompt
        )
        return response.text