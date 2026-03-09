import requests
import json
import sys
sys.path.append('./memory')

from session_memory import SessionMemory
from vector_store import VectorStore

def generate_with_context(query, context):
    prompt = f"""You are a helpful conversational assistant.

You have memory of past conversations:
{context}

User says: {query}

Rules:
- Have a natural conversation
- Only mention memory facts if directly relevant
- If user shares new info, acknowledge it naturally
- If asked a question, answer it directly
- Keep responses short and friendly
- Do NOT repeat all facts back to user every time
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


def run_pipeline(user_query, session, vector_store):
    """
    Full memory pipeline:
    New Query
    → Search memory (FAISS)
    → Fetch similar context
    → Inject in prompt
    → Generate with context
    """

    print(f"\nUser: {user_query}")
    print("-" * 40)

    # Step 1: Search memory
    print("Step 1: Searching memory...")
    faiss_context = vector_store.get_context_for_query(user_query)
    session_context = session.get_context()

    # Combine both contexts
    context = ""
    if session_context:
        context += f"Current conversation:\n{session_context}\n"
    if faiss_context:
        context += f"{faiss_context}"

    # Step 2: Fetch similar context
    if context:
        print(f"Step 2: Found relevant context:\n{context}")
    else:
        print("Step 2: No relevant context found")

    # Step 3: Inject context in prompt and generate
    print("Step 3: Injecting context and generating response...")
    response = generate_with_context(user_query, context)

    # Step 4: Store new interaction in session memory
    session.add_message("user", user_query)
    session.add_message("assistant", response)

    print(f"Assistant: {response}")

    return response


if __name__ == "__main__":
    print("=" * 60)
    print("Agent Memory System - Day 4")
    print("=" * 60)

    # Ask for username
    username = input("Enter your name: ").strip()
    print(f"\nWelcome {username}!")

    # Initialize memory systems with user_id
    session = SessionMemory(user_id=username, max_messages=10)
    vector_store = VectorStore()

    # Load only this user's facts from long_term.db
    print(f"\nLoading memory for {username}...")
    vector_store.load_from_db(user_id=username)

    print("\nStarting conversation... (type 'quit' to exit)")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("\nSummarizing and saving facts...")
            facts = session.summarize_facts()
            if facts:
                session.save_facts_to_db(facts)
                vector_store.add_text(facts)
                print("Facts saved to long-term memory!")
            print(f"Goodbye {username}!")
            break

        run_pipeline(user_input, session, vector_store)