from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def embed(text):

    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return np.array(res.data[0].embedding)