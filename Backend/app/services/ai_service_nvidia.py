from openai import OpenAI
from app.memory.chat_memory import chat_history

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def analyze_symptoms(symptoms):

    history_text = "\n".join(chat_history)

    prompt = f"""
You are MediCheck AI, a professional medical assistant.

IMPORTANT:
Use BOTH the conversation history and the latest message.

Conversation History:
{history_text}

Latest User Message:
{symptoms}

If the user asks to summarize symptoms, list ALL symptoms mentioned in the conversation history.

Respond ONLY in this format:

Possible Conditions:
- condition 1
- condition 2

Urgency Level:
- Low / Moderate / High

Basic Advice:
- advice

Red Flags:
- red flag 1
- red flag 2

When To See A Doctor:
- recommendation
"""

    print("\n========== MEMORY DEBUG ==========")
    print(history_text)
    print("==================================\n")

    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a medical assistant that remembers previous conversation context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=250
    )

    response = completion.choices[0].message.content

    chat_history.append(f"User: {symptoms}")
    chat_history.append(f"AI: {response}")

    # Keep only latest 20 entries
    if len(chat_history) > 20:
        del chat_history[:-20]

    return response