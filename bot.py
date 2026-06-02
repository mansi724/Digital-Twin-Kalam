from google import genai
from dotenv import load_dotenv
import os

from persona import get_system_prompt, get_timeline
from rag.rag_pipeline import initialize_rag, retrieve_relevant_chunks
from memory.memory import ShortTermMemory, LongTermMemory





load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



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

        print("Digital Twin ready!\n")
        
        
    def extract_user_memory(self, user_message):
        """
        Extracts important facts from user messages
        and stores them in long-term memory.
        """

        message = user_message.lower()

        if "my name is" in message:
            name = user_message.split("is", 1)[1].strip()
            self.long_term.set_user_name(name)

        elif "i am studying" in message:
            education = user_message.replace("I am studying", "").strip()
            self.long_term.set_education(education)

        elif "i want to become" in message:
            goal = user_message.replace("I want to become", "").strip()
            self.long_term.set_career_goal(goal)

        elif "i am interested in" in message:
            interest = user_message.replace("I am interested in", "").strip()
            self.long_term.add_interest(interest)

    def chat(self, user_message):
        """
        Main chat function.
        Takes user message and returns bot response.
        """
        
        self.extract_user_memory(user_message)

        # Step 1 — Retrieve relevant chunks from RAG
        chunks, sources = retrieve_relevant_chunks(
            user_message,
            self.collection,
            top_k=5
        )
        rag_context = "\n\n".join(chunks)

        # Step 2 — Get memory context
        long_term_context = self.long_term.get_context()
        short_term_context = self.short_term.get_history()

        # Step 3 — Build the full prompt
        full_prompt = f"""
{get_system_prompt()}

## Relevant Knowledge from Your Writings
Use the following excerpts from your books and speeches 
to ground your answer in your actual words:
{rag_context}

## What You Remember About This User
{long_term_context}

## Recent Conversation History
{short_term_context}

## User's Current Message
{user_message}

Now respond as Dr. APJ Abdul Kalam would.
"""

        # Step 4 — Get response from Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        bot_response = response.text

        # Step 5 — Update short term memory
        self.short_term.add_turn("User", user_message)
        self.short_term.add_turn("Dr. Kalam", bot_response)

        # Step 6 — Update long term memory
        self.long_term.add_topic(user_message[:50])

        return bot_response, sources