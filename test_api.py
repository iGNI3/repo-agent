import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")
print(f"Using API Key: {key[:5]}...{key[-5:] if key else 'None'}")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=key
)

def test_call(model_name):
    model = model_name
    if (model.startswith("gpt-") or model.startswith("text-") or model.startswith("gemini-")) and "/" not in model:
        model = f"google/{model}" if "gemini" in model else f"openai/{model}"
    
    print(f"\nTesting model: {model}")
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "hi"}]
        )
        print("Success:", res.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

test_call("google/gemini-flash-1.5")
test_call("openai/gpt-3.5-turbo")
