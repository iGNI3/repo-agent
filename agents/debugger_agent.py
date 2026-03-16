from core.llm_client import ask_llm
from dotenv import load_dotenv
import os

load_dotenv()
def debug(error, code):

    return ask_llm(
        "You are a debugging expert",
        f"Fix this error:\n{error}\n\nCode:\n{code}"
    )