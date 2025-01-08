import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firecrawl web scraper
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

# For LlamaParse advanced PDF parsing
LLAMA_CLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY')
os.environ['LLAMA_CLOUD_API_KEY'] = LLAMA_CLOUD_API_KEY

# Open AI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
