from core.llm_client import ask_llm
from config.prompts import REVIEWER_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

def review_code(task, generated_code):

    prompt = f"""
Task:
{task}

Generated Code:
{generated_code}

Review the code and improve it if needed.
Return the corrected version of the code.
"""

    result = ask_llm(REVIEWER_PROMPT, prompt)

    return result