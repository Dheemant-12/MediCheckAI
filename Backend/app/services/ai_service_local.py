from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

def analyze_symptoms(symptoms):

    prompt = f"""
You are a helpful medical assistant.

Patient symptoms:
{symptoms}

Give a SHORT response in this exact format:

Possible Conditions:
- condition 1
- condition 2

Urgency Level:
- Low / Moderate / High

Basic Advice:
- short advice
"""

    result = generator(
        prompt,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.3,
        repetition_penalty=1.2
    )

    response = result[0]["generated_text"]

    cleaned_response = response.replace(
        prompt,
        ""
    ).strip()

    return cleaned_response