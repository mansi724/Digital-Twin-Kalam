# test_bot.py
# Quick test to check if the full bot works

from bot import DigitalTwin

# Initialize the bot
twin = DigitalTwin()

# Test questions
questions = [
    "What was your childhood like in Rameswaram?",
    "What do you think about the importance of education?",
    "Tell me about the Agni missile project.",
]

for question in questions:
    print(f"\nUser: {question}")
    print("-" * 50)
    response, sources = twin.chat(question)
    print(f"Dr. Kalam: {response}")
    print(f"\nSources used: {set(sources)}")
    print("=" * 50)