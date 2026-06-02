

import json
import os
from datetime import datetime

# Path where long term memory is saved
MEMORY_FILE = "memory/long_term_memory.json"


# SHORT TERM MEMORY
# Keeps track of current conversation


class ShortTermMemory:
    """
    Stores the current conversation history.
    Resets when the session ends.
    """

    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns  # Keep last 10 turns

    def add_turn(self, role, message):
        """Add a new turn to conversation history"""
        self.history.append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        # Keep only last max_turns to avoid context overflow
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def get_history(self):
        """Returns conversation history as formatted string"""
        if not self.history:
            return "No previous conversation."

        formatted = ""
        for turn in self.history:
            formatted += f"{turn['role']}: {turn['message']}\n"
        return formatted

    def get_history_for_gemini(self):
        """Returns history in format suitable for Gemini API"""
        gemini_history = []
        for turn in self.history:
            role = "user" if turn["role"] == "User" else "model"
            gemini_history.append({
                "role": role,
                "parts": [{"text": turn["message"]}]
            })
        return gemini_history

    def clear(self):
        """Clear conversation history"""
        self.history = []



# LONG TERM MEMORY
# Persists important info across sessions


class LongTermMemory:
    """
    Saves important information across sessions.
    Stored as a JSON file on disk.
    """

    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        """Load memory from JSON file"""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        return {
            "user_name": None,
            "education": None,
            "career_goal": None,
            "user_interests": [],
            "past_topics": [],
            "important_facts": [],
            "session_count": 0,
            "last_session": None
        }

    def save_memory(self):
        """Save memory to JSON file"""
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=4)

    def update_session(self):
        """Update session count and last session date"""
        self.memory["session_count"] += 1
        self.memory["last_session"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.save_memory()

    def set_user_name(self, name):
        """Remember user's name"""
        self.memory["user_name"] = name
        self.save_memory()

    def add_topic(self, topic):
        """Remember topics discussed"""
        if topic not in self.memory["past_topics"]:
            self.memory["past_topics"].append(topic)
            # Keep only last 20 topics
            self.memory["past_topics"] = self.memory["past_topics"][-20:]
            self.save_memory()

    def add_interest(self, interest):
        """Remember user interests"""
        if interest not in self.memory["user_interests"]:
            self.memory["user_interests"].append(interest)
            self.save_memory()

    def add_important_fact(self, fact):
        """Remember important facts about user"""
        self.memory["important_facts"].append(fact)
        self.memory["important_facts"] = self.memory["important_facts"][-10:]
        self.save_memory()
        
    def set_education(self, education):
        self.memory["education"] = education
        self.save_memory()

    def set_career_goal(self, goal):
        self.memory["career_goal"] = goal
        self.save_memory()

    def get_context(self):
        """Returns memory context as string for the prompt"""
        context = ""

        if self.memory["user_name"]:
            context += f"User's name: {self.memory['user_name']}\n"

        if self.memory["user_interests"]:
            context += f"User's interests: {', '.join(self.memory['user_interests'])}\n"

        if self.memory["past_topics"]:
            context += f"Previously discussed topics: {', '.join(self.memory['past_topics'][-5:])}\n"

        if self.memory["important_facts"]:
            context += f"Important facts: {', '.join(self.memory['important_facts'])}\n"

        if self.memory["session_count"] > 0:
            context += f"This is session number: {self.memory['session_count']}\n"
            
        if self.memory["education"]:
            context += f"Education: {self.memory['education']}\n"

        if self.memory["career_goal"]:
            context += f"Career Goal: {self.memory['career_goal']}\n"

        return context if context else "No previous memory."
    
    
    from google import genai

def extract_and_update_llm(self, message, client):
    prompt = f"""
Extract structured user information from the message.

Return ONLY valid JSON in this format:
{{
  "name": "",
  "education": "",
  "career_goal": "",
  "interests": []
}}

Rules:
- If info not present, return empty string or empty list
- Do not add explanations
- Only JSON output

Message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        data = json.loads(response.text)

        if data.get("name"):
            self.set_user_name(data["name"])

        if data.get("education"):
            self.set_education(data["education"])

        if data.get("career_goal"):
            self.set_career_goal(data["career_goal"])

        for i in data.get("interests", []):
            self.add_interest(i)

    except:
        pass  # fail safe

    self.save_memory()

    def get_user_name(self):
        return self.memory["user_name"]