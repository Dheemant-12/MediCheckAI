from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def analyze_symptoms(symptoms):

    prompt = f"""
You are MediCheck AI, a professional medical assistant.

Patient symptoms:
{symptoms}

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

    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful medical assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=250
    )

    return completion.choices[0].message.content