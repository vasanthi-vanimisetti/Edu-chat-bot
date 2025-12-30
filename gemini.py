import os
from google import genai

client = genai.Client(api_key=os.getenv("AIzaSyCPgR14Zvjv88Ci2s3eNv2Bmz6LjWPX61A"))

response = client.models.generate_content(
    model="models/gemini-flash-lite-latest",
    contents="Explain internal and external evaluation in education"
)

print(response.text)