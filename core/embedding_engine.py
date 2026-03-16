from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")


def embed(text):

    model = EMBED_MODEL
    # Ensure OpenRouter compatibility for OpenAI models
    if "text-embedding" in model and "/" not in model:
        model = f"openai/{model}"

    res = client.embeddings.create(
        model=model,
        input=text
    )

    return np.array(res.data[0].embedding)