from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("WARNING: OPENROUTER_API_KEY not found in environment!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL = os.getenv("MODEL")


def ask_llm(system, user):

    model = MODEL
    # Ensure OpenRouter compatibility for OpenAI models
    if (model.startswith("gpt-") or model.startswith("text-")) and "/" not in model:
        model = f"openai/{model}"

    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )

    return res.choices[0].message.content