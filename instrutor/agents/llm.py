import os

from google.adk.models.lite_llm import LiteLlm

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

AZURE_API_KEY = os.getenv("SUBSCRIPTION_KEY")
AZURE_API_BASE= os.getenv("ENDPOINT")
AZURE_API_VERSION = os.getenv("API_VERSION")

LLM = LiteLlm(model=f"azure/{MODEL_NAME}")
