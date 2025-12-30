import os
from google import genai

client = genai.Client(api_key=os.getenv("AIzaSyCPgR14Zvjv88Ci2s3eNv2Bmz6LjWPX61A"))

models = client.models.list()
for m in models:
    print(m.name)