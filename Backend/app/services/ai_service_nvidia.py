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
- short advice

Keep the response short, clean, and professional.
"""

    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a concise medical assistant AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=120
    )

    return completion.choices[0].message.content