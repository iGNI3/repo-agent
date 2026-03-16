from core.llm_client import ask_llm
from config.prompts import CODER_PROMPT

from dotenv import load_dotenv
import os

load_dotenv()
def implement(task, files):

    return ask_llm(
        CODER_PROMPT,
        f"Task:\n{task}\n\nRelevant Files:\n{files}"
    )