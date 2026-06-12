import base64
from groq import Groq
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def identify_plant(image_bytes: bytes, lang: str = "es") -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": f"""
Analyze this image and identify the plant(s).

First verify: is there a plant in the image?
- If NO plant: return {{"is_plant": false, "message": "No plant detected"}}
- If YES: return a JSON object with:
  - is_plant: true
  - results: list of top 3 matches, each with:
    - common_name
    - scientific_name
    - confidence_percentage (integer 0-100)
    - description (2 sentences)
    - care_tips (list of 4 tips)
    - toxicity (safe/toxic to pets and humans)
    - origin (native region)
    - fun_fact (one curious fact)

Respond ONLY in valid JSON, in {lang} language, no extra text.
"""}
            ]
        }],
        max_tokens=800,
    )
    return response.choices[0].message.content