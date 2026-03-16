from core.llm_client import ask_llm
from config.prompts import PLANNER_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

def create_plan(task, file_list):
    return ask_llm(
        PLANNER_PROMPT,
        f"Task: {task}\n\nRepository Files:\n{file_list}\n\nPropose a plan."
    )