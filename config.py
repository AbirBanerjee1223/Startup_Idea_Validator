"""
Configuration settings for the Startup Idea Validator.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Model Settings
MODEL_NAME = "gemini-pro-latest"
TEMPERATURE = 0.2

# Agent Settings
DEFAULT_MEMORY_KEY = "chat_history"
VERBOSE = True

# Paths
OUTPUT_DIR = "output_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Web Interface
STREAMLIT_TITLE = "Startup Idea Validator"
STREAMLIT_DESCRIPTION = """
Enter your startup idea below, and our AI agents will analyze it from multiple 
perspectives to provide a comprehensive validation report.
"""
