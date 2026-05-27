from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

def analyze_symptoms(symptoms):

    prompt = f"""
    Symptoms:
    {symptoms}

    Possible Conditions:
    """

    result = generator(
        prompt,
        max_length=120,
        num_return_sequences=1
    )

    return result[0]["generated_text"]